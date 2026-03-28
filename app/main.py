from fastapi import FastAPI
from app.database import engine
from sqlalchemy import text

app = FastAPI()

@app.on_event("startup")
def startup():
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
            """))
            conn.commit()
            print("✅ Coluna senha_hash verificada/criada!")
        except Exception as e:
            print("❌ Erro ao criar coluna:", e)




from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from app.database import init_db

# controllers
from app.controllers import (
    empresa_controller,
    servico_controller,
    usuario_controller
)

# 🔥 startup moderno (substitui on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

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

# rota teste
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}