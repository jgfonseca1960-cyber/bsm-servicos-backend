from fastapi import FastAPI

from app.database import engine, Base
from app.models import empresa_model, usuario_model, avaliacao_model

from app.routers import auth, empresa, avaliacao

app = FastAPI()

Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    conn.execute(
        "ALTER TABLE empresas ADD COLUMN categoria VARCHAR;"
    )
    conn.commit()
    
app.include_router(auth.router)
app.include_router(empresa.router)
app.include_router(avaliacao.router)