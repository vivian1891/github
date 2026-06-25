document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var path = window.location.pathname || "/";
  document.querySelectorAll(".site-nav a").forEach(function (link) {
    if (link.getAttribute("href") === path) {
      link.classList.add("is-active");
    }
    if (path === "/" && link.getAttribute("href") === "/") {
      link.classList.add("is-active");
    }
  });

  document.querySelectorAll(".faq-item button").forEach(function (button) {
    button.addEventListener("click", function () {
      var item = button.closest(".faq-item");
      if (item) item.classList.toggle("is-open");
    });
  });
});