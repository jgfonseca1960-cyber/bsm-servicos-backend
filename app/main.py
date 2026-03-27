from fastapi import FastAPI
from fastapi.responses import Response

from app.database import init_db

# controllers
from app.controllers import (
    empresa_controller,
    servico_controller,
    usuario_controller
)

app = FastAPI(
    title="BSM Serviços API",
    version="1.0.0"
)


# 🔥 CRIA AS TABELAS NO STARTUP (FORMA CORRETA)
@app.on_event("startup")
def on_startup():
    init_db()


# 🔧 evita erro favicon no navegador
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


# rota teste
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}