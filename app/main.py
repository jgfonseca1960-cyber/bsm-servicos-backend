from fastapi import FastAPI
from sqlalchemy import text

# from app.database import engine, Base
from app.core.database import engine, Base

from app.models import empresa_model, usuario_model, avaliacao_model

from app.routers import auth, empresa, avaliacao

app = FastAPI()

Base.metadata.create_all(bind=engine)

with engine.connect() as conn:

    # empresas
    conn.execute(text(
        "ALTER TABLE empresas ADD COLUMN IF NOT EXISTS categoria VARCHAR;"
    ))

    conn.execute(text(
        "ALTER TABLE empresas ADD COLUMN IF NOT EXISTS estado VARCHAR;"
    ))

    conn.execute(text(
        "ALTER TABLE empresas ADD COLUMN IF NOT EXISTS bairro VARCHAR;"
    ))

    conn.execute(text(
        "ALTER TABLE empresas ADD COLUMN IF NOT EXISTS descricao TEXT;"
    ))

    # usuarios

    conn.execute(text(
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS nome VARCHAR;"
    ))

    conn.execute(text(
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS tipo VARCHAR;"
    ))

    conn.execute(text(
        "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS empresa_id INTEGER;"
    ))

    conn.commit()

app.include_router(auth.router)
app.include_router(empresa.router)
app.include_router(avaliacao.router)