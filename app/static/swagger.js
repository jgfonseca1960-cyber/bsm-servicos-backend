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
            const token = localStorage.getItem("access_token");

            if (token && token !== "undefined" && token !== "null") {
                req.headers["Authorization"] = "Bearer " + token;
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

        btn.onclick = async () => {
            const email = prompt("Email:");
            const senha = prompt("Senha:");

            if (!email || !senha) return;

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

                // 🔥 salva token LIMPO
                localStorage.setItem("access_token", data.access_token);

                alert("✅ Logado com sucesso!");
                location.reload();

            } catch (err) {
                alert("Erro de conexão");
            }
        };

        topbar.appendChild(btn);
    }, 1500);
};