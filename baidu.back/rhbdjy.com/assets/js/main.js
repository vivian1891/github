document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  var currentPath = window.location.pathname || "/";
  var parentPath = {
    "/vpp-channel.html": "/overview.html",
    "/route.html": "/setup.html",
    "/device.html": "/overview.html",
    "/status.html": "/setup.html",
    "/security.html": "/overview.html",
    "/download.html": "/setup.html",
    "/contact.html": "/about.html",
    "/privacy.html": "/about.html",
    "/news-1.html": "/news.html",
    "/news-2.html": "/news.html",
    "/news-3.html": "/news.html",
    "/news-4.html": "/news.html",
    "/news-5.html": "/news.html",
    "/news-6.html": "/news.html"
  };
  var activePath = parentPath[currentPath] || currentPath;
  document.querySelectorAll(".site-nav a").forEach(function (link) {
    if (link.getAttribute("href") === activePath) {
      link.setAttribute("aria-current", "page");
    }
  });
});
