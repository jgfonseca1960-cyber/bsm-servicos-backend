from pydantic import BaseModel

class FornecedorCreate(BaseModel):
    nome: str
    telefone: str
    cidade: str

class FornecedorResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    cidade: str

    class Config:
        from_attributes = True