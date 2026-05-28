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

# =========================================================
# 🌐 BASE URL
# =========================================================

BASE_URL = "https://bsm-servicos-backend.onrender.com"

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
# 📦 SERIALIZAR EMPRESA
# =========================================================

def serializar_empresa(e, db: Session):

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

        "ativo": bool(e.ativo),

        # ⭐ PREMIUM
        "premium": bool(e.premium),
        "destaque": bool(e.destaque),
        "plano": e.plano,
        "prioridade": int(e.prioridade or 0),
        "whatsapp_destacado": bool(e.whatsapp_destacado),
        "exibir_no_topo": bool(e.exibir_no_topo),
        "selo_premium": bool(e.selo_premium),

        "is_premium": bool(e.is_premium),

        "avaliacao_media": media,

        "cpf": e.cpf,
        "cnpj": e.cnpj,

        "servico_id": e.servico_id,

        "foto_principal": obter_foto_principal(
            e.fotos
        ),

        "fotos": lista_fotos,

        "total_avaliacoes": len(avaliacoes),

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

        if data.get("servico_id") == 0:
            data["servico_id"] = None

        nova = Empresa(**data)

        db.add(nova)

        db.commit()

        db.refresh(nova)

        empresa_atualizada = db.query(Empresa).filter(
            Empresa.id == nova.id
        ).first()

        return serializar_empresa(
            empresa_atualizada,
            db
        )

    except Exception as e:

        db.rollback()

        print("❌ ERRO CREATE EMPRESA")
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

        print("📥 UPDATE DATA:")
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

        # 🔥 FORÇA RECARREGAR DO BANCO
        db.expire_all()

        empresa_atualizada = db.query(Empresa).filter(
            Empresa.id == empresa_id
        ).first()

        print("🔥 RESULTADO FINAL:")
        print("premium =", empresa_atualizada.premium)
        print("destaque =", empresa_atualizada.destaque)
        print("plano =", empresa_atualizada.plano)

        return serializar_empresa(
            empresa_atualizada,
            db
        )

    except Exception as e:

        db.rollback()

        print("❌ ERRO UPDATE EMPRESA")
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