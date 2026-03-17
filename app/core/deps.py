from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import os

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

SECRET = os.getenv("SECRET_KEY", "123")


def get_current_user(
    token: str = Depends(oauth2)
):

    try:

        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"]
        )

        return payload["sub"]

    except:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )