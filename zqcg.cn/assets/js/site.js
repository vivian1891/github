document.addEventListener("DOMContentLoaded", function () {
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function closeNav() {
    document.body.classList.remove("nav-open");
    if (navToggle) {
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "打开导航");
    }
  }

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var isOpen = document.body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      navToggle.setAttribute("aria-label", isOpen ? "关闭导航" : "打开导航");
    });
    nav.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeNav();
        navToggle.focus();
      }
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });
  }

  document.querySelectorAll(".faq-item").forEach(function (item) {
    var button = item.querySelector(".faq-question");
    var panel = item.querySelector(".faq-answer");
    if (!button || !panel) {
      return;
    }
    panel.hidden = true;
    button.addEventListener("click", function () {
      var expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      panel.hidden = expanded;
    });
  });
});
