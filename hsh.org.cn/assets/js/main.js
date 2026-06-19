document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var opened = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", opened ? "true" : "false");
    });
  }

  var path = window.location.pathname;
  document.querySelectorAll(".nav a").forEach(function (link) {
    var href = link.getAttribute("href");
    if ((path === "/" && href === "/") || (href !== "/" && path.endsWith(href))) {
      link.classList.add("active");
    }
  });
});
