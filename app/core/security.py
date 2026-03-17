from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

SECRET = os.getenv("SECRET_KEY", "123")

pwd = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_senha(senha: str):
    return pwd.hash(senha)


def verificar_senha(
    senha,
    hash
):
    return pwd.verify(senha, hash)


def criar_token(
    data: dict
):
    payload = data.copy()

    payload["exp"] = (
        datetime.utcnow()
        + timedelta(hours=8)
    )

    return jwt.encode(
        payload,
        SECRET,
        algorithm="HS256"
    )