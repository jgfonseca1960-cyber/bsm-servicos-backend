from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from sqlalchemy import text
import traceback

from app.database import engine, init_db

# Controllers
from app.controllers.auth_controller import router as auth_router
from app.controllers.empresa_controller import router as empresa_router
from app.controllers.servico_controller import router as servico_router
from app.controllers.usuario_controller import router as usuario_router


# =========================
# 🔧 AJUSTE DE BANCO
# =========================
def ajustar_banco():
    try:
        print("🔥 Ajustando banco...")

        with engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
            """))
            conn.commit()

        print("✅ Banco pronto!")

    except Exception:
        print("❌ ERRO AO AJUSTAR BANCO:")
        traceback.print_exc()


# =========================
# 🔥 STARTUP
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("🚀 Iniciando aplicação...")

        init_db()
        ajustar_banco()

        print("✅ Inicialização concluída!")

    except Exception:
        print("❌ ERRO NA INICIALIZAÇÃO:")
        traceback.print_exc()

    yield


# =========================
# 🚀 APP (CRIA PRIMEIRO)
# =========================
app = FastAPI(
    title="BSM Serviços API",
    version="1.0.0",
    description="API com autenticação JWT",
    lifespan=lifespan
)


# =========================
# 🔧 FAVICON
# =========================
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


# =========================
# 📌 ROTAS
# =========================
app.include_router(auth_router)
app.include_router(empresa_router)
app.include_router(servico_router)
app.include_router(usuario_router)


# =========================
# 🧪 TESTE
# =========================
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}