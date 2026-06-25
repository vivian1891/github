document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var current = window.location.pathname || "/";
  document.querySelectorAll(".main-nav a").forEach(function (link) {
    if (link.getAttribute("href") === current) {
      link.classList.add("is-active");
    }
  });
});