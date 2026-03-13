from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioResponse
from app.dependencies import get_current_user


router = APIRouter()


# =========================
# USUARIO LOGADO
# =========================

@router.get("/me", response_model=UsuarioResponse)
def usuario_logado(
    usuario: Usuario = Depends(get_current_user)
):

    return usuario