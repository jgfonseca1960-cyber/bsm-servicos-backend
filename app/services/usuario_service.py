from app.models.usuario_model import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str):
    return pwd_context.hash(senha)


# 🔹 CRIAR
def criar_usuario(db, data):
    existente = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existente:
        raise ValueError("Email já cadastrado")

    novo = Usuario(
        nome=data.nome,
        email=data.email,
        senha_hash=hash_senha(data.senha)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# 🔹 LISTAR
def listar_usuarios(db):
    return db.query(Usuario).all()


# 🔹 BUSCAR POR ID
def get_usuario_por_id(db, usuario_id):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


# 🔹 ATUALIZAR
def atualizar_usuario(db, usuario_id, data):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        return None

    if data.nome:
        usuario.nome = data.nome

    if data.email:
        usuario.email = data.email

    if data.senha:
        usuario.senha_hash = hash_senha(data.senha)

    db.commit()
    db.refresh(usuario)

    return usuario


# 🔹 DELETAR
def deletar_usuario(db, usuario_id):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        return None

    db.delete(usuario)
    db.commit()

    return usuario