document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var path = window.location.pathname || "/";
  if (path === "") path = "/";
  document.querySelectorAll(".site-nav a[href]").forEach(function (link) {
    var href = link.getAttribute("href");
    if (href === path || (path === "/" && href === "/")) {
      link.classList.add("active");
    }
  });
});