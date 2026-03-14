from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioResponse
from app.dependencies import get_current_user
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/me")
def me(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email
    }

router = APIRouter()


# =========================
# USUARIO LOGADO
# =========================

@router.get("/me", response_model=UsuarioResponse)
def usuario_logado(
    usuario: Usuario = Depends(get_current_user)
):

    return usuario