from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

# from app.database import SessionLocal
from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.usuario_model import Usuario
from app.models.avaliacao_model import Avaliacao

from app.schemas.empresa_schema import EmpresaCreate, EmpresaResponse
from ..dependencies import get_current_user


router = APIRouter(prefix="/empresas", tags=["Empresas"])


# ✅ API PUBLICA
@router.get("/publico", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()


# ✅ CRIAR EMPRESA
from app.schemas.empresa_schema import EmpresaCreate

@router.post("/")
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):

    nova_empresa = Empresa(
        **dados.model_dump(),
        usuario_id=usuario.id
    )

    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return nova_empresa


# ✅ POR CIDADE
@router.get("/cidade/{cidade}", response_model=list[EmpresaResponse])
def empresas_por_cidade(cidade: str, db: Session = Depends(get_db)):

    return db.query(Empresa).filter(
        Empresa.cidade.ilike(f"%{cidade}%")
    ).all()


# ✅ POR CTIPO DE SERVIÇO

@router.get("/tipo-servico/{tipo}", response_model=list[EmpresaResponse])
def empresas_por_tipo_servico(
    tipo: str,
    db: Session = Depends(get_db)
):

    return db.query(Empresa).filter(
        Empresa.tipo_servico.ilike(f"%{tipo}%")
    ).all()


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

    return [
        {
            "nome": r[0],
            "media": float(r[1] or 0),
            "total": r[2]
        }
        for r in res
    ]