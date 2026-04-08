from sqlalchemy.orm import Session
from app.models.servico_model import Servico
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from app.models.usuario_model import Usuario
from app.repositories import servico_repo

def criar_servico(db: Session, data):
    servico = Servico(
        empresa_id=data.empresa_id,
        nome=data.nome,
        descricao=data.descricao
    )
    return servico_repo.create_servico(db, servico)

def listar_servico(db: Session):
    return servico_repo.get_servico(db)

def listar_servico_por_empresa(db: Session, empresa_id: int):
    return servico_repo.get_servico_por_empresa(db, empresa_id)

def atualizar_servico(db: Session, servico_id: int, data):
    servico = servico_repo.get_servico(db, servico_id)
    if not servico:
        return None
    servico.nome = data.nome
    servico.descricao = data.descricao
    return servico_repo.update_servico(db, servico)

def deletar_servico(db: Session, servico_id: int):
    return servico_repo.delete_servico(db, servico_id)