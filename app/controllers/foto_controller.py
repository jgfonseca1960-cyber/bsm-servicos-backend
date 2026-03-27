from fastapi import APIRouter

router = APIRouter(prefix="/fotos", tags=["Fotos"])

@router.get("/")
def listar_fotos():
    return {"msg": "listar fotos"}