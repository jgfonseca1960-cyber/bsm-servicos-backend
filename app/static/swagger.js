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
                // 🔥 REMOVE ASPAS AUTOMATICAMENTE
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

        const btn = document.createElement("button");
        btn.innerText = "🔐 Login";
        btn.style.marginLeft = "10px";
        btn.style.padding = "5px 10px";
        btn.style.cursor = "pointer";

        btn.onclick = async () => {
            const email = prompt("Email:");
            const senha = prompt("Senha:");

            if (!email || !senha) return;

            const res = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, senha })
            });

            if (!res.ok) {
                alert("Erro no login");
                return;
            }

            const data = await res.json();

            // 🔥 GARANTE QUE SALVA LIMPO
            localStorage.setItem("access_token", data.access_token);

            alert("✅ Login realizado!");
        };

        topbar.appendChild(btn);
    }, 1000);
};