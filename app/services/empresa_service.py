from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.empresa_model import Empresa
from app.models.servico_model import Servico

from app.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate


# =========================
# 🔹 SERIALIZADOR (🔥 NOVO)
# =========================
def serialize_empresa(e: Empresa):
    return {
        "id": e.id,
        "nome": e.nome,
        "descricao": e.descricao,
        "telefone": e.telefone,

        "endereco": e.endereco,
        "bairro": e.bairro,
        "cidade": e.cidade,
        "estado": e.estado,
        "cep": e.cep,

        "latitude": e.latitude,
        "longitude": e.longitude,

        "ativo": e.ativo,
        "avaliacao_media": e.avaliacao_media,

        "cpf": e.cpf,
        "cnpj": e.cnpj,

        "servico_id": e.servico_id,

        # 🔥 FOTO PRINCIPAL (property do model)
        "foto_principal": e.foto_principal,

        # 🔥 FOTOS RELACIONADAS
        "fotos": [
            {
                "id": f.id,
                "url": f.url,
                "principal": f.principal
            }
            for f in e.fotos
        ],

        "distancia_km": None
    }


# =========================
# 🔹 CRIAR EMPRESA
# =========================
def criar_empresa(db: Session, data: EmpresaCreate):
    servico = db.query(Servico).filter(Servico.id == data.servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    empresa = Empresa(
        nome=data.nome,
        descricao=data.descricao,
        telefone=data.telefone,
        endereco=data.endereco,
        bairro=data.bairro,
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

    return serialize_empresa(empresa)


# =========================
# 🔹 LISTAR TODAS (🔥 CORRIGIDO)
# =========================
def listar_empresas(db: Session):
    empresas = db.query(Empresa).all()
    return [serialize_empresa(e) for e in empresas]


# =========================
# 🔹 BUSCAR POR ID (🔥 CORRIGIDO)
# =========================
def buscar_empresa(db: Session, empresa_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return serialize_empresa(empresa)


# =========================
# 🔹 ATUALIZAR (🔥 CORRIGIDO)
# =========================
def atualizar_empresa(db: Session, empresa_id: int, data: EmpresaUpdate):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    if data.servico_id is not None:
        servico = db.query(Servico).filter(Servico.id == data.servico_id).first()
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return serialize_empresa(empresa)


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