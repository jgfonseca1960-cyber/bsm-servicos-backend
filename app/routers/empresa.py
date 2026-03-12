from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

# from app.database import SessionLocal
from app.database import SessionLocal
from app.models.empresa_model import Empresa
from app.models.usuario_model import Usuario
from app.models.avaliacao_model import Avaliacao

from app.schemas.empresa_schema import EmpresaCreate, EmpresaResponse
from ..dependencies import get_current_user


router = APIRouter(prefix="/empresas", tags=["Empresas"])


# ✅ get_db precisa vir antes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ API PUBLICA
@router.get("/publico", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()


# ✅ CRIAR EMPRESA
@router.post("/")
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    dados = empresa.model_dump()

    nova_empresa = Empresa(
    **dados.dict(),
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


# ✅ POR CATEGORIA
router.get("/categoria/{categoria}", response_model=list[EmpresaResponse])
def empresas_por_categoria(categoria: str, db: Session = Depends(get_db)):

    return db.query(Empresa).filter(
        Empresa.categoria.ilike(f"%{categoria}%")
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