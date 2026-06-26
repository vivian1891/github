document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var path = window.location.pathname || "/";
  document.querySelectorAll(".site-nav a").forEach(function (link) {
    if (link.getAttribute("href") === path || (path === "/" && link.getAttribute("href") === "/")) {
      link.classList.add("active");
    }
  });
});