from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import EmpresaCreate
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
)


@router.post("/")
def criar(
    dados: EmpresaCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not current_user:
        raise HTTPException(status_code=401, detail="Usuario não autenticado")

    nova = Empresa(
        nome=dados.nome,
        cnpj=dados.cnpj,
        cpf=dados.cpf,
        responsavel=dados.responsavel,
        endereco=dados.endereco,
        bairro=dados.bairro,
        cidade=dados.cidade,
        estado=dados.estado,
        tipo_servico=dados.tipo_servico,
        latitude=dados.latitude,
        longitude=dados.longitude,
        avaliacao=dados.avaliacao,
        usuario_id=current_user.id
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova