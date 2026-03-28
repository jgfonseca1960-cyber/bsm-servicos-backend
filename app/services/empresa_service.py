from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from sqlalchemy.orm import Session

from app.repositories import empresa_repo

def criar_empresa(db: Session, data):
    empresa = Empresa(nome=data.nome, telefone=data.telefone, cidade=data.cidade)
    return empresa_repo.create_empresa(db, empresa)

def listar_empresas(db: Session):
    return empresa_repo.get_empresas(db)

def adicionar_foto(db: Session, empresa_id: int, url: str):
    foto = EmpresaFoto(empresa_id=empresa_id, url=url)
    return empresa_repo.add_foto(db, foto)

def listar_fotos(db: Session, empresa_id: int):
    return empresa_repo.get_fotos(db, empresa_id)