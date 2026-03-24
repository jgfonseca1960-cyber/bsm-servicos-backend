from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

import os

from app.database import Base, engine

# models
from app.models.usuario_model import Usuario
from app.models.empresa_model import Empresa
from app.models.avaliacao_model import Avaliacao
from app.models.categoria_model import Categoria
from app.models.foto_model import Foto


# routers
from app.routers import auth
from app.routers import usuario
from app.routers import empresa
from app.routers import avaliacao
from app.routers import categoria


app = FastAPI()

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CRIAR TABELAS
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# PASTA UPLOADS
# =========================

if not os.path.exists("uploads"):
    os.makedirs("uploads")


app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# =========================
# ROUTERS
# =========================

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(empresa.router)
app.include_router(avaliacao.router)
app.include_router(categoria.router)


# =========================
# DEBUG
# =========================

@app.get("/debug/database")
def debug_database():
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL")
    }


@app.get("/debug/usuarios")
def debug_usuarios():

    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT * FROM usuarios")
        )

        return [dict(row._mapping) for row in result]


@app.get("/debug/tabelas")
def tabelas():

    with engine.connect() as conn:

        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname='public'"
        ))

        return [r[0] for r in result]


# =========================
# DEBUG FOTO
# =========================

@app.get("/debug/criar_fotos")
def criar_fotos():

    try:

        Foto.__table__.create(bind=engine)

        return {"msg": "tabela fotos criada"}

    except Exception as e:

        return {"erro": str(e)}


@app.get("/debug/add_principal_foto")
def add_principal_foto():

    try:

        with engine.connect() as conn:

            conn.execute(text("""
                ALTER TABLE fotos
                ADD COLUMN principal BOOLEAN DEFAULT false
            """))

            conn.commit()

        return {"msg": "coluna principal criada"}

    except Exception as e:

        return {"erro": str(e)}
    

app.include_router(
    empresa.router,
    prefix="/empresa"
)