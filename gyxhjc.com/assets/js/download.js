const DOWNLOAD_PAGE = "/kexue.html";

(function () {
  document.querySelectorAll('[data-download="true"]').forEach((button) => {
    button.setAttribute("href", DOWNLOAD_PAGE);
    button.setAttribute("target", "_blank");
    button.setAttribute("rel", "nofollow sponsored noopener noreferrer");
  });
})();
