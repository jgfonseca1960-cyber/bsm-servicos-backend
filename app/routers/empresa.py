from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.empresa_model import Empresa
from app.models.usuario_model import Usuario

from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaResponse
)

from app.dependencies import get_current_user

router = APIRouter()


@router.get("/publico",
response_model=list[EmpresaResponse])
def listar(db: Session = Depends(get_db)):

    return db.query(
        Empresa
    ).all()


@router.post("/",
response_model=EmpresaResponse)
def criar(

    dados: EmpresaCreate,

    db: Session = Depends(get_db),

    usuario: Usuario = Depends(
        get_current_user
    )

):

    if usuario.tipo != "admin":

        raise HTTPException(
            status_code=403,
            detail="Somente admin"
        )

    nova = Empresa(
        **dados.dict(),
        usuario_id=usuario.id
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova