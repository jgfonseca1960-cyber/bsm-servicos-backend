print("🔥🔥🔥 MAIN CARREGADO 🔥🔥🔥")

import app.config.cloudinary_config

from fastapi import FastAPI, Response, Depends, Request
from contextlib import asynccontextmanager
from sqlalchemy import text
import traceback
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app.database import engine, init_db

# CONTROLLERS
from app.controllers.auth_controller import router as auth_router
from app.controllers.empresa_controller import router as empresa_router
from app.controllers.servico_controller import router as servico_router
from app.controllers.usuario_controller import router as usuario_router
from app.routers.utils import router as utils_router


# =========================
# 🌐 CONFIG
# =========================
BASE_URL = os.getenv(
    "BASE_URL",
    "https://bsm-servicos-backend.onrender.com"
)


# =========================
# 🔐 AUTH
# =========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token, "is_admin": True}


# =========================
# 🔧 BANCO (SEGURO)
# =========================
def ajustar_banco():
    try:
        print("🔥 Ajustando banco...")

        with engine.begin() as conn:

            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas 
                ADD COLUMN IF NOT EXISTS whatsapp VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas 
                ADD COLUMN IF NOT EXISTS email VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas 
                ADD COLUMN IF NOT EXISTS bairro VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas 
                ADD COLUMN IF NOT EXISTS estado VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas 
                ADD COLUMN IF NOT EXISTS cep VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas 
                ADD COLUMN IF NOT EXISTS cpf VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas 
                ADD COLUMN IF NOT EXISTS cnpj VARCHAR;
            """))

        print("✅ Banco atualizado!")

    except Exception as e:
        print("❌ ERRO BANCO:")
        traceback.print_exc()


# =========================
# 📁 UPLOAD
# =========================
UPLOAD_DIR = "uploads"
EMPRESA_DIR = os.path.join(UPLOAD_DIR, "empresas")

os.makedirs(EMPRESA_DIR, exist_ok=True)


# =========================
# 🚀 LIFESPAN (CORRIGIDO)
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando aplicação...")

    try:
        init_db()
        ajustar_banco()

        print("🌐 BASE_URL:", BASE_URL)
        print("✅ App pronta!")

    except Exception:
        print("❌ ERRO NA INICIALIZAÇÃO:")
        traceback.print_exc()

    yield  # 🔥 ESSENCIAL (NÃO REMOVER)

    print("🛑 Encerrando aplicação...")


# =========================
# 🚀 APP
# =========================
app = FastAPI(
    title="BSM Serviços API",
    version="1.0.2",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)


# =========================
# 🌐 CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 📁 STATIC
# =========================
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)


# =========================
# 🔗 ROUTES
# =========================
app.include_router(auth_router, prefix="/auth")
app.include_router(empresa_router, prefix="/empresa")
app.include_router(servico_router, prefix="/servicos")
app.include_router(usuario_router, prefix="/usuarios")
app.include_router(utils_router)


# =========================
# 🔧 AUX
# =========================
def gerar_url_imagem(caminho: str):
    if not caminho:
        return None
    return f"{BASE_URL}/{caminho.replace('\\', '/')}"


# =========================
# 🔧 HEALTHCHECK (IMPORTANTE)
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# 🔧 ROOT
# =========================
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}


# =========================
# 💥 ERRO GLOBAL
# =========================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("\n💥 ERRO GLOBAL:")
    print(f"URL: {request.url}")
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno"}
    )