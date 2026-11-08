
import io
import logging
import warnings

import cloudinary
import cloudinary.uploader

from PIL import (
    Image,
    ImageOps,
    UnidentifiedImageError,
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.core.dependencies import get_current_admin

from app.models.empresa_model import Empresa
from app.models.avaliacao_model import Avaliacao
from app.models.empresa_foto_model import EmpresaFoto

from app.schemas.empresa_schema import (
    EmpresaResponse,
    EmpresaCreate,
    EmpresaUpdate,
)


# =========================================================
# LOGGING
# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# CONFIGURAÇÕES DE FOTOS
# =========================================================

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000
MAX_IMAGE_DIMENSIONS = (1600, 1200)
JPEG_QUALITY = 85

FORMATOS_PERMITIDOS = {"JPEG", "PNG", "WEBP"}

def normalizar_plano(plano: str | None) -> str:
    valor = str(plano or "gratuito").strip().lower()

    if valor in ("gratis", "gratuito"):
        return "gratuito"

    return valor

# =========================================================
# SISTEMA DE PLANOS
# =========================================================

def get_permissoes(plano: str) -> dict:
    plano = normalizar_plano(plano)

    regras = {
        "gratuito": {
            "galeria": False,
            "destaque": False,
            "whatsapp_destacado": False,
            "exibir_no_topo": False,
            "selo_premium": False,
        },
        "premium": {
            "galeria": True,
            "destaque": True,
            "whatsapp_destacado": True,
            "exibir_no_topo": False,
            "selo_premium": True,
        },
        "master": {
            "galeria": True,
            "destaque": True,
            "whatsapp_destacado": True,
            "exibir_no_topo": True,
            "selo_premium": True,
        },
    }

    return regras.get(plano, regras["gratuito"])


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(tags=["Empresa"])


# =========================================================
# QUALIFICAÇÃO AUTOMÁTICA DAS FOTOS
# =========================================================

def qualificar_foto(conteudo: bytes) -> tuple[bytes, int, int]:
    """
    Valida e normaliza uma imagem antes do envio ao Cloudinary.

    Retorna:
        bytes JPEG, largura final e altura final.
    """

    if not conteudo:
        raise HTTPException(
            status_code=400,
            detail="O arquivo enviado está vazio.",
        )

    try:
        with warnings.catch_warnings():
            warnings.simplefilter(
                "error",
                Image.DecompressionBombWarning,
            )

            # Primeira abertura: validar formato e dimensões.
            with Image.open(io.BytesIO(conteudo)) as imagem:

                if imagem.format not in FORMATOS_PERMITIDOS:
                    raise HTTPException(
                        status_code=415,
                        detail=(
                            "Formato não permitido. "
                            "Envie uma imagem JPEG, PNG ou WebP."
                        ),
                    )

                if getattr(imagem, "n_frames", 1) != 1:
                    raise HTTPException(
                        status_code=415,
                        detail=(
                            "Imagens animadas não são permitidas. "
                            "Envie uma imagem estática."
                        ),
                    )

                largura, altura = imagem.size

                if largura <= 0 or altura <= 0:
                    raise HTTPException(
                        status_code=400,
                        detail="A imagem possui dimensões inválidas.",
                    )

                if largura * altura > MAX_IMAGE_PIXELS:
                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "A resolução da imagem é muito alta. "
                            "Reduza a resolução antes de enviar."
                        ),
                    )

                imagem.verify()

            # Segunda abertura: processar imagem validada.
            with Image.open(io.BytesIO(conteudo)) as imagem:

                imagem = ImageOps.exif_transpose(imagem)

                # Redimensiona sem distorcer e sem ampliar.
                imagem.thumbnail(
                    MAX_IMAGE_DIMENSIONS,
                    Image.Resampling.LANCZOS,
                )

                # Padroniza transparência sobre fundo branco.
                imagem_rgba = imagem.convert("RGBA")

                fundo = Image.new(
                    "RGBA",
                    imagem_rgba.size,
                    (255, 255, 255, 255),
                )

                imagem_final = Image.alpha_composite(
                    fundo,
                    imagem_rgba,
                ).convert("RGB")

                largura_final, altura_final = imagem_final.size

                saida = io.BytesIO()

                imagem_final.save(
                    saida,
                    format="JPEG",
                    quality=JPEG_QUALITY,
                    optimize=True,
                    progressive=True,
                )

                return (
                    saida.getvalue(),
                    largura_final,
                    altura_final,
                )

    except HTTPException:
        raise

    except (
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
        OSError,
        ValueError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Não foi possível processar a imagem. "
                "Verifique se o arquivo está íntegro."
            ),
        ) from exc



# =========================================================
# DEFINIR FOTO PRINCIPAL
# =========================================================

@router.put("/{empresa_id}/fotos/{foto_id}/principal")
def definir_foto_principal(
    empresa_id: int,
    foto_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada.",
        )

    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id,
        EmpresaFoto.empresa_id == empresa_id,
    ).first()

    if not foto:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada para esta empresa.",
        )

    try:
        db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id
        ).update(
            {EmpresaFoto.principal: False},
            synchronize_session=False,
        )

        foto.principal = True

        db.commit()
        db.refresh(foto)

        return {
            "mensagem": "Foto principal atualizada com sucesso.",
            "empresa_id": empresa_id,
            "foto_id": foto.id,
            "url": foto.url,
            "principal": True,
        }

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERRO AO DEFINIR FOTO PRINCIPAL DA EMPRESA ID %s",
            empresa_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Não foi possível definir a foto principal.",
        ) from exc


# =========================================================
# EXCLUIR FOTO DA EMPRESA
# =========================================================

@router.delete("/{empresa_id}/fotos/{foto_id}")
def excluir_foto_empresa(
    empresa_id: int,
    foto_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada.",
        )

    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id,
        EmpresaFoto.empresa_id == empresa_id,
    ).first()

    if not foto:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada para esta empresa.",
        )

    public_id = foto.public_id
    era_principal = bool(foto.principal)

    try:
        # Se a foto excluída era principal,
        # selecionar outra foto automaticamente.
        if era_principal:
            proxima_foto = db.query(EmpresaFoto).filter(
                EmpresaFoto.empresa_id == empresa_id,
                EmpresaFoto.id != foto_id,
            ).order_by(
                EmpresaFoto.id.asc()
            ).first()

            db.query(EmpresaFoto).filter(
                EmpresaFoto.empresa_id == empresa_id
            ).update(
                {EmpresaFoto.principal: False},
                synchronize_session=False,
            )

            if proxima_foto:
                proxima_foto.principal = True

        db.delete(foto)
        db.commit()

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERRO AO EXCLUIR FOTO %s DA EMPRESA %s",
            foto_id,
            empresa_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Não foi possível excluir a foto.",
        ) from exc

    # Excluir a imagem remota somente após
    # confirmar a exclusão no banco de dados.
    remover_foto_cloudinary(public_id)

    return {
        "mensagem": "Foto excluída com sucesso.",
        "empresa_id": empresa_id,
        "foto_id": foto_id,
        "era_principal": era_principal,
    }

def obter_foto_principal(fotos):
    if not fotos:
        return None

    principal = next(
        (foto.url for foto in fotos if getattr(foto, "principal", False)),
        None,
    )

    return principal or fotos[0].url

# =========================================================
# SERIALIZAÇÃO DA EMPRESA
# =========================================================

def serializar_empresa(e, db: Session):

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == e.id
    ).all()

    media = (
        round(
            sum(a.nota for a in avaliacoes) / len(avaliacoes),
            1,
        )
        if avaliacoes
        else 0.0
    )

    plano = normalizar_plano(
        getattr(e, "plano", None)
    )

    return {

        "id": e.id,
        "nome": e.nome,
        "descricao": e.descricao,
        "telefone": e.telefone,
        "whatsapp": e.whatsapp,
        "email": e.email,

        # Redes sociais e presença digital
        "instagram": e.instagram,
        "facebook": e.facebook,
        "site": e.site,

        # Aplicativo de vendas
        "possui_app": bool(e.possui_app),
        "link_app_android": e.link_app_android,
        "link_app_ios": e.link_app_ios,

        # Endereço e localização
        "endereco": e.endereco,
        "bairro": e.bairro,
        "cidade": e.cidade,
        "estado": e.estado,
        "cep": e.cep,
        "latitude": e.latitude,
        "longitude": e.longitude,

        "ativo": bool(getattr(e, "ativo", True)),
        "plano": plano,

        # Avaliações
        "avaliacao_media": media,
        "total_avaliacoes": len(avaliacoes),

        # Dados cadastrais
        "cpf": e.cpf,
        "cnpj": e.cnpj,
        "servico_id": e.servico_id,

        # Fotos
        "foto_principal": obter_foto_principal(e.fotos),

        "fotos": [
            {
                "id": foto.id,
                "url": foto.url,
                "principal": bool(foto.principal),
                "public_id": foto.public_id,
            }
            for foto in (e.fotos or [])
        ],

        # Lista de avaliações
        "avaliacoes": [
            {
                "id": avaliacao.id,
                "empresa_id": avaliacao.empresa_id,
                "usuario_id": avaliacao.usuario_id,
                "usuario": (
                    avaliacao.usuario.nome
                    if getattr(avaliacao, "usuario", None)
                    else f"Usuário {avaliacao.usuario_id}"
                ),
                "nota": avaliacao.nota,
                "comentario": avaliacao.comentario,
            }
            for avaliacao in avaliacoes
        ],
    }


# =========================================================
# SCORE DE PLANO
# =========================================================

def get_plano_score(e):

    plano = normalizar_plano(
        getattr(e, "plano", None)
    )

    if plano == "master":
        return 3

    if plano == "premium":
        return 2

    return 1


# =========================================================
# LISTAR EMPRESAS
# =========================================================

@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):

    empresas = db.query(Empresa).all()

    empresas.sort(
        key=lambda empresa: (
            -get_plano_score(empresa),
            not bool(
                getattr(empresa, "exibir_no_topo", False)
            ),
            not bool(
                getattr(empresa, "destaque", False)
            ),
            -int(
                getattr(empresa, "prioridade", 0) or 0
            ),
            (empresa.nome or "").lower(),
        )
    )

    return [
        serializar_empresa(empresa, db)
        for empresa in empresas
    ]


# =========================================================
# DETALHE DA EMPRESA
# =========================================================

@router.get("/{empresa_id}", response_model=EmpresaResponse)
def detalhe_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    return serializar_empresa(empresa, db)


# =========================================================
# CRIAR EMPRESA
# =========================================================

@router.post("/", response_model=EmpresaResponse)
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    empresa = Empresa(**dados.model_dump())

    try:
        db.add(empresa)
        db.commit()
        db.refresh(empresa)

        return serializar_empresa(empresa, db)

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERRO AO CRIAR EMPRESA"
        )

        raise HTTPException(
            status_code=500,
            detail="Não foi possível cadastrar a empresa.",
        ) from exc


# =========================================================
# ATUALIZAR EMPRESA
# =========================================================

@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    update_data = dados.model_dump(
        exclude_unset=True
    )

    try:
        for campo, valor in update_data.items():
            setattr(empresa, campo, valor)

        db.commit()
        db.refresh(empresa)

        return serializar_empresa(empresa, db)

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERRO AO ATUALIZAR EMPRESA ID %s",
            empresa_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Não foi possível atualizar a empresa.",
        ) from exc


# =========================================================
# EXCLUSÃO DE UMA FOTO NO CLOUDINARY EM CASO DE FALHA
# =========================================================

def remover_foto_cloudinary(public_id: str | None) -> None:

    if not public_id:
        return

    try:
        cloudinary.uploader.destroy(
            public_id,
            resource_type="image",
        )

    except Exception:
        # Não substituir o erro original por falha de limpeza.
        logger.exception(
            "Falha ao remover imagem do Cloudinary: %s",
            public_id,
        )


# =========================================================
# UPLOAD E QUALIFICAÇÃO DA FOTO
# =========================================================

@router.post("/{empresa_id}/fotos")
def upload_foto_empresa(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    resultado = None
    foto_gravada = False

    try:
        empresa = db.query(Empresa).filter(
            Empresa.id == empresa_id
        ).first()

        if not empresa:
            raise HTTPException(
                status_code=404,
                detail="Empresa não encontrada",
            )

        plano = normalizar_plano(
            getattr(empresa, "plano", None)
        )

        # Plano gratuito permite somente uma foto.
        if plano == "gratuito":
            total_fotos = db.query(EmpresaFoto).filter(
                EmpresaFoto.empresa_id == empresa_id
            ).count()

            if total_fotos >= 1:
                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Plano gratuito permite apenas 1 foto."
                    ),
                )

        # Limite aplicado aos bytes efetivamente recebidos.
        conteudo = file.file.read(
            MAX_UPLOAD_BYTES + 1
        )

        if not conteudo:
            raise HTTPException(
                status_code=400,
                detail="Nenhum arquivo foi enviado.",
            )

        if len(conteudo) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail="A foto ultrapassa o limite de 10 MB.",
            )

        # Validação, orientação, redimensionamento e compressão.
        imagem_jpeg, largura, altura = qualificar_foto(
            conteudo
        )

        # Envia ao Cloudinary somente a imagem processada.
        resultado = cloudinary.uploader.upload(
            io.BytesIO(imagem_jpeg),
            folder="bsm/empresas",
            resource_type="image",
            format="jpg",
        )

        url_segura = resultado.get("secure_url")
        public_id = resultado.get("public_id")

        if not url_segura or not public_id:
            raise HTTPException(
                status_code=502,
                detail=(
                    "O serviço de imagens não confirmou "
                    "o envio da foto."
                ),
            )

        # Recalcula para determinar se será a principal.
        total_fotos = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id
        ).count()

        foto = EmpresaFoto(
            empresa_id=empresa_id,
            url=url_segura,
            public_id=public_id,
            principal=(total_fotos == 0),
        )

        db.add(foto)
        db.commit()

        foto_gravada = True

        db.refresh(foto)

        return {
            "id": foto.id,
            "url": foto.url,
            "public_id": foto.public_id,
            "empresa_id": empresa_id,
            "principal": bool(foto.principal),
            "formato": "jpg",
            "largura": largura,
            "altura": altura,
            "qualidade": JPEG_QUALITY,
        }

    except HTTPException:
        db.rollback()

        if resultado and not foto_gravada:
            remover_foto_cloudinary(
                resultado.get("public_id")
            )

        raise

    except Exception as exc:
        db.rollback()

        logger.exception(
            "ERRO NO UPLOAD DE FOTO DA EMPRESA ID %s",
            empresa_id,
        )

        if resultado and not foto_gravada:
            remover_foto_cloudinary(
                resultado.get("public_id")
            )

        raise HTTPException(
            status_code=502,
            detail=(
                "Não foi possível processar e salvar a foto. "
                "Tente novamente."
            ),
        ) from exc

    finally:
        file.file.close()
