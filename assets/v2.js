/* FestHey v2 interactions */
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

  /* ================= wristband filter ================= */
  const bandsEl = $('.bands'), bands = $$('.band');
  const items = $$('.fest, .ev');
  bands.forEach(b => b.addEventListener('click', () => {
    const k = b.dataset.cat;
    bands.forEach(x => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b); });
    bandsEl.classList.toggle('picked', k !== 'all');
    items.forEach(it => it.classList.toggle('hide', !(k === 'all' || it.dataset.cat.split(' ').includes(k))));
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
    setTimeout(() => chat.appendChild(typing), 260);
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
      x, y, vx: rand(-9, 9), vy: rand(-17, -5), s: rand(6, 12), c: cols[Math.random() * cols.length | 0],
      a: rand(0, 6), va: rand(-.3, .3), life: 1
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

  /* ================= neon sign ================= */
  const foot = $('.foot'), sign = $('.sign'), sw = $('.switch');
  function setNeon(on) {
    sign.classList.toggle('on', on); foot.classList.toggle('lit', on);
    sw.classList.toggle('is-on', on); sw.setAttribute('aria-pressed', on);
  }
  if (sign) {
    if (STATIC) setNeon(true);
    else {
      setNeon(false);
      const io = new IntersectionObserver(es => es.forEach(en => {
        if (en.isIntersecting) { setTimeout(() => setNeon(true), 250); io.disconnect(); }
      }), { threshold: .3 });
      io.observe(sign);
      sw.addEventListener('click', () => setNeon(!sign.classList.contains('on')));
      let bt;
      sign.addEventListener('pointerenter', () => {
        if (!sign.classList.contains('on')) return;
        sign.classList.remove('buzz'); void sign.offsetWidth; sign.classList.add('buzz');
        clearTimeout(bt); bt = setTimeout(() => sign.classList.remove('buzz'), 600);
      });
    }
  }

  /* ================= featured fest cycle ================= */
  const ADS = [
    { name: 'MSRIT Sports Meet', href: 'https://festhey.agpro.co.in/fests/msrit-sports-meet' },
    { name: 'Utsav Winter Edition', href: 'https://festhey.agpro.co.in/fests/utsav-winter-edition' },
    { name: 'Hack RVCE Winter', href: 'https://festhey.agpro.co.in/fests/hack-rvce-winter' },
  ];
  const featName = $('.feat-name'), feat = $('.feat'), cta = $('.btn-or');
  const tickets = $$('.tk');
  let featI = 0, onFeature = null;
  function feature(i) {
    featI = i;
    featName.classList.add('swap');
    setTimeout(() => { featName.textContent = ADS[i].name; featName.classList.remove('swap'); }, 230);
    feat.href = cta.href = ADS[i].href;
    tickets.forEach(t => t.classList.toggle('is-feat', +t.dataset.fest === i));
    onFeature && onFeature(i);
  }

  /* ================= physics merch drop ================= */
  const hero = $('.hero'), pile = $('#pile');
  const P = { bodies: [], kickAll: () => {} };

  function initPile() {
    if (!window.Matter || !pile) return;
    const { Engine, Bodies, Body, Composite, Constraint, Query, Vector } = Matter;
    const els = $$('.obj', pile).filter(el => getComputedStyle(el).display !== 'none');
    const engine = Engine.create({ gravity: { y: 1.2 }, positionIterations: 8, velocityIterations: 6 });
    const world = engine.world;
    let W = hero.clientWidth, H = hero.clientHeight;
    const S = () => (W < 700 ? .56 : W < 1100 ? .76 : clamp(W / 1440, .86, 1.12));
    let scale = S();
    let statics = [];

    // layout boxes via offsets, so intro transforms on the headline don't skew them
    const box = el => { let x = 0, y = 0, n = el; while (n && n !== hero) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; } return { x, y, w: el.offsetWidth, h: el.offsetHeight }; };
    // wide screens: things land on the headline. Narrow: a drop zone under the button.
    let dropMode = false, shelfY = 0;
    function buildStatics() {
      if (statics.length) Composite.remove(world, statics);
      statics = [];
      W = hero.clientWidth; H = hero.clientHeight;
      const lines = $$('.hero-h .w').map(box);
      const gutter = Math.min(...lines.map(l => l.x), ...lines.map(l => W - l.x - l.w));
      dropMode = gutter < 150;
      const o = { isStatic: true, friction: .7, restitution: .15 };
      const floor = W < 700 ? 40 : 52;
      statics.push(Bodies.rectangle(W / 2, H - floor + 60, W * 3, 120, o));
      statics.push(Bodies.rectangle(-60, H / 2 - 800, 120, H * 2 + 1600, o));
      statics.push(Bodies.rectangle(W + 60, H / 2 - 800, 120, H * 2 + 1600, o));
      if (dropMode) {
        const c = box($('.hero-foot'));
        shelfY = c.y + c.h + 14;
        statics.push(Bodies.rectangle(W / 2, shelfY - 30, W * 3, 60, o));
      } else {
        $$('.hero-h .w, .hero-p, .btn-or, .feat').forEach(el => {
          const r = box(el);
          if (!r.w) return;
          let h = r.h, y = r.y + r.h / 2;
          if (el.classList.contains('w') && !el.classList.contains('hl')) { h = r.h * .72; y += r.h * .08; }
          const b = Bodies.rectangle(r.x + r.w / 2, y, r.w, h, Object.assign({ chamfer: { radius: Math.min(14, h / 3) } }, o));
          if (el.classList.contains('hl')) Body.setAngle(b, -2 * Math.PI / 180);
          statics.push(b);
        });
      }
      Composite.add(world, statics);
    }
    buildStatics();

    pile.classList.add('live');
    const order = els.map((el, i) => ({ el, i, k: Math.random() })).sort((a, b) => a.k - b.k);
    const bodies = [];
    const byEl = new Map();
    order.forEach(({ el }, n) => {
      const bw = +el.dataset.bw * scale, bh = +el.dataset.bh * scale;
      // wide: mostly into the gutters beside the headline, a few onto it. narrow: pop in under the button
      const side = Math.random() < .5 ? 0 : 1, gut = .27;
      const x = dropMode ? rand(W * .14, W * .86)
        : Math.random() < .78 ? (side ? rand(W * (1 - gut), W * .95) : rand(W * .05, W * gut)) : rand(W * .3, W * .7);
      const y = dropMode ? shelfY + 70 : -180 - n * (STATIC ? 140 : 95);
      const opts = { restitution: .32, friction: .5, frictionAir: .014, density: .0018 };
      const b = el.dataset.shape === 'circle' ? Bodies.circle(x, y, bw / 2, opts)
        : Bodies.rectangle(x, y, bw, bh, Object.assign({ chamfer: { radius: Math.min(bw, bh) * .16 } }, opts));
      Body.setAngle(b, rand(-.7, .7));
      Body.setAngularVelocity(b, rand(-.06, .06));
      b.el = el; b.w = el.offsetWidth; b.h = el.offsetHeight; b.pop = dropMode ? 0 : 1;
      bodies.push(b); byEl.set(el, b);
      el.classList.add('pending');
    });
    P.bodies = bodies;

    function render() {
      for (const b of bodies) {
        const { x, y } = b.position;
        if (y > -60 && b.added) b.el.classList.remove('pending');
        if (b.added && b.pop < 1) b.pop = Math.min(1, b.pop + .06);
        const k = b.pop < 1 ? 1 + 2.7 * Math.pow(b.pop - 1, 3) + 1.7 * Math.pow(b.pop - 1, 2) : 1;
        b.el.style.transform = `translate3d(${(x - b.w / 2).toFixed(1)}px,${(y - b.h / 2).toFixed(1)}px,0) rotate(${b.angle.toFixed(4)}rad) scale(${(scale * k).toFixed(3)})`;
      }
    }

    if (STATIC) {
      bodies.forEach(b => {
        b.added = true; b.pop = 1; Composite.add(world, b);
        for (let i = 0; i < (dropMode ? 50 : 6); i++) Engine.update(engine, 1000 / 60);
      });
      for (let i = 0; i < 1400; i++) Engine.update(engine, 1000 / 60);
      render();
      return;
    }

    // drop them in one by one
    bodies.forEach((b, n) => setTimeout(() => { b.added = true; Composite.add(world, b); }, (dropMode ? 900 : 500) + n * (dropMode ? 160 : 85)));

    // mouse drag + throw; touch tap = bounce
    let drag = null, lastMoved = 0;
    const local = e => { const r = hero.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };
    pile.addEventListener('pointerdown', e => {
      const el = e.target.closest('.obj'); if (!el) return;
      const b = byEl.get(el); if (!b) return;
      const p = local(e);
      if (e.pointerType === 'mouse') {
        e.preventDefault();
        const c = Constraint.create({ pointA: p, bodyB: b, pointB: Vector.sub(p, b.position), stiffness: .18, damping: .12, length: 0 });
        c.angleB = b.angle;
        Composite.add(world, c);
        drag = { b, c, sx: e.clientX, sy: e.clientY, moved: 0 };
        el.style.zIndex = 20;
      } else {
        drag = { touch: true, b, sx: e.clientX, sy: e.clientY, moved: 0 };
      }
    });
    addEventListener('pointermove', e => {
      if (drag) {
        drag.moved = Math.max(drag.moved, Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy));
        if (drag.c) drag.c.pointA = local(e);
      }
    });
    const end = () => {
      if (!drag) return;
      lastMoved = drag.moved;
      if (drag.c) { Composite.remove(world, drag.c); drag.b.el.style.zIndex = ''; }
      else if (drag.moved < 10 && drag.b.el.tagName !== 'A') {
        Body.setVelocity(drag.b, { x: rand(-5, 5), y: -rand(13, 18) });
        Body.setAngularVelocity(drag.b, rand(-.25, .25));
      }
      drag = null;
    };
    addEventListener('pointerup', end); addEventListener('pointercancel', end);
    pile.addEventListener('click', e => { if (lastMoved > 6 && e.target.closest('a')) e.preventDefault(); lastMoved = 0; }, true);

    // cursor brushing nudges things
    let lp = null;
    hero.addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse' || drag) { lp = null; return; }
      const p = local(e);
      if (lp) {
        const v = Vector.sub(p, lp), sp = Vector.magnitude(v);
        if (sp > 4) Query.point(bodies, p).forEach(b => Body.setVelocity(b, Vector.add(b.velocity, Vector.mult(v, .16))));
      }
      lp = p;
    });
    hero.addEventListener('pointerleave', () => lp = null);

    P.kickAll = (amt) => {
      bodies.forEach(b => {
        if (Math.random() < .55 && b.position.y > H * .3) {
          Body.setVelocity(b, { x: b.velocity.x + rand(-2, 2), y: -amt * rand(.6, 1.1) * (dropMode ? .55 : 1) });
          Body.setAngularVelocity(b, rand(-.12, .12));
        }
      });
    };
    onFeature = i => {
      const t = bodies.find(b => +b.el.dataset.fest === i);
      if (t) { Body.setVelocity(t, { x: rand(-3, 3), y: -15 }); Body.setAngularVelocity(t, rand(-.15, .15)); }
    };

    // loop, paused off screen
    let visible = true;
    new IntersectionObserver(es => es.forEach(en => visible = en.isIntersecting)).observe(hero);
    let acc = 0, last = performance.now();
    (function loop(now) {
      const dt = Math.min(64, now - last); last = now;
      if (visible) {
        acc += dt;
        while (acc >= 1000 / 60) { Engine.update(engine, 1000 / 60); acc -= 1000 / 60; }
        for (const b of bodies) if (b.position.y > H + 400 || b.position.x < -200 || b.position.x > W + 200) {
          Body.setPosition(b, { x: rand(W * .15, W * .85), y: dropMode ? shelfY + 70 : -200 }); Body.setVelocity(b, { x: 0, y: 0 });
        }
        render();
      }
      requestAnimationFrame(loop);
    })(last);

    let rt;
    addEventListener('resize', () => {
      clearTimeout(rt);
      rt = setTimeout(() => {
        const ns = S();
        buildStatics();
        if (ns !== scale) {
          bodies.forEach(b => Body.scale(b, ns / scale, ns / scale));
          scale = ns;
        }
        bodies.forEach(b => Body.setPosition(b, { x: clamp(b.position.x, 60, W - 60), y: dropMode ? clamp(b.position.y, shelfY + 40, H - 80) : Math.min(b.position.y, H - 80) }));
      }, 200);
    });
  }

  const start = () => {
    initPile();
    if (!STATIC) setInterval(() => feature((featI + 1) % ADS.length), 4600);
    else tickets.forEach(t => t.classList.toggle('is-feat', +t.dataset.fest === 0));
  };
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => requestAnimationFrame(start));

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

  /* ================= events peek ================= */
  const lineup = $('.lineup'), peek = $('.peek'), peekImg = peek && $('img', peek), fe = $('.fe');
  if (lineup && peek && matchMedia('(hover: hover)').matches) {
    $$('.ev', lineup).forEach(r => { const i = new Image(); i.src = r.dataset.img; });
    let px = 0, py = 0, tx = 0, ty = 0, rot = 0, on = false;
    lineup.addEventListener('pointermove', e => {
      const r = fe.getBoundingClientRect();
      // keep the photo in the open space between the event name and the price
      const pr = $('.ev-price', lineup).getBoundingClientRect(), mr = $('.ev-main', lineup).getBoundingClientRect();
      tx = clamp(e.clientX - r.left + 36, mr.left - r.left + 300, pr.left - r.left - 290);
      ty = e.clientY - r.top - 155;
      const row = e.target.closest('.ev');
      if (row && peekImg.getAttribute('src') !== row.dataset.img) peekImg.src = row.dataset.img;
      if (!on) { px = tx; py = ty; on = true; peek.classList.add('show'); }
    });
    lineup.addEventListener('pointerleave', () => { on = false; peek.classList.remove('show'); });
    (function loop() {
      const vx = tx - px;
      px += (tx - px) * .16; py += (ty - py) * .16;
      rot += (clamp(vx * .12, -12, 12) - rot) * .12;
      peek.style.transform = `translate3d(${px.toFixed(1)}px,${py.toFixed(1)}px,0) rotate(${rot.toFixed(2)}deg)`;
      requestAnimationFrame(loop);
    })();
  }

  if (!window.gsap) return;
  gsap.registerPlugin(ScrollTrigger);

  /* ================= smooth scroll ================= */
  let lenis = null, lastKick = 0, lastY = 0;
  const onScroll = (y, v) => {
    if (y > 40 && y > lastY) nav.classList.add('hide'); else nav.classList.remove('hide');
    lastY = y;
    const now = performance.now();
    if (Math.abs(v) > 6 && now - lastKick > 260 && y < hero.offsetHeight) { lastKick = now; P.kickAll(clamp(Math.abs(v) * .5, 4, 13)); }
    if (pass) pass.kick(clamp(v, -30, 30) * .0012);
  };
  if (window.Lenis) {
    lenis = new Lenis({ lerp: .1, smoothWheel: true });
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
    .from('.hero-h .w', { yPercent: 110, duration: 1.05, stagger: .09 }, .12)
    .from('.hero-h .hl', { scale: .6, rotate: -14, duration: .9, ease: 'back.out(2)' }, .4)
    .from('.hero-foot > *', { y: 24, opacity: 0, duration: .8, stagger: .08 }, .5);

  /* ================= reveals ================= */
  const park = els => () => els.forEach(el => el.style.transition = 'none');
  const unpark = els => () => els.forEach(el => { el.style.transition = ''; el.style.transform = ''; el.style.opacity = ''; });
  const rv = (sel, vars = {}) => $$(sel).forEach(el => gsap.from(el, Object.assign({
    y: 46, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } }, vars)));

  rv('.fe-head h2');
  gsap.from(bands, { y: -40, opacity: 0, rotate: i => (i % 2 ? 14 : -14), duration: 1, ease: 'elastic.out(1,.55)', stagger: .06,
    onStart: park(bands), onComplete: unpark(bands), scrollTrigger: { trigger: '.bands', start: 'top 88%' } });
  rv('.sub-head');
  ScrollTrigger.batch('.fest', { start: 'top 90%', once: true, onEnter: b => gsap.from(b, {
    y: -70, rotate: i => (i % 2 ? 6 : -6), opacity: 0, duration: 1.3, ease: 'elastic.out(1,.6)', stagger: .08,
    transformOrigin: '50% 0', onStart: park(b), onComplete: unpark(b) }) });
  ScrollTrigger.batch('.ev', { start: 'top 94%', once: true, onEnter: b => gsap.from(b, {
    y: 30, opacity: 0, duration: .8, ease: 'power3.out', stagger: .06, onStart: park(b), onComplete: unpark(b) }) });
  rv('.faq-side > :not(.faq-list)', { y: 30 });
  ScrollTrigger.batch('.qa', { start: 'top 94%', once: true, onEnter: b => gsap.from(b, { y: 24, opacity: 0, duration: .7, ease: 'power3.out', stagger: .05 }) });
  gsap.from('.phone-wrap', { y: 160, rotate: 8, opacity: 0, duration: 1.3, ease: 'power3.out', scrollTrigger: { trigger: '.faq', start: 'top 70%' } });
  rv('.pit-copy > *', { y: 30 });
  gsap.from('.crowd', { yPercent: 40, ease: 'none', scrollTrigger: { trigger: '.pit', start: 'top bottom', end: 'center center', scrub: .6 } });
  if (pass) ScrollTrigger.create({ trigger: '.pit', start: 'top 70%', once: true, onEnter: () => pass.kick(1.4) });
  ScrollTrigger.batch('.poster', { start: 'top 92%', once: true, onEnter: b => gsap.from(b, {
    scale: 1.25, opacity: 0, rotate: i => (i % 2 ? 12 : -12), duration: .7, ease: 'back.out(1.6)', stagger: .12,
    onStart: park(b), onComplete: unpark(b) }) });

  addEventListener('load', () => ScrollTrigger.refresh());
})();
