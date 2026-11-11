/* FestHey v5 interactions */
(function () {
  const root = document.documentElement;
  const FIGMA = root.classList.contains('figma');
  const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const STATIC = FIGMA || REDUCE;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const rand = (a, b) => a + Math.random() * (b - a);
  const params = new URLSearchParams(location.search);

  /* ================= nav ================= */
  const nav = $('.nav'), menuBtn = $('.nav-menu');
  menuBtn && menuBtn.addEventListener('click', () => {
    const o = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', o);
  });

  /* ================= events treatment (?ev=ticket | calendar | poster) ================= */
  const evRow = $('#events .ev-row');
  const ev = params.get('ev');
  if (evRow && ['ticket', 'calendar', 'poster'].includes(ev)) evRow.className = 'ev-row v-' + ev;

  /* ================= category filter ================= */
  const chips = $$('.fe .chips .chip');
  const filterables = () => $$('.fest, #events .evc');
  function setCat(k) {
    const hit = it => k === 'all' || it.dataset.cat.split(' ').includes(k);
    chips.forEach(x => { const on = x.dataset.cat === k; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
    filterables().forEach(it => it.classList.toggle('hide', !hit(it)));
    if (window.gsap && !STATIC) {
      const vis = filterables().filter(i => !i.classList.contains('hide'));
      vis.forEach(t => t.style.transition = 'none');
      gsap.fromTo(vis, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .6, ease: 'power3.out', stagger: .03, clearProps: 'transform,opacity,transition' });
      window.ScrollTrigger && ScrollTrigger.refresh();
    }
  }
  chips.forEach(b => b.addEventListener('click', () => setCat(b.dataset.cat)));

  /* ================= FAQ: chat on desktop, accordion below 1025 ================= */
  const qas = $$('.qa'), chat = $('.chat-body');
  const desk = () => matchMedia('(min-width: 1025px)').matches;
  let asking = 0;
  function ask(i) {
    const q = qas[i];
    const me = document.createElement('div');
    me.className = 'bub bub-me bub-in'; me.textContent = $('.qa-t', q).textContent;
    chat.appendChild(me);
    const typing = document.createElement('div');
    typing.className = 'bub bub-bot bub-typing bub-in'; typing.innerHTML = '<span></span><span></span><span></span>';
    const token = ++asking;
    setTimeout(() => token === asking && chat.appendChild(typing), 260);
    setTimeout(() => {
      typing.remove();
      if (token !== asking) return;
      const a = document.createElement('div');
      a.className = 'bub bub-bot bub-in'; a.innerHTML = $('.bub', q).innerHTML;
      chat.appendChild(a);
      while (chat.children.length > 6) chat.firstElementChild.remove();
    }, 1050);
    while (chat.children.length > 6) chat.firstElementChild.remove();
  }
  qas.forEach((q, i) => $('.qa-q', q).addEventListener('click', () => {
    const wasOn = q.classList.contains('is-on');
    if (desk()) {
      if (wasOn) return;
      qas.forEach(o => { o.classList.toggle('is-on', o === q); $('.qa-q', o).setAttribute('aria-expanded', o === q); });
      ask(i);
    } else {
      qas.forEach(o => { const on = o === q && !wasOn; o.classList.toggle('is-on', on); $('.qa-q', o).setAttribute('aria-expanded', on); });
    }
  }));

  /* ================= lanyard pass (pit) ================= */
  class Pass {
    constructor(el) {
      this.el = el; this.arm = $('.p-arm', el); this.card = $('.p-card', el); this.sheen = $('.sheen', el);
      this.a = 0; this.w = 0; this.r = 0; this.v = 0; this.K1 = parseFloat(el.dataset.k) || 6; this.K2 = 30;
      this.max = parseFloat(el.dataset.max) || 1; this.drag = false; this.target = 0; this.seed = Math.random() * 100;
      const c = this.card;
      c.addEventListener('pointerdown', e => {
        if (e.target.closest('input,button,a,label,form')) return;
        this.drag = true; c.setPointerCapture(e.pointerId); this.aim(e);
      });
      c.addEventListener('pointermove', e => this.drag && this.aim(e));
      const up = () => { this.drag = false; };
      c.addEventListener('pointerup', up); c.addEventListener('pointercancel', up);
    }
    kick(x) { this.w += x; }
    aim(e) {
      const b = this.el.getBoundingClientRect();
      this.target = clamp(-Math.atan2(e.clientX - (b.left + b.width / 2), Math.max(30, e.clientY - b.top)), -this.max, this.max);
    }
    step(dt, t) {
      const ext = this.drag ? 70 * (this.target - this.a) - 9 * this.w : 0.08 * Math.sin(t * .9 + this.seed);
      const acc1 = -this.K1 * Math.sin(this.a) - 1.2 * this.w + ext;
      this.w += acc1 * dt; this.a += this.w * dt;
      const acc2 = -this.K2 * Math.sin(this.r) - 2.4 * this.v - acc1 * .6;
      this.v += acc2 * dt; this.r += this.v * dt;
      if (Math.abs(this.a) > this.max) { this.a = Math.sign(this.a) * this.max; this.w *= -.35; }
      this.r = clamp(this.r, -.6, .6);
    }
    render() {
      this.arm.style.transform = 'rotate(' + this.a.toFixed(4) + 'rad)';
      this.card.style.transform = 'rotate(' + this.r.toFixed(4) + 'rad)';
      this.sheen && this.sheen.style.setProperty('--sx', ((this.a + this.r) * 260).toFixed(1) + 'px');
    }
  }
  const passEl = $('.pass--access');
  const pass = passEl && !STATIC ? new Pass(passEl) : null;

  /* ================= confetti + crowd cheer ================= */
  const cv = $('.confetti'), crowd = $('.crowd');
  function confetti(x, y) {
    if (!cv || STATIC) return;
    const ctx = cv.getContext('2d'), r = cv.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio || 1);
    cv.width = r.width * dpr; cv.height = r.height * dpr; ctx.scale(dpr, dpr);
    const cols = ['#FF5A14', '#FFD400', '#F7F5F0', '#140A04', '#FFFFFF'];
    const ps = Array.from({ length: 170 }, () => ({ x, y, vx: rand(-9, 9), vy: rand(-17, -5), s: rand(6, 12), c: cols[Math.random() * cols.length | 0], a: rand(0, 6), va: rand(-.3, .3), life: 1 }));
    let t0 = performance.now();
    (function tick(now) {
      const dt = Math.min(2, (now - t0) / 16.7); t0 = now;
      ctx.clearRect(0, 0, r.width, r.height);
      let alive = 0;
      ps.forEach(p => {
        p.vy += .38 * dt; p.vx *= .99; p.x += p.vx * dt; p.y += p.vy * dt; p.a += p.va * dt; p.life -= .006 * dt;
        if (p.life > 0 && p.y < r.height + 20) {
          alive++;
          ctx.save(); ctx.globalAlpha = clamp(p.life * 1.5, 0, 1); ctx.translate(p.x, p.y); ctx.rotate(p.a);
          ctx.fillStyle = p.c; ctx.fillRect(-p.s / 2, -p.s / 4, p.s, p.s / 2); ctx.restore();
        }
      });
      if (alive) requestAnimationFrame(tick); else ctx.clearRect(0, 0, r.width, r.height);
    })(t0);
  }
  const form = $('.acc-form');
  form && form.addEventListener('submit', e => {
    e.preventDefault();
    const inp = $('input', form);
    if (!/.+@.+\..+/.test(inp.value)) { inp.focus(); pass && pass.kick(-2); return; }
    form.classList.add('is-done');
    pass && pass.kick(2.4);
    const b = $('.btn', form).getBoundingClientRect(), s = cv.getBoundingClientRect();
    confetti(b.left - s.left + b.width / 2, b.top - s.top);
    if (crowd) { crowd.classList.add('cheer'); setTimeout(() => crowd.classList.remove('cheer'), 2600); }
  });

  /* ================= hero: the three featured fests, fanned ================= */
  const trio = $('.trio');
  if (trio) {
    const cards = $$('.fcard', trio), dots = $$('.trio-dots span', trio);
    const POS = ['is-c', 'is-r', 'is-l'];
    let c = 0, timer = null;
    const set = i => {
      c = (i % 3 + 3) % 3;
      cards.forEach((el, j) => { el.classList.remove('is-c', 'is-l', 'is-r'); el.classList.add(POS[(j - c + 3) % 3]); });
      dots.forEach((d, j) => d.classList.toggle('on', j === c));
    };
    const restart = () => { clearInterval(timer); if (!STATIC) timer = setInterval(() => set(c + 1), 4800); };
    cards.forEach((el, j) => el.addEventListener('click', e => {
      if (swiped) { e.preventDefault(); return; }
      if (!el.classList.contains('is-c')) { e.preventDefault(); set(j); restart(); }
    }));
    // swipe on touch screens
    let sx = null, swiped = false;
    trio.addEventListener('pointerdown', e => { sx = e.clientX; swiped = false; });
    trio.addEventListener('pointerup', e => {
      if (sx === null) return;
      const dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 40) { swiped = true; set(c + (dx < 0 ? 1 : -1)); restart(); setTimeout(() => swiped = false, 60); }
    });
    trio.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') clearInterval(timer); });
    trio.addEventListener('pointerleave', restart);
    restart();
  }

  /* ================= events: drag + arrows ================= */
  const track = $('#events .ev-track');
  if (track) {
    let drag = null, moved = 0, push = 0, vel = 0;
    track.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      drag = { x: e.clientX, sl: track.scrollLeft, lx: e.clientX, t: performance.now() }; moved = 0;
      track.classList.add('dragging');
    });
    addEventListener('pointermove', e => {
      if (!drag) return;
      const dx = e.clientX - drag.x; moved = Math.max(moved, Math.abs(dx));
      track.scrollLeft = drag.sl - dx;
      const now = performance.now(); vel = (e.clientX - drag.lx) / Math.max(8, now - drag.t) * 16; drag.lx = e.clientX; drag.t = now;
    });
    addEventListener('pointerup', () => { if (!drag) return; drag = null; track.classList.remove('dragging'); push = -vel; });
    track.addEventListener('click', e => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } moved = 0; }, true);
    track.addEventListener('dragstart', e => e.preventDefault());
    (function glide() { if (!drag && Math.abs(push) > .3) { track.scrollLeft += push; push *= .92; } requestAnimationFrame(glide); })();
    const step = () => { const c = $$('.evc', track).find(x => !x.classList.contains('hide')); return c ? c.offsetWidth + 22 : 320; };
    $('.ev-next').addEventListener('click', () => track.scrollBy({ left: step() * 2, behavior: 'smooth' }));
    $('.ev-prev').addEventListener('click', () => track.scrollBy({ left: -step() * 2, behavior: 'smooth' }));
  }

  if (STATIC) return;

  /* ================= pass loop ================= */
  if (pass) {
    let vis = false;
    new IntersectionObserver(es => es.forEach(e => vis = e.isIntersecting)).observe($('.pit'));
    let last = performance.now();
    (function loop(now) {
      const dt = Math.min(.05, (now - last) / 1000); last = now;
      if (vis) { for (let k = 0; k < 4; k++) pass.step(dt / 4, now / 1000); pass.render(); }
      requestAnimationFrame(loop);
    })(last);
  }

  if (!window.gsap) return;
  gsap.registerPlugin(ScrollTrigger);

  /* ================= smooth scroll ================= */
  let lastY = 0;
  const onScroll = (y, v) => {
    if (y > 40 && y > lastY) nav.classList.add('hide'); else nav.classList.remove('hide');
    lastY = y;
    if (pass) pass.kick(clamp(v, -30, 30) * .0012);
  };
  if (window.Lenis) {
    const lenis = window.__lenis = new Lenis({ lerp: .1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    lenis.on('scroll', e => onScroll(e.scroll, e.velocity || 0));
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
      const id = a.getAttribute('href'); const t = id === '#top' ? 0 : $(id);
      if (t === null) return;
      e.preventDefault(); lenis.scrollTo(t, { duration: 1.4 });
    }));
  } else {
    let ly = scrollY;
    addEventListener('scroll', () => { const v = scrollY - ly; ly = scrollY; onScroll(scrollY, v); }, { passive: true });
  }

  /* ================= hero intro ================= */
  gsap.timeline({ defaults: { ease: 'power4.out' } })
    .from('.ticker', { yPercent: -100, duration: .8 }, 0)
    .from('.notch', { y: -80, duration: 1.1, ease: 'back.out(1.6)' }, .2)
    .from('.nav-links, .nav-end, .nav-menu', { y: -20, opacity: 0, duration: .8, stagger: .06 }, .35)
    .from('.hero-h .ln', { y: 60, opacity: 0, duration: 1.1, stagger: .1 }, .15)
    .from('.hero-p, .hero-cta, .hero .joined', { y: 24, opacity: 0, duration: .8, stagger: .08 }, .45)
    .from('.trio', { y: 160, rotate: 4, opacity: 0, duration: 1.4, ease: 'expo.out' }, .35);

  /* ================= reveals ================= */
  const park = els => () => els.forEach(el => el.style.transition = 'none');
  const unpark = els => () => els.forEach(el => { el.style.transition = ''; el.style.transform = ''; el.style.opacity = ''; });
  const rv = (sel, vars = {}) => $$(sel).forEach(el => gsap.from(el, Object.assign({ y: 46, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } }, vars)));

  rv('.fe .sec-head h2');
  gsap.from(chips, { y: 20, opacity: 0, duration: .7, ease: 'power3.out', stagger: .04, onStart: park(chips), onComplete: unpark(chips), scrollTrigger: { trigger: '.fe .chips', start: 'top 90%' } });
  rv('.sub-head');
  ScrollTrigger.batch('.fe .fest', { start: 'top 90%', once: true, onEnter: b => gsap.from(b, {
    y: -70, rotate: i => (i % 2 ? 6 : -6), opacity: 0, duration: 1.3, ease: 'elastic.out(1,.6)', stagger: .08, transformOrigin: '50% 0', onStart: park(b), onComplete: unpark(b) }) });
  ScrollTrigger.batch('#events .evc', { start: 'top 92%', once: true, onEnter: b => gsap.from(b, {
    y: 70, opacity: 0, duration: 1, ease: 'power3.out', stagger: .07, onStart: park(b), onComplete: unpark(b) }) });
  rv('.faq-head > *', { y: 30 });
  ScrollTrigger.batch('.qa', { start: 'top 94%', once: true, onEnter: b => gsap.from(b, { y: 24, opacity: 0, duration: .7, ease: 'power3.out', stagger: .05 }) });
  gsap.from('.phone-wrap', { y: 220, rotate: 6, duration: 1.4, ease: 'power3.out', scrollTrigger: { trigger: '.faq', start: 'top 65%' } });
  rv('.pit-copy > *', { y: 30 });
  gsap.from('.crowd', { yPercent: 40, ease: 'none', scrollTrigger: { trigger: '.pit', start: 'top bottom', end: 'center center', scrub: .6 } });
  if (pass) ScrollTrigger.create({ trigger: '.pit', start: 'top 70%', once: true, onEnter: () => pass.kick(1.4) });
  const hostEls = $$('.host-card, .host-photo');
  gsap.from(hostEls, { y: 90, rotate: i => (i ? 8 : -6), opacity: 0, duration: 1.1, ease: 'back.out(1.4)', stagger: .12, onStart: park(hostEls), onComplete: unpark(hostEls), scrollTrigger: { trigger: '.host', start: 'top 80%' } });
  ScrollTrigger.batch('.poster', { start: 'top 92%', once: true, onEnter: b => gsap.from(b, {
    scale: 1.25, opacity: 0, rotate: i => (i % 2 ? 12 : -12), duration: .7, ease: 'back.out(1.6)', stagger: .12, onStart: park(b), onComplete: unpark(b) }) });
  gsap.from('.mural', { y: 80, scale: .92, opacity: 0, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: '.mural', start: 'top 90%' } });

  addEventListener('load', () => ScrollTrigger.refresh());
})();
