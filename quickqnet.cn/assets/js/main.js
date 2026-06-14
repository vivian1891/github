document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.querySelector(".menu-toggle");
    var nav = document.querySelector(".site-nav");
    if (toggle && nav) {
        toggle.addEventListener("click", function () {
            var open = nav.classList.toggle("open");
            toggle.setAttribute("aria-expanded", open ? "true" : "false");
        });
    }

    var targets = document.querySelectorAll(".section, .news-card, .info-card, .factor-card, .scenario-card");
    if ("IntersectionObserver" in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        targets.forEach(function (item) {
            item.classList.add("reveal");
            observer.observe(item);
        });
    } else {
        targets.forEach(function (item) {
            item.classList.add("visible");
        });
    }
});