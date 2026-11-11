/* FestHey v3 interactions */
(function () {
  const root = document.documentElement;
  const FIGMA = root.classList.contains('figma');
  const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const STATIC = FIGMA || REDUCE;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const rand = (a, b) => a + Math.random() * (b - a);

  /* ================= nav ================= */
  const nav = $('.nav'), menuBtn = $('.nav-menu');
  menuBtn && menuBtn.addEventListener('click', () => {
    const o = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', o);
  });

  /* ================= category filter ================= */
  const cats = $$('.cat');
  const items = $$('.fest');
  const LINE = { kick: () => {} };
  cats.forEach(b => b.addEventListener('click', () => {
    const k = b.dataset.cat;
    const hit = it => k === 'all' || it.dataset.cat.split(' ').includes(k);
    cats.forEach(x => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b); });
    items.forEach(it => it.classList.toggle('hide', !hit(it)));
    $$('.hang').forEach(f => f.classList.toggle('hide', !hit(f)));
    $$('.hang').forEach(h => h.classList.remove('is-last'));
    const hv = $$('.hang').filter(h => !h.classList.contains('hide')); hv.length && hv[hv.length - 1].classList.add('is-last');
    if (window.gsap && !STATIC) {
      const vis = items.filter(i => !i.classList.contains('hide'));
      vis.forEach(t => t.style.transition = 'none');
      gsap.fromTo(vis, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .6, ease: 'power3.out', stagger: .035,
        clearProps: 'transform,opacity,transition' });
      window.ScrollTrigger && ScrollTrigger.refresh();
    }
  }));

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
      this.arm.style.transform = `rotate(${this.a.toFixed(4)}rad)`;
      this.card.style.transform = `rotate(${this.r.toFixed(4)}rad)`;
      this.sheen && this.sheen.style.setProperty('--sx', `${((this.a + this.r) * 260).toFixed(1)}px`);
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
    const ps = Array.from({ length: 170 }, () => ({
      x, y, vx: rand(-9, 9), vy: rand(-17, -5), s: rand(6, 12), c: cols[Math.random() * cols.length | 0], a: rand(0, 6), va: rand(-.3, .3), life: 1
    }));
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
    const b = $('.btn-acc', form).getBoundingClientRect(), s = cv.getBoundingClientRect();
    confetti(b.left - s.left + b.width / 2, b.top - s.top);
    if (crowd) { crowd.classList.add('cheer'); setTimeout(() => crowd.classList.remove('cheer'), 2600); }
  });

  /* ================= the fest wheel ================= */
  const ADS = [
    { name: 'MSRIT Sports Meet', href: 'https://festhey.agpro.co.in/fests/msrit-sports-meet' },
    { name: 'Utsav Winter Edition', href: 'https://festhey.agpro.co.in/fests/utsav-winter-edition' },
    { name: 'Hack RVCE Winter', href: 'https://festhey.agpro.co.in/fests/hack-rvce-winter' },
  ];
  const wheel = $('#wheel');
  const W = { omega: 0, kick: () => {} };
  function initWheel() {
    if (!wheel) return;
    const rot = $('.wheel-rot', wheel), cabs = $$('.cab', wheel), N = cabs.length;
    let D = 0, R = 0, k = 1;
    const measure = () => {
      D = wheel.offsetWidth; R = D * .44; k = D / 920;
      wheel.style.setProperty('--k', k.toFixed(3));
      cabs.forEach(c => { c.w = c.offsetWidth; });
    };
    measure();
    wheel.classList.add('is-spun');
    const BASE = STATIC ? 0 : .12;
    let th = STATIC ? -.16 : -1.1, om = STATIC ? 0 : 2.2, prevOm = om;
    const sw = cabs.map(() => ({ p: 0, v: 0, seed: Math.random() * 10 }));
    function place() {
      rot.setAttribute('transform', `rotate(${(th * 180 / Math.PI).toFixed(3)})`);
      cabs.forEach((c, i) => {
        const a = th + i * 2 * Math.PI / N;
        const x = D / 2 + R * Math.sin(a), y = D / 2 - R * Math.cos(a);
        c.style.transform = `translate3d(${(x - c.w / 2).toFixed(1)}px,${y.toFixed(1)}px,0) rotate(${sw[i].p.toFixed(4)}rad)`;
      });
    }
    place();
    if (STATIC) return;

    // drag to spin (mouse), with inertia
    let drag = null, moved = 0;
    const ang = e => { const r = wheel.getBoundingClientRect(); return Math.atan2(e.clientX - r.left - D / 2, -(e.clientY - r.top - D / 2)); };
    wheel.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      e.preventDefault();
      drag = { a0: ang(e), th0: th, last: ang(e), t: performance.now(), x: e.clientX, y: e.clientY };
      moved = 0; wheel.classList.add('dragging');
    });
    addEventListener('pointermove', e => {
      if (!drag) return;
      moved = Math.max(moved, Math.hypot(e.clientX - drag.x, e.clientY - drag.y));
      let a = ang(e), d = a - drag.last;
      if (d > Math.PI) d -= 2 * Math.PI; if (d < -Math.PI) d += 2 * Math.PI;
      const now = performance.now(), dt = Math.max(8, now - drag.t) / 1000;
      th += d; om = om * .5 + (d / dt) * .5; drag.last = a; drag.t = now;
    });
    const end = () => { if (drag) { drag = null; wheel.classList.remove('dragging'); om = clamp(om, -6, 6); } };
    addEventListener('pointerup', end); addEventListener('pointercancel', end);
    wheel.addEventListener('click', e => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } moved = 0; }, true);
    W.kick = v => { om = clamp(om + v, -4, 4); };

    let vis = true;
    new IntersectionObserver(es => es.forEach(en => vis = en.isIntersecting)).observe(wheel);
    let last = performance.now();
    (function loop(now) {
      const dt = Math.min(.05, (now - last) / 1000); last = now;
      if (vis) {
        if (!drag) { om += (BASE - om) * Math.min(1, dt * .8); th += om * dt; }
        const alpha = (om - prevOm) / Math.max(dt, .001); prevOm = om;
        const t = now / 1000;
        sw.forEach(s => {
          const acc = -18 * Math.sin(s.p) - 2.6 * s.v - clamp(alpha, -30, 30) * .05 - om * om * 0 + .25 * Math.sin(t * 1.3 + s.seed);
          s.v += acc * dt; s.p = clamp(s.p + s.v * dt, -.5, .5);
        });
        place();
      }
      requestAnimationFrame(loop);
    })(last);
    let rt;
    addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(measure, 150); });
  }

  // featured fest: the chip cycles the three ads and their cabin lights up
  const featName = $('.feat-name'), feat = $('.feat'), cta = $('.btn-or');
  const adCabs = $$('.cab.is-ad');
  let featI = 0;
  function feature(i) {
    featI = i;
    featName.classList.add('swap');
    setTimeout(() => { featName.textContent = ADS[i].name; featName.classList.remove('swap'); }, 230);
    feat.href = cta.href = ADS[i].href;
    adCabs.forEach((c, j) => c.classList.toggle('is-feat', j === i));
  }
  adCabs.length && adCabs[0].classList.add('is-feat');

  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => requestAnimationFrame(() => {
    initWheel();
    if (!STATIC) setInterval(() => feature((featI + 1) % ADS.length), 5000);
  }));

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
    if (y < (wheel ? wheel.offsetHeight : 0) + 200) W.kick(clamp(v, -40, 40) * .006);
    if (pass) pass.kick(clamp(v, -30, 30) * .0012);
    LINE.kick(clamp(v, -30, 30) * .25);
  };
  if (window.Lenis) {
    const lenis = new Lenis({ lerp: .1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    lenis.on('scroll', e => onScroll(e.scroll, e.velocity || 0));
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    $$('a[href="#top"]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); lenis.scrollTo(0, { duration: 1.6 }); }));
  } else {
    let ly = scrollY;
    addEventListener('scroll', () => { const v = scrollY - ly; ly = scrollY; onScroll(scrollY, v); }, { passive: true });
  }

  /* ================= hero intro ================= */
  gsap.timeline({ defaults: { ease: 'power4.out' } })
    .from('.nav-pill', { y: -30, opacity: 0, duration: .8 }, 0)
    .from('.feat', { y: 20, opacity: 0, duration: .7 }, .1)
    .from('.hero-h .w', { yPercent: 110, duration: 1.05, stagger: .08 }, .12)
    .from('.hero-h .hl', { scale: .6, rotate: -14, duration: .9, ease: 'back.out(2)' }, .45)
    .from('.hero-p, .hero-cta', { y: 24, opacity: 0, duration: .8, stagger: .08 }, .55)
    .from('.sun', { scale: .4, opacity: 0, duration: 1.4, ease: 'expo.out' }, .1)
    .from('.sun-ring', { scale: .4, opacity: 0, duration: 1.6, ease: 'expo.out' }, .2)
    .from('.wheel-svg, .wheel-legs, .hub', { y: 120, opacity: 0, duration: 1.3, ease: 'expo.out' }, .25)
    .from('.cab', { opacity: 0, duration: .8, stagger: .05, ease: 'power2.out' }, .5);

  /* ================= reveals ================= */
  const park = els => () => els.forEach(el => el.style.transition = 'none');
  const unpark = els => () => els.forEach(el => { el.style.transition = ''; el.style.transform = ''; el.style.opacity = ''; });
  const rv = (sel, vars = {}) => $$(sel).forEach(el => gsap.from(el, Object.assign({
    y: 46, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } }, vars)));

  rv('.fe-head h2');
  gsap.from(cats, { y: 20, opacity: 0, duration: .7, ease: 'power3.out', stagger: .04, onStart: park(cats), onComplete: unpark(cats),
    scrollTrigger: { trigger: '.cats', start: 'top 90%' } });
  rv('.sub-head');
  ScrollTrigger.batch('.fest', { start: 'top 90%', once: true, onEnter: b => gsap.from(b, {
    y: -70, rotate: i => (i % 2 ? 6 : -6), opacity: 0, duration: 1.3, ease: 'elastic.out(1,.6)', stagger: .08,
    transformOrigin: '50% 0', onStart: park(b), onComplete: unpark(b) }) });

  /* ================= events: the clothesline ================= */
  const track = $('.line-track');
  if (track) {
    const hangs = $$('.hang', track);
    const S = hangs.map(h => ({ el: $('.pol', h), rest: parseFloat(h.style.getPropertyValue('--tilt')) || 0, p: 0, v: 0, sc: 1, hov: false, seed: Math.random() * 10 }));
    S.forEach(s => {
      s.p = s.rest;
      s.el.addEventListener('pointerenter', () => { s.hov = true; s.v += 30; });
      s.el.addEventListener('pointerleave', () => { s.hov = false; });
    });
    // mouse drag scrolls the line with a little inertia; touch keeps native swipe
    let drag = null, moved = 0, vel = 0, lastX = track.scrollLeft, push = 0;
    track.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      drag = { x: e.clientX, sl: track.scrollLeft, t: performance.now(), lx: e.clientX }; moved = 0; vel = 0;
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
    const step = () => (hangs.find(h => !h.classList.contains('hide')) || hangs[0]).offsetWidth;
    $('.ev-next').addEventListener('click', () => track.scrollBy({ left: step() * 2, behavior: 'smooth' }));
    $('.ev-prev').addEventListener('click', () => track.scrollBy({ left: -step() * 2, behavior: 'smooth' }));
    LINE.kick = v => S.forEach(s => { s.v += v * (0.6 + Math.random() * .8); });
    // the polaroids swing from their pegs as the line moves
    let vis = false;
    new IntersectionObserver(es => es.forEach(en => vis = en.isIntersecting)).observe(track);
    let last = performance.now();
    (function loop(now) {
      const dt = Math.min(.05, (now - last) / 1000); last = now;
      if (vis) {
        if (!drag && Math.abs(push) > .2) { track.scrollLeft += push; push *= .92; }
        const sv = track.scrollLeft - lastX; lastX = track.scrollLeft;
        const t = now / 1000;
        S.forEach(s => {
          const target = s.hov ? 0 : s.rest;
          const acc = -40 * (s.p - target) - 5 * s.v + clamp(sv, -40, 40) * 4.2 + 1.4 * Math.sin(t * 1.1 + s.seed);
          s.v += acc * dt; s.p = clamp(s.p + s.v * dt, -16, 16);
          s.sc += ((s.hov ? 1.04 : 1) - s.sc) * Math.min(1, dt * 10);
          s.el.style.transform = 'rotate(' + s.p.toFixed(2) + 'deg) scale(' + s.sc.toFixed(3) + ')';
        });
      }
      requestAnimationFrame(loop);
    })(last);
    gsap.from('.hang', { y: -60, opacity: 0, duration: 1, ease: 'power3.out', stagger: .07, scrollTrigger: { trigger: '.events', start: 'top 70%' } });
    gsap.from('.cord svg', { scaleY: 0, transformOrigin: '50% 0', duration: 1, ease: 'elastic.out(1,.5)', scrollTrigger: { trigger: '.events', start: 'top 75%' } });
  }

  rv('.faq-head > *', { y: 30 });
  ScrollTrigger.batch('.qa', { start: 'top 94%', once: true, onEnter: b => gsap.from(b, { y: 24, opacity: 0, duration: .7, ease: 'power3.out', stagger: .05 }) });
  gsap.from('.phone-wrap', { y: 220, rotate: 6, duration: 1.4, ease: 'power3.out', scrollTrigger: { trigger: '.faq', start: 'top 65%' } });
  rv('.pit-copy > *', { y: 30 });
  gsap.from('.crowd', { yPercent: 40, ease: 'none', scrollTrigger: { trigger: '.pit', start: 'top bottom', end: 'center center', scrub: .6 } });
  if (pass) ScrollTrigger.create({ trigger: '.pit', start: 'top 70%', once: true, onEnter: () => pass.kick(1.4) });
  gsap.from('.mural', { y: 80, scale: .92, opacity: 0, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: '.foot', start: 'top 75%' } });
  ScrollTrigger.batch('.poster', { start: 'top 92%', once: true, onEnter: b => gsap.from(b, {
    scale: 1.25, opacity: 0, rotate: i => (i % 2 ? 12 : -12), duration: .7, ease: 'back.out(1.6)', stagger: .12,
    onStart: park(b), onComplete: unpark(b) }) });

  addEventListener('load', () => ScrollTrigger.refresh());
})();
