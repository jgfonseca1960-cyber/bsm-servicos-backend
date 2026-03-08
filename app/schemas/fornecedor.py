from pydantic import BaseModel

class FornecedorCreate(BaseModel):
    nome: str
    responsavel: str
    telefone: str
    descricao: str
    cidade: str
    bairro: str