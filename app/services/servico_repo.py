from sqlalchemy.orm import Session
from app.models.servico_model import Servico
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from app.models.usuario_model import Usuario

def create_servico(db: Session, servico: Servico):
    db.add(servico)
    db.commit()
    db.refresh(servico)
    return servico

def get_servicos(db: Session):
    return db.query(Servico).all()

def get_servicos_por_empresa(db: Session, empresa_id: int):
    return db.query(Servico).filter(Servico.empresa_id == empresa_id).all()

def get_servico(db: Session, servico_id: int):
    return db.query(Servico).filter(Servico.id == servico_id).first()

def update_servico(db: Session, servico: Servico):
    db.commit()
    db.refresh(servico)
    return servico

def delete_servico(db: Session, servico_id: int):
    servico = get_servico(db, servico_id)
    if servico:
        db.delete(servico)
        db.commit()
    return servico