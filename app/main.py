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

# 🔥 AUTH
from app.controllers.auth_controller import router as auth_router

# 🔥 SWAGGER JWT
from fastapi.openapi.utils import get_openapi


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
# 🚀 APP
# =========================
app = FastAPI(
    title="BSM Serviços API",
    version="1.0.0",
    description="API com autenticação JWT",
    lifespan=lifespan
)


# =========================
# 🔐 CONFIG SWAGGER JWT
# =========================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="BSM Serviços API",
        version="1.0.0",
        description="API com autenticação JWT",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# =========================
# 🔧 FAVICON
# =========================
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


# =========================
# 📌 ROTAS
# =========================

# ⚠️ IMPORTANTE: NÃO DUPLICAR PREFIXO
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