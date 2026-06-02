from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
import math
import os

from app.database import get_db

from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from app.models.servico_model import Servico
from app.models.avaliacao_model import Avaliacao

from app.utils.files import gerar_url_imagem

import cloudinary.uploader

from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaUpdate,
    EmpresaResponse
)

router = APIRouter(
    prefix="/empresa",
    tags=["Empresas"]
)

# =========================================================
# 📁 GARANTE PASTA UPLOAD
# =========================================================

os.makedirs(
    "uploads/empresas",
    exist_ok=True
)

# =========================================================
# 📍 DISTÂNCIA
# =========================================================

def calcular_distancia(
    lat1,
    lon1,
    lat2,
    lon2
):

    if (
        lat1 is None
        or lon1 is None
        or lat2 is None
        or lon2 is None
    ):
        return None

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return round(R * c, 2)

# =========================================================
# 🔧 TRATAR URL
# =========================================================

def tratar_url(url: str):

    if not url:
        return None

    if url.startswith("http"):
        return url

    return gerar_url_imagem(url)

# =========================================================
# 🔥 SERIALIZER
# =========================================================

def serializar_empresa(
    e: Empresa,
    db: Session,
    user_lat=None,
    user_lon=None
):


    # =====================================================
    # ⭐ AVALIAÇÕES
    # =====================================================

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

    # =====================================================
    # 📸 FOTOS
    # =====================================================

    fotos_validas = []

    fotos_ordenadas = sorted(
        e.fotos or [],
        key=lambda x: (
            not x.principal,
            x.id
        )
    )

    for f in fotos_ordenadas:

        url = tratar_url(f.url)

        if not url:
            continue

        fotos_validas.append({
            "id": f.id,
            "url": url,
            "principal": bool(f.principal)
        })

    foto_principal = None

    for foto in fotos_validas:

        if foto["principal"]:
            foto_principal = foto["url"]
            break

    if not foto_principal and fotos_validas:

        foto_principal = fotos_validas[0]["url"]

    # =====================================================
    # 📍 DISTÂNCIA
    # =====================================================

    distancia = None

    if (
        user_lat is not None
        and user_lon is not None
        and e.latitude is not None
        and e.longitude is not None
    ):

        distancia = calcular_distancia(
            user_lat,
            user_lon,
            e.latitude,
            e.longitude
        )

    # =====================================================
    # 🚀 SERIALIZAÇÃO
    # =====================================================

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

        "destaque": bool(
            getattr(e, "destaque", False)
        ),

        "plano": getattr(
            e,
            "plano",
            "gratuito"
        ),

        "prioridade": int(
            getattr(e, "prioridade", 0) or 0
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
              
        # ⭐ AVALIAÇÃO
        "avaliacao_media": media,
        "total_avaliacoes": len(avaliacoes),

        # 📄 DOCUMENTOS
        "cpf": e.cpf,
        "cnpj": e.cnpj,

        # 🧩 SERVIÇO
        "servico_id": e.servico_id,

        # 📸 FOTOS
        "foto_principal": foto_principal,
        "fotos": fotos_validas,

    "distancia_km": distancia,

    "avaliacoes": [
        {
            "id": a.id,
            "usuario": f"Usuário {a.usuario_id}",
            "nota": a.nota,
            "comentario": a.comentario
        }
        for a in avaliacoes
    ]
}

# =========================================================
# 🏆 PESO DOS PLANOS
# =========================================================

def peso_plano(plano):

    plano = (plano or "").lower()

    if plano == "master":
        return 0

    if plano == "premium":
        return 1

    return 2

# =========================================================
# 🔍 LISTAR EMPRESAS
# =========================================================

@router.get(
    "/",
    response_model=List[EmpresaResponse]
)
def listar_empresas(
    db: Session = Depends(get_db),
    servico_id: Optional[int] = None,
    cidade: Optional[str] = None,
    bairro: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
):

    query = db.query(Empresa)

    if servico_id:
        query = query.filter(
            Empresa.servico_id == servico_id
        )

    if cidade:
        query = query.filter(
            Empresa.cidade.ilike(f"%{cidade}%")
        )

    if bairro:
        query = query.filter(
            Empresa.bairro.ilike(f"%{bairro}%")
        )

    empresas = query.all()

    resultado = [
        serializar_empresa(
            e,
            db,
            latitude,
            longitude
        )
        for e in empresas
    ]

    resultado.sort(
        key=lambda x: (
            not bool(x.get("exibir_no_topo", False)),
            peso_plano(x.get("plano")),
            -int(x.get("prioridade", 0)),
            x["nome"].lower()
        )
    )

    if latitude is not None and longitude is not None:

        resultado.sort(
            key=lambda x: (
                peso_plano(x.get("plano")),
                x["distancia_km"]
                if x["distancia_km"] is not None
                else 999999
            )
        )

    return resultado

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
# ➕ CRIAR EMPRESA
# =========================================================

@router.post(
    "/",
    response_model=EmpresaResponse
)
def criar_empresa(
    data: EmpresaCreate,
    db: Session = Depends(get_db)
):

    empresa = Empresa(**data.model_dump())

    db.add(empresa)

    db.commit()

    db.refresh(empresa)

    return serializar_empresa(
        empresa,
        db
    )

# =========================================================
# ✏️ ATUALIZAR EMPRESA
# =========================================================

@router.put(
    "/{empresa_id}",
    response_model=EmpresaResponse
)
def atualizar_empresa(
    empresa_id: int,
    data: EmpresaUpdate,
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

    update_data = data.model_dump(
        exclude_unset=True
    )

    # ==========================================
    # REGRAS DOS PLANOS
    # ==========================================

    plano = update_data.get("plano")

    if plano == "gratuito":
        update_data["destaque"] = False
        update_data["whatsapp_destacado"] = False
        update_data["exibir_no_topo"] = False
        update_data["selo_premium"] = False
        update_data["prioridade"] = 0

    elif plano == "premium":
        update_data["destaque"] = True
        update_data["whatsapp_destacado"] = True
        update_data["exibir_no_topo"] = False
        update_data["selo_premium"] = True
        update_data["prioridade"] = 50

    elif plano == "master":
        update_data["destaque"] = True
        update_data["whatsapp_destacado"] = True
        update_data["exibir_no_topo"] = True
        update_data["selo_premium"] = True
        update_data["prioridade"] = 100

    for key, value in update_data.items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return serializar_empresa(
        empresa,
        db
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
        "msg": "Empresa deletada"
    }