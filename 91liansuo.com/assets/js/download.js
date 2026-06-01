const DOWNLOAD_PAGE = "/kexue.html";

document.addEventListener("click", function (event) {
  const link = event.target.closest("[data-download='true']");
  if (!link) return;
  link.setAttribute("href", DOWNLOAD_PAGE);
  link.setAttribute("target", "_blank");
  link.setAttribute("rel", "nofollow sponsored noopener noreferrer");
});

document.querySelectorAll("[data-download='true']").forEach(function (link) {
  link.setAttribute("href", DOWNLOAD_PAGE);
  link.setAttribute("target", "_blank");
  link.setAttribute("rel", "nofollow sponsored noopener noreferrer");
});
