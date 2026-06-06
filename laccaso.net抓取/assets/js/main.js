(() => {
  const header = document.querySelector("[data-header]");
  const nav = document.querySelector("[data-nav]");
  const toggle = document.querySelector("[data-menu-toggle]");

  const backTop = document.createElement("a");
  backTop.className = "back-top";
  backTop.href = "#main";
  backTop.setAttribute("aria-label", "返回顶部");
  backTop.textContent = "↑";
  document.body.appendChild(backTop);

  const updateChrome = () => {
    const scrolled = window.scrollY > 16;
    header?.classList.toggle("is-scrolled", scrolled);
    backTop.classList.toggle("is-visible", window.scrollY > 520);
  };

  updateChrome();
  window.addEventListener("scroll", updateChrome, { passive: true });

  toggle?.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    nav?.classList.toggle("is-open", !expanded);
  });

  nav?.addEventListener("click", (event) => {
    if (!event.target.closest("a")) return;
    nav.classList.remove("is-open");
    toggle?.setAttribute("aria-expanded", "false");
  });

  const revealItems = document.querySelectorAll(".feature-card, .news-card, .screen-card, .mini-panel, .content-card, .contact-card");
  revealItems.forEach((item) => item.classList.add("reveal"));

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries, currentObserver) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          currentObserver.unobserve(entry.target);
        });
      },
      { threshold: 0.14 },
    );
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }
})();
