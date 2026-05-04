from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# =========================
# 🔹 FOTO RESPONSE
# =========================
class FotoResponse(BaseModel):
    id: int
    url: str
    principal: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# 🔹 BASE (COMPARTILHADO)
# =========================
class EmpresaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None

    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    ativo: Optional[bool] = True
    avaliacao_media: Optional[float] = None

    cpf: Optional[str] = None
    cnpj: Optional[str] = None


# =========================
# 🔹 CREATE
# =========================
class EmpresaCreate(EmpresaBase):
    servico_id: int


# =========================
# 🔹 UPDATE
# =========================
class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None

    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    ativo: Optional[bool] = None
    avaliacao_media: Optional[float] = None

    cpf: Optional[str] = None
    cnpj: Optional[str] = None

    servico_id: Optional[int] = None


# =========================
# 🔹 RESPONSE
# =========================
class EmpresaResponse(EmpresaBase):
    id: int
    servico_id: Optional[int] = None

    foto_principal: Optional[str] = None
    fotos: List[FotoResponse] = []  # OK pois FastAPI controla

    distancia_km: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)