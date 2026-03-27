from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os
from app.database import get_db
from app.services import empresa_service
from app.schemas import EmpresaCreate, EmpresaResponse, FotoResponse
from app.config import UPLOAD_DIR

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/", response_model=EmpresaResponse)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    return empresa_service.criar_empresa(db, empresa)

@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    return empresa_service.listar_empresas(db)

@router.post("/{empresa_id}/fotos", response_model=FotoResponse)
def upload_foto(empresa_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return empresa_service.adicionar_foto(db, empresa_id, file_path)

@router.get("/{empresa_id}/fotos", response_model=list[FotoResponse])
def listar_fotos(empresa_id: int, db: Session = Depends(get_db)):
    return empresa_service.listar_fotos(db, empresa_id)