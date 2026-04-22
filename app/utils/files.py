import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def gerar_url_imagem(caminho: str) -> str:
    if not caminho:
        return None

    caminho = caminho.replace("\\", "/")

    return f"{BASE_URL}/{caminho}"