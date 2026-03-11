from sqlalchemy import Column, Integer, String
from app.database import Base

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    email = Column(String(150), unique=True)
    senha = Column(String(200))