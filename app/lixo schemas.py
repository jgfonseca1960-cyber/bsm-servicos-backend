from pydantic import BaseModel

# Empresa
class EmpresaBase(BaseModel):
    nome: str
    telefone: str | None = None
    cidade: str | None = None

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int
    class Config:
        orm_mode = True

# Serviço
class ServicoBase(BaseModel):
    nome: str
    descricao: str | None = None
    empresa_id: int

class ServicoCreate(ServicoBase):
    pass

class ServicoResponse(ServicoBase):
    id: int
    class Config:
        orm_mode = True

# Usuário
class UsuarioBase(BaseModel):
    nome: str
    email: str
    tipo: str = "usuario"

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

# Foto
class EmpresaFotoResponse(BaseModel):
    id: int
    empresa_id: int
    caminho: str
    class Config:
        orm_mode = True