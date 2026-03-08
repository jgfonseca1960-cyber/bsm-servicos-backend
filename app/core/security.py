from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# configuração do JWT
# SECRET_KEY = "bsm_servicos_secret"
# ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

# criptografia da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# autenticação swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ==============================
# GERAR HASH DA SENHA
# ==============================

def get_password_hash(password: str):
    return pwd_context.hash(password)


# ==============================
# VERIFICAR SENHA
# ==============================

def verificar_senha(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ==============================
# CRIAR TOKEN
# ==============================

def criar_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# ==============================
# VALIDAR TOKEN
# ==============================

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")