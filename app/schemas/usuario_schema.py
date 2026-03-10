from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True