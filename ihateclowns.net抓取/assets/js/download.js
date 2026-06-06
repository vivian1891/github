const DOWNLOAD_PAGE = "/kexue.html";

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-download='true']").forEach(function (button) {
    button.setAttribute("href", DOWNLOAD_PAGE);
    button.setAttribute("target", "_blank");
    button.setAttribute("rel", "nofollow sponsored noopener noreferrer");
  });
});
