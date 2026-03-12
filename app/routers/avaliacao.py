from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.avaliacao_model import Avaliacao
from app.schemas.avaliacao_schema import AvaliacaoCreate, AvaliacaoResponse
from app.core.security import verificar_token

from app.dependencies import get_current_user

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AvaliacaoResponse)
def criar_avaliacao(avaliacao: AvaliacaoCreate, db: Session = Depends(get_db), user=Depends(verificar_token)):
    nova_avaliacao = Avaliacao(**avaliacao.dict())
    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)
    return nova_avaliacao