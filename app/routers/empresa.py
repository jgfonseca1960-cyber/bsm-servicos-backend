from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import EmpresaCreate
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
)


@router.post("/")
def criar(
    dados: EmpresaCreate,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    nova = Empresa(
        nome=dados.nome,
        cidade=dados.cidade,
        usuario_id=user
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


@router.get("/")
def listar(
    db: Session = Depends(get_db)
):

    return db.query(Empresa).all()