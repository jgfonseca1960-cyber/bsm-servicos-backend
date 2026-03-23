from fastapi import FastAPI
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


# cria tabelas
Base.metadata.create_all(bind=engine)


# cria pasta uploads se não existir
if not os.path.exists("uploads"):
    os.makedirs("uploads")


# rota de arquivos
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# routers
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

        result = conn.execute(text("SELECT * FROM usuarios"))

        return [dict(row._mapping) for row in result]


@app.get("/debug/tabelas")
def tabelas():

    with engine.connect() as conn:

        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname='public'"
        ))

        return [r[0] for r in result]
    
    from app.models.foto_model import Foto
from sqlalchemy import text

# Criar Tabela Fotos 

@app.get("/debug/criar_fotos")
def criar_fotos():

    try:

        Foto.__table__.create(bind=engine)

        return {"msg": "tabela fotos criada"}

    except Exception as e:

        return {"erro": str(e)}
    

    ### PROVISORIAMENTE RETIRADO Recriação da tabela Empresa

# from sqlalchemy import text
# from app.models.empresa_model import Empresa


# @app.get("/debug/recriar_empresas")
# def recriar_empresas():

#     try:

#         with engine.connect() as conn:

#             conn.execute(text("DROP TABLE IF EXISTS empresas CASCADE"))
#             conn.commit()

#         Empresa.__table__.create(bind=engine)

#         return {"msg": "tabela empresas recriada"}

#     except Exception as e:

#         return {"erro": str(e)}