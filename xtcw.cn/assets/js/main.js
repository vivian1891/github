document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll(".faq-item").forEach(function (item, index) {
    const button = item.querySelector(".faq-question");
    if (!button) return;
    if (index === 0) item.classList.add("is-open");
    button.addEventListener("click", function () {
      item.classList.toggle("is-open");
    });
  });
});