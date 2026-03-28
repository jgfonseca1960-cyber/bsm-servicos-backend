from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

import app.models.usuario_model
import app.models.empresa_model
import app.models.empresa_foto_model

# Base dos modelos
Base = declarative_base()

# Engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

# Sessão
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

# Dependência do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicialização do banco

def init_db():
    print("🔥 Recriando banco...")

    import app.models

    Base.metadata.create_all(bind=engine)

    print("✅ Banco recriado!")