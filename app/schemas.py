from pydantic import BaseModel
from typing import Optional

# ================= EMPRESA =================
class EmpresaBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    servico_id: Optional[int] = None


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaResponse(EmpresaBase):
    id: int

    class Config:
        from_attributes = True


# ================= SERVICO =================
class ServicoBase(BaseModel):
    nome: str


class ServicoCreate(ServicoBase):
    pass


class ServicoResponse(ServicoBase):
    id: int

    class Config:
        from_attributes = True


# ================= USUARIO =================
class UsuarioBase(BaseModel):
    nome: str
    email: str


class UsuarioCreate(UsuarioBase):
    senha: str
    tipo: str  = "False' # 👈 ADICIONE ISSO

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


# ================= FOTO =================
class EmpresaFotoBase(BaseModel):
    url: str
    empresa_id: int


class EmpresaFotoCreate(EmpresaFotoBase):
    pass


class EmpresaFotoResponse(EmpresaFotoBase):
    id: int

    class Config:
        from_attributes = True

        
        
from pydantic import BaseModel

class FotoResponse(BaseModel):
    id: int
    caminho: str
    principal: bool

    class Config:
        from_attributes = True