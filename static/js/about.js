document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll(".number");
    let started = false;

    function animateCounters() {
        counters.forEach(counter => {
            let target = +counter.dataset.target;
            let duration = 2000;
            let step = target / (duration / 30);
            let value = 0;

            let update = setInterval(() => {
                value += step;
                if (value >= target) {
                    value = target;
                    clearInterval(update);
                }
                counter.textContent = Math.floor(value);
            }, 30);
        });
    }

    // запускаем анимацию один раз, когда секция появилась на экране
    const statsSection = document.querySelector(".stats-section");
    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !started) {
            started = true;
            animateCounters();
        }
    });

    if (statsSection) {
        observer.observe(statsSection);
    }
});
