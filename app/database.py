# backend/app/database.py

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session
from app.config import DATABASE_URL

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Ajuste do path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from app.config import DATABASE_URL

# Base dos modelos
Base = declarative_base()

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

def init_db():
    print("🔥 Criando todas as tabelas...")

    # 🔥 Importação LOCAL (evita circular import)
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    print("✅ Todas as tabelas foram criadas!")


# Execução direta
if __name__ == "__main__":
    init_db()