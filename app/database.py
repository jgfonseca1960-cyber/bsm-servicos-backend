from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 VALIDAÇÃO (EVITA ESSE ERRO PRA SEMPRE)
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não está definida!")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)