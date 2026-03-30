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
        senha_hash=hash_senha(data.senha),
        is_admin=data.is_admin if data.is_admin is not None else False
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


# 🔹 ATUALIZAR (CORRIGIDO)
def atualizar_usuario(db, usuario_id, data):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        return None

    # 🔥 VALIDA EMAIL DUPLICADO
    if data.email:
        existente = db.query(Usuario).filter(Usuario.email == data.email).first()
        if existente and existente.id != usuario_id:
            raise ValueError("Email já cadastrado")

    # 🔥 ATUALIZA SOMENTE SE NÃO FOR NONE
    if data.nome is not None:
        usuario.nome = data.nome

    if data.email is not None:
        usuario.email = data.email

    if data.senha is not None:
        usuario.senha_hash = hash_senha(data.senha)

    if data.is_admin is not None:
        usuario.is_admin = data.is_admin

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