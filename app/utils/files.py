import os

BASE_URL = os.getenv("BASE_URL", "http://192.168.0.17:8000")

def gerar_url_imagem(caminho: str) -> str:
    if not caminho:
        return None

    caminho = caminho.replace("\\", "/")

    return f"{BASE_URL}/{caminho}"