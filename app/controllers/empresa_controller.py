from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import os
from uuid import uuid4

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto

# 🔥 SEM PREFIXO AQUI (REGRA DE OURO)
router = APIRouter(
    tags=["Empresas"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
# 🔧 SERIALIZER
# =========================
def empresa_to_dict(e: Empresa):
    return {
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
            for f in (e.fotos or [])
        ]
    }


# =========================
# 📌 LISTAGEM
# =========================
@router.get("/")
def listar_empresas(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    empresas = db.query(Empresa).offset(skip).limit(limit).all()
    return [empresa_to_dict(e) for e in empresas]


# =========================
# 🔥 ROTAS FIXAS
# =========================

@router.get("/_stats/overview")
def estatisticas(db: Session = Depends(get_db)):
    total = db.query(Empresa).count()
    ativas = db.query(Empresa).filter(Empresa.ativo == True).count()

    return {
        "total_empresas": total,
        "empresas_ativas": ativas,
        "taxa_ativas": round((ativas / total) * 100, 2) if total else 0
    }


@router.get("/ranking")
def ranking(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).order_by(
        Empresa.avaliacao_media.desc().nullslast()
    ).limit(20).all()

    return [empresa_to_dict(e) for e in empresas]


@router.get("/buscar")
def buscar(q: str, cidade: Optional[str] = None, ativo: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(Empresa)

    if q:
        query = query.filter(Empresa.nome.ilike(f"%{q}%"))

    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))

    if ativo is not None:
        query = query.filter(Empresa.ativo == ativo)

    return [empresa_to_dict(e) for e in query.limit(50).all()]


@router.get("/proximas")
def proximas(lat: float, lng: float, raio: float = 10, db: Session = Depends(get_db)):
    empresas = db.query(Empresa).filter(
        Empresa.latitude.isnot(None),
        Empresa.longitude.isnot(None)
    ).all()

    resultado = []

    for e in empresas:
        dist = ((e.latitude - lat)**2 + (e.longitude - lng)**2) ** 0.5

        if dist <= raio:
            resultado.append({
                "id": e.id,
                "nome": e.nome,
                "distancia": round(dist, 4),
                "cidade": e.cidade
            })

    return resultado


@router.get("/_health")
def health():
    return {"status": "ok"}


# =========================
# 🔍 DETALHE (POR ÚLTIMO)
# =========================
@router.get("/{empresa_id}")
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
@router.put("/{empresa_id}")
def atualizar_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa atualizada"}


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

    return {"msg": "Empresa deletada"}


# =========================
# 📸 UPLOAD FOTO
# =========================
@router.post("/{empresa_id}/upload-foto")
async def upload_foto(empresa_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    filename = f"{uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    foto = EmpresaFoto(
        empresa_id=empresa_id,
        url=f"/uploads/{filename}"
    )

    db.add(foto)
    db.commit()

    return {"msg": "Foto enviada", "url": foto.url}