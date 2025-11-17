(function () {
  var storageKey = 'theme';
  var mql = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');

  function apply(theme) {
    var html = document.documentElement;
    if (theme === 'dark') {
      html.classList.add('dark');
      html.setAttribute('data-bs-theme', 'dark');
    } else {
      html.classList.remove('dark');
      html.setAttribute('data-bs-theme', 'light');
    }
    var isDark = theme === 'dark';
    var sunEl = document.querySelector('#theme-toggle .theme-sun');
    var moonEl = document.querySelector('#theme-toggle .theme-moon');
    if (sunEl && moonEl) {
      sunEl.classList.toggle('d-none', isDark);
      moonEl.classList.toggle('d-none', !isDark);
    }
  }

  function getCurrent() {
    try {
      var saved = localStorage.getItem(storageKey);
      if (saved) return saved;
    } catch (e) { }
    if (mql && mql.matches) return 'dark';
    return 'light';
  }

  document.addEventListener('DOMContentLoaded', function () {
    apply(getCurrent());
    var btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.addEventListener('click', function () {
        var next = getCurrent() === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem(storageKey, next); } catch (e) { }
        apply(next);
      });
    }
  });

  if (mql && mql.addEventListener) {
    mql.addEventListener('change', function () {
      try {
        if (!localStorage.getItem(storageKey)) {
          apply(getCurrent());
        }
      } catch (e) {
        apply(getCurrent());
      }
    });
  }
})();


