from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.usuario_model import Usuario
from app.core.security import verificar_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    user_id = verificar_token(token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = db.query(Usuario).filter(
        Usuario.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return user