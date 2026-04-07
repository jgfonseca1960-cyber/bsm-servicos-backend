from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # 🔥 ISSO É O SEGREDO
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Senha inválida")

    token = create_access_token({
        "sub": str(user.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }