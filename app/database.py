from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.core.config import settings

import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# DATABASE_URL = "postgresql+psycopg://postgres:brg7573x@localhost/bsm_servicos"

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()