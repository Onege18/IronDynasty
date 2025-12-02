document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.classes-track');
    if (!track) return;

    const prevBtn = document.querySelector('.classes-nav.prev');
    const nextBtn = document.querySelector('.classes-nav.next');

    const getScrollAmount = () => {
        // Прокручиваем примерно ширину видимой области
        return track.clientWidth * (window.innerWidth < 900 ? 0.9 : 0.8);
    };

    prevBtn.addEventListener('click', () => {
        track.scrollBy({
            left: -getScrollAmount(),
            behavior: 'smooth'
        });
    });

    nextBtn.addEventListener('click', () => {
        track.scrollBy({
            left: getScrollAmount(),
            behavior: 'smooth'
        });
    });
});
