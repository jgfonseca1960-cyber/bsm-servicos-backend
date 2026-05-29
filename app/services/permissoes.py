def get_permissoes(plano: str) -> dict:
    plano = (plano or "gratuito").lower()

    if plano == "master":
        return {
            "galeria": True,
            "destaque": True,
            "whatsapp_destacado": True,
            "exibir_no_topo": True,
            "analytics": True,
            "editar_avaliacoes": True
        }

    if plano == "premium":
        return {
            "galeria": True,
            "destaque": True,
            "whatsapp_destacado": True,
            "exibir_no_topo": False,
            "analytics": False,
            "editar_avaliacoes": False
        }

    return {
        "galeria": False,
        "destaque": False,
        "whatsapp_destacado": False,
        "exibir_no_topo": False,
        "analytics": False,
        "editar_avaliacoes": False
    }