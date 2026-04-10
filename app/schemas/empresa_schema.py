from pydantic import BaseModel
from typing import Optional
from app.schemas.servico_schema import ServicoSimple


# 🔹 BASE
class EmpresaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = True


# 🔹 CRIAÇÃO
class EmpresaCreate(EmpresaBase):
    servico_id: int  # 🔥 obrigatório na criação


# 🔹 ATUALIZAÇÃO
class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = None
    servico_id: Optional[int] = None


# 🔹 RESPOSTA
class EmpresaResponse(BaseModel):
    id: int
    nome: str
    servico_id: Optional[int] = None  # 🔥 CORREÇÃO AQUI

    class Config:
        from_attributes = True