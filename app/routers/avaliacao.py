from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_model import Avaliacao

router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliações"]
)


@router.post("/")
def criar_avaliacao(
    nota: int,
    comentario: str,
    empresa_id: int,
    db: Session = Depends(get_db)
):

    nova = Avaliacao(
        nota=nota,
        comentario=comentario,
        empresa_id=empresa_id
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


@router.get("/")
def listar(db: Session = Depends(get_db)):
    return db.query(Avaliacao).all()