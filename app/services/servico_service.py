from sqlalchemy.orm import Session
from app.models.servico_model import Servico
from app.schemas.servico_schema import ServicoCreate



def criar_servico(db: Session, data: ServicoCreate):
    novo_servico = Servico(
        nome=data.nome
    )

    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico


def listar_servicos(db: Session):
    return db.query(Servico).all()


def get_servico_por_id(db: Session, servico_id: int):
    return db.query(Servico).filter(Servico.id == servico_id).first()


def deletar_servico(db: Session, servico_id: int):
    servico = get_servico_por_id(db, servico_id)

    if not servico:
        return None

    db.delete(servico)
    db.commit()

    return servico