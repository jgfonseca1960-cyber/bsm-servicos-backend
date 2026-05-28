from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

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

# =========================================================
# 🚀 ROUTER
# =========================================================

router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
)

# =========================================================
# 🌐 BASE URL
# =========================================================

BASE_URL = os.getenv(
    "BASE_URL",
    "https://bsm-servicos-backend-1.onrender.com"
)

# =========================================================
# 📁 CONFIG UPLOAD
# =========================================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# =========================================================
# ☁️ CLOUDINARY
# =========================================================

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

print("🔥 Cloudinary carregado!")

# =========================================================
# 🔥 FOTO PRINCIPAL
# =========================================================

def obter_foto_principal(fotos):

    principal = next(
        (
            f.url
            for f in fotos
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
# 📦 SERIALIZAR EMPRESA
# =========================================================

def serializar_empresa(
    e,
    db: Session
):

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == e.id
    ).all()

    media = 0.0

    if avaliacoes:

        media = round(
            sum(a.nota for a in avaliacoes)
            / len(avaliacoes),
            1
        )

    lista_fotos = [
        {
            "id": f.id,
            "url": f.url,
            "principal": bool(f.principal),
            "public_id": getattr(
                f,
                "public_id",
                None
            )
        }
        for f in e.fotos
    ]

    empresa_serializada = {

        # =================================================
        # BÁSICO
        # =================================================

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

        "ativo": bool(
            getattr(
                e,
                "ativo",
                True
            )
        ),

        # =================================================
        # ⭐ PREMIUM
        # =================================================

        "premium": bool(
            getattr(
                e,
                "premium",
                False
            )
        ),

        "destaque": bool(
            getattr(
                e,
                "destaque",
                False
            )
        ),

        "plano": getattr(
            e,
            "plano",
            "gratuito"
        ),

        "prioridade": int(
            getattr(
                e,
                "prioridade",
                0
            ) or 0
        ),

        "whatsapp_destacado": bool(
            getattr(
                e,
                "whatsapp_destacado",
                False
            )
        ),

        "exibir_no_topo": bool(
            getattr(
                e,
                "exibir_no_topo",
                False
            )
        ),

        "selo_premium": bool(
            getattr(
                e,
                "selo_premium",
                False
            )
        ),

        "is_premium": bool(
            getattr(
                e,
                "is_premium",
                False
            )
        ),

        # =================================================
        # AVALIAÇÃO
        # =================================================

        "avaliacao_media": media,

        "total_avaliacoes": len(
            avaliacoes
        ),

        # =================================================
        # DOCUMENTOS
        # =================================================

        "cpf": e.cpf,

        "cnpj": e.cnpj,

        # =================================================
        # SERVIÇO
        # =================================================

        "servico_id": e.servico_id,

        # =================================================
        # FOTOS
        # =================================================

        "foto_principal": obter_foto_principal(
            e.fotos
        ),

        "fotos": lista_fotos,

        # =================================================
        # AVALIAÇÕES
        # =================================================

        "avaliacoes": [
            {
                "id": a.id,

                "usuario": (
                    a.usuario.nome
                    if a.usuario
                    else f"Usuário {a.usuario_id}"
                ),

                "nota": a.nota,

                "comentario": a.comentario
            }
            for a in avaliacoes
        ]
    }

    print("\n🔥 SERIALIZANDO EMPRESA:")
    print("ID =", empresa_serializada["id"])
    print("NOME =", empresa_serializada["nome"])
    print("PREMIUM =", empresa_serializada["premium"])
    print("DESTAQUE =", empresa_serializada["destaque"])
    print("PLANO =", empresa_serializada["plano"])

    return empresa_serializada


# =========================================================
# ☁️ UPLOAD FOTO
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

        url = resultado.get(
            "secure_url"
        )

        total_fotos = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id
        ).count()

        principal = (
            total_fotos == 0
        )

        foto = EmpresaFoto(
            empresa_id=empresa_id,
            url=url,
            principal=principal,
            public_id=resultado.get(
                "public_id"
            )
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

        print("❌ ERRO UPLOAD FOTO")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ⭐ DEFINIR FOTO PRINCIPAL
# =========================================================

@router.put(
    "/{empresa_id}/foto-principal/{foto_id}"
)
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


# =========================================================
# ❌ DELETAR FOTO
# =========================================================

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

        print(
            f"❌ ERRO CLOUDINARY: {e}"
        )

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


# =========================================================
# ➕ CRIAR EMPRESA
# =========================================================

@router.post(
    "/",
    response_model=EmpresaResponse
)
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db)
):

    try:

        data = dados.model_dump()

        print("\n📥 CREATE DATA:")
        print(data)

        if data.get("servico_id") == 0:

            data["servico_id"] = None

        nova = Empresa(**data)

        db.add(nova)

        db.commit()

        db.refresh(nova)

        db.expire_all()

        empresa_atualizada = db.query(Empresa).filter(
            Empresa.id == nova.id
        ).first()

        return serializar_empresa(
            empresa_atualizada,
            db
        )

    except Exception as e:

        db.rollback()

        print("\n❌ ERRO CREATE EMPRESA")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# 📡 LISTAR EMPRESAS
# =========================================================

@router.get(
    "/",
    response_model=list[EmpresaResponse]
)
def listar_empresas(
    db: Session = Depends(get_db)
):

    empresas = db.query(Empresa).all()

    print(
        f"\n🔥 TOTAL EMPRESAS: {len(empresas)}"
    )

    for emp in empresas:

        print(
            emp.id,
            emp.nome,
            getattr(emp, "premium", None)
        )

    empresas.sort(
        key=lambda x: (
            -int(
                getattr(
                    x,
                    "prioridade",
                    0
                ) or 0
            ),

            not bool(
                getattr(
                    x,
                    "premium",
                    False
                )
            ),

            not bool(
                getattr(
                    x,
                    "destaque",
                    False
                )
            ),

            x.nome.lower()
        )
    )

    return [
        serializar_empresa(
            e,
            db
        )
        for e in empresas
    ]


# =========================================================
# 🔍 DETALHE EMPRESA
# =========================================================

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

    print("\n🔥 DETALHE EMPRESA:")
    print("ID =", empresa.id)
    print("PREMIUM =", empresa.premium)

    return serializar_empresa(
        empresa,
        db
    )


# =========================================================
# ✏️ UPDATE EMPRESA
# =========================================================

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

    try:

        update_data = dados.model_dump(
            exclude_unset=True
        )

        print("\n📥 UPDATE DATA:")
        print(update_data)

        if update_data.get("servico_id") == 0:

            update_data["servico_id"] = None

        for key, value in update_data.items():

            setattr(
                empresa,
                key,
                value
            )

        db.commit()

        db.expire_all()

        empresa_atualizada = db.query(Empresa).filter(
            Empresa.id == empresa_id
        ).first()

        print("\n🔥 RESULTADO FINAL:")
        print("premium =", empresa_atualizada.premium)
        print("destaque =", empresa_atualizada.destaque)
        print("plano =", empresa_atualizada.plano)

        return serializar_empresa(
            empresa_atualizada,
            db
        )

    except Exception as e:

        db.rollback()

        print("\n❌ ERRO UPDATE EMPRESA")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ❌ DELETAR EMPRESA
# =========================================================

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