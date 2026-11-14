/* FestHey dashboards: plan state, menus, tabs and filters, status pills, scanner, uploads, wizard, forms */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const P = new URLSearchParams(location.search);
  const toast = msg => { const t = $('.fd-toast'); if (!t) return; t.textContent = msg; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 2400); };
  const store = (k, v) => { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } };

  // plan state (prototype): ?plan=pro|free, remembered for the visit
  if (P.has('plan')) store('fh-plan', P.get('plan'));
  if ((P.get('plan') || store('fh-plan')) === 'pro') document.documentElement.dataset.plan = 'pro';
  $$('[data-open="m-cancel"]').forEach(() => { const a = $('#m-cancel .m-go'); a && a.addEventListener('click', () => store('fh-plan', 'free')); });
  const dl = $('.dl');
  if (dl && dl.classList.contains('rp') && P.get('state') === 'done') dl.classList.add('is-done');

  // dropdown menus
  const closeMenus = except => $$('.dmenu').forEach(m => { if (m !== except) { m.hidden = true; const b = $(`[data-menu="${m.dataset.menuFor}"]`); b && b.setAttribute('aria-expanded', 'false'); } });
  $$('[data-menu]').forEach(b => b.addEventListener('click', ev => {
    ev.stopPropagation(); const m = $(`[data-menu-for="${b.dataset.menu}"]`); if (!m) return;
    const open = m.hidden; closeMenus(m); m.hidden = !open; b.setAttribute('aria-expanded', open);
  }));
  document.addEventListener('click', ev => { if (!ev.target.closest('.dmenu')) closeMenus(); });
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape') closeMenus(); });

  // tabs: panel switchers and status filters
  const scopeOf = el => el.closest('.dsec, [data-panel], .dm');
  function filter(scope) {
    const tab = $('[data-tabs="filter"] [aria-selected="true"]', scope), q = $('[data-search]', scope);
    const k = tab ? tab.dataset.tab : 'all', s = q ? q.value.trim().toLowerCase() : '';
    let n = 0;
    $$('[data-status]', scope).forEach(it => { if (scopeOf(it) !== scope && !scope.contains(it)) return; const ok = (k === 'all' || it.dataset.status === k) && (!s || it.textContent.toLowerCase().includes(s)); it.hidden = !ok; if (ok) n++; });
    const empty = $('.d-empty', scope); if (empty) empty.hidden = n > 0;
  }
  function selectTab(group, key) {
    const btns = $$('[data-tab]', group); if (!btns.some(b => b.dataset.tab === key)) return;
    btns.forEach(b => b.setAttribute('aria-selected', b.dataset.tab === key));
    if (group.dataset.tabs === 'filter') return filter(scopeOf(group));
    const root = group.parentElement;
    $$(':scope > [data-panel]', root).forEach(p => p.hidden = p.dataset.panel !== key);
  }
  $$('[data-tabs]').forEach(g => {
    $$('[data-tab]', g).forEach(b => b.addEventListener('click', () => selectTab(g, b.dataset.tab)));
    if (g.dataset.tabs !== 'filter' && P.get('tab')) selectTab(g, P.get('tab'));
  });
  $$('[data-search]').forEach(i => i.addEventListener('input', () => filter(scopeOf(i))));
  $$('[data-goto]').forEach(a => a.addEventListener('click', ev => { ev.preventDefault(); const g = $('[data-tabs]:not([data-tabs="filter"])'); g && selectTab(g, a.dataset.goto); scrollTo({ top: 0, behavior: 'smooth' }); }));

  // status pills
  const KIND = { live: 'live', pub: 'up', draft: 'draft', cancel: 'bad', pend: 'live', ok: 'ok', wait: 'draft', rej: 'bad' };
  const setPill = (sel, v) => { const l = sel.closest('.pill-sel'); l.className = 'pill-sel pill--' + KIND[v]; const row = sel.closest('[data-status]'); if (row) row.dataset.status = v; };
  $$('[data-pill]').forEach(s => s.addEventListener('change', () => { setPill(s, s.value); toast('Status changed to ' + s.selectedOptions[0].text); }));

  // bulk actions on registrations
  const bulk = $('.bulk');
  if (bulk) {
    const cks = $$('.rc-ck input'), upd = () => { const n = cks.filter(c => c.checked).length; bulk.hidden = !n; $('[data-bulk-n]', bulk).textContent = n; };
    cks.forEach(c => c.addEventListener('change', upd));
    $$('[data-bulk]', bulk).forEach(b => b.addEventListener('click', () => {
      const v = b.dataset.bulk, sel = cks.filter(c => c.checked);
      sel.forEach(c => { const s = $('[data-pill]', c.closest('.rcard')); s.value = v; setPill(s, v); c.checked = false; });
      upd(); toast(sel.length + (sel.length === 1 ? ' registration ' : ' registrations ') + (v === 'ok' ? 'approved' : 'waitlisted'));
    }));
  }

  // misc buttons
  $$('[data-toast]').forEach(b => b.addEventListener('click', ev => { if (b.tagName === 'BUTTON') ev.preventDefault(); toast(b.dataset.toast); const m = b.closest('.modal'); if (m) { m.hidden = true; document.documentElement.classList.remove('modal-open'); } }));
  $$('[data-confirm]').forEach(i => { const btn = $('[data-confirm-btn]', i.closest('.modal-card')); i.addEventListener('input', () => btn.disabled = i.value.trim() !== i.dataset.confirm); });

  // gate scanner
  const cam = $('[data-cam]');
  if (cam) {
    const video = $('video', cam), err = $('.cam-err', cam), form = $('.code'), res = $('.res'), list = $('.hlist'), count = $('.hcount b');
    $$('.seg button').forEach(b => b.addEventListener('click', () => {
      $$('.seg button').forEach(x => x.classList.toggle('is-on', x === b));
      const code = b.dataset.mode === 'code'; cam.hidden = code; form.hidden = !code; if (code) $('input', form).focus();
    }));
    $('.cam-start', cam).addEventListener('click', async () => {
      err.hidden = true;
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        video.srcObject = stream; video.hidden = false; await video.play(); cam.classList.add('is-live');
      } catch (e) { err.hidden = false; }
    });
    const seen = new Set($$('.hrow--ok small', list).map(s => s.textContent));
    const show = (kind, t, p) => {
      res.className = 'res res--' + kind; void res.offsetWidth; res.classList.add('pop');
      $('.res-t', res).textContent = t; $('.res-p', res).textContent = p;
    };
    form.addEventListener('submit', ev => {
      ev.preventDefault();
      const inp = $('input', form), id = inp.value.trim().toUpperCase(); if (!id) return inp.focus();
      let ok = /^FH-CC-26-[A-Z0-9]{4}$/.test(id), msg;
      if (ok && seen.has(id)) { ok = false; msg = 'This pass was already used at ' + new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) + '.'; }
      const time = new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
      if (ok) { seen.add(id); show('ok', 'VALID PASS', 'Team SpiderTrack, 3 members. Let them in.'); count.textContent = +count.textContent + 1; }
      else show('bad', ok === false && msg ? 'ALREADY CHECKED IN' : 'NOT VALID', msg || 'This ID isn’t registered for Chords & Chaos.');
      const li = document.createElement('li');
      li.className = 'hrow is-new hrow--' + (ok ? 'ok' : 'bad');
      li.innerHTML = `<span class="hrow-ic"></span><span><b>${ok ? 'Rohan Verma' : 'Rejected scan'}</b><small></small></span><time>${time}</time>`;
      $('small', li).textContent = id; $('.hrow-ic', li).innerHTML = $((ok ? '.hrow--ok' : '.hrow--bad') + ' .hrow-ic', list).innerHTML;
      list.prepend(li); inp.value = ''; inp.focus();
    });
  }

  // uploads with preview
  const preview = (input, img) => { const f = input.files && input.files[0]; if (!f || !img) return; const r = new FileReader(); r.onload = () => { img.src = r.result; img.hidden = false; }; r.readAsDataURL(f); };
  $$('.drop, .cprof-banner, .pf-av').forEach(d => {
    const input = $('input[type=file]', d), img = $('.drop-img', d);
    input.addEventListener('change', () => { preview(input, img); toast('Image ready to upload'); });
    ['dragenter', 'dragover'].forEach(t => d.addEventListener(t, ev => { ev.preventDefault(); d.classList.add('is-over'); }));
    ['dragleave', 'drop'].forEach(t => d.addEventListener(t, ev => { ev.preventDefault(); d.classList.remove('is-over'); if (t === 'drop' && ev.dataTransfer.files.length) { input.files = ev.dataTransfer.files; input.dispatchEvent(new Event('change')); } }));
  });
  $$('.gal-add input').forEach(input => input.addEventListener('change', () => {
    const add = input.closest('.gal-add');
    [...input.files].forEach(f => { const r = new FileReader(); r.onload = () => { const fig = document.createElement('figure'); fig.innerHTML = '<img alt=""><button class="gal-x" aria-label="Remove photo">×</button>'; $('img', fig).src = r.result; add.before(fig); }; r.readAsDataURL(f); });
    toast(input.files.length + ' photo' + (input.files.length === 1 ? '' : 's') + ' added');
  }));
  document.addEventListener('click', ev => { const x = ev.target.closest('.gal-x'); if (x) { ev.preventDefault(); x.closest('figure').remove(); toast('Photo removed'); } });

  // create fest live preview
  const prev = $('.prev');
  if (prev) {
    const f = $('.cf-form'), title = $('[name=title]', f), tag = $('[name=tag]', f), cat = $('select', f), dates = $$('input[type=date]', f);
    const fmt = v => v ? new Date(v + 'T00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) : '';
    const upd = () => {
      $('[data-prev-title]').textContent = title.value || 'Your fest title';
      $('[data-prev-tag]').textContent = tag.value || 'Your tagline shows up on cards across FestHey.';
      $('[data-prev-cat]').textContent = cat.value;
      const a = fmt(dates[2].value), b = fmt(dates[3].value); $('[data-prev-date]').textContent = a ? (b ? a + ' to ' + b : a) : 'Dates appear here';
    };
    f.addEventListener('input', upd); f.addEventListener('change', upd);
    const bannerIn = $('.drop input', f); bannerIn.addEventListener('change', () => preview(bannerIn, $('[data-prev-img]')));
  }

  // chips that toggle (amenities, interests)
  $$('.amen .chip').forEach(c => c.addEventListener('click', () => { const on = c.getAttribute('aria-pressed') !== 'true'; c.setAttribute('aria-pressed', on); c.classList.toggle('is-on', on); c.closest('form') && c.closest('form').dispatchEvent(new Event('input')); }));

  // steppers
  $$('.stepper').forEach(s => { const i = $('input', s), [m, p] = $$('button', s); m.addEventListener('click', () => { i.value = Math.max(+i.min || 0, (+i.value || 0) - 1); }); p.addEventListener('click', () => { i.value = (+i.value || 0) + 1; }); });

  // repeaters
  $$('[data-add]').forEach(b => b.addEventListener('click', () => {
    const rep = $(`[data-rep="${b.dataset.add}"]`), first = rep.firstElementChild, c = first.cloneNode(true);
    $$('input', c).forEach(i => i.value = ''); rep.appendChild(c); $('input', c).focus();
  }));
  document.addEventListener('click', ev => { const x = ev.target.closest('.rep-x'); if (!x) return; const rep = x.closest('.rep'), row = x.closest('.rep > *'); if (rep.children.length > 1) row.remove(); else $$('input', row).forEach(i => i.value = ''); });

  // wizard
  const wiz = $('.wiz');
  if (wiz) {
    const steps = $$('.wstep', wiz), dots = $$('.wsteps li'); let k = 0;
    const go = n => {
      k = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach((s, i) => s.hidden = i !== k);
      dots.forEach((d, i) => { d.classList.toggle('is-on', i === k); d.classList.toggle('is-done', i < k); });
      $('[data-prev]', wiz).hidden = k === 0; $('[data-next]', wiz).hidden = k === steps.length - 1; $('[data-create]', wiz).hidden = k !== steps.length - 1;
      scrollTo({ top: 0, behavior: 'smooth' });
    };
    $('[data-next]', wiz).addEventListener('click', () => { toast('Draft saved'); go(k + 1); });
    $('[data-prev]', wiz).addEventListener('click', () => go(k - 1));
    dots.forEach((d, i) => d.addEventListener('click', () => go(i)));
  }

  // ad summary
  const pos = $$('input[name=pos]');
  if (pos.length) {
    const rs = n => '₹' + n.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const upd = () => { const c = pos.find(p => p.checked), fee = +c.dataset.price, gst = fee * .18; $('[data-sum-name]').textContent = c.dataset.name; $('[data-sum-fee]').textContent = rs(fee); $('[data-sum-gst]').textContent = rs(gst); $('[data-sum-total]').textContent = rs(fee + gst); };
    const want = P.get('pos'); if (want && pos[+want - 1]) pos[+want - 1].checked = true;
    pos.forEach(p => p.addEventListener('change', upd)); upd();
  }

  // upgrade terms
  const terms = $('[data-terms]');
  if (terms) {
    const pay = $('[data-pay]');
    terms.addEventListener('change', () => { pay.classList.toggle('is-off', !terms.checked); pay.setAttribute('aria-disabled', !terms.checked); });
    pay.addEventListener('click', () => store('fh-plan', 'pro'));
  }

  // profile: unsaved changes bar
  const pf = $('.pf-form');
  if (pf) {
    const bar = $('.savebar', pf);
    pf.addEventListener('input', () => bar.hidden = false); pf.addEventListener('change', () => bar.hidden = false);
    pf.addEventListener('reset', () => setTimeout(() => bar.hidden = true));
    pf.addEventListener('submit', ev => { ev.preventDefault(); bar.hidden = true; toast('Profile saved'); });
  }

  // saved: un-saving removes the card
  if ($('.side-a.is-on[href*="me-saved"]')) {
    $$('.lc-save, .cc-save, .evc-save').forEach(b => { b.setAttribute('aria-pressed', 'true'); b.addEventListener('click', ev => {
      ev.preventDefault(); ev.stopPropagation(); const c = b.closest('.lc, .cc, .evc'); c.style.transition = 'opacity .3s,transform .3s'; c.style.opacity = 0; c.style.transform = 'scale(.96)';
      setTimeout(() => c.remove(), 300); toast('Removed from saved');
    }, true); });
  }
})();
