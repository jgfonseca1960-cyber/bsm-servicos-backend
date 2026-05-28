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

# 👇 NOVO IMPORT (PERMISSÕES)
from app.services.permissoes import get_permissoes


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

    if not fotos:
        return None

    principal = next(
        (
            f.url
            for f in fotos
            if getattr(f, "principal", False)
        ),
        None
    )

    if principal:
        return principal

    return fotos[0].url


# =========================================================
# 📦 SERIALIZAR EMPRESA
# =========================================================

def serializar_empresa(
    e,
    db: Session
):

    # =====================================================
    # ⭐ AVALIAÇÕES
    # =====================================================

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == e.id
    ).all()

    media = 0.0

    if len(avaliacoes) > 0:

        media = round(
            sum(a.nota for a in avaliacoes)
            / len(avaliacoes),
            1
        )

    # =====================================================
    # 📷 FOTOS
    # =====================================================

    lista_fotos = []

    for f in e.fotos:

        lista_fotos.append({
            "id": f.id,
            "url": f.url,
            "principal": bool(f.principal),
            "public_id": getattr(
                f,
                "public_id",
                None
            )
        })

    # =====================================================
    # 📦 SERIALIZAÇÃO BASE
    # =====================================================

    plano = getattr(e, "plano", "gratuito")

    empresa_serializada = {

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

        # =================================================
        # ⭐ PLANO (FONTE DA VERDADE)
        # =================================================

        "plano": plano,

        # =================================================
        # 🔐 PERMISSÕES (NOVO SISTEMA)
        # =================================================

        "permissoes": get_permissoes(plano),

        # =================================================
        # ⭐ CAMPOS LEGADOS (mantidos por compatibilidade)
        # =================================================

        "premium": bool(getattr(e, "premium", False)),
        "destaque": bool(getattr(e, "destaque", False)),

        "prioridade": int(getattr(e, "prioridade", 0) or 0),

        "whatsapp_destacado": bool(getattr(e, "whatsapp_destacado", False)),
        "exibir_no_topo": bool(getattr(e, "exibir_no_topo", False)),
        "selo_premium": bool(getattr(e, "selo_premium", False)),
        "is_premium": bool(getattr(e, "is_premium", False)),

        # =================================================
        # ⭐ AVALIAÇÃO
        # =================================================

        "avaliacao_media": media,
        "total_avaliacoes": len(avaliacoes),

        # =================================================
        # 📄 DOCUMENTOS
        # =================================================

        "cpf": e.cpf,
        "cnpj": e.cnpj,

        # =================================================
        # 🛠 SERVIÇO
        # =================================================

        "servico_id": e.servico_id,

        # =================================================
        # 📷 FOTOS
        # =================================================

        "foto_principal": obter_foto_principal(e.fotos),
        "fotos": lista_fotos,

        # =================================================
        # ⭐ AVALIAÇÕES DETALHADAS
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
    print("PLANO =", empresa_serializada["plano"])
    print("PERMISSÕES =", empresa_serializada["permissoes"])

    return empresa_serializada


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

    print(f"\n🔥 TOTAL EMPRESAS: {len(empresas)}")

    empresas.sort(
        key=lambda x: (
            -int(getattr(x, "prioridade", 0) or 0),
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

    return serializar_empresa(empresa, db)