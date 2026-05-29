from fastapi import HTTPException

def require_permission(permissoes: dict, key: str):

    if not permissoes.get(key, False):
        raise HTTPException(
            status_code=403,
            detail=f"Acesso negado: plano não permite '{key}'"
        )