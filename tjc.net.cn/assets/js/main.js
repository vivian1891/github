(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.querySelector(".nav-toggle");
    const nav = document.querySelector(".site-nav");

    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        const open = nav.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", String(open));
      });

      nav.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
          nav.classList.remove("is-open");
          toggle.setAttribute("aria-expanded", "false");
        });
      });
    }

    document.querySelectorAll(".faq-question").forEach(function (button) {
      button.addEventListener("click", function () {
        const item = button.closest(".faq-item");
        const answer = item ? item.querySelector(".faq-answer") : null;
        if (!item || !answer) return;
        const open = item.classList.toggle("is-open");
        button.setAttribute("aria-expanded", String(open));
        answer.hidden = !open;
      });
    });

    const header = document.querySelector(".site-header");
    const onScroll = function () {
      if (header) header.classList.toggle("is-scrolled", window.scrollY > 18);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 });
      document.querySelectorAll(".reveal").forEach(function (el) {
        observer.observe(el);
      });
    } else {
      document.querySelectorAll(".reveal").forEach(function (el) {
        el.classList.add("is-visible");
      });
    }
  });
})();
