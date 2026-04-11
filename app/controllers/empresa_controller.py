from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.servico_model import Servico

# 🔹 SERVICE
from app.services.empresa_service import (
    criar_empresa,
    listar_empresas,
    buscar_empresa,
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
@router.get("/", response_model=List[EmpresaResponse])
def listar_todas_empresas(db: Session = Depends(get_db)):
    try:
        return listar_empresas(db)
    except Exception as e:
        print("🔥 ERRO LISTAR:", str(e))
        raise HTTPException(status_code=500, detail="Erro ao listar empresas")


# =========================
# 🔹 BUSCAR POR ID
# =========================
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa_por_id(empresa_id: int, db: Session = Depends(get_db)):
    try:
        return buscar_empresa(db, empresa_id)
    except HTTPException:
        raise
    except Exception as e:
        print("🔥 ERRO AO BUSCAR EMPRESA:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao buscar empresa")


# =========================
# 🔥 ATUALIZAR (ADMIN)
# =========================
@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa_existente(
    empresa_id: int,
    dados: EmpresaUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")

        update_data = dados.dict(exclude_unset=True)

        for key, value in update_data.items():

            # 🔥 validação forte
            if key == "servico_id":
                if value is not None:
                    servico = db.query(Servico).filter(Servico.id == value).first()
                    if not servico:
                        raise HTTPException(
                            status_code=400,
                            detail="servico_id inválido"
                        )

            setattr(empresa, key, value)

        db.commit()
        db.refresh(empresa)

        return empresa

    except HTTPException:
        raise
    except Exception as e:
        print("🔥 ERRO AO ATUALIZAR:", str(e))
        raise HTTPException(status_code=500, detail="Erro ao atualizar empresa")


# =========================
# 🔥 DELETAR (ADMIN)
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa_existente(
    empresa_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        return deletar_empresa(db, empresa_id)
    except Exception as e:
        print("🔥 ERRO AO DELETAR:", str(e))
        raise HTTPException(status_code=500, detail="Erro ao deletar empresa")