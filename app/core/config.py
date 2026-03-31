import os
from pathlib import Path
from dotenv import load_dotenv

# 🔹 Carrega variáveis do .env (local)
load_dotenv()

# 🔹 Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent

# =========================
# 🗄️ BANCO DE DADOS
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não definida no ambiente!")

# 🔥 Correção obrigatória do Render (postgres → postgresql)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")


# =========================
# 🔐 SEGURANÇA (JWT)
# =========================
SECRET_KEY = os.getenv("brg7573xpxp0376x")

if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY não definida no ambiente! (Render ou .env)")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================
# 📂 UPLOADS
# =========================
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


# =========================
# 🔎 DEBUG (opcional)
# =========================
print("🔐 CONFIG CARREGADA:")
print("DATABASE_URL OK")
print("SECRET_KEY OK")