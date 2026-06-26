document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll("details").forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      var parent = item.parentElement;
      if (!parent || !parent.classList.contains("compact")) return;
      parent.querySelectorAll("details").forEach(function (other) {
        if (other !== item) other.open = false;
      });
    });
  });
});