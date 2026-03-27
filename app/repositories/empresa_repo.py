from sqlalchemy.orm import Session
from app.models import Empresa, EmpresaFoto

def create_empresa(db: Session, empresa: Empresa):
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa

def get_empresas(db: Session):
    return db.query(Empresa).all()

def get_empresa(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def add_foto(db: Session, foto: EmpresaFoto):
    db.add(foto)
    db.commit()
    db.refresh(foto)
    return foto

def get_fotos(db: Session, empresa_id: int):
    return db.query(EmpresaFoto).filter(EmpresaFoto.empresa_id == empresa_id).all()