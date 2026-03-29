from sqlalchemy.orm import Session

from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto

from app.repositories import empresa_repo


# 🔹 CRIAR EMPRESA
def criar_empresa(db: Session, data):
    empresa = Empresa(
        nome=data.nome,
        telefone=data.telefone,
        cidade=data.cidade
    )

    return empresa_repo.create_empresa(db, empresa)


# 🔹 LISTAR EMPRESAS
def listar_empresas(db: Session):
    return empresa_repo.get_empresas(db)


# 🔥 🔹 BUSCAR POR ID (ESTAVA FALTANDO)
def get_empresa_por_id(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()


# 🔥 🔹 ATUALIZAR EMPRESA
def atualizar_empresa(db: Session, empresa_id: int, data):
    empresa = get_empresa_por_id(db, empresa_id)

    if not empresa:
        return None

    # atualiza somente campos enviados
    for key, value in data.dict(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return empresa


# 🔥 🔹 DELETAR EMPRESA
def deletar_empresa(db: Session, empresa_id: int):
    empresa = get_empresa_por_id(db, empresa_id)

    if not empresa:
        return None

    db.delete(empresa)
    db.commit()

    return empresa


# 🔹 ADICIONAR FOTO
def adicionar_foto(db: Session, empresa_id: int, url: str):
    foto = EmpresaFoto(
        empresa_id=empresa_id,
        url=url