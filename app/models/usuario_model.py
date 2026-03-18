from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios2"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    is_admin = Column(Boolean, default=False)