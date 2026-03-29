from app.models.usuario_model import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str):
    return pwd_context.hash(senha)


def criar_usuario(db, data):
    # 🔍 verifica se já existe
    existente = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existente:
        raise Exception(...)

    # 🔐 cria usuário
    novo = Usuario(
        nome=data.nome,
        email=data.email,
        senha_hash=hash_senha(data.senha)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo