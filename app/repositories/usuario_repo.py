from sqlalchemy.orm import Session
from app.models import Usuario


# =========================
# CRIAR USUÁRIO
# =========================
def create_usuario(db: Session, usuario: Usuario):
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# =========================
# LISTAR TODOS
# =========================
def get_usuarios(db: Session):
    return db.query(Usuario).all()


# =========================
# BUSCAR POR ID
# =========================
def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


# =========================
# 🔥 BUSCAR POR EMAIL (ESSENCIAL)
# =========================
def get_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


# =========================
# ATUALIZAR
# =========================
def update_usuario(db: Session, usuario: Usuario):
    db.commit()
    db.refresh(usuario)
    return usuario


# =========================
# DELETAR
# =========================
def delete_usuario(db: Session, usuario_id: int):
    usuario = get_usuario(db, usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario