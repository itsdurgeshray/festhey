/* FestHey redesign interactions */
(function () {
  const root = document.documentElement;
  const FIGMA = root.classList.contains('figma');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------------- nav menu ---------------- */
  const nav = $('.nav'), menuBtn = $('.nav-menu');
  menuBtn && menuBtn.addEventListener('click', () => {
    const o = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', o);
  });

  /* ---------------- category filter ---------------- */
  const cats = $$('.cat');
  const items = $$('.fest, .ticket');
  cats.forEach(c => c.addEventListener('click', () => {
    const k = c.dataset.cat;
    cats.forEach(x => { x.classList.toggle('is-on', x === c); x.setAttribute('aria-pressed', x === c); });
    items.forEach(it => {
      const show = k === 'all' || it.dataset.cat.split(' ').includes(k);
      it.classList.toggle('hide', !show);
    });
    if (window.gsap && !FIGMA) {
      gsap.fromTo(items.filter(i => !i.classList.contains('hide')), { y: 24, opacity: 0 },
        { y: 0, opacity: 1, duration: .6, ease: 'power3.out', stagger: .04, clearProps: 'transform,opacity,transition',
          onStart() { this.targets().forEach(t => { t.style.transition = 'none'; }); } });
      window.ScrollTrigger && ScrollTrigger.refresh();
    }
  }));

  /* ---------------- FAQ ---------------- */
  const qas = $$('.qa');
  qas.forEach(q => $('.qa-q', q).addEventListener('click', () => {
    const open = !q.classList.contains('is-open');
    qas.forEach(o => { o.classList.remove('is-open'); $('.qa-q', o).setAttribute('aria-expanded', 'false'); });
    if (open) { q.classList.add('is-open'); $('.qa-q', q).setAttribute('aria-expanded', 'true'); }
  }));

  /* ---------------- access form ---------------- */
  const form = $('.acc-form');
  form && form.addEventListener('submit', e => {
    e.preventDefault();
    const inp = $('input', form);
    if (!inp.value || !/.+@.+\..+/.test(inp.value)) { inp.focus(); pitPass && pitPass.kick(-2.2); return; }
    form.classList.add('is-done');
    pitPass && pitPass.kick(2.6);
  });

  if (FIGMA) return;

  /* ---------------- lanyard physics ---------------- */
  class Pass {
    constructor(el) {
      this.el = el;
      this.arm = $('.p-arm', el);
      this.card = $('.p-card', el);
      this.sheen = $('.sheen', el);
      this.a = 0; this.w = 0; this.r = 0; this.v = 0;
      this.K1 = parseFloat(el.dataset.k) || 7 + Math.random() * 2;
      this.K2 = 30; this.drag = false; this.target = 0;
      this.seed = Math.random() * 100; this.moved = 0;
      this.max = parseFloat(el.dataset.max) || 1.25;
      this.bind();
    }
    kick(x) { this.w += x; }
    pivot() {
      const b = this.el.getBoundingClientRect();
      return { x: b.left + b.width / 2, y: b.top };
    }
    bind() {
      const c = this.card;
      c.addEventListener('pointerdown', e => {
        if (e.target.closest('input,button,a,label')) return;
        this.drag = true; this.moved = 0; this.sx = e.clientX; this.sy = e.clientY;
        c.setPointerCapture(e.pointerId);
        this.aim(e);
      });
      c.addEventListener('pointermove', e => {
        if (!this.drag) return;
        this.moved = Math.max(this.moved, Math.hypot(e.clientX - this.sx, e.clientY - this.sy));
        this.aim(e);
      });
      const up = () => {
        if (!this.drag) return;
        this.drag = false;
        if (this.moved < 6 && this.onTap) this.onTap();
      };
      c.addEventListener('pointerup', up);
      c.addEventListener('pointercancel', up);
      c.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this.onTap && this.onTap(); }
      });
    }
    aim(e) {
      const p = this.pivot();
      const ang = -Math.atan2(e.clientX - p.x, Math.max(30, e.clientY - p.y));
      this.target = Math.max(-1.1, Math.min(1.1, ang));
    }
    step(dt, t) {
      let ext;
      if (this.drag) ext = 70 * (this.target - this.a) - 9 * this.w;
      else ext = 0.09 * Math.sin(t * 0.9 + this.seed) + 0.05 * Math.sin(t * 2.3 + this.seed * 2);
      const acc1 = -this.K1 * Math.sin(this.a) - 1.2 * this.w + ext;
      this.w += acc1 * dt; this.a += this.w * dt;
      const acc2 = -this.K2 * Math.sin(this.r) - 2.4 * this.v - acc1 * 0.6;
      this.v += acc2 * dt; this.r += this.v * dt;
      if (Math.abs(this.a) > this.max) { this.a = Math.sign(this.a) * this.max; this.w *= -0.35; }
      this.r = Math.max(-0.8, Math.min(0.8, this.r));
    }
    render() {
      this.arm.style.transform = `rotate(${this.a.toFixed(4)}rad)`;
      this.card.style.transform = `rotate(${this.r.toFixed(4)}rad)`;
      if (this.sheen) this.sheen.style.setProperty('--sx', `${((this.a + this.r) * 260).toFixed(1)}px`);
    }
  }

  const heroPasses = $$('.rig-hero .pass').map(el => new Pass(el));
  const pitEl = $('.rig-pit .pass');
  const pitPass = pitEl ? new Pass(pitEl) : null;
  const all = pitPass ? [...heroPasses, pitPass] : heroPasses;

  // featured pass (replaces the old ad carousel)
  const featName = $('.feat-name'), feat = $('.feat'), cta = $('.btn-sun');
  let cur = 0, timer;
  function feature(i, auto) {
    cur = i;
    heroPasses.forEach((p, j) => {
      p.el.classList.toggle('is-on', j === i);
      p.el.style.zIndex = j === i ? 5 : (j === 1 ? 4 : 3);
    });
    const el = heroPasses[i].el;
    featName.classList.add('swap');
    setTimeout(() => { featName.textContent = el.dataset.name; featName.classList.remove('swap'); }, 220);
    feat.href = cta.href = el.dataset.href;
    heroPasses[i].kick(auto ? 1.4 : 0.6);
    clearInterval(timer); timer = setInterval(() => feature((cur + 1) % heroPasses.length, true), 5200);
  }
  heroPasses.forEach((p, i) => { p.onTap = () => feature(i); });
  if (heroPasses.length) {
    heroPasses.forEach((p, j) => p.el.style.zIndex = j === 0 ? 5 : (j === 1 ? 4 : 3));
    timer = setInterval(() => feature((cur + 1) % heroPasses.length, true), 5200);
  }

  // entrance swing
  heroPasses.forEach((p, i) => { p.a = [0.32, -0.26, 0.24][i] || 0; p.r = -p.a * .5; });
  if (pitPass) { pitPass.a = -0.35; }

  // wind from pointer movement over the hero
  const hero = $('.hero');
  let lx = null;
  hero && hero.addEventListener('pointermove', e => {
    if (lx !== null) {
      const vx = e.clientX - lx;
      heroPasses.forEach(p => {
        if (p.drag) return;
        const b = p.card.getBoundingClientRect();
        const d = Math.hypot(e.clientX - (b.left + b.width / 2), e.clientY - (b.top + b.height / 2));
        if (d < 260) p.kick(-vx * 0.0045 * (1 - d / 260));
      });
    }
    lx = e.clientX;
  });
  hero && hero.addEventListener('pointerleave', () => lx = null);

  // physics loop, paused when off screen
  const vis = new Set();
  const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? vis.add(e.target) : vis.delete(e.target)));
  all.forEach(p => io.observe(p.el.closest('section')));
  let last = performance.now();
  function loop(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    const t = now / 1000;
    all.forEach(p => {
      if (!vis.has(p.el.closest('section'))) return;
      const n = 4, h = dt / n;
      for (let k = 0; k < n; k++) p.step(h, t);
      p.render();
    });
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);

  if (!window.gsap || reduce) return;

  /* ---------------- smooth scroll ---------------- */
  gsap.registerPlugin(ScrollTrigger);
  let lenis = null;
  if (window.Lenis) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    lenis.on('scroll', e => {
      const v = Math.max(-40, Math.min(40, e.velocity || 0));
      const m = innerWidth < 760 ? 0.0012 : 0.0028;
      all.forEach(p => { if (!p.drag) p.kick(v * m * (p === pitPass ? 0.5 : 1)); });
    });
    gsap.ticker.add(time => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  } else {
    let ly = scrollY;
    addEventListener('scroll', () => { const v = scrollY - ly; ly = scrollY; all.forEach(p => p.kick(Math.max(-40, Math.min(40, v)) * 0.0028)); }, { passive: true });
  }

  /* ---------------- hero intro ---------------- */
  const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
  tl.from('.hero-h .ln > span', { yPercent: 115, duration: 1.1, stagger: .1 })
    .from('.hero-h .hl', { rotate: -14, scale: .7, duration: .9, ease: 'back.out(2.2)' }, .35)
    .from('.rig-hero .pass', { y: -420, duration: 1.1, stagger: .12, ease: 'power3.out' }, .15)
    .from('.hero-foot > *', { y: 26, opacity: 0, duration: .8, stagger: .08 }, .55)
    .from('.nav-pill', { y: -30, opacity: 0, duration: .8 }, .1);

  gsap.to('.hero-h', { yPercent: 18, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

  /* ---------------- reveals ---------------- */
  const rv = (sel, vars = {}) => $$(sel).forEach(el => gsap.from(el, Object.assign({
    y: 50, opacity: 0, duration: 1, ease: 'power3.out',
    scrollTrigger: { trigger: el, start: 'top 88%' }
  }, vars)));
  // CSS hover transitions on cards would fight GSAP, so park them during entrances
  const noT = els => () => els.forEach(el => { el.style.transition = 'none'; });
  const reT = els => () => els.forEach(el => { el.style.transition = ''; el.style.transform = ''; el.style.opacity = ''; });
  rv('.fe .sec-head h2');
  const catEls = $$('.cat');
  gsap.from(catEls, { y: 60, opacity: 0, rotate: (i) => (i % 2 ? 6 : -6), duration: .9, ease: 'back.out(1.6)', stagger: .06,
    onStart: noT(catEls), onComplete: reT(catEls),
    scrollTrigger: { trigger: '.cats', start: 'top 85%' } });
  rv('.sub-head');
  ScrollTrigger.batch('.fest', { start: 'top 90%', once: true,
    onEnter: b => gsap.from(b, { y: -60, rotate: (i) => (i % 2 ? 5 : -5), opacity: 0, duration: 1.2, ease: 'elastic.out(1, .6)', stagger: .08, transformOrigin: '50% 0', onStart: noT(b), onComplete: reT(b) }) });
  ScrollTrigger.batch('.ticket', { start: 'top 92%', once: true,
    onEnter: b => gsap.from(b, { x: (i) => (i % 2 ? 60 : -60), opacity: 0, duration: .9, ease: 'power3.out', stagger: .07, onStart: noT(b), onComplete: reT(b) }) });
  rv('.faq-side > *', { y: 30 });
  ScrollTrigger.batch('.qa', { start: 'top 92%', once: true,
    onEnter: b => gsap.from(b, { y: 30, opacity: 0, duration: .7, ease: 'power3.out', stagger: .05 }) });
  rv('.pit-copy > *', { y: 30 });

  gsap.fromTo('.pit-hand', { yPercent: 45, rotate: -10 }, { yPercent: 0, rotate: 4, ease: 'none',
    scrollTrigger: { trigger: '.pit', start: 'top 85%', end: 'center 45%', scrub: .8 } });
  gsap.fromTo('.pit-bg img', { scale: 1.18, yPercent: -6 }, { scale: 1, yPercent: 6, ease: 'none',
    scrollTrigger: { trigger: '.pit', start: 'top bottom', end: 'bottom top', scrub: true } });
  if (pitPass) ScrollTrigger.create({ trigger: '.pit', start: 'top 70%', once: true, onEnter: () => pitPass.kick(1.3) });

  gsap.from('.foot-mark img', { yPercent: 40, scale: .86, rotate: -3, ease: 'none',
    scrollTrigger: { trigger: '.foot', start: 'top bottom', end: 'bottom bottom', scrub: true } });

  addEventListener('load', () => ScrollTrigger.refresh());
})();
