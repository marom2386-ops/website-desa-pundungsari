/* Progressive enhancement: every page and service remains readable without JavaScript. */
(function (scope) {
  'use strict';
  function normalize(value) {
    return String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('id-ID').replace(/\s+/g, ' ').trim();
  }
  function matches(text, query) {
    const haystack = normalize(text);
    return normalize(query).split(' ').filter(Boolean).every(term => haystack.includes(term));
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { normalize, matches };
  if (!scope.document) return;
  const document = scope.document;
  document.querySelectorAll('[data-filter]').forEach(input => {
    const container = document.getElementById(input.getAttribute('data-filter'));
    if (!container) return;
    const ui = input.closest('[data-search-ui]');
    if (ui) ui.hidden = false;
    const items = Array.from(container.querySelectorAll('[data-search-text]'));
    const counter = document.getElementById(input.getAttribute('aria-describedby'));
    const empty = document.getElementById(input.getAttribute('data-empty'));
    const filter = () => {
      let count = 0;
      items.forEach(item => {
        const show = matches(item.getAttribute('data-search-text'), input.value);
        item.hidden = !show;
        if (show) count += 1;
      });
      if (counter) counter.textContent = count + ' dari ' + items.length + ' informasi ditampilkan';
      if (empty) empty.hidden = count !== 0;
    };
    input.addEventListener('input', filter);
    filter();
  });
  function openAnchor() {
    const id = scope.location.hash.slice(1);
    if (!id) return;
    let decoded;
    try { decoded = decodeURIComponent(id); } catch (_) { return; }
    const target = document.getElementById(decoded);
    if (target && target.tagName === 'DETAILS') target.open = true;
  }
  openAnchor();
  scope.addEventListener('hashchange', openAnchor);
})(typeof window !== 'undefined' ? window : globalThis);
