print("🔥🔥🔥 MAIN CARREGADO 🔥🔥🔥")

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

# 🔥 IMPORTANTE: garantir carregamento dos models
from app.models import empresa_model
from app.models import empresa_foto_model

@app.get("/empresa/listar")
def debug_rota_errada():
    print("🔥 ALGUÉ
Você atingiu o limite do Free par


# =========================
# 🔧 AJUSTE DE BANCO
# =========================
def ajustar_banco():
    try:
        print("🔥 Ajustando banco...")

        with engine.begin() as conn:  # 🔥 melhor que connect()
            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
            """))

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

        init_db()  # cria tabelas
        ajustar_banco()  # ajustes extras

        print("✅ Inicialização concluída!")

    except Exception:
        print("❌ ERRO NA INICIALIZAÇÃO:")
        traceback.print_exc()

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

# 🔥 ADICIONE AQUI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(servico_router, prefix="/servicos", tags=["Serviços"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])


# =========================
# 🧪 TESTE
# =========================
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}