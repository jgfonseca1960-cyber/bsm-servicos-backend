from sqlalchemy.orm import Session
from app.models import Usuario

def create_usuario(db: Session, usuario: Usuario):
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def get_usuarios(db: Session):
    return db.query(Usuario).all()

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def update_usuario(db: Session, usuario: Usuario):
    db.commit()
    db.refresh(usuario)
    return usuario

def delete_usuario(db: Session, usuario_id: int):
    usuario = get_usuario(db, usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario