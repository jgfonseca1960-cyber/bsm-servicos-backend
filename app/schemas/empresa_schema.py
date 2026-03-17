from pydantic import BaseModel


class EmpresaCreate(BaseModel):

    nome: str
    cidade: str


class EmpresaOut(BaseModel):

    id: int
    nome: str
    cidade: str

    class Config:
        from_attributes = True