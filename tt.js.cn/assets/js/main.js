document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");

  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll("details").forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      var parent = item.parentElement;
      if (!parent || !parent.classList.contains("faq-list")) return;
      parent.querySelectorAll("details[open]").forEach(function (other) {
        if (other !== item && !parent.classList.contains("compact")) {
          other.removeAttribute("open");
        }
      });
    });
  });
});