print("🔥🔥🔥 MAIN CARREGADO 🔥🔥🔥")

import os
import traceback

import app.config.cloudinary_config

from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Response,
    Depends,
    Request
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer

from fastapi.staticfiles import StaticFiles

from sqlalchemy import text

from app.database import (
    engine,
    init_db
)


# =========================================================
# CONTROLLERS / ROUTERS
# =========================================================

from app.controllers.auth_controller import (
    router as auth_router
)

from app.routes.empresa import router as empresa_router

app.include_router(empresa_router)

from app.controllers.servico_controller import (
    router as servico_router
)

from app.controllers.usuario_controller import (
    router as usuario_router
)

from app.routers.utils import (
    router as utils_router
)

from app.routers.avaliacao import (
    router as avaliacoes_router
)

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

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    return {
        "token": token,
        "is_admin": True
    }


# =========================================================
# 🔧 AJUSTAR BANCO
# =========================================================

def ajustar_banco():

    try:

        print("🔥 Ajustando banco...")

        with engine.begin() as conn:

            # =====================================================
            # 👤 USUÁRIOS
            # =====================================================

            conn.execute(text("""
                ALTER TABLE usuarios
                ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
            """))

            # =====================================================
            # 🏢 EMPRESAS
            # =====================================================

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

            # =====================================================
            # ⭐ PREMIUM
            # =====================================================

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

            # =====================================================
            # 🔥 DEBUG BANCO
            # =====================================================

            resultado = conn.execute(text("""
                SELECT
                    id,
                    nome,
                    premium,
                    destaque,
                    plano
                FROM empresas
                ORDER BY id
                LIMIT 10;
            """))

            print("\n🔥 DADOS PREMIUM NO BANCO:")

            for row in resultado:
                print(dict(row._mapping))

        print("\n✅ Banco atualizado!")

    except Exception as e:

        print("\n❌ ERRO BANCO:")
        print(repr(e))

        traceback.print_exc()


# =========================================================
# 📁 UPLOADS
# =========================================================

UPLOAD_DIR = "uploads"

EMPRESA_DIR = os.path.join(
    UPLOAD_DIR,
    "empresas"
)

os.makedirs(
    EMPRESA_DIR,
    exist_ok=True
)

# =========================================================
# 🚀 LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n🚀 Iniciando aplicação...")

    try:

        init_db()

        ajustar_banco()

        print("\n✅ Aplicação pronta!")

    except Exception as e:

        print("\n❌ ERRO NA INICIALIZAÇÃO:")
        print(repr(e))

        traceback.print_exc()

    yield

    print("\n🛑 Encerrando aplicação...")


# =========================================================
# 🚀 APP
# =========================================================

app = FastAPI(
    title="BSM Serviços API",
    version="1.0.5",
    description="API BSM Serviços",
    lifespan=lifespan,
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

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)

# =========================================================
# 📁 STATIC FILES
# =========================================================

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

# =========================================================
# 🔗 ROUTERS
# =========================================================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    empresa_router
)

app.include_router(
    servico_router,
    prefix="/servicos",
    tags=["Serviços"]
)

app.include_router(
    usuario_router,
    prefix="/usuarios",
    tags=["Usuários"]
)

app.include_router(
    utils_router
)

app.include_router(
    avaliacoes_router,
    prefix="/avaliacoes",
    tags=["Avaliações"]
)

# =========================================================
# 🔧 AUXILIAR URL IMAGEM
# =========================================================

def gerar_url_imagem(
    caminho: str
):

    if not caminho:
        return None

    caminho = caminho.replace(
        "\\",
        "/"
    )

    return f"{BASE_URL}/{caminho}"


# =========================================================
# ❤️ HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================================================
# 🏠 ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "msg": "API BSM Serviços rodando 🚀"
    }


@app.get("/favicon.ico")
def favicon():

    return Response(
        status_code=204
    )


# =========================================================
# 💥 ERRO GLOBAL
# =========================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    print("\n💥 ERRO GLOBAL REAL:")
    print(f"URL: {request.url}")
    print(f"ERRO: {repr(exc)}")

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
    )


# =========================================================
# 🔥 DEBUG ROTAS
# =========================================================

print("\n🔥🔥🔥 BACKEND NOVO RODANDO 🔥🔥🔥")

for route in app.routes:
    print(route.path)