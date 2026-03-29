from pydantic import BaseModel
from typing import Optional


# 🔹 Base
class ServicoBase(BaseModel):
    nome: str


# 🔹 Criação
class ServicoCreate(ServicoBase):
    pass


# 🔹 Atualização
class ServicoUpdate(BaseModel):
    nome: Optional[str] = None


# 🔹 Resposta
class ServicoResponse(ServicoBase):
    id: int

    class Config:
        from_attributes = True