from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.core.security import hash_senha

router = APIRouter(
    prefix="/usuario",
    tags=["Usuario"]
)


@router.post("/")
def criar(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):

    user = Usuario(
        email=dados.email,
        senha=hash_senha(dados.senha)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user