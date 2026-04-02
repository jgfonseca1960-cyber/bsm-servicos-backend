window.onload = function () {

    const ui = SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",

        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset
        ],

        layout: "StandaloneLayout",

        requestInterceptor: (req) => {
            let token = localStorage.getItem("access_token");

            // 🔥 REMOVE ASPAS AUTOMATICAMENTE
            if (token) {
                token = token.replace(/"/g, "").trim();

                // 🔥 GARANTE QUE É TOKEN VÁLIDO
                if (token && token.split(".").length === 3) {
                    req.headers["Authorization"] = "Bearer " + token;
                }
            }

            return req;
        }
    });

    window.ui = ui;

    // 🔥 BOTÃO LOGIN
    setTimeout(() => {
        const topbar = document.querySelector(".topbar");

        if (!topbar) return;

        const btn = document.createElement("button");
        btn.innerText = "🔐 Login";
        btn.style.marginLeft = "10px";
        btn.style.padding = "5px 10px";
        btn.style.cursor = "pointer";
        btn.style.background = "#4CAF50";
        btn.style.color = "white";
        btn.style.border = "none";
        btn.style.borderRadius = "4px";

        btn.onclick = async () => {
            const email = prompt("Email:");
            const senha = prompt("Senha:");

            if (!email || !senha) {
                alert("Preencha email e senha");
                return;
            }

            try {
                const res = await fetch("/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, senha })
                });

                if (!res.ok) {
                    alert("❌ Erro no login");
                    return;
                }

                const data = await res.json();

                // 🔥 VALIDA TOKEN
                if (!data.access_token) {
                    alert("❌ Token não recebido");
                    return;
                }

                // 🔥 LIMPA E SALVA CORRETO
                const tokenLimpo =