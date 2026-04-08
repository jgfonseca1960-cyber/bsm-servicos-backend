from sqlalchemy.orm import Session
from app import models, schemas

# ================= EMPRESA =================
def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


def get_empresas(db: Session):
    return db.query(models.Empresa).all()


def get_empresa(db: Session, empresa_id: int):
    return db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()


def delete_empresa(db: Session, empresa_id: int):
    empresa = get_empresa(db, empresa_id)
    if empresa:
        db.delete(empresa)
        db.commit()
    return empresa


# ================= SERVICO =================
def create_servico(db: Session, servico: schemas.ServicoCreate):
    obj = models.Servico(**servico.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_servico(db: Session):
    return db.query(models.Servico).all()


# ================= USUARIO =================
def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    obj = models.Usuario(**usuario.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_usuarios(db: Session):
    return db.query(models.Usuario).all()


# ================= FOTO =================
def create_foto(db: Session, foto: schemas.EmpresaFotoCreate):
    obj = models.EmpresaFoto(**foto.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj