print("🔥🔥🔥 MAIN NOVO 🔥🔥🔥")

import os
import traceback
from app.routers.dashboard_router import router as dashboard_router
from contextlib import asynccontextmanager

import app.config.cloudinary_config
from app.controllers.dashboard_controller import router as dashboard_router

from fastapi import (
    FastAPI,
    Response,
    Request,
    Depends
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles

from app.database import (
    init_db
)

# =========================================================
# 🌐 CONFIG
# =========================================================

BASE_URL = os.getenv(
    "BASE_URL",
    "https://bsm-servicos-backend.onrender.com"
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
# 🔥 LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n🚀 Iniciando aplicação...")

    try:

        init_db()

        print("✅ Banco conectado")
        print("✅ Aplicação pronta")

    except Exception as e:

        print("\n❌ ERRO NA INICIALIZAÇÃO")
        print(repr(e))

        traceback.print_exc()

    yield

    print("\n🛑 Encerrando aplicação")

# =========================================================
# 🚀 APP
# =========================================================

app = FastAPI(
    title="BSM Serviços API",
    version="1.0.6",
    description="API Oficial BSM Serviços",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True
    }
)



# =========================================================
# 🔗 ROUTERS
# =========================================================

from app.controllers.auth_controller import (
    router as auth_router
)

from app.controllers.servico_controller import (
    router as servico_router
)

from app.controllers.usuario_controller import (
    router as usuario_router
)

from app.routers.utils import (
    router as utils_router
)

from app.routers.empresa import (
    router as empresa_router
)

from app.routers.avaliacao import (
    router as avaliacoes_router
)

# =========================================================
# 🌐 CORS
# =========================================================

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:51361",
    "http://127.0.0.1:51361",
    "https://bsm-servicos-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# =========================================================
# TESTE CORS
# =========================================================

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {"ok": True}


# =========================================================
# 📁 UPLOADS
# =========================================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

# =========================================================
# 🔗 REGISTRO DAS ROTAS
# =========================================================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    empresa_router,
    prefix="/empresa",
    tags=["Empresa"]
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
    avaliacoes_router
)

# =========================================================
# ❤️ HEALTH CHECK
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

# =========================================================
# 🔇 FAVICON
# =========================================================

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

    print("\n💥 ERRO GLOBAL")

    print(f"URL: {request.url}")
    print(f"ERRO: {repr(exc)}")

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
    )

app.include_router(dashboard_router)

#
# =========================================================
# 🔥 LOG FINAL
# =========================================================
#

print("🔥 BACKEND CARREGADO")
print("📄 Swagger: /docs")
print("📄 Redoc: /redoc")
print("❤️ Health: /health")