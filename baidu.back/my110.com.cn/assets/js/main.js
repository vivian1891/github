document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.querySelector(".menu-toggle-my110-govcn");
  const nav = document.querySelector(".main-nav-my110-govcn");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      const isOpen = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  document.querySelectorAll(".faq-item-my110-govcn").forEach(function (item, index) {
    const question = item.querySelector(".faq-question");
    if (!question) return;
    if (index === 0) item.classList.add("open");
    question.addEventListener("click", function () {
      item.classList.toggle("open");
    });
  });
});
