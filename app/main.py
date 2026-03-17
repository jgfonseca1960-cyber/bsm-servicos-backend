from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app.routers import auth, empresa, usuario


app = FastAPI()


@app.on_event("startup")
def start_db():

    Base.metadata.create_all(bind=engine)

    # adiciona coluna tipo se não existir
    try:
        with engine.connect() as conn:
            conn.execute(
                text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS tipo VARCHAR DEFAULT 'normal'")
            )
            conn.commit()
            print("COLUNA TIPO OK")

    except Exception as e:
        print("ERRO AO ALTERAR TABELA", e)


app.include_router(auth.router, prefix="/auth")
app.include_router(empresa.router, prefix="/empresas")
app.include_router(usuario.router)