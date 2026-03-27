import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 🔥 Pega do Render (ESSENCIAL)
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔧 Ajuste automático (compatibilidade Render)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# Segurança e JWT (opcional)
SECRET_KEY = "minha_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Uploads
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)