(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  document.querySelectorAll('.faq-question').forEach(function (button) {
    button.addEventListener('click', function () {
      var item = button.closest('.faq-item');
      var expanded = button.getAttribute('aria-expanded') === 'true';
      item.classList.toggle('is-open', !expanded);
      button.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    });
  });

  document.querySelectorAll('a[data-download="true"]').forEach(function (link) {
    link.addEventListener('click', function () {
      link.classList.add('is-loading');
    });
  });
})();