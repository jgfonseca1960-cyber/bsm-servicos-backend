from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models.empresa_model import Empresa
from app.models.usuario_model import Usuario
from app.models.avaliacao_model import Avaliacao

from app.schemas.empresa_schema import EmpresaCreate
from ..dependencies import get_current_user


# ✅ router precisa vir antes dos endpoints
router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.get("/publico")
def listar_empresas(db: Session = Depends(get_db)):

    empresas = db.query(Empresa).all()

    return empresas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CRIAR EMPRESA
@router.post("/")
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    dados = empresa.model_dump()

    nova_empresa = Empresa(
        **dados,
        usuario_id=usuario.id
    )

    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return nova_empresa


# ✅ RANKING
@router.get("/ranking")
def ranking(db: Session = Depends(get_db)):

    res = db.query(
        Empresa.nome,
        func.avg(Avaliacao.nota).label("media"),
        func.count(Avaliacao.id).label("total")
    ).join(
        Avaliacao,
        Avaliacao.empresa_id == Empresa.id,
        isouter=True
    ).group_by(Empresa.id).all()

    return res