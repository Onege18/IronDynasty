// Переключение между Login / Register с анимацией
console.log("auth.js loaded");

document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.querySelector(".forms-wrapper");
    if (!wrapper) return;

    const goRegisterButtons = document.querySelectorAll(".go-register");
    const goLoginButtons = document.querySelectorAll(".go-login");

    goRegisterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            wrapper.classList.add("show-register");
        });
    });

    goLoginButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            wrapper.classList.remove("show-register");
        });
    });
});

document.querySelectorAll(".toggle-password").forEach(icon => {
    icon.addEventListener("click", function () {
        const targetId = this.getAttribute("data-target") || "passwordField";
        const input = document.getElementById(targetId);

        if (input.type === "password") {
            input.type = "text";
            this.classList.remove("bx-hide");
            this.classList.add("bx-show");
        } else {
            input.type = "password";
            this.classList.remove("bx-show");
            this.classList.add("bx-hide");
        }
    });
});

