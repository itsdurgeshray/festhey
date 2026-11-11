/* Fest listing: search, category chips + checkboxes, location, date range, bookmarks */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const cards = $$('.lc'), chips = $$('.lb-chips .chip'), checks = $$('.ck input');
  const search = $('.lb-search input'), loc = $('.sel select'), count = $('.lb-n'), empty = $('.lb-empty');
  const NOW_MONTH = new Date().getMonth() + 1;
  let cats = new Set();

  function apply() {
    const q = search.value.trim().toLowerCase(), city = loc.value;
    const when = ($('.rd input:checked') || {}).value || 'all';
    let n = 0;
    cards.forEach(c => {
      const m = +c.dataset.month, ahead = (m - NOW_MONTH + 12) % 12;
      const ok = (!cats.size || c.dataset.cat.split(' ').some(k => cats.has(k)))
        && (!q || c.dataset.name.includes(q))
        && (city === 'all' || c.dataset.city === city)
        && (when === 'all' || (when === 'month' ? ahead === 0 : ahead < 3));
      c.hidden = !ok; if (ok) n++;
    });
    count.textContent = n; empty.hidden = n > 0;
  }
  function syncUI() {
    chips.forEach(ch => { const on = ch.dataset.cat === 'all' ? !cats.size : cats.has(ch.dataset.cat); ch.classList.toggle('is-on', on); ch.setAttribute('aria-pressed', on); });
    checks.forEach(i => { i.checked = cats.has(i.value); });
  }
  chips.forEach(ch => ch.addEventListener('click', () => {
    const k = ch.dataset.cat;
    if (k === 'all') cats.clear(); else cats.has(k) ? cats.delete(k) : cats.add(k);
    syncUI(); apply();
  }));
  checks.forEach(i => i.addEventListener('change', () => { i.checked ? cats.add(i.value) : cats.delete(i.value); syncUI(); apply(); }));
  search.addEventListener('input', apply);
  loc.addEventListener('change', apply);
  $$('.rd input').forEach(r => r.addEventListener('change', apply));
  $('.lb-apply').addEventListener('click', () => { apply(); $('.lb-main').scrollIntoView({ behavior: 'smooth', block: 'start' }); });
  $$('.lb-reset').forEach(b => b.addEventListener('click', () => {
    cats.clear(); search.value = ''; loc.value = 'all'; $('.rd input[value="all"]').checked = true; syncUI(); apply();
  }));
  $$('.lc-save').forEach(b => b.addEventListener('click', () => b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true')));
  apply();
})();
