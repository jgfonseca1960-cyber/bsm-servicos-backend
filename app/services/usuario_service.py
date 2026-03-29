from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.repositories import usuario_repo
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# CRIAR USUÁRIO
# =========================
def criar_usuario(db: Session, data):
    # 🔍 verifica se já existe usuário com mesmo email
    existente = usuario_repo.get_usuario_por_email(db, data.email)

    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # 🔐 gera hash da senha
    senha_hash = pwd_context.hash(data.senha)

    usuario = Usuario(
        nome=data.nome,
        email=data.email,
        senha_hash=senha_hash,
        tipo=data.tipo
    )

    return usuario_repo.create_usuario(db, usuario)


# =========================
# LISTAR USUÁRIOS
# =========================
def listar_usuarios(db: Session):
    return usuario_repo.get_usuarios(db)


# =========================
# BUSCAR POR ID
# =========================
def get_usuario_por_id(db: Session, usuario_id: int):
    return usuario_repo.get_usuario(db, usuario_id)


# =========================
# ATUALIZAR USUÁRIO
# =========================
def atualizar_usuario(db: Session, usuario_id: int, data):
    usuario = usuario_repo.get_usuario(db, usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 🔍 verifica se outro usuário já usa esse email
    existente = usuario_repo.get_usuario_por_email(db, data.email)

    if existente and existente.id != usuario_id:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    usuario.nome = data.nome
    usuario.email = data.email
    usuario.tipo = data.tipo

    # 🔐 atualiza senha apenas se enviada
    if hasattr(data, "senha") and data.senha:
        usuario.senha_hash = pwd_context.hash(data.senha)

    return usuario_repo.update_usuario(db, usuario)


# =========================
# DELETAR USUÁRIO
# =========================
def deletar_usuario(db: Session, usuario_id: int):
    usuario = usuario_repo.get_usuario(db, usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario_repo.delete_usuario(db, usuario_id)