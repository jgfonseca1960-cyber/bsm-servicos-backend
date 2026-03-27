from sqlalchemy.orm import Session
from app.models import Usuario
from app.repositories import usuario_repo
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_usuario(db: Session, data):
    existente = usuario_repo.get_usuario_por_email(db, data.email)
    if existente:
        raise ValueError("Email já cadastrado")

    senha_hash = pwd_context.hash(data.senha)

    usuario = Usuario(
        nome=data.nome,
        email=data.email,
        senha_hash=senha_hash,
        tipo=getattr(data, "tipo", "cliente")
    )

    return usuario_repo.create_usuario(db, usuario)


def listar_usuarios(db: Session):
    return usuario_repo.get_usuarios(db)


def get_usuario_por_id(db: Session, usuario_id: int):
    return usuario_repo.get_usuario(db, usuario_id)


def atualizar_usuario(db: Session, usuario_id: int, data):
    usuario = usuario_repo.get_usuario(db, usuario_id)
    if not usuario:
        return None

    usuario.nome = data.nome
    usuario.email = data.email
    usuario.tipo = getattr(data, "tipo", usuario.tipo)

    if hasattr(data, "senha") and data.senha:
        usuario.senha_hash = pwd_context.hash(data.senha)

    return usuario_repo.update_usuario(db, usuario)


def deletar_usuario(db: Session, usuario_id: int):
    return usuario_repo.delete_usuario(db, usuario_id)