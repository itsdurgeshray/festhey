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
  const setRole = r => {
    roles.forEach(b => { const on = b.dataset.role === r; b.classList.toggle('is-on', on); b.setAttribute('aria-checked', on); });
    $$('[data-for]').forEach(el => el.hidden = el.dataset.for !== r);
    const f = $('[data-auth="register"]'); if (f) f.action = url('verify') + '?role=' + r;
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
    vf.action = url(org ? 'org-verify' : 'me');
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
})();
