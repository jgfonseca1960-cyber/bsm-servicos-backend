from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servico_service
from app.schemas import ServicoCreate, ServicoResponse

router = APIRouter(prefix="/servicos", tags=["Serviços"])


@router.post("/", response_model=ServicoResponse)
def criar_servico(servico: ServicoCreate, db: Session = Depends(get_db)):
    return servico_service.criar_servico(db, servico)


@router.get("/", response_model=list[ServicoResponse])
def listar_servico(db: Session = Depends(get_db)):
    return servico_service.listar_servicos(db)

@router.get("/servico")
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(Servico).all()

