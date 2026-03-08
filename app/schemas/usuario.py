from pydantic import BaseModel

class Login(BaseModel):
    email: str
    senha: str