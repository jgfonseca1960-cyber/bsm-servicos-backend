from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import os
from uuid import uuid4

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto

router = APIRouter(
    prefix="/empresa",
    tags=["Empresas"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# 📦 SCHEMAS (NÃO QUEBRA SWAGGER)
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
# 📌 LISTAGEM (ORIGINAL + FILTROS OPCIONAIS)
# =========================
@router.get("/")
def listar_empresas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    cidade: Optional[str] = None,
    servico_id: Optional[int] = None,
    busca: Optional[str] = None
):
    query = db.query(Empresa)

    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))

    if servico_id:
        query = query.filter(Empresa.servico_id == servico_id)

    if busca:
        query = query.filter(Empresa.nome.ilike(f"%{busca}%"))

    empresas = query.offset(skip).limit(limit).all()

    return [
        {
            "id": e.id,
            "nome": e.nome,
            "descricao": e.descricao,
            "telefone": e.telefone,

            "endereco": e.endereco,
            "bairro": e.bairro,
            "cidade": e.cidade,
            "estado": e.estado,
            "cep": e.cep,

            "latitude": e.latitude,
            "longitude": e.longitude,

            "ativo": e.ativo,
            "avaliacao_media": e.avaliacao_media,

            "cpf": e.cpf,
            "cnpj": e.cnpj,

            "servico_id": e.servico_id,

            "fotos": [
                {"id": f.id, "url": f.url}
                for f in e.fotos
            ]
        }
        for e in empresas
    ]


# =========================
# 🔍 DETALHE (MANTIDO)
# =========================
@router.get("/{empresa_id}")
def detalhe_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "descricao": empresa.descricao,
        "telefone": empresa.telefone,

        "endereco": empresa.endereco,
        "bairro": empresa.bairro,
        "cidade": empresa.cidade,
        "estado": empresa.estado,
        "cep": empresa.cep,

        "latitude": empresa.latitude,
        "longitude": empresa.longitude,

        "ativo": empresa.ativo,
        "avaliacao_media": empresa.avaliacao_media,

        "cpf": empresa.cpf,
        "cnpj": empresa.cnpj,

        "servico_id": empresa.servico_id,

        "fotos": [
            {"id": f.id, "url": f.url}
            for f in empresa.fotos
        ]
    }


# =========================
# ➕ CRIAR (SEGURO PARA FLUTTER)
# =========================
@router.post("/")
def criar_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    empresa = Empresa(**data.model_dump())

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa criada com sucesso", "id": empresa.id}


# =========================
# ✏️ ATUALIZAR
# =========================
@router.put("/{empresa_id}")
def atualizar_empresa(
    empresa_id: int,
    data: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa atualizada com sucesso"}


# =========================
# ❌ DELETAR
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()

    return {"msg": "Empresa deletada com sucesso"}


# =========================
# 📸 UPLOAD FOTO
# =========================
@router.post("/{empresa_id}/upload-foto")
async def upload_foto(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    filename = f"{uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    url = f"/uploads/{filename}"

    foto = EmpresaFoto(
        empresa_id=empresa_id,
        url=url
    )

    db.add(foto)
    db.commit()

    return {"msg": "Foto enviada com sucesso", "url": url}


# =========================================================
# 🚀 EVOLUÇÕES SEGURAS (NOVAS FUNCIONALIDADES SEM QUEBRAR)
# =========================================================


# 📊 ESTATÍSTICAS
@router.get("/_stats/overview")
def estatisticas(db: Session = Depends(get_db)):
    total = db.query(Empresa).count()
    ativas = db.query(Empresa).filter(Empresa.ativo == True).count()

    return {
        "total_empresas": total,
        "empresas_ativas": ativas,
        "taxa_ativas": round((ativas / total) * 100, 2) if total > 0 else 0
    }


# 🏆 RANKING
@router.get("/ranking")
def ranking(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).order_by(
        Empresa.avaliacao_media.desc().nullslast()
    ).limit(20).all()

    return [
        {
            "id": e.id,
            "nome": e.nome,
            "avaliacao_media": e.avaliacao_media,
            "cidade": e.cidade
        }
        for e in empresas
    ]


# 🔎 BUSCA AVANÇADA
@router.get("/buscar")
def buscar(
    q: str,
    cidade: Optional[str] = None,
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Empresa)

    if q:
        query = query.filter(Empresa.nome.ilike(f"%{q}%"))

    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))

    if ativo is not None:
        query = query.filter(Empresa.ativo == ativo)

    return query.limit(50).all()


# 📊 CONTAGEM
@router.get("/count")
def count(db: Session = Depends(get_db)):
    return {"total": db.query(Empresa).count()}


# 📍 EMPRESAS PRÓXIMAS (BÁSICO)
@router.get("/proximas")
def proximas(lat: float, lng: float, raio: float = 10, db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()

    resultado = []

    for e in empresas:
        if e.latitude is None or e.longitude is None:
            continue

        dist = ((e.latitude - lat)**2 + (e.longitude - lng)**2) ** 0.5

        if dist <= raio:
            resultado.append({
                "id": e.id,
                "nome": e.nome,
                "distancia": round(dist, 4),
                "cidade": e.cidade
            })

    return resultado


# 🧪 STATUS
@router.get("/_health")
def health():
    return {
        "module": "empresa",
        "status": "ok",
        "version": "stable-v3"
    }