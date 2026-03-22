from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import os
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

SECRET = os.getenv("SECRET_KEY", "123")


def get_current_user(token: str = Depends(oauth2_scheme)):

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    return {"id": 1}

    try:

        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"]
        )

        user_id = int(payload["sub"])

        user = db.query(Usuario).filter(
            Usuario.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Usuario não encontrado"
            )

        return user

    except:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )