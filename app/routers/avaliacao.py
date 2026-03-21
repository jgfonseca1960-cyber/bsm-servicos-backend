from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_model import Avaliacao
from app.schemas.avaliacao_schema import AvaliacaoCreate


router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliações"]
)


@router.post("/")
def criar(av: AvaliacaoCreate, db: Session = Depends(get_db)):

    nova = Avaliacao(**av.dict())

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


@router.get("/")
def listar(db: Session = Depends(get_db)):

    return db.query(Avaliacao).all()