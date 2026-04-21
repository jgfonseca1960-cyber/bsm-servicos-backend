print("🔥🔥🔥 MAIN CARREGADO 🔥🔥🔥")

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

# Controllers
from app.controllers.auth_controller import router as auth_router
from app.controllers.empresa_controller import router as empresa_router
from app.controllers.servico_controller import router as servico_router
from app.controllers.usuario_controller import router as usuario_router


# =========================
# 🔐 AUTH
# =========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token, "is_admin": True}


# =========================
# 🔧 BANCO
# =========================
def ajustar_banco():
    try:
        print("🔥 Ajustando banco...")

        with engine.begin() as conn:
            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
            """))

        print("✅ Banco pronto!")

    except Exception:
        print("❌ ERRO AO AJUSTAR BANCO:")
        traceback.print_exc()


# =========================
# 🚀 LIFESPAN
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando aplicação...")

    try:
        init_db()
        ajustar_banco()

        # 🔥 DEBUG: listar arquivos da pasta uploads
        if os.path.exists("uploads"):
            arquivos = os.listdir("uploads")
            print(f"📂 Arquivos em /uploads: {arquivos}")
        else:
            print("⚠️ Pasta uploads não existe")

        print("✅ Inicialização concluída!")

    except Exception:
        print("❌ ERRO NA INICIALIZAÇÃO:")
        traceback.print_exc()

    yield

    print("🛑 Encerrando aplicação...")


# =========================
# 🚀 FASTAPI APP
# =========================
app = FastAPI(
    title="BSM Serviços API",
    version="1.0.0",
    description="API com autenticação JWT",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True
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
# 📁 STATIC FILES (IMAGENS)
# =========================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

print(f"📁 Pasta uploads: {os.path.abspath(UPLOAD_DIR)}")

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

print("🖼 StaticFiles ativo em /uploads")


# =========================
# 🔧 FAVICON
# =========================
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


# =========================
# 🔐 AUTH CHECK
# =========================
@app.get("/auth-check")
def auth_check(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# =========================
# 📌 ROUTERS
# =========================
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(empresa_router, prefix="/empresa", tags=["Empresas"])
app.include_router(servico_router, prefix="/servicos", tags=["Serviços"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])


# =========================
# 🧪 ROOT
# =========================
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}


# =========================
# 💥 ERRO GLOBAL (DEBUG FORTE)
# =========================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("\n💥 ERRO GLOBAL:")
    print(f"URL: {request.url}")
    print(str(exc))
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno no servidor"}
    )


print("🔥🔥🔥 BACKEND NOVO RODANDO 🔥🔥🔥")