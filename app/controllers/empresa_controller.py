from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
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

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# =========================
# 📌 LISTAR EMPRESAS
# =========================
@router.get("/empresas", response_model=List[dict])
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()

    return [
        {
            "id": e.id,
            "nome": e.nome,
            "telefone": e.telefone,
            "email": e.email,
            "endereco": e.endereco,
            "latitude": e.latitude,
            "longitude": e.longitude,

            # 🔥 FOTOS
            "fotos": [
                {
                    "id": f.id,
                    "url": f.url
                }
                for f in e.fotos
            ]
        }
        for e in empresas
    ]


# =========================
# 🔄 COMPATIBILIDADE
# =========================
@router.get("/listar")
def listar_empresas_compat(db: Session = Depends(get_db)):
    return listar_empresas(db)


# =========================
# 🔍 DETALHE
# =========================
@router.get("/detalhe/{empresa_id}")
def detalhe_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "telefone": empresa.telefone,
        "email": empresa.email,
        "endereco": empresa.endereco,
        "latitude": empresa.latitude,
        "longitude": empresa.longitude,
        "fotos": [{"id": f.id, "url": f.url} for f in empresa.fotos]
    }


# =========================
# ➕ CRIAR
# =========================
@router.post("/")
def criar_empresa(data: dict, db: Session = Depends(get_db)):
    empresa = Empresa(**data)

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa criada", "id": empresa.id}


# =========================
# ✏️ ATUALIZAR
# =========================
@router.put("/{empresa_id}")
def atualizar_empresa(empresa_id: int, data: dict, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in data.items():
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

    url = f"https://bsm-servicos-backend.onrender.com/uploads/{filename}"

    foto = EmpresaFoto(
        empresa_id=empresa_id,
        url=url
    )

    db.add(foto)
    db.commit()

    return {"msg": "Foto enviada", "url": url}