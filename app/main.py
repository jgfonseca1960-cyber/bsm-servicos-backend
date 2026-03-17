from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine

from app.routers import auth, empresa, usuario


app = FastAPI()


@app.on_event("startup")
def start_db():

    Base.metadata.create_all(bind=engine)

    try:
        with engine.connect() as conn:

            conn.execute(
                text(
                    "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS tipo VARCHAR DEFAULT 'normal'"
                )
            )

            conn.commit()

    except Exception as e:
        print(e)


app.include_router(auth.router, prefix="/auth")
app.include_router(usuario.router, prefix="/usuarios")
app.include_router(empresa.router, prefix="/empresas")