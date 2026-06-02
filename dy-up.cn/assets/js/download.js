const DOWNLOAD_PAGE = "/kexue.html";

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('[data-download="true"]').forEach((link) => {
    link.setAttribute("href", DOWNLOAD_PAGE);
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "nofollow sponsored noopener noreferrer");
  });
});
