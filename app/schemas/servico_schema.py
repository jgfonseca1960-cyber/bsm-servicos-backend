from pydantic import BaseModel


class ServicoSimple(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True