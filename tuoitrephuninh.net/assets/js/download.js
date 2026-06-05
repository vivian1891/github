(function () {
  const DOWNLOAD_PAGE = "/kexue.html";
  document.querySelectorAll('[data-download="true"]').forEach(function (link) {
    link.setAttribute("href", DOWNLOAD_PAGE);
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "nofollow sponsored noopener noreferrer");
  });
})();
