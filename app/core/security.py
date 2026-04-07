from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# 🔐 Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 dia

# 🔑 Hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Gerar hash da senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ✅ Verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Criar token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Decodificar token JWT
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# 🔥🔥🔥 CORREÇÃO DEFINITIVA (COMPATIBILIDADE)
# evita quebrar arquivos antigos que usam português
verificar_senha = verify_password
criar_token = create_access_token