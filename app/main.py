print("🔥🔥🔥 MAIN CARREGADO 🔥🔥🔥")

import os
import traceback

import app.config.cloudinary_config  # mantém inicialização

from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Response,
    Request
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text

from app.database import engine, init_db

# =========================================================
# 🌐 CONFIG
# =========================================================

BASE_URL = os.getenv(
    "BASE_URL",
    "https://bsm-servicos-backend-1.onrender.com"
)

print("🌐 BASE_URL =", BASE_URL)

# =========================================================
# 🔐 AUTH
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = oauth2_scheme):
    return {
        "token": token,
        "is_admin": True
    }


# =========================================================
# 🚀 APP (CRIAÇÃO PRIMEIRO!)
# =========================================================

app = FastAPI(
    title="BSM Serviços API",
    version="1.0.5",
    description="API BSM Serviços",
    lifespan=None,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True
    }
)

# =========================================================
# 🌐 CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =========================================================
# 📁 STATIC FILES
# =========================================================

UPLOAD_DIR = "uploads"

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

# =========================================================
# 🔧 BANCO
# =========================================================

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

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS foto_principal VARCHAR;
            """))

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS premium BOOLEAN DEFAULT FALSE;
            """))

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS destaque BOOLEAN DEFAULT FALSE;
            """))

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS plano VARCHAR DEFAULT 'gratuito';
            """))

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS prioridade INTEGER DEFAULT 0;
            """))

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS whatsapp_destacado BOOLEAN DEFAULT FALSE;
            """))

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS exibir_no_topo BOOLEAN DEFAULT FALSE;
            """))

            conn.execute(text("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS selo_premium BOOLEAN DEFAULT FALSE;
            """))

        print("✅ Banco atualizado!")

    except Exception as e:
        print("❌ ERRO BANCO:", repr(e))
        traceback.print_exc()


# =========================================================
# 🚀 LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n🚀 Iniciando aplicação...")

    try:
        init_db()
        ajustar_banco()
        print("✅ Aplicação pronta!")

    except Exception as e:
        print("❌ ERRO NA INICIALIZAÇÃO:", repr(e))
        traceback.print_exc()

    yield

    print("\n🛑 Encerrando aplicação...")


app.router.lifespan_context = lifespan


# =========================================================
# 🔗 ROUTERS (IMPORT CORRETO E SEM DUPLICAÇÃO)
# =========================================================

from app.controllers.auth_controller import router as auth_router
from app.routes.empresa import router as empresa_router
from app.controllers.servico_controller import router as servico_router
from app.controllers.usuario_controller import router as usuario_router
from app.routers.utils import router as utils_router
from app.routers.avaliacao import router as avaliacoes_router

# =========================================================
# 📌 INCLUDE ROUTERS
# =========================================================

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(empresa_router)  # 🔥 AQUI entra /empresa/{id}/fotos
app.include_router(servico_router, prefix="/servicos", tags=["Serviços"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(utils_router)
app.include_router(avaliacoes_router, prefix="/avaliacoes", tags=["Avaliações"])

# =========================================================
# 🔧 HELPERS
# =========================================================

def gerar_url_imagem(caminho: str):
    if not caminho:
        return None

    return f"{BASE_URL}/{caminho.replace('\\', '/')}"


# =========================================================
# ❤️ HEALTH
# =========================================================

@app.get("/health")
def health():
    return {"status": "ok"}


# =========================================================
# 🏠 ROOT
# =========================================================

@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


# =========================================================
# 💥 ERRO GLOBAL
# =========================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    print("\n💥 ERRO GLOBAL REAL:")
    print(f"URL: {request.url}")
    print(f"ERRO: {repr(exc)}")

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


# =========================================================
# 🔥 DEBUG ROTAS
# =========================================================

print("\n🔥🔥🔥 BACKEND NOVO RODANDO 🔥🔥🔥")

for route in app.routes:
    print(route.path)