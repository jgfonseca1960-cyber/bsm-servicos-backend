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

            if (token) {
                token = token.replace(/"/g, "");
                req.headers["Authorization"] = "Bearer " + token;
            }

            return req;
        }
    });

    window.ui = ui;

    // 🔐 BOTÃO LOGIN
    setTimeout(() => {
        const topbar = document.querySelector(".topbar");

        if (!topbar) return;

        const btn = document.createElement("button");
        btn.innerText = "🔐 Login";
        btn.style.marginLeft = "10px";
        btn.style.padding = "6px 12px";
        btn.style.cursor = "pointer";

        btn.onclick = async () => {
            try {
                const email = prompt("Email:");
                const senha = prompt("Senha:");

                if (!email || !senha) {
                    alert("Preencha email e senha");
                    return;
                }

                const res = await fetch("/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, senha })
                });

                const data = await res.json();

                console.log("LOGIN RESPONSE:", data);

                if (!res.ok) {
                    alert("Erro no login: " + JSON.stringify(data));
                    return;
                }

                if (!data.access_token) {
                    alert("Token não veio na resposta!");
                    return;
                }

                // 🔥 SALVA TOKEN
                localStorage.setItem("access_token", data.access_token);

                alert("✅ Login realizado com sucesso!");
            } catch (err) {
                console.error(err);
                alert("Erro inesperado no login");
            }
        };

        topbar.appendChild(btn);
    }, 1000);
};