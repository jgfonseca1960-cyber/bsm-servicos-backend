from pydantic import BaseModel


class ServicoBase(BaseModel):
    nome: str


class ServicoCreate(ServicoBase):
    pass


class ServicoResponse(ServicoBase):
    id: int

    class Config:
        from_attributes = True