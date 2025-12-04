// Загружаем звук
const uiSound = new Audio("/static/audio/ui-select.wav");
uiSound.preload = "auto";
uiSound.volume = 0.35; // чуть тише, мягче

function attachSoundToInteractiveElements() {
    const elements = document.querySelectorAll(
        "button, .btn-primary, .btn-outline, a, .class-card, .menu-link"
    );

    elements.forEach(el => {

        // Hover (наведение курсора)
        el.addEventListener("mouseenter", () => {
            uiSound.currentTime = 0;
            uiSound.play().catch(() => {});
        });

        // Click
        el.addEventListener("click", () => {
            uiSound.currentTime = 0;
            uiSound.play().catch(() => {});
        });
    });
}

document.addEventListener("DOMContentLoaded", attachSoundToInteractiveElements);
