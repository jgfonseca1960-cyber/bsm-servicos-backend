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

# 🔥 IMPORT DO AUTH (ESSENCIAL)
from app.controllers.auth_controller import router as auth_router


# 🔧 AJUSTE DE BANCO
def ajustar_banco():
    print("🔥 Ajustando banco...")

    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE usuarios 
            ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
        """))
        conn.commit()

    print("✅ Banco pronto!")


# 🔥 STARTUP MODERNO
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    ajustar_banco()
    yield


# 🚀 APP
app = FastAPI(lifespan=lifespan)


# 🔧 evita erro favicon
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


# =========================
# ROTAS
# =========================

app.include_router(
    empresa_controller.router,
    prefix="/empresas",
    tags=["Empresas"]
)

app.include_router(
    servico_controller.router,
    prefix="/servicos",
    tags=["Serviços"]
)

app.include_router(
    usuario_controller.router,
    prefix="/usuarios",
    tags=["Usuários"]
)

# 🔥 ROTA DE LOGIN (AGORA VAI FUNCIONAR)
app.include_router(auth_router)


# rota teste
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}