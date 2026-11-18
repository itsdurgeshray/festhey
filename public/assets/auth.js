/* FestHey auth: password eye + strength, role switch, OTP boxes, resend timer, verification method, light validation */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const P = new URLSearchParams(location.search);
  // works on the static site (page.html) and the Next.js routes (/page)
  const url = p => (/\.html$/.test(location.pathname) ? p + '.html' : '/' + p);
  const toast = msg => { const t = $('.fd-toast'); if (!t) return; t.textContent = msg; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 2600); };
  if (P.get('reset') === '1') toast('Password updated. Log in with your new password.');

  // show / hide password
  $$('.pw-eye').forEach(b => b.addEventListener('click', () => {
    const i = $('input', b.closest('.fld')), on = i.type === 'password';
    i.type = on ? 'text' : 'password'; b.setAttribute('aria-pressed', on); b.setAttribute('aria-label', on ? 'Hide password' : 'Show password');
  }));
  // strength meter
  const score = v => (v.length >= 8) + /[A-Z]/.test(v) * .5 + /[a-z]/.test(v) * .5 + /\d/.test(v) + /[^A-Za-z0-9]/.test(v);
  const LABEL = ['Use 8+ characters with a number and a symbol', 'Weak', 'Okay', 'Good', 'Strong'];
  $$('.pw-meter').forEach(m => { const i = $('input', m.closest('.df')); i.addEventListener('input', () => { const s = i.value ? Math.max(1, Math.min(4, Math.floor(score(i.value)))) : 0; m.dataset.s = s; $('small', m).textContent = LABEL[s]; }); });

  // role switch on register
  const roles = $$('.au-role button');
  const store = (k, v) => { try { return v === undefined ? localStorage.getItem(k) : localStorage.setItem(k, v); } catch (e) { return null; } };
  const lf = $('[data-auth="login"]');
  if (lf) lf.action = url(store('fh-role') === 'organiser' ? 'org' : 'me');
  const setRole = r => {
    roles.forEach(b => { const on = b.dataset.role === r; b.classList.toggle('is-on', on); b.setAttribute('aria-checked', on); });
    $$('[data-for]').forEach(el => el.hidden = el.dataset.for !== r);
    const f = $('[data-auth="register"]'); if (f) { f.action = url('verify') + '?role=' + r; store('fh-role', r); }
  };
  roles.forEach(b => b.addEventListener('click', () => setRole(b.dataset.role)));
  if (roles.length) setRole(['organiser', 'organizer'].includes(P.get('role')) ? 'organiser' : 'student');

  // OTP boxes: auto advance, backspace, paste
  $$('.otp').forEach(g => {
    const ins = $$('input', g);
    const sync = () => { ins.forEach(i => i.classList.toggle('is-on', !!i.value)); g.classList.remove('is-bad'); g.dispatchEvent(new CustomEvent('otp', { bubbles: true, detail: ins.map(i => i.value).join('') })); };
    ins.forEach((i, k) => {
      i.addEventListener('input', () => { i.value = i.value.replace(/\D/g, '').slice(-1); if (i.value && ins[k + 1]) ins[k + 1].focus(); sync(); });
      i.addEventListener('keydown', ev => { if (ev.key === 'Backspace' && !i.value && ins[k - 1]) { ins[k - 1].focus(); ins[k - 1].value = ''; sync(); } if (ev.key === 'ArrowLeft' && ins[k - 1]) ins[k - 1].focus(); if (ev.key === 'ArrowRight' && ins[k + 1]) ins[k + 1].focus(); });
      i.addEventListener('paste', ev => { const d = (ev.clipboardData.getData('text') || '').replace(/\D/g, '').slice(0, 6); if (!d) return; ev.preventDefault(); ins.forEach((x, j) => x.value = d[j] || ''); (ins[d.length] || ins[5]).focus(); sync(); });
    });
  });
  // resend countdown
  $$('[data-resend]').forEach(b => {
    let t = 30, timer;
    const tick = () => { const s = $('span', b); t--; if (t <= 0) { clearInterval(timer); b.disabled = false; b.textContent = 'Resend now'; } else if (s) s.textContent = t; };
    const start = () => { t = 30; b.disabled = true; b.innerHTML = 'Resend in <span>30</span>s'; clearInterval(timer); timer = setInterval(tick, 1000); };
    b.addEventListener('click', () => { toast('A new code is on its way'); start(); });
    if (!b.closest('[hidden]')) start(); else b._start = start;
  });

  // verify email
  const vf = $('[data-auth="otp"]');
  if (vf) {
    const go = $('[data-otp-go]', vf), org = ['organiser', 'organizer'].includes(P.get('role'));
    vf.action = url(org ? 'onboard-org' : 'onboard');
    vf.addEventListener('otp', ev => go.classList.toggle('is-off', ev.detail.length < 6));
    vf.addEventListener('submit', ev => { const code = $$('.otp input', vf).map(i => i.value).join(''); if (code.length < 6) { ev.preventDefault(); $('.otp', vf).classList.add('is-bad'); } });
  }

  // organiser verification
  const ov = $('[data-auth="orgv"]');
  if (ov) {
    if (P.get('state') === 'sent') { $('.ov-form').hidden = true; $('.ov-done').hidden = false; }
    $$('input[name=ov]').forEach(r => r.addEventListener('change', () => $$('[data-ov]').forEach(p => p.hidden = p.dataset.ov !== r.value)));
    $('[data-send]', ov).addEventListener('click', () => {
      const e = $('#cemail'); if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(e.value)) { e.closest('.fld').classList.add('is-bad'); e.focus(); return toast('Enter your official college email'); }
      e.closest('.fld').classList.remove('is-bad'); const box = $('.ov-code', ov); box.hidden = false; const r = $('[data-resend]', box); r && r._start && r._start(); $('.otp input', box).focus(); toast('Code sent to ' + e.value);
    });
    const drop = $('.drop', ov), fi = drop && $('input', drop);
    fi && fi.addEventListener('change', () => { const f = fi.files[0]; if (!f) return; $('b', drop).textContent = f.name; $('small', drop).textContent = Math.round(f.size / 1024) + ' KB, ready to submit'; if (f.type.startsWith('image/')) { const r = new FileReader(), img = $('.drop-img', drop); r.onload = () => { img.src = r.result; img.hidden = false; }; r.readAsDataURL(f); } });
  }

  // reset password gate
  const rf = $('[data-auth="reset"]');
  if (rf) {
    const go = $('[data-reset-go]', rf), a = $('#np1'), b = $('#np2'), hint = $('.pw-match', rf);
    const check = () => { const code = $$('.otp input', rf).map(i => i.value).join(''); const match = a.value && a.value === b.value; hint.hidden = !b.value || match; go.classList.toggle('is-off', !(code.length === 6 && a.value.length >= 8 && match)); };
    rf.addEventListener('input', check); rf.addEventListener('otp', check);
  }

  // light validation for the main forms
  $$('[data-auth="login"], [data-auth="register"], [data-auth="forgot"]').forEach(f => f.addEventListener('submit', ev => {
    const bad = $$('input[required]', f).filter(i => !i.closest('[hidden]') && (i.type === 'checkbox' ? !i.checked : !i.value.trim() || (i.type === 'email' && !/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(i.value))));
    $$('.fld', f).forEach(x => x.classList.remove('is-bad'));
    const p1 = $('#pw1', f), p2 = $('#pw2', f);
    if (p1 && p2 && p1.value !== p2.value) bad.push(p2);
    if (bad.length) { ev.preventDefault(); bad.forEach(i => { const fl = i.closest('.fld'); fl && fl.classList.add('is-bad'); }); const first = bad[0]; first.focus(); toast(first.type === 'checkbox' ? 'Please accept the terms to continue' : p2 && bad.includes(p2) && p2.value ? 'Passwords don’t match' : 'Fill in the highlighted fields'); }
  }));

  // onboarding (students and organisers): one step at a time, checked before moving on
  const ob = $('[data-ob]');
  if (ob) {
    const f = $('.ob-f', ob), steps = $$('.ob-step', ob), n = steps.length, bar = $$('.ob-bar li', ob);
    const back = $('[data-ob-back]', ob), next = $('[data-ob-next]', ob), done = $('[data-ob-done]', ob), skip = $('[data-ob-skip]', ob);
    let i = 0;
    const vis = el => !el.closest('[hidden]');
    const picked = () => $('.ob-cols input:checked', ob);
    const newOpen = () => { const nw = $('.ob-new', ob); return nw && !nw.hidden; };
    const fillSum = () => {
      const r = picked(), nm = r ? r.value : ($('#ncname') || {}).value || '';
      const short = r ? r.dataset.short : nm.split(/\s+/).filter(Boolean).slice(0, 2).map(w => w[0]).join('').toUpperCase();
      const city = r ? r.dataset.city : [($('#nccity') || {}).value, ($('#ncstate') || {}).value].filter(Boolean).join(', ');
      const set = (k, v) => { const el = $(`[data-sum="${k}"]`, ob); if (el && v) el.textContent = v; };
      set('college', nm); set('short', short); set('city', city); set('role', ($('#orole') || {}).value);
      const t = $$('.ob-invl li', ob).length; set('team', t ? t + (t === 1 ? ' invite' : ' invites') + ' ready to send' : 'None yet');
      if (nm) store('fh-ob-college', nm);
    };
    const show = (k, quiet) => {
      i = k;
      steps.forEach((s, j) => s.hidden = j !== k);
      bar.forEach((b, j) => { b.classList.toggle('is-on', j === k); b.classList.toggle('is-done', j < k); });
      $('[data-ob-i]', ob).textContent = k + 1;
      back.hidden = k === 0; next.hidden = k === n - 1; done.hidden = k !== n - 1; skip.hidden = !steps[k].hasAttribute('data-optional');
      if (k === n - 1) fillSum();
      if (!quiet) window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    const valid = () => {
      const s = steps[i], bad = [];
      $$('.is-bad', s).forEach(x => x.classList.remove('is-bad'));
      $$('select', s).filter(vis).filter(x => !x.value).forEach(x => bad.push(x.closest('.sel')));
      $$('[data-min]', s).filter(g => !$$('.is-on', g).length).forEach(g => bad.push(g));
      const cols = $('.ob-cols', s);
      if (cols && !picked() && !newOpen()) bad.push(cols);
      if (newOpen()) $$('[data-req-new]', s).filter(x => !x.value.trim()).forEach(x => bad.push(x.closest('.fld')));
      bad.forEach(x => x && x.classList.add('is-bad'));
      if (bad.length) {
        const first = bad[0]; first.scrollIntoView({ block: 'center', behavior: 'smooth' });
        const fc = $('select,input', first); fc && fc.focus({ preventScroll: true });
        toast(cols && bad.includes(cols) ? 'Pick your college, or add it if it is not listed' : (bad[0].matches('[data-min]') ? 'Pick at least one' : 'Fill in the highlighted fields'));
      }
      return !bad.length;
    };
    next.addEventListener('click', () => { if (valid()) show(i + 1); });
    back.addEventListener('click', () => show(i - 1));
    skip.addEventListener('click', () => show(Math.min(i + 1, n - 1)));
    f.addEventListener('submit', ev => { ev.preventDefault(); if (i < n - 1) { if (valid()) show(i + 1); return; } fillSum(); location.href = f.getAttribute('action'); });
    f.addEventListener('change', ev => { const x = ev.target.closest('.is-bad'); x && x.classList.remove('is-bad'); });
    // year of study, interests
    $$('.ob-seg', ob).forEach(g => $$('button', g).forEach(b => b.addEventListener('click', () => $$('button', g).forEach(x => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-checked', x === b); }))));
    $$('.ob-chips .chip', ob).forEach(c => c.addEventListener('click', () => { const on = !c.classList.contains('is-on'); c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on); c.closest('.ob-chips').classList.remove('is-bad'); }));
    // photo and document previews
    $$('.ob-av, .ob .drop', ob).forEach(d => { const fi = $('input[type=file]', d); fi && fi.addEventListener('change', () => {
      const file = fi.files[0]; if (!file) return; const b = $('b', d); if (b && d.classList.contains('drop')) b.textContent = file.name;
      if (file.type.startsWith('image/')) { const r = new FileReader(), img = $('.drop-img', d); r.onload = () => { img.src = r.result; img.hidden = false; d.classList.add('has-img'); }; r.readAsDataURL(file); }
    }); });
    // organiser: search the college list, or add a new one
    const q = $('[data-ob-search]', ob);
    q && q.addEventListener('input', () => {
      const v = q.value.trim().toLowerCase(); let k = 0;
      $$('.ob-col', ob).forEach(c => { const hit = !v || c.dataset.name.includes(v); c.hidden = !hit; k += hit; });
      $('.ob-none', ob).hidden = k > 0;
    });
    const nt = $('[data-ob-new]', ob), nw = $('.ob-new', ob);
    nt && nt.addEventListener('click', () => {
      const open = nw.hidden; nw.hidden = !open; nt.setAttribute('aria-expanded', open); nt.classList.toggle('is-on', open);
      if (open) { $$('.ob-cols input', ob).forEach(r => r.checked = false); $('.ob-cols', ob).classList.remove('is-bad'); const nm = $('#ncname'); if (q && q.value && !nm.value) nm.value = q.value; nm.focus(); }
    });
    $$('.ob-cols input', ob).forEach(r => r.addEventListener('change', () => { if (nw) { nw.hidden = true; nt.setAttribute('aria-expanded', 'false'); nt.classList.remove('is-on'); } $('.ob-cols', ob).classList.remove('is-bad'); }));
    // co-organiser invites
    const ib = $('[data-ob-invite]', ob);
    ib && ib.addEventListener('click', () => {
      const e = $('.ob-inv input', ob), list = $('.ob-invl', ob);
      if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(e.value)) { e.closest('.fld').classList.add('is-bad'); e.focus(); return toast('Enter a valid email'); }
      e.closest('.fld').classList.remove('is-bad');
      const li = document.createElement('li'); li.innerHTML = '<span></span><button type="button" aria-label="Remove invite">&times;</button>';
      li.firstChild.textContent = e.value.trim(); li.lastChild.addEventListener('click', () => li.remove()); list.append(li); e.value = ''; e.focus();
    });
    const ie = $('.ob-inv input', ob); ie && ie.addEventListener('keydown', ev => { if (ev.key === 'Enter') { ev.preventDefault(); ib.click(); } });
    // adding a second (or third) college from the dashboard
    if (P.get('add') === '1') { const h = $('.ob-step[data-step="1"] .au-t', ob), eb = $('.ob-step[data-step="1"] .eyebrow', ob); if (h) h.textContent = 'ADD ANOTHER COLLEGE'; if (eb) eb.lastChild.textContent = 'Organiser setup'; }
    show(0, true);
  }
  // verification names the college picked during setup
  const obc = store('fh-ob-college');
  if (obc) $$('[data-ob-short]').forEach(x => x.textContent = x.closest('.au-t') ? obc.toUpperCase() : obc);
})();
