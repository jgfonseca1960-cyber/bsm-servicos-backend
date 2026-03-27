from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parent

# 🔥 CONFIGURAÇÃO DIRETA (sem .env)
DB_USER = "postgres"
DB_PASSWORD_RAW = "brg7573x"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bsm_servicos"

# Codifica senha (IMPORTANTE)
DB_PASSWORD = quote_plus(DB_PASSWORD_RAW)

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Segurança e JWT (opcional)
SECRET_KEY = "minha_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Uploads
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)