document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll(".site-nav a").forEach(function (link) {
    link.addEventListener("click", function () {
      document.body.classList.remove("nav-open");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    });
  });

  document.querySelectorAll("details").forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      const parent = item.parentElement;
      if (!parent || !parent.classList.contains("faq-list")) return;
      parent.querySelectorAll("details[open]").forEach(function (other) {
        if (other !== item) other.removeAttribute("open");
      });
    });
  });
});