from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os

# =========================
# 🔐 CONFIGURAÇÕES JWT
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 dia

# 🔥 IMPORTANTE (corrige o Authorize)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# =========================
# 🔑 HASH DE SENHA
# =========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# ✅ GERAR HASH
# =========================
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# =========================
# ✅ VERIFICAR SENHA
# =========================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =========================
# ✅ CRIAR TOKEN
# =========================
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# ✅ DECODIFICAR TOKEN
# =========================
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# =========================
# 🔥 COMPATIBILIDADE
# =========================
verificar_senha = verify_password
criar_token = create_access_token