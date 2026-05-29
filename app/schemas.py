from pydantic import BaseModel
from typing import Optional


# =====================================================
# 📸 FOTO
# =====================================================

class FotoResponse(BaseModel):

    id: int
    url: str
    principal: bool
    public_id: Optional[str] = None

    class Config:
        from_attributes = True


# =====================================================
# 🏢 EMPRESA BASE
# =====================================================

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

    cpf: Optional[str] = None
    cnpj: Optional[str] = None

    servico_id: Optional[int] = None

    # ⭐ PREMIUM

    destaque: Optional[bool] = False

    plano: Optional[str] = "gratuito"

    prioridade: Optional[int] = 0

    whatsapp_destacado: Optional[bool] = False

    exibir_no_topo: Optional[bool] = False

    selo_premium: Optional[bool] = False


# =====================================================
# ➕ CREATE
# =====================================================

class EmpresaCreate(EmpresaBase):
    pass


# =====================================================
# ✏️ UPDATE
# =====================================================

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

    cpf: Optional[str] = None
    cnpj: Optional[str] = None

    servico_id: Optional[int] = None

    # ⭐ PREMIUM

    destaque: Optional[bool] = None

    plano: Optional[str] = None

    prioridade: Optional[int] = None

    whatsapp_destacado: Optional[bool] = None

    exibir_no_topo: Optional[bool] = None

    selo_premium: Optional[bool] = None


# =====================================================
# 📦 RESPONSE
# =====================================================

class EmpresaResponse(EmpresaBase):

    id: int

    avaliacao_media: Optional[float] = 0.0

    foto_principal: Optional[str] = None

    fotos: list[FotoResponse] = []

    total_avaliacoes: Optional[int] = 0

    class Config:
        from_attributes = True


# =====================================================
# 🔧 SERVIÇO
# =====================================================

class ServicoBase(BaseModel):
    nome: str


class ServicoCreate(ServicoBase):
    pass


class ServicoResponse(ServicoBase):

    id: int

    class Config:
        from_attributes = True


# =====================================================
# 👤 USUÁRIO
# =====================================================

class UsuarioBase(BaseModel):

    nome: str
    email: str


class UsuarioCreate(UsuarioBase):

    senha: str

    tipo: str = "False"


class UsuarioResponse(UsuarioBase):

    id: int

    class Config:
        from_attributes = True