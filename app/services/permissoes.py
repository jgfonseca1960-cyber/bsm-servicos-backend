def get_permissoes(plano: str):
    if plano == "master":
        return {
            "galeria": True,
            "destaque": True,
            "analytics": True,
            "editar": True
        }

    if plano == "premium":
        return {
            "galeria": True,
            "destaque": True,
            "analytics": False,
            "editar": True
        }

    return {  # gratuito
        "galeria": False,
        "destaque": False,
        "analytics": False,
        "editar": False
    }