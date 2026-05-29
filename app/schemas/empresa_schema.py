from pydantic import BaseModel, Field
from typing import Optional, List

# =========================================================
# 📸 FOTO RESPONSE
# =========================================================

class FotoResponse(BaseModel):

    id: int
    url: str
    principal: bool
    public_id: Optional[str] = None

    class Config:
        from_attributes = True


# =========================================================
# ⭐ AVALIAÇÃO RESPONSE
# =========================================================

class AvaliacaoResponse(BaseModel):

    id: int
    usuario: str
    nota: int
    comentario: Optional[str] = None

    class Config:
        from_attributes = True


# =========================================================
# 🏢 EMPRESA BASE
# =========================================================

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

    # ==========================================
    # 🏆 PLANOS E DESTAQUES
    # ==========================================

    destaque: Optional[bool] = False

    plano: Optional[str] = "gratuito"

    prioridade: Optional[int] = 0

    whatsapp_destacado: Optional[bool] = False

    exibir_no_topo: Optional[bool] = False

    selo_premium: Optional[bool] = False

# =========================================================
# ➕ CREATE
# =========================================================

class EmpresaCreate(EmpresaBase):
    pass


# =========================================================
# ✏️ UPDATE
# =========================================================

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

    # =====================================================
    # ⭐ PREMIUM
    # =====================================================

    destaque: Optional[bool] = None

    plano: Optional[str] = None

    prioridade: Optional[int] = None

    whatsapp_destacado: Optional[bool] = None
    exibir_no_topo: Optional[bool] = None
    selo_premium: Optional[bool] = None


# =========================================================
# 📦 RESPONSE
# =========================================================

class EmpresaResponse(EmpresaBase):

    id: int

    foto_principal: Optional[str] = None

    fotos: List[FotoResponse] = Field(default_factory=list)

    avaliacao_media: Optional[float] = 0

    total_avaliacoes: Optional[int] = 0

    avaliacoes: List[AvaliacaoResponse] = Field(default_factory=list)
 
    class Config:
        from_attributes = True