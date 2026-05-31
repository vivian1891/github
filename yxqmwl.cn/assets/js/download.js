const DOWNLOAD_PAGE = "/kexue.html";
document.addEventListener("click", function(event) {
  const target = event.target.closest("[data-download]");
  if (!target) return;
  event.preventDefault();
  window.location.href = DOWNLOAD_PAGE;
});