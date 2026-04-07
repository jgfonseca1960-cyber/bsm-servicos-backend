from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from app.database import engine, init_db

# controllers
from app.controllers import (
    empresa_controller,
    servico_controller,
    usuario_controller
)

from app.controllers.auth_controller import router as auth_router


# =========================
# 🔧 AJUSTE DE BANCO
# =========================
def ajustar_banco():
    print("🔥 Ajustando banco...")

    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE usuarios 
            ADD COLUMN IF NOT EXISTS senha_hash VARCHAR;
        """))
        conn.commit()

    print("✅ Banco pronto!")


# =========================
# 🔥 STARTUP
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    ajustar_banco()
    yield


# =========================
# 🚀 APP (COM TOKEN AUTOMÁTICO)
# =========================
app = FastAPI(
    title="BSM Serviços API",
    version="1.0.0",
    description="API com autenticação automática",
    lifespan=lifespan,
    swagger_ui_parameters={
        "requestInterceptor": """
        (req) => {
            const token = localStorage.getItem("access_token");

            if (token && token !== "null") {
                req.headers["Authorization"] = "Bearer " + token;
            }

            return req;
        }
        """
    }
)


# =========================
# 🔧 REMOVE BOTÃO AUTHORIZE (SEM QUEBRAR)
# =========================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="BSM Serviços API",
        version="1.0.0",
        description="API com autenticação automática",
        routes=app.routes,
    )

    # remove segurança global (tira botão Authorize)
    openapi_schema.pop("security", None)

    if "components" in openapi_schema:
        openapi_schema["components"].pop("securitySchemes", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# =========================
# 📁 ARQUIVOS ESTÁTICOS (opcional)
# =========================
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# =========================
# 🔐 TELA DE LOGIN SIMPLES
# =========================
@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <html>
        <body style="font-family: Arial; padding: 40px;">
            <h2>🔐 Login BSM Serviços</h2>

            <input id="email" placeholder="Email"><br><br>
            <input id="senha" type="password" placeholder="Senha"><br><br>

            <button onclick="login()">Entrar</button>

            <script>
                async function login() {
                    const email = document.getElementById("email").value;
                    const senha = document.getElementById("senha").value;

                    const res = await fetch("/auth/login", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ email, senha })
                    });

                    const data = await res.json();

                    if (!data.access_token) {
                        alert("Erro no login");
                        return;
                    }

                    localStorage.setItem("access_token", data.access_token);

                    alert("✅ Login realizado!");

                    window.location.href = "/docs";
                }
            </script>
        </body>
    </html>
    """


# =========================
# 🔧 FAVICON
# =========================
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


# =========================
# 📌 ROTAS
# =========================
app.include_router(empresa_controller.router)
app.include_router(servico_controller.router)
app.include_router(usuario_controller.router)
app.include_router(auth_router)


# =========================
# 🧪 TESTE
# =========================
@app.get("/")
def root():
    return {"msg": "API BSM Serviços rodando 🚀"}