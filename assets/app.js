/* FestHey app pages: states, modals, team form, copy, blog filter, article TOC */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const toast = msg => { const t = $('.fd-toast'); if (!t) return; t.textContent = msg; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 2200); };
  const P = new URLSearchParams(location.search);

  // page state: ?state=pending|done (team defaults to pending, ?state=complete = done)
  const main = $('main[data-state]');
  if (main) { let s = P.get('state'); if (s === 'complete') s = 'done'; if (['open', 'pending', 'done'].includes(s)) main.dataset.state = s; }

  // modals
  let last = null;
  const open = id => { const m = document.getElementById(id); if (!m) return; last = document.activeElement; m.hidden = false; document.documentElement.classList.add('modal-open'); const f = $('input,button.btn,a.btn', m); f && setTimeout(() => f.focus(), 60); };
  const close = m => { m.hidden = true; document.documentElement.classList.remove('modal-open'); last && last.focus && last.focus(); };
  document.addEventListener('click', ev => {
    const o = ev.target.closest('[data-open]'); if (o) { ev.preventDefault(); open(o.dataset.open); return; }
    const c = ev.target.closest('[data-close]'); if (c) { ev.preventDefault(); close(c.closest('.modal')); }
  });
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape') $$('.modal:not([hidden])').forEach(close); });
  const m = P.get('modal'); if (m) open('m-' + m);
  // fest promo shows once per visit on the event page
  if (!m && $('#m-ad') && !P.has('figma')) { let seen = false; try { seen = sessionStorage.getItem('fh-ad'); sessionStorage.setItem('fh-ad', 1); } catch (e) {} if (!seen) setTimeout(() => { if (!$('.modal:not([hidden])')) open('m-ad'); }, 2400); }

  // create team form
  const form = $('#m-team form, form.modal-form');
  if (form) {
    const inp = $('input', form), left = $('.m-left', form), fld = inp.closest('.fld');
    inp.addEventListener('input', () => { left.textContent = 24 - inp.value.length; fld.classList.remove('is-bad'); });
    form.addEventListener('submit', ev => { if (!inp.value.trim()) { ev.preventDefault(); fld.classList.add('is-bad'); inp.focus(); toast('Give your team a name first'); } });
  }

  // copy invite link
  $$('[data-copy]').forEach(b => b.addEventListener('click', async () => { try { await navigator.clipboard.writeText(b.dataset.copy); toast('Invite link copied'); } catch (e) { toast(b.dataset.copy); } }));

  // save / share on event + article
  const save = $('.fd-save');
  save && save.addEventListener('click', () => { const on = save.getAttribute('aria-pressed') !== 'true'; save.setAttribute('aria-pressed', on); $('span', save).textContent = on ? 'Saved' : 'Save'; toast(on ? 'Event saved to your list' : 'Removed from saved'); });
  $$('.fd-share,.ar-share').forEach(b => b.addEventListener('click', async () => {
    if (navigator.share) { try { await navigator.share({ title: document.title, url: location.href }); } catch (e) {} return; }
    try { await navigator.clipboard.writeText(location.href); toast('Link copied'); } catch (e) { toast(location.href); }
  }));

  // event phone dock
  const dock = $('.fd-dock'), facts = $('.fd-facts');
  if (dock && facts) new IntersectionObserver(([en]) => dock.classList.toggle('show', !en.isIntersecting && en.boundingClientRect.top < 0)).observe(facts);

  // blog filter
  const posts = $$('.bl-list .post');
  if (posts.length) {
    const q = $('.lb-search input'); let cat = 'all';
    const apply = () => { const s = q.value.trim().toLowerCase(); let n = 0; posts.forEach(p => { const ok = (cat === 'all' || p.dataset.cat === cat) && (!s || p.dataset.name.includes(s)); p.hidden = !ok; if (ok) n++; }); $('.lb-n').textContent = n; $('.lb-empty').hidden = n > 0; };
    $$('.lb-chips .chip').forEach(c => c.addEventListener('click', () => { $$('.lb-chips .chip').forEach(x => { x.classList.remove('is-on'); x.setAttribute('aria-pressed', 'false'); }); c.classList.add('is-on'); c.setAttribute('aria-pressed', 'true'); cat = c.dataset.cat; apply(); }));
    q.addEventListener('input', apply);
  }

  // article progress + TOC
  const bar = $('.ar-progress i');
  if (bar) {
    const body = $('.ar-body');
    const tick = () => { const r = body.getBoundingClientRect(); bar.style.width = Math.min(100, Math.max(0, (innerHeight - r.top) / r.height * 100)) + '%'; };
    addEventListener('scroll', tick, { passive: true }); tick();
    const links = $$('.ar-toc a[href^="#"]');
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id)); }), { rootMargin: '-20% 0px -70% 0px' });
    links.forEach(a => { const s = $(a.getAttribute('href')); s && io.observe(s); });
  }

  // blog featured carousel
  const car = $('.bcar');
  if (car) {
    const tr = $('.bcar-track', car), dots = $$('.bcar-dots button', car), n = dots.length;
    const idx = () => Math.round(tr.scrollLeft / (tr.scrollWidth / n));
    const go = i => tr.scrollTo({ left: ((i + n) % n) * (tr.scrollWidth / n), behavior: 'smooth' });
    $('.bcar-prev', car).addEventListener('click', () => go(idx() - 1));
    $('.bcar-next', car).addEventListener('click', () => go(idx() + 1));
    dots.forEach((d, i) => d.addEventListener('click', () => go(i)));
    tr.addEventListener('scroll', () => { const k = idx(); dots.forEach((d, i) => d.classList.toggle('is-on', i === k)); }, { passive: true });
  }
})();
