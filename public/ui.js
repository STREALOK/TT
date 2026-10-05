/* TT site: reader controls (5 Oct 2026, his ask: light/dark, a font choice, text shadow). Each choice is the
   reader's own, kept in this browser only (localStorage), like the text-size knob. No network, no tracking. */
(function () {
  var root = document.documentElement;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function apply() {
    var theme = get('tt-theme'); if (theme === 'light' || theme === 'dark') root.setAttribute('data-theme', theme); else root.removeAttribute('data-theme');
    var font = get('tt-font') || 'serif'; root.setAttribute('data-font', font);
    var shadow = get('tt-shadow') === 'on'; root.setAttribute('data-shadow', shadow ? 'on' : 'off');
    document.querySelectorAll('[data-theme-toggle]').forEach(function (b) {
      var dark = theme ? theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
      b.textContent = dark ? '☀' : '☾'; b.setAttribute('aria-pressed', dark ? 'true' : 'false');
    });
    document.querySelectorAll('select[data-font]').forEach(function (s) { s.value = font; });
    document.querySelectorAll('[data-shadow-toggle]').forEach(function (b) { b.setAttribute('aria-pressed', shadow ? 'true' : 'false'); });
  }
  document.querySelectorAll('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var cur = get('tt-theme'); var dark = cur ? cur === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
      set('tt-theme', dark ? 'light' : 'dark'); apply();
    });
  });
  document.querySelectorAll('select[data-font]').forEach(function (s) {
    s.addEventListener('change', function () { set('tt-font', s.value); apply(); });
  });
  document.querySelectorAll('[data-shadow-toggle]').forEach(function (b) {
    b.addEventListener('click', function () { set('tt-shadow', get('tt-shadow') === 'on' ? 'off' : 'on'); apply(); });
  });
  apply();
})();
