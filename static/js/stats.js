document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll(".number");
    let started = false;

    function animateCounters() {
        if (started) return;
        started = true;

        counters.forEach(counter => {
            const target = +counter.getAttribute("data-target");
            let count = 0;
            const speed = target / 100;

            const update = () => {
                count += speed;
                if (count < target) {
                    counter.innerText = Math.ceil(count);
                    requestAnimationFrame(update);
                } else {
                    counter.innerText = target;
                }
            };

            update();
        });
    }

    const observer = new IntersectionObserver(
        (entries) => {
            if (entries[0].isIntersecting) {
                animateCounters();
            }
        },
        { threshold: 0.4 }
    );

    observer.observe(document.querySelector(".stats-section"));
});
