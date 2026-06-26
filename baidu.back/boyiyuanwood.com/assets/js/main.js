document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      nav.classList.toggle("open");
    });
  }

  document.querySelectorAll(".site-nav a").forEach(function (link) {
    link.addEventListener("click", function () {
      if (nav && nav.classList.contains("open")) {
        nav.classList.remove("open");
        if (toggle) {
          toggle.setAttribute("aria-expanded", "false");
        }
      }
    });
  });
});