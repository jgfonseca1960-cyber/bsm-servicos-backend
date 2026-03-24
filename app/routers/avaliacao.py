from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.avaliacao_model import Avaliacao
from app.schemas.avaliacao_schema import AvaliacaoCreate


router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliações"]
)


# criar avaliação
@router.post("/")
def criar(av: AvaliacaoCreate, db: Session = Depends(get_db)):

    existe = db.query(Avaliacao).filter(
        Avaliacao.usuario_id == av.usuario_id,
        Avaliacao.empresa_id == av.empresa_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Usuário já avaliou"
        )

    nova = Avaliacao(**av.dict())

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


# listar todas
@router.get("/")
def listar(db: Session = Depends(get_db)):

    return db.query(Avaliacao).all()


# listar por empresa

@router.get("/empresa/{empresa_id}")
def por_empresa(empresa_id: int, db: Session = Depends(get_db)):

    return db.query(Avaliacao).filter(
        Avaliacao.empresa_id == empresa_id
    ).all()


# média da empresa
@router.get("/media/{empresa_id}")
def media(empresa_id: int, db: Session = Depends(get_db)):

    m = db.query(
        func.avg(Avaliacao.nota)
    ).filter(
        Avaliacao.empresa_id == empresa_id
    ).scalar()

    return {"media": m}


# ranking empresas
@router.get("/ranking")
def ranking(db: Session = Depends(get_db)):

    r = db.query(
        Avaliacao.empresa_id,
        func.avg(Avaliacao.nota).label("media"),
        func.count(Avaliacao.id).label("total")
    ).group_by(
        Avaliacao.empresa_id
    ).order_by(
        func.avg(Avaliacao.nota).desc()
    ).all()

    return r
