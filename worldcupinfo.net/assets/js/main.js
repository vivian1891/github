(function () {
    var links = document.querySelectorAll('.download-pill, .hero .primary-btn');
    links.forEach(function (link) {
        link.addEventListener('click', function () {
            link.setAttribute('aria-busy', 'true');
        });
    });
})();

(function () {
    var ticker = document.querySelector('.betting-ticker');
    if (!ticker) return;

    var track = ticker.querySelector('.ticker-track');
    var firstSet = ticker.querySelector('.ticker-set');
    if (!track || !firstSet) return;

    function updateTicker() {
        var width = Math.ceil(firstSet.getBoundingClientRect().width);
        if (!width) return;

        track.style.setProperty('--ticker-distance', '-' + width + 'px');
        track.style.setProperty('--ticker-duration', Math.max(10, Math.round(width / 92)) + 's');
        track.style.animation = 'none';
        track.offsetHeight;
        track.style.animation = '';
    }

    updateTicker();
    window.addEventListener('load', updateTicker);

    var resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(updateTicker, 150);
    });
})();
