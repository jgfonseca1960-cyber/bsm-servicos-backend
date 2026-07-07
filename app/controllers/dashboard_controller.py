from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.empresa_model import Empresa
from app.models.servico_model import Servico
from app.models.avaliacao_model import Avaliacao

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)