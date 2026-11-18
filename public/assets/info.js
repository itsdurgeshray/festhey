/* FestHey info pages: colleges filter, follow, help search + accordion, legal TOC */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const toast = msg => { const t = $('.fd-toast'); if (!t) return; t.textContent = msg; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 2200); };

  // colleges filter
  const cards = $$('.cl-page .cc');
  if (cards.length) {
    const q = $('.cl .lb-search input'), city = $('.cl-city'), live = $('.cl-live'); let type = 'all';
    const apply = () => {
      const s = q.value.trim().toLowerCase(); let n = 0;
      cards.forEach(c => { const ok = (!s || c.dataset.name.includes(s)) && (city.value === 'all' || c.dataset.city === city.value) && (type === 'all' || c.dataset.type === type) && (!live.checked || c.dataset.up === '1'); c.hidden = !ok; if (ok) n++; });
      $('.cl-n').textContent = n; $('.cl .lb-empty').hidden = n > 0;
    };
    $$('.cl-chips .chip').forEach(b => b.addEventListener('click', () => { $$('.cl-chips .chip').forEach(x => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b); }); type = b.dataset.type; apply(); }));
    q.addEventListener('input', apply); city.addEventListener('change', apply); live.addEventListener('change', apply);
    $('.cl-reset').addEventListener('click', () => { q.value = ''; city.value = 'all'; live.checked = false; $$('.cl-chips .chip')[0].click(); });
  }
  // follow / save college
  $$('.cc-save').forEach(b => b.addEventListener('click', () => { const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', on); toast(on ? 'Following. We’ll alert you when fests open.' : 'Unfollowed'); }));
  const fols = $$('.fol, .cg-follow');
  fols.forEach(b => b.addEventListener('click', () => {
    const on = b.getAttribute('aria-pressed') !== 'true';
    fols.forEach(x => { x.setAttribute('aria-pressed', on); const t = x.firstChild; if (x.classList.contains('cg-follow')) t.textContent = on ? 'Following' : 'Follow for alerts'; else $('span', x).textContent = on ? 'Following' : 'Follow'; });
    toast(on ? 'Following RVCE. You’ll get fest alerts.' : 'Unfollowed RVCE');
  }));

  // help center: topic rail + search across every answer
  const hqs = $$('.hq');
  if (hqs.length) {
    hqs.forEach(h => { h._q = $('.hq-q span', h).textContent; h._a = $('.hq-a p', h).innerHTML; });
    const open = (h, on) => { h.classList.toggle('is-on', on); $('.hq-q', h).setAttribute('aria-expanded', on); };
    $$('.hq-q').forEach(b => b.addEventListener('click', () => { const h = b.closest('.hq'); open(h, !h.classList.contains('is-on')); }));
    const q = $('.hp-search input'), sx = $('.hx-sx'), clear = $('.hp-clear'), title = $('[data-hx-title]'), cnt = $('[data-hx-n]');
    const ts = $$('.hx-t'); let cat = 'all';
    const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const apply = () => {
      const s = q.value.trim().toLowerCase(); let n = 0;
      hqs.forEach(h => {
        const txt = (h._q + ' ' + h._a.replace(/<[^>]+>/g, '')).toLowerCase();
        const ok = (cat === 'all' || h.dataset.cat === cat) && (!s || txt.includes(s));
        h.hidden = !ok; if (ok) n++;
        $('.hq-q span', h).innerHTML = s && ok ? h._q.replace(new RegExp('(' + esc(s) + ')', 'ig'), '<mark>$1</mark>') : h._q;
        if (s) open(h, ok);
      });
      $$('.hgroup').forEach(g => g.hidden = !$$('.hq', g).some(h => !h.hidden));
      const t = ts.find(x => x.dataset.cat === cat);
      title.textContent = s ? 'RESULTS FOR “' + q.value.trim().toUpperCase() + '”' : (cat === 'all' ? 'ALL ANSWERS' : $('span:nth-child(2)', t).textContent.toUpperCase());
      cnt.textContent = n; $('.hp-empty').hidden = n > 0; clear.hidden = cat === 'all' && !s; sx.hidden = !s;
    };
    const toList = () => { const l = $('#answers'); l && l.scrollIntoView({ behavior: 'smooth', block: 'start' }); };
    q.addEventListener('input', apply);
    q.addEventListener('keydown', ev => { if (ev.key === 'Enter') { ev.preventDefault(); toList(); } });
    sx.addEventListener('click', () => { q.value = ''; apply(); q.focus(); });
    $$('.hp-pop button').forEach(b => b.addEventListener('click', () => { cat = 'all'; ts.forEach(x => { x.classList.toggle('is-on', x.dataset.cat === 'all'); x.setAttribute('aria-pressed', x.dataset.cat === 'all'); }); q.value = b.dataset.q; apply(); toList(); }));
    ts.forEach(b => b.addEventListener('click', () => {
      cat = b.dataset.cat; ts.forEach(x => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b); });
      apply(); if (matchMedia('(max-width: 960px)').matches) b.scrollIntoView({ inline: 'center', block: 'nearest', behavior: 'smooth' });
      const top = $('.hp-list'); if (top.getBoundingClientRect().top < 0) toList();
    }));
    clear.addEventListener('click', () => { cat = 'all'; q.value = ''; ts.forEach(x => { x.classList.toggle('is-on', x.dataset.cat === 'all'); x.setAttribute('aria-pressed', x.dataset.cat === 'all'); }); apply(); });
    const P = new URLSearchParams(location.search);
    if (P.get('q')) { q.value = P.get('q'); apply(); }
    else if (P.get('topic')) { const t = ts.find(x => x.dataset.cat === P.get('topic')); t && t.click(); }
    else open(hqs[0], true);
  }

  // legal TOC highlight
  const links = $$('.lg-toc a');
  if (links.length) {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id)); }), { rootMargin: '-20% 0px -70% 0px' });
    $$('.lg-s').forEach(s => io.observe(s));
  }
})();
