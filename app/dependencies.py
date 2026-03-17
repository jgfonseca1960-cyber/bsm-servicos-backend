from fastapi import Depends, HTTPException
from jose import jwt

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario

SECRET_KEY = "segredo"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = int(
            payload["sub"]
        )

    except:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = db.query(
        Usuario
    ).get(user_id)

    if not user:

        raise HTTPException(
            status_code=401
        )

    return user