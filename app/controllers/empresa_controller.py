from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from pydantic import BaseModel
import math

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from app.utils.files import gerar_url_imagem

router = APIRouter(tags=["Empresas"])


# =========================
# 📦 SCHEMAS
# =========================
class EmpresaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = True
    avaliacao_media: Optional[float] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    servico_id: Optional[int] = None


class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = None
    avaliacao_media: Optional[float] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    servico_id: Optional[int] = None


# =========================
# 📍 FUNÇÃO DISTÂNCIA (HAVERSINE)
# =========================
def calcular_distancia(lat1, lon1, lat2, lon2):
    if not lat1 or not lon1 or not lat2 or not lon2:
        return None

    R = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)


# =========================
# 🔧 URL IMAGEM
# =========================
def tratar_url(url: str):
    if not url:
        return None

    if url.startswith("http"):
        return url

    return gerar_url_imagem(url)


# =========================
# 🔧 SERIALIZER
# =========================
def empresa_to_dict(e: Empresa, user_lat=None, user_lon=None):
    fotos_validas = []

    for f in (e.fotos or []):
        url = tratar_url(f.url)

        if not url:
            continue

        fotos_validas.append({
            "id": f.id,
            "url": url,
            "principal": f.principal
        })

    foto_principal = None

    for f in fotos_validas:
        if f["principal"]:
            foto_principal = f["url"]
            break

    if not foto_principal and fotos_validas:
        foto_principal = fotos_validas[0]["url"]

    distancia = None
    if user_lat and user_lon and e.latitude and e.longitude:
        distancia = calcular_distancia(
            user_lat, user_lon,
            e.latitude, e.longitude
        )

    return {
        "id": e.id,
        "nome": e.nome,
        "descricao": e.descricao,
        "telefone": e.telefone,
        "cidade": e.cidade,
        "bairro": e.bairro,
        "latitude": e.latitude,
        "longitude": e.longitude,
        "servico_id": e.servico_id,
        "foto_principal": foto_principal,
        "fotos": fotos_validas,
        "distancia_km": distancia  # 🔥 NOVO
    }


# =========================
# 🔍 BUSCA PROFISSIONAL
# =========================
@router.get("/")
def listar_empresas(
    db: Session = Depends(get_db),

    servico_id: Optional[int] = None,
    cidade: Optional[str] = None,
    bairro: Optional[str] = None,

    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
):
    query = db.query(Empresa)

    # 🔍 FILTROS
    if servico_id:
        query = query.filter(Empresa.servico_id == servico_id)

    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))

    if bairro:
        query = query.filter(Empresa.bairro.ilike(f"%{bairro}%"))

    empresas = query.all()

    resultado = [
        empresa_to_dict(e, latitude, longitude)
        for e in empresas
    ]

    # 📏 ORDENA POR DISTÂNCIA
    if latitude and longitude:
        resultado.sort(
            key=lambda x: x["distancia_km"] if x["distancia_km"] else 9999
        )

    return resultado


# =========================
# 🔍 DETALHE
# =========================
@router.get("/id/{empresa_id}")
def detalhe_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return empresa_to_dict(empresa)


# =========================
# ➕ CRIAR
# =========================
@router.post("/")
def criar_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    empresa = Empresa(**data.model_dump())
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa criada", "id": empresa.id}


# =========================
# ✏️ ATUALIZAR
# =========================
@router.put("/id/{empresa_id}")
def atualizar_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    return {"msg": "Empresa atualizada"}


# =========================
# ❌ DELETAR
# =========================
@router.delete("/id/{empresa_id}")
def deletar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()

    return {"msg": "Empresa deletada"}