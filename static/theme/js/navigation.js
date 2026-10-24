/* The legacy stylesheet uses .in for its mobile menu. No Bootstrap JS is needed. */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.navbar-dropdown').forEach(function (navbar) {
    var menu = navbar.querySelector('.nav-dropdown');
    var toggles = navbar.querySelectorAll('.navbar-toggler');
    if (!menu) return;

    function setOpen(open) {
      var hidden = menu.classList.contains('nav-dropdown-sm') && !open;
      menu.inert = hidden;
      menu.setAttribute('aria-hidden', String(hidden));
      menu.classList.toggle('in', open);
      navbar.classList.toggle('opened', open);
      document.body.classList.toggle('navbar-dropdown-open', open);
      toggles.forEach(function (toggle) {
        toggle.setAttribute('aria-expanded', String(open));
        toggle.classList.toggle('collapsed', !open);
      });
    }

    function resize() {
      menu.classList.toggle('nav-dropdown-sm', window.innerWidth < 768);
      setOpen(false);
    }

    toggles.forEach(function (toggle) {
      toggle.setAttribute('aria-controls', menu.id);
      toggle.setAttribute('aria-label', 'Toggle navigation');
      toggle.addEventListener('click', function () {
        setOpen(!menu.classList.contains('in'));
      });
    });
    menu.addEventListener('click', function (event) {
      if (event.target.closest('a, button[type="submit"]')) setOpen(false);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.classList.contains('in')) {
        setOpen(false);
        toggles[0].focus();
      }
    });
    window.addEventListener('resize', resize);
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('navbar-short', window.scrollY > 0);
    }, {passive: true});
    resize();
  });
});
