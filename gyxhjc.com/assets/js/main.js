(function () {
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  const currentPath = window.location.pathname === "/" ? "/" : window.location.pathname.replace(/\/$/, "");
  document.querySelectorAll("[data-nav] a").forEach((link) => {
    const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, "") || "/";
    if (linkPath === currentPath || (currentPath.startsWith("/news-") && linkPath === "/news.html")) {
      link.classList.add("is-active");
    }
  });
})();
