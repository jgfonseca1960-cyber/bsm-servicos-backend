from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.usuario_model import Usuario

from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaResponse
)

from app.dependencies import get_current_user


router = APIRouter()


# =========================
# LISTAR PUBLICO
# =========================

@router.get("/publico", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):

    return db.query(Empresa).all()


# =========================
# BUSCAR POR CIDADE
# =========================

@router.get("/cidade/{cidade}", response_model=list[EmpresaResponse])
def buscar_por_cidade(
    cidade: str,
    db: Session = Depends(get_db)
):

    return db.query(Empresa).filter(
        Empresa.cidade.ilike(f"%{cidade}%")
    ).all()


# =========================
# BUSCAR POR TIPO SERVICO
# =========================

@router.get("/tipo-servico/{tipo}", response_model=list[EmpresaResponse])
def buscar_por_tipo(
    tipo: str,
    db: Session = Depends(get_db)
):

    return db.query(Empresa).filter(
        Empresa.tipo_servico.ilike(f"%{tipo}%")
    ).all()


# =========================
# RANKING
# =========================

@router.get("/ranking", response_model=list[EmpresaResponse])
def ranking(db: Session = Depends(get_db)):

    return db.query(Empresa).order_by(
        Empresa.id.desc()
    ).all()


# =========================
# CRIAR EMPRESA (ADMIN)
# =========================

@router.post("/", response_model=EmpresaResponse)
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    if usuario.tipo != "admin":
        raise HTTPException(
            status_code=403,
            detail="Somente admin pode criar empresa"
        )

    nova = Empresa(
        nome=dados.nome,
        cidade=dados.cidade,
        tipo_servico=dados.tipo_servico,
        categoria=dados.categoria,
        telefone=dados.telefone,
        endereco=dados.endereco,
        descricao=dados.descricao,
        latitude=dados.latitude,
        longitude=dados.longitude,
        usuario_id=usuario.id
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova