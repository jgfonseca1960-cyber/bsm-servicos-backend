from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.core.security import gerar_hash

router = APIRouter(
    prefix="/usuario",
    tags=["Usuario"]
)


@router.post("/")
def criar(dados: UsuarioCreate, db: Session = Depends(get_db)):

    novo = Usuario(
        email=dados.email,
        senha_hash=gerar_hash(dados.senha),  # ✅ correto
        nome=dados.nome,
        is_admin=dados.is_admin
    )

    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    return novo