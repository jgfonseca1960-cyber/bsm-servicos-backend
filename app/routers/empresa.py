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