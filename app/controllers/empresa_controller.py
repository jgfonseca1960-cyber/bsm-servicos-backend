from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.database import get_db
from app.models.empresa_model import Empresa

# 🔹 SERVICE
from app.services.empresa_service import (
    criar_empresa,
    listar_empresas,
    buscar_empresa,
    atualizar_empresa,
    deletar_empresa
)

# 🔹 SCHEMAS
from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaResponse,
    EmpresaUpdate
)

# 🔥 AUTH
from app.dependencies.auth import get_current_admin

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


# =========================
# 🔥 CRIAR (ADMIN)
# =========================
@router.post("/", response_model=EmpresaResponse)
def criar_nova_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return criar_empresa(db, empresa)


# =========================
# 🔹 LISTAR (PÚBLICO)
# =========================

@router.get("/")
def listar_todas_empresas(db: Session = Depends(get_db)):
    try:
        return db.query(Empresa).all()
    except Exception as e:
        print("ERRO LISTAR:", str(e))
        raise

# =========================
# 🔹 BUSCAR POR ID
# =========================
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa_por_id(
    empresa_id: int,
    db: Session = Depends(get_db)  # ✔ obrigatório
):
    return buscar_empresa(db, empresa_id)


# =========================
# 🔥 ATUALIZAR (ADMIN)
# =========================

@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa_existente(
    empresa_id: int,
    empresa: EmpresaUpdate,  # ✔ body
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return atualizar_empresa(db, empresa_id, empresa)

# =========================
# 🔥 DELETAR (ADMIN)
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa_existente(
    empresa_id: int,
    db: Session = Depends(get_db),  # ✔ obrigatório
    admin=Depends(get_current_admin)
):
    return deletar_empresa(db, empresa_id)