from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.database import engine, init_db

# controllers
from app.controllers import (
    empresa_controller,
    servico_controller,
    usuario_controller
)

from app.controllers.auth_controller import router as auth_router


# =========================
# 🔧 AJUSTE DE BANCO
# =========================
def ajustar_banco():
    print("🔥 Ajustando banco...")

    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE usuarios 
            ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
        """))
        conn.commit()

    print("✅ Banco pronto!")


# =========================
# 🔥 STARTUP
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    ajustar_banco()
    yield


# =========================
# 🚀 APP LIMPO
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
app.include_router(empresa_controller.router)
app.include_router(servico_controller.router)
app.include_router(usuario_controller.router)
app.include_router(auth_router)


# =========================
# 🧪 TESTE
# =========================
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}