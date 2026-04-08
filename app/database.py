from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não está definida!")

# 🔥 GARANTE SSL AUTOMATICAMENTE (MESMO SE ESQUECER NA URL)
if "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # evita conexão morta
    pool_recycle=300,     # recicla conexão (Render precisa disso)
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # ✅ IMPORTAÇÃO LOCAL (EVITA IMPORT CIRCULAR)
    import app.models

    Base.metadata.create_all(bind=engine)