from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def dashboard_overview(db: Session = Depends(get_db)):
    return {
        "usuarios": 0,
        "empresas": 0,
        "servicos": 0,
        "avaliacoes": 0,
    }