const DOWNLOAD_PAGE = "/kexue.html";

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".btn-download").forEach(function (button) {
    button.setAttribute("href", DOWNLOAD_PAGE);
    button.setAttribute("rel", "nofollow noopener noreferrer");
    button.setAttribute("target", "_blank");
    button.setAttribute("referrerpolicy", "no-referrer");
  });

  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
  }

  const contactForm = document.querySelector(".contact-form");
  if (contactForm) {
    contactForm.addEventListener("submit", function (event) {
      event.preventDefault();
      alert("信息已记录，请通过邮箱 support@example.com 获取进一步支持。");
    });
  }
});
