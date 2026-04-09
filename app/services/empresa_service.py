from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.empresa_model import Empresa
from app.models.servico_model import Servico

from app.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate


# =========================
# 🔹 CRIAR EMPRESA
# =========================
def criar_empresa(db: Session, data: EmpresaCreate):
    # 🔥 valida se o serviço existe
    servico = db.query(Servico).filter(Servico.id == data.servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    empresa = Empresa(
        nome=data.nome,
        descricao=data.descricao,
        telefone=data.telefone,
        endereco=data.endereco,
        cidade=data.cidade,
        estado=data.estado,
        cep=data.cep,
        latitude=data.latitude,
        longitude=data.longitude,
        ativo=data.ativo,
        servico_id=data.servico_id
    )

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return empresa


# =========================
# 🔹 LISTAR TODAS
# =========================
def listar_empresas(db: Session):
    empresas = db.query(Empresa).all()
    return empresas


# =========================
# 🔹 BUSCAR POR ID
# =========================
def buscar_empresa(db: Session, empresa_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return empresa


# =========================
# 🔹 ATUALIZAR
# =========================
def atualizar_empresa(db: Session, empresa_id: int, data: EmpresaUpdate):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    # 🔥 se vier servico_id, valida
    if data.servico_id is not None:
        servico = db.query(Servico).filter(Servico.id == data.servico_id).first()
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

    # 🔥 atualiza só os campos enviados
    for key, value in data.dict(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return empresa


# =========================
# 🔹 DELETAR
# =========================
def deletar_empresa(db: Session, empresa_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()

    return {"message": "Empresa deletada com sucesso"}