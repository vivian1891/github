const DOWNLOAD_PAGE = "/kexue.html";

(function () {
  document.querySelectorAll('[data-download="true"]').forEach(function (item) {
    item.setAttribute("href", DOWNLOAD_PAGE);
    item.setAttribute("target", "_blank");
    item.setAttribute("rel", "nofollow sponsored noopener noreferrer");
  });
})();
