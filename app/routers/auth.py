from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import verificar_senha, criar_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()

    if not user:
        return {"erro": "usuario nao encontrado"}

    if not verificar_senha(
        form_data.password,
        user.senha
    ):
        return {"erro": "senha invalida"}

    token = criar_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }