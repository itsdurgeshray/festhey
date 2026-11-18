/* Fest detail: tab highlighting, event filters, save, share, read more, FAQ, mobile dock */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const toast = msg => { const t = $('.fd-toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 2200); };

  // in-page tabs follow the section in view
  const tabs = $$('.fd-tabs a');
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) tabs.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id));
  }), { rootMargin: '-30% 0px -60% 0px' });
  tabs.forEach(a => { const s = $(a.getAttribute('href')); s && io.observe(s); });

  // events: search, category, free only, sort
  const grid = $('.fd-events'), cards = $$('.evc', grid);
  const price = c => parseFloat(($('.evc-price b', c).textContent || '0').replace(/[^\d.]/g, '')) || 0;
  const q = $('.fd-bar input[type=search]'), cat = $('.fd-cat'), sort = $('.fd-sort'), free = $('.fd-free input');
  function apply() {
    const s = q.value.trim().toLowerCase(); let n = 0;
    cards.forEach(c => {
      const ok = (!s || $('.evc-name', c).textContent.toLowerCase().includes(s)) && (cat.value === 'all' || c.dataset.cat === cat.value) && (!free.checked || price(c) === 0);
      c.hidden = !ok; if (ok) n++;
    });
    const key = sort.value;
    [...cards].sort((a, b) => key === 'price' ? price(a) - price(b) : key === 'name' ? $('.evc-name', a).textContent.localeCompare($('.evc-name', b).textContent) : cards.indexOf(a) - cards.indexOf(b)).forEach(c => grid.appendChild(c));
    $('.fd-n').textContent = n; $('#events .lb-empty').hidden = n > 0;
  }
  [q, cat, sort, free].forEach(el => el.addEventListener(el === q ? 'input' : 'change', apply));

  // save + share
  const save = $('.fd-save');
  save.addEventListener('click', () => { const on = save.getAttribute('aria-pressed') !== 'true'; save.setAttribute('aria-pressed', on); $('span', save).textContent = on ? 'Saved' : 'Save'; toast(on ? 'Fest saved to your list' : 'Removed from saved'); });
  $('.fd-share').addEventListener('click', async () => {
    const data = { title: document.title, url: location.href };
    if (navigator.share) { try { await navigator.share(data); } catch (e) {} return; }
    try { await navigator.clipboard.writeText(location.href); toast('Link copied'); } catch (e) { toast(location.href); }
  });
  $$('.evc').forEach(c => c.addEventListener('click', e => { if (e.target.closest('.evc-save')) e.preventDefault(); }));

  // phone dock appears once the facts bar scrolls away
  const dock = $('.fd-dock');
  new IntersectionObserver(([en]) => dock.classList.toggle('show', !en.isIntersecting && en.boundingClientRect.top < 0)).observe($('.fd-facts'));
})();
