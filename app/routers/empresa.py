from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
import os
import cloudinary

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.avaliacao_model import Avaliacao
from app.schemas.empresa_schema import EmpresaResponse


# =========================================================
# 🔐 SISTEMA DE PLANOS
# =========================================================

def get_permissoes(plano: str) -> dict:
    plano = (plano or "gratuito").strip().lower()

    regras = {
        "gratuito": {
            "galeria": False,
            "destaque": False,
            "whatsapp_destacado": False,
            "exibir_no_topo": False,
            "selo_premium": False
        },
        "premium": {
            "galeria": True,
            "destaque": True,
            "whatsapp_destacado": True,
            "exibir_no_topo": False,
            "selo_premium": True
        },
        "master": {
            "galeria": True,
            "destaque": True,
            "whatsapp_destacado": True,
            "exibir_no_topo": True,
            "selo_premium": True
        }
    }

    return regras.get(plano, regras["gratuito"])


# =========================================================
# 🚀 ROUTER
# =========================================================

router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
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
# 📷 FOTO PRINCIPAL
# =========================================================

def obter_foto_principal(fotos):
    if not fotos:
        return None

    principal = next(
        (f.url for f in fotos if getattr(f, "principal", False)),
        None
    )

    return principal or (fotos[0].url if fotos else None)


# =========================================================
# 📦 SERIALIZAÇÃO
# =========================================================

def serializar_empresa(e, db: Session):

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == e.id
    ).all()

    media = (
        round(sum(a.nota for a in avaliacoes) / len(avaliacoes), 1)
        if avaliacoes else 0.0
    )

    plano = (getattr(e, "plano", "gratuito") or "").strip().lower()

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

        "ativo": bool(getattr(e, "ativo", True)),

        "plano": plano,
        "permissoes": get_permissoes(plano),

        "avaliacao_media": media,
        "total_avaliacoes": len(avaliacoes),

        "cpf": e.cpf,
        "cnpj": e.cnpj,
        "servico_id": e.servico_id,

        "foto_principal": obter_foto_principal(e.fotos),

        "fotos": [
            {
                "id": f.id,
                "url": f.url,
                "principal": bool(f.principal)
            }
            for f in e.fotos
        ],

        "avaliacoes": [
            {
                "id": a.id,
                "usuario": a.usuario.nome if a.usuario else f"Usuário {a.usuario_id}",
                "nota": a.nota,
                "comentario": a.comentario
            }
            for a in avaliacoes
        ]
    }


# =========================================================
# 🧠 SCORE DE PLANO (🔥 ESSENCIAL PARA ORDERNAR)
# =========================================================

def get_plano_score(e):
    plano = (getattr(e, "plano", "gratuito") or "").strip().lower()

    if plano == "master":
        return 3
    if plano == "premium":
        return 2
    return 1


# =========================================================
# 📡 LISTAR EMPRESAS (SORT CORRIGIDO)
# =========================================================

@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):

    empresas = db.query(Empresa).all()

for e in empresas:
    print(
        "EMPRESA:",
        e.nome,
        "| PLANO:",
        getattr(e, "plano", None)
    )
    

    empresas.sort(
        key=lambda x: (
            -get_plano_score(x),  # 🔥 PREMIUM REAL PRIMEIRO
            not bool(getattr(x, "exibir_no_topo", False)),
            not bool(getattr(x, "destaque", False)),
            -int(getattr(x, "prioridade", 0) or 0),
            x.nome.lower()
        )
    )

    return [
        serializar_empresa(e, db)
        for e in empresas
    ]


# =========================================================
# 🔍 DETALHE
# =========================================================

@router.get("/{empresa_id}", response_model=EmpresaResponse)
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