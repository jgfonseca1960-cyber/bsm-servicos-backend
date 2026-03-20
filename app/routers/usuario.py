from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.core.security import gerar_hash

router = APIRouter(
    prefix="/usuario",
    tags=["Usuario"]
)


@router.post("/")
def criar(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):

    novo = Usuario(
        email=dados.email,
        senha=gerar_hash(dados.senha),
        nome=dados.nome,
        is_admin=dados.is_admin
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo