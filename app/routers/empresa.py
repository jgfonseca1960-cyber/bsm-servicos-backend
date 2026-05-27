from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

import os
import cloudinary
import cloudinary.uploader

from app.database import get_db

from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from app.models.avaliacao_model import Avaliacao

from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaUpdate,
    EmpresaResponse
)

router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
)

# =========================
# 🌐 BASE URL
# =========================
BASE_URL = "https://bsm-servicos-backend.onrender.com"

# =========================
# 📁 CONFIG UPLOAD LOCAL
# =========================
UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# =========================================================
# ☁️ CLOUDINARY CONFIG
# =========================================================
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# =========================================================
# 🔥 FOTO PRINCIPAL
# =========================================================
def obter_foto_principal(fotos):

    principal = next(
        (
            f.url for f in fotos
            if f.principal
        ),
        None
    )

    if principal:
        return principal

    if fotos:
        return fotos[0].url

    return None


# =========================================================
# 📦 SERIALIZADOR EMPRESA
# =========================================================
def serializar_empresa(e, db: Session):

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == e.id
    ).all()

    media = 0

    if avaliacoes:
        media = round(
            sum([a.nota for a in avaliacoes])
            / len(avaliacoes),
            1
        )

    lista_fotos = [
        {
            "id": f.id,
            "url": f.url,
            "principal": f.principal,
            "public_id": getattr(f, "public_id", None)
        }
        for f in e.fotos
    ]

    return {
        "id": e.id,
        "nome": e.nome,
        "descricao": e.descricao,

        "telefone": e.telefone,
        "whatsapp": e.whatsapp,
        "email": e.email,

        "endereco": e.endereco,
        "bairro": e.bairro,
        "cidade": e.cidade,
        "estado": e.estado,
        "cep": e.cep,

        "latitude": e.latitude,
        "longitude": e.longitude,

        "ativo": e.ativo,

        # ⭐ PREMIUM
        "premium": bool(getattr(e, "premium", False)),
        "destaque": bool(getattr(e, "destaque", False)),
        "plano": getattr(e, "plano", "gratuito"),
        "prioridade": getattr(e, "prioridade", 0),
        "whatsapp_destacado": bool(
            getattr(e, "whatsapp_destacado", False)
        ),
        "exibir_no_topo": bool(
            getattr(e, "exibir_no_topo", False)
        ),
        "selo_premium": bool(
            getattr(e, "selo_premium", False)
        ),
        
        "is_premium": e.is_premium,

        "avaliacao_media": media,

        "cpf": e.cpf,
        "cnpj": e.cnpj,

        "servico_id": e.servico_id,

        "foto_principal": obter_foto_principal(e.fotos),

        "fotos": lista_fotos,

        "avaliacoes": [
            {
                "id": a.id,
                "usuario": (
                    a.usuario.nome
                    if a.usuario else
                    f"Usuário {a.usuario_id}"
                ),
                "nota": a.nota,
                "comentario": a.comentario
            }
            for a in avaliacoes
        ]
    }


# =========================================================
# ☁️ UPLOAD CLOUDINARY
# =========================================================
@router.post("/{empresa_id}/fotos")
def upload_foto(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    try:

        resultado = cloudinary.uploader.upload(
            file.file,
            folder="bsm/empresas"
        )

        url = resultado.get("secure_url")

        total_fotos = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id
        ).count()

        principal = (total_fotos == 0)

        foto = EmpresaFoto(
            empresa_id=empresa_id,
            url=url,
            principal=principal,
            public_id=resultado.get("public_id")
        )

        db.add(foto)

        db.commit()
        db.refresh(foto)

        return {
            "message": "Foto enviada com sucesso",
            "foto": {
                "id": foto.id,
                "url": foto.url,
                "principal": foto.principal,
                "public_id": foto.public_id
            }
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Erro upload: {str(e)}"
        )


# =========================
# ⭐ DEFINIR FOTO PRINCIPAL
# =========================
@router.put("/{empresa_id}/foto-principal/{foto_id}")
def definir_foto_principal(
    empresa_id: int,
    foto_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    fotos = db.query(EmpresaFoto).filter(
        EmpresaFoto.empresa_id == empresa_id
    ).all()

    foto_principal = None

    for foto in fotos:

        foto.principal = False

        if foto.id == foto_id:
            foto.principal = True
            foto_principal = foto

    if not foto_principal:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada"
        )

    db.commit()

    return {
        "message": "Foto principal atualizada"
    }


# =========================
# ❌ DELETAR FOTO
# =========================
@router.delete("/foto/{foto_id}")
def deletar_foto(
    foto_id: int,
    db: Session = Depends(get_db)
):

    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id
    ).first()

    if not foto:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada"
        )

    empresa = db.query(Empresa).filter(
        Empresa.id == foto.empresa_id
    ).first()

    era_principal = foto.principal

    try:

        if foto.public_id:

            cloudinary.uploader.destroy(
                foto.public_id
            )

    except Exception as e:
        print(f"Erro removendo cloudinary: {e}")

    db.delete(foto)

    db.commit()

    if era_principal and empresa:

        nova_principal = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa.id
        ).first()

        if nova_principal:
            nova_principal.principal = True
            db.commit()

    return {
        "message": "Foto removida"
    }


# =========================
# ➕ CRIAR EMPRESA
# =========================
@router.post(
    "/",
    response_model=EmpresaResponse
)
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db)
):

    data = dados.dict()

    # evita FK inválida
    if data.get("servico_id") == 0:
        data["servico_id"] = None

    nova = Empresa(**data)

    db.add(nova)

    db.commit()

    db.refresh(nova)

    return serializar_empresa(nova, db)


# =========================
# 📡 LISTAR EMPRESAS
# =========================
@router.get(
    "/",
    response_model=list[EmpresaResponse]
)
def listar_empresas(
    db: Session = Depends(get_db)
):

    empresas = db.query(Empresa).all()

    # ⭐ PREMIUM PRIMEIRO
    empresas.sort(
        key=lambda x: (
            -int(getattr(x, "prioridade", 0)),
            not bool(getattr(x, "premium", False)),
            not bool(getattr(x, "destaque", False)),
            x.nome.lower()
        )
    )

    return [
        serializar_empresa(e, db)
        for e in empresas
    ]


# =========================
# 🔍 DETALHE EMPRESA
# =========================
@router.get(
    "/{empresa_id}",
    response_model=EmpresaResponse
)
def detalhe_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return serializar_empresa(empresa, db)


# =========================
# ✏️ ATUALIZAR EMPRESA
# =========================
@router.put(
    "/{empresa_id}",
    response_model=EmpresaResponse
)
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaUpdate,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    update_data = dados.model_dump(
        exclude_unset=True
    )

    print("📥 UPDATE DATA RECEBIDO:")
    print(update_data)

    # =====================================================
    # 🔥 CAMPOS COMUNS
    # =====================================================

    empresa.nome = update_data.get(
        "nome",
        empresa.nome
    )

    empresa.descricao = update_data.get(
        "descricao",
        empresa.descricao
    )

    empresa.telefone = update_data.get(
        "telefone",
        empresa.telefone
    )

    empresa.whatsapp = update_data.get(
        "whatsapp",
        empresa.whatsapp
    )

    empresa.email = update_data.get(
        "email",
        empresa.email
    )

    empresa.endereco = update_data.get(
        "endereco",
        empresa.endereco
    )

    empresa.bairro = update_data.get(
        "bairro",
        empresa.bairro
    )

    empresa.cidade = update_data.get(
        "cidade",
        empresa.cidade
    )

    empresa.estado = update_data.get(
        "estado",
        empresa.estado
    )

    empresa.cep = update_data.get(
        "cep",
        empresa.cep
    )

    empresa.latitude = update_data.get(
        "latitude",
        empresa.latitude
    )

    empresa.longitude = update_data.get(
        "longitude",
        empresa.longitude
    )

    empresa.ativo = update_data.get(
        "ativo",
        empresa.ativo
    )

    empresa.servico_id = update_data.get(
        "servico_id",
        empresa.servico_id
    )

    # =====================================================
    # ⭐ PREMIUM
    # =====================================================

    if "premium" in update_data:
        empresa.premium = bool(
            update_data["premium"]
        )

    if "destaque" in update_data:
        empresa.destaque = bool(
            update_data["destaque"]
        )

    if "whatsapp_destacado" in update_data:
        empresa.whatsapp_destacado = bool(
            update_data["whatsapp_destacado"]
        )

    if "exibir_no_topo" in update_data:
        empresa.exibir_no_topo = bool(
            update_data["exibir_no_topo"]
        )

    if "selo_premium" in update_data:
        empresa.selo_premium = bool(
            update_data["selo_premium"]
        )

    if "plano" in update_data:
        empresa.plano = update_data["plano"]

    if "prioridade" in update_data:
        empresa.prioridade = int(
            update_data["prioridade"]
        )

    # =====================================================
    # DEBUG
    # =====================================================

    print("🔥 VALORES APÓS UPDATE:")
    print("premium =", empresa.premium)
    print("destaque =", empresa.destaque)
    print("plano =", empresa.plano)

    db.commit()

    db.refresh(empresa)

    return serializar_empresa(
        empresa,
        db
    )

# =========================
# ❌ DELETAR EMPRESA
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    db.delete(empresa)

    db.commit()

    return {
        "message": "Empresa removida com sucesso"
    }