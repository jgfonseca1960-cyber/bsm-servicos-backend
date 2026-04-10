from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔥 URL fixa (temporário pra garantir que funciona)
DATABASE_URL = "postgresql+psycopg2://bsm_user:CFFwJtRUdOODyLDWy4mwY8ZDX4iJ77iS@dpg-d7b6jjkvjg8s73etqljg-a.oregon-postgres.render.com/bsm_servicos_4ccv?sslmode=require"


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# 🔥 FUNÇÃO QUE O MAIN PRECISA
def init_db():
    from app.models import (
        empresa_model,
        empresa_foto_model,
        usuario_model,
        servico_model,
    )
    Base.metadata.create_all(bind=engine)

    # =========================
# 🔥 DEPENDÊNCIA DO FASTAPI
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()