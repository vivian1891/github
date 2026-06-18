document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      document.body.classList.toggle("is-locked", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        document.body.classList.remove("is-locked");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var currentPath = window.location.pathname || "/";
  document.querySelectorAll(".site-nav a").forEach(function (link) {
    var linkPath = new URL(link.getAttribute("href"), window.location.origin).pathname;
    if (linkPath === currentPath) {
      link.classList.add("is-active");
    }
  });
});
