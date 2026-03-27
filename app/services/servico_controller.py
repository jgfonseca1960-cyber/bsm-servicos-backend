from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ServicoCreate, ServicoResponse
from app.services import servico_service

router = APIRouter(prefix="/servicos", tags=["Serviços"])

@router.post("/", response_model=ServicoResponse)
def criar_servico(servico: ServicoCreate, db: Session = Depends(get_db)):
    return servico_service.criar_servico(db, servico)

@router.get("/", response_model=list[ServicoResponse])
def listar_servicos(db: Session = Depends(get_db)):
    return servico_service.listar_servicos(db)

@router.get("/empresa/{empresa_id}", response_model=list[ServicoResponse])
def listar_servicos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    return servico_service.listar_servicos_por_empresa(db, empresa_id)

@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar_servico(servico_id: int, servico: ServicoCreate, db: Session = Depends(get_db)):
    updated = servico_service.atualizar_servico(db, servico_id, servico)
    if not updated:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return updated

@router.delete("/{servico_id}", response_model=ServicoResponse)
def deletar_servico(servico_id: int, db: Session = Depends(get_db)):
    deleted = servico_service.deletar_servico(db, servico_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return deleted