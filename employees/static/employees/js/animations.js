// Card entrance animations
function animateCards() {
    anime({
        targets: '.card',
        scale: [0.9, 1],
        opacity: [0, 1],
        translateY: [20, 0],
        delay: anime.stagger(100),
        duration: 800,
        easing: 'easeOutElastic(1, .5)'
    });
}

// Table row entrance animations
function animateTableRows() {
    anime({
        targets: 'tbody tr',
        translateX: [-20, 0],
        opacity: [0, 1],
        delay: anime.stagger(50),
        duration: 600,
        easing: 'easeOutSine'
    });
}

// Button hover effect
function initButtonAnimations() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', (e) => {
            anime({
                targets: e.target,
                scale: 1.05,
                duration: 200,
                easing: 'easeOutQuad'
            });
        });
        
        btn.addEventListener('mouseleave', (e) => {
            anime({
                targets: e.target,
                scale: 1,
                duration: 200,
                easing: 'easeOutQuad'
            });
        });
    });
}

// Alert message animations
function animateAlerts() {
    anime({
        targets: '.alert',
        translateX: [-20, 0],
        opacity: [0, 1],
        duration: 800,
        easing: 'easeOutElastic(1, .5)'
    });
}

// Initialize all animations
document.addEventListener('DOMContentLoaded', () => {
    animateCards();
    animateTableRows();
    initButtonAnimations();
    animateAlerts();
});
