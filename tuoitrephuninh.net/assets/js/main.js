(function () {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      const opened = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", opened ? "true" : "false");
    });
  }

  const current = window.location.pathname;
  document.querySelectorAll(".main-nav a").forEach(function (link) {
    const href = link.getAttribute("href");
    if (href === current) {
      link.classList.add("is-active");
    }
  });

  const observer = "IntersectionObserver" in window
    ? new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 })
    : null;

  document.querySelectorAll(".section, .page-hero, .hero-section").forEach(function (el) {
    el.classList.add("reveal-ready");
    if (observer) {
      observer.observe(el);
    } else {
      el.classList.add("is-visible");
    }
  });
})();
