#!/usr/bin/env python3
"""FestHey v2: builds index.html as static markup (Figma-import safe). Run: python3 assets/src/build.py"""
import html, json, re, os

ROOT = '/Users/durgesh/Desktop/WFT/festhey'
OUT = f'{ROOT}/index.html'
BASE = 'https://festhey.agpro.co.in'
META = json.load(open(f'{ROOT}/assets/img/v2/meta.json'))
e = html.escape

I = {
 'arrow': '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
 'up': '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
 'lock': '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 'msg': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 'menu': '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
 'insta': '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
 'linkedin': '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
 'youtube': '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
 'send': '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
}
def ic(n, c='ic'):
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{I[n]}</svg>'

STAR = '<svg class="star" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0l2.6 8.2L23 6.5l-6.3 5.5L23 17.5l-8.4-1.7L12 24l-2.6-8.2L1 17.5l6.3-5.5L1 6.5l8.4 1.7z"/></svg>'
AV = ''.join(f'<img src="assets/img/av{i}.jpg" alt="" width="40" height="40">' for i in range(1, 5))

# ---------------- data (client copy, word for word) ----------------
ADS = [
  dict(tag='Football, Basketball and More', name='MSRIT Sports Meet', col='M S Ramaiah Institute of Technology', href='/fests/msrit-sports-meet', tone='snow'),
  dict(tag='Three Nights of Music and Dance at BMSCE', name='Utsav Winter Edition', col='B M S College of Engineering', href='/fests/utsav-winter-edition', tone='sun'),
  dict(tag='Overnight Builds, ₹75K in Prizes', name='Hack RVCE Winter', col='R V College of Engineering', href='/fests/hack-rvce-winter', tone='orange'),
]
# prop: (file, desktop width, shape, fallback left %, mobile)
PROPS = [
  ('sunglasses', 186, 'rect', 6, 1), ('vinyl', 176, 'circle', 15, 1), ('camera', 168, 'rect', 78, 1),
  ('foamfinger', 118, 'rect', 90, 1), ('megaphone', 176, 'rect', 62, 0), ('buckethat', 168, 'rect', 30, 0),
  ('cassette', 172, 'rect', 46, 1), ('can', 158, 'rect', 70, 0), ('wristband', 146, 'circle', 22, 1),
  ('bolt', 70, 'rect', 38, 1),
]
POLAROIDS = [('fest-cultural', 'snow', 12), ('fest-sports', 'snow', 84)]

CATS = [('all', 'All Categories'), ('cultural', 'Cultural'), ('technical', 'Technical'), ('sports', 'Sports'),
        ('quiz', 'Quiz'), ('hackathon', 'Hackathon'), ('other', 'Other')]

FESTS = [
  ('8th Mile Encore', 'Dec 5', 'Dec 6', '7+', '0', 'fest-cultural', '8th-mile-encore', 'cultural', 'snow'),
  ('BMSCE Esports Showdown', 'Dec 12', 'Dec 13', '5+', '0', 'event-esports', 'bmsce-esports-showdown', 'other', 'sun'),
  ('Brain Wars', 'Dec 30', 'Dec 31', '5+', '0', 'gallery-stage', 'brain-wars', 'quiz', 'snow'),
  ('Christ Code Sprint', 'Dec 17', 'Dec 18', '5+', '0', 'event-hackathon', 'christ-code-sprint', 'hackathon', 'orange'),
  ('Christ Inter-College Athletics', 'Nov 20', 'Nov 22', '7+', '0', 'fest-sports', 'christ-inter-college-athletics', 'sports', 'orange'),
  ('Christ Lit Fest', 'Nov 13', 'Nov 14', '5+', '0', 'blog-fest-season', 'christ-lit-fest', 'cultural', 'snow'),
  ('Hack RVCE Winter', 'Nov 14', 'Nov 15', '7+', '0', 'ad-event-hackathon', 'hack-rvce-winter', 'hackathon technical', 'sun'),
  ('Hack-a-Thon BMS', 'Dec 26', 'Dec 27', '5+', '1', 'fest-technical', 'hack-a-thon-bms', 'hackathon technical', 'snow'),
]

EVENTS = [
  ('Brain Wars', 'Line Follower Sprint', '30', 'Main Grounds, MSRIT', '₹349.00', 'line-follower-sprint-ymdlgs', 'technical', 'event-robotics-demo'),
  ('Brain Wars', 'Slam Poetry', '31', 'Electronics Lab, MSRIT', '₹0', 'slam-poetry-xyhzfg', 'cultural', 'blog-fest-season-crowd'),
  ('Brain Wars', 'Science & Tech Quiz', '30', 'ESB Seminar Hall, MSRIT', '₹0', 'science-tech-quiz-phiblg', 'quiz', 'gallery-hands'),
  ('Brain Wars', 'General Quiz', '31', 'Main Grounds, MSRIT', '₹199.00', 'general-quiz-hhbpkh', 'quiz', 'gallery-stage'),
  ('Brain Wars', 'India Quiz', '30', 'Electronics Lab, MSRIT', '₹0', 'india-quiz-ww8o81', 'quiz', 'fest-cultural'),
  ('Hack-a-Thon BMS', 'Pop Culture Quiz', '26', 'PJA Auditorium, BMSCE', '₹199.00', 'pop-culture-quiz-67epp3', 'quiz', 'ad-fest-music'),
  ('Hack-a-Thon BMS', 'IoT Build-off', '27', 'Mechanical Seminar Hall, BMSCE', '₹0', 'iot-build-off-fvihvz', 'technical', 'event-robotics'),
  ('Hack-a-Thon BMS', 'Line Follower Sprint', '26', 'Football Ground, BMSCE', '₹349.00', 'line-follower-sprint', 'technical', 'fest-technical'),
]

FAQ = [
 ('What is FestHey?', '<p>FestHey is India\'s leading campus fest management platform that connects students with college festivals, events, and competitions across the country.</p>'),
 ('How do I register for a fest?', '<p>Open the fest, pick any event inside it, and hit Register. Solo events confirm instantly. Team events let you invite teammates by link before you check out.</p>'),
 ('Is there any registration fee?', '<p>It depends on the event - many are completely free. Where there is a fee, both the amount and the convenience fee are shown before you pay, so there are no surprises at checkout.</p>'),
 ('Can I participate in multiple events?', '<p>Yes. You can register for as many events as you like, including several within the same fest, as long as their schedules do not clash.</p>'),
 ('How will I get updates about events?', '<p>Confirmations and reminders go to your registered email. Your dashboard also tracks every registration with its current status.</p>'),
 ('What if I face an issue during registration?', '<p>Check these first:</p><ul><li>Your payment went through - see the Payments tab.</li><li>The registration deadline has not passed.</li><li>Your team has enough members to check out.</li></ul><p>Still stuck? Contact the organiser directly from the event page.</p>'),
 ('Can I get a refund if I cancel my registration?', '<p>Refund policy is set by the organising college, not by FestHey. Check the event terms, then contact the organiser to request a cancellation.</p>'),
 ('How can I contact the support team?', '<p>Use the Contact Us button on this page, or reach the organiser from any event. We usually reply within one working day.</p>'),
]

# crowd hands in the pit: (hand file index, left %, height px, delay s, flip, back row)
CROWD = [(1,-2,430,0,0,1),(6,6,380,.25,1,1),(3,13,470,.1,0,0),(8,22,400,.35,0,1),(5,30,460,.05,0,0),(2,39,390,.3,1,1),
         (7,46,450,.15,0,0),(4,54,420,.4,1,1),(1,61,470,.2,1,0),(6,69,390,.05,0,1),(3,76,440,.3,1,0),(8,84,400,.1,1,1),
         (5,90,460,.35,1,0),(2,97,410,.2,0,1)]

# ---------------- builders ----------------
def prop(p, i):
    name, w, shape, left, mob = p
    m = META[name]; k = w / m['w']; pad = m['pad']
    W = round((m['w'] + 2 * pad) * k); H = round((m['h'] + 2 * pad) * k)
    bw = round(m['w'] * k); bh = round(m['h'] * k)
    return (f'<div class="obj obj-prop{"" if mob else " d-only"}" data-shape="{shape}" data-bw="{bw}" data-bh="{bh}" '
            f'style="width:{W}px;height:{H}px;left:{left}%;"><img src="assets/img/v2/p-{name}.png" alt="" width="{W}" height="{H}" draggable="false"></div>')

def ticket(a, i):
    return f'''<a class="obj tk tk--{a['tone']}" href="{BASE}{a['href']}" data-shape="rect" data-bw="272" data-bh="124" data-fest="{i}" style="left:{[34,48,64][i]}%" draggable="false">
          <span class="tk-main"><span class="tk-tag">{e(a['tag'])}</span><span class="tk-name">{e(a['name'])}</span><span class="tk-col">{e(a['col'])}</span></span>
          <span class="tk-stub"><span class="nt nt-a"></span><span class="nt nt-b"></span><span class="tk-ad">AD</span><img src="assets/img/barcode.svg" alt="" width="60" height="16"></span>
        </a>'''

def polaroid(p, i):
    img, tone, left = p
    return f'''<div class="obj pol{" d-only" if i == 1 else ""}" data-shape="rect" data-bw="150" data-bh="180" style="left:{left}%"><img class="pol-ph" src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720" draggable="false"><img class="pol-tape" src="assets/img/v2/tape{i+1}.png" alt="" draggable="false"></div>'''

STICKER = f'''<div class="obj stk" data-shape="circle" data-bw="164" data-bh="164" style="left:72%">
          <img class="stk-bg" src="assets/img/flower.svg" alt="" width="164" height="164" draggable="false">
          <span class="stk-in"><span class="avs avs-s">{AV}</span><span class="stk-t">Joined by</span><b>2000+ Students</b></span>
        </div>'''

def band(c):
    k, label = c
    on = ' is-on' if k == 'all' else ''
    return (f'<button class="band band--{k}{on}" data-cat="{k}" aria-pressed="{"true" if on else "false"}">'
            f'<span class="band-bead"></span><span class="band-body" style="background-image:url(assets/img/v2/band-{k}.png)">{label}</span>'
            f'<span class="band-tail" style="background-image:url(assets/img/v2/band-{k}.png)"></span></button>')

def fest(f):
    name, d1, d2, evs, att, img, slug, cat, tone = f
    return f'''
        <a class="fest fest--{tone}" href="{BASE}/fests/{slug}" data-cat="{cat}">
          <span class="slot"></span>
          <span class="f-ph"><img src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720"><span class="f-date">{d1} to {d2}</span><span class="f-city">Bengaluru</span></span>
          <span class="f-name">{e(name)}</span>
          <span class="f-stats"><span><b>{evs}</b>Events</span><span><b>{att}</b>Attending</span></span>
          <span class="f-cta">Explore<span class="dot">{ic('arrow')}</span></span>
        </a>'''

def ev(t, i):
    festn, name, day, venue, price, slug, cat, img = t
    free = price == '₹0'
    return f'''
        <a class="ev{' is-free' if free else ''}" href="{BASE}/events/{slug}" data-cat="{cat}" data-img="assets/img/fests/{img}.jpg">
          <span class="ev-date"><small>December</small><b>{day}</b></span>
          <img class="ev-thumb" src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720">
          <span class="ev-main"><span class="ev-name">{e(name)}</span><span class="ev-meta">{e(festn)}<i></i>{e(venue)}</span></span>
          <span class="ev-price"><b>{price}</b>/ Member</span>
          <span class="ev-reg">Register<span class="dot">{ic('arrow')}</span></span>
        </a>'''

def qa(i, q):
    qq, a = q
    on = ' is-on' if i == 0 else ''
    return f'''
          <div class="qa{on}" data-i="{i}">
            <button class="qa-q" aria-expanded="{'true' if i == 0 else 'false'}" aria-controls="qa{i+1}" id="qq{i+1}">
              <span class="qa-n">{i+1:02d}</span><span class="qa-t">{e(qq)}</span><span class="qa-go">{ic('arrow')}</span>
            </button>
            <div class="qa-a" id="qa{i+1}" role="region" aria-labelledby="qq{i+1}"><div><div class="bub bub-bot">{a}</div></div></div>
          </div>'''

def hand(h):
    n, left, hh, d, flip, back = h
    return (f'<img class="hand{" hand-back" if back else ""}{" hand-flip" if flip else ""}" src="assets/img/v2/hand{n}.png" alt="" '
            f'style="left:{left}%;--hh:{hh}px;--d:{d}s"width="{META[f"hand{n}"]["w"]}" height="{META[f"hand{n}"]["h"]}">')

def tape_run():
    return ''.join(f'<span>{w}</span>{STAR}' for w in ['Cultural', 'Technical', 'Sports', 'Quiz', 'Hackathon', 'Other'])

# neon sign from the real logo paths (mark stays whole; only lit)
svg = open(f'{ROOT}/assets/src/logo.svg').read()
paths = re.findall(r'<path class="(st[01])" d="([^"]+)"', svg)
defs = ''.join(f'<path id="lp{i}" d="{d}"/>' for i, (c, d) in enumerate(paths))
def uses(cls):
    return ''.join(f'<use href="#lp{i}"/>' for i, (c, d) in enumerate(paths) if c == cls)
NEON = f'''<svg class="neon" viewBox="-20 -20 1064 349" role="img" aria-label="FestHey">
          <defs>{defs}<filter id="nglow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="9"/></filter><filter id="nglow2" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="3"/></filter></defs>
          <g class="nz nz-y">
            <g class="n-off">{uses('st0')}</g>
            <g class="n-halo" filter="url(#nglow)">{uses('st0')}</g>
            <g class="n-tube" filter="url(#nglow2)">{uses('st0')}</g>
            <g class="n-core">{uses('st0')}</g>
          </g>
          <g class="nz nz-o">
            <g class="n-off">{uses('st1')}</g>
            <g class="n-halo" filter="url(#nglow)">{uses('st1')}</g>
            <g class="n-tube" filter="url(#nglow2)">{uses('st1')}</g>
            <g class="n-core">{uses('st1')}</g>
          </g>
        </svg>'''

PH = META['phone']; sx0, sy0, sx1, sy1 = PH['screen']

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FestHey | Discover College Fests &amp; Events Across India</title>
<meta name="description" content="Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.">
<meta name="theme-color" content="#F7F5F0">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600,700&amp;f[]=satoshi@400,500,700,900&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script>(function(){{var f=/[?&]figma/.test(location.search)||navigator.webdriver;document.documentElement.className=f?'figma':'anim';}})();</script>
</head>
<body>

<header class="nav">
  <div class="wrap">
    <nav class="nav-pill" aria-label="Main">
      <a class="nav-logo" href="{BASE}/" aria-label="FestHey home"><img src="assets/img/logo.svg" alt="FestHey" width="118" height="36"></a>
      <div class="nav-links">
        <a href="{BASE}/colleges">Colleges</a>
        <a href="{BASE}/fests">Fests</a>
        <a href="{BASE}/blogs">Blogs</a>
      </div>
      <div class="nav-end">
        <a class="btn-get" href="{BASE}/auth/login?redirect=%2F">Get Started<span class="dot">{ic('arrow')}</span></a>
        <button class="nav-menu" aria-label="Menu" aria-expanded="false">{ic('menu')}</button>
      </div>
    </nav>
    <div class="nav-sheet">
      <a href="{BASE}/colleges">Colleges</a>
      <a href="{BASE}/fests">Fests</a>
      <a href="{BASE}/blogs">Blogs</a>
    </div>
  </div>
</header>

<main>
  <!-- ============ HERO: the merch drop ============ -->
  <section class="hero" id="top">
    <div class="hero-stage wrap">
      <a class="feat" href="{BASE}{ADS[0]['href']}"><span class="live"></span><span class="feat-name">MSRIT Sports Meet</span>{ic('arrow','ic ic-s')}</a>
      <h1 class="hero-h">
        <span class="ln"><span class="w">THE BEAT</span></span>
        <span class="ln"><span class="w hl">OF THE</span></span>
        <span class="ln"><span class="w w-or">CAMPUS</span></span>
      </h1>
      <div class="hero-foot">
        <p class="hero-p">Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.</p>
        <a class="btn-or" href="{BASE}{ADS[0]['href']}">Explore Event<span class="dot">{ic('arrow')}</span></a>
      </div>
    </div>
    <div class="pile" id="pile">
        {''.join(prop(p, i) for i, p in enumerate(PROPS))}
        {''.join(ticket(a, i) for i, a in enumerate(ADS))}
        {''.join(polaroid(p, i) for i, p in enumerate(POLAROIDS))}
        {STICKER}
    </div>
    <div class="grain"></div>
  </section>

  <div class="tapes" aria-hidden="true">
    <div class="tape tape-sun"><div class="tape-run">{tape_run()*4}</div></div>
  </div>

  <!-- ============ FESTS & EVENTS ============ -->
  <section class="fe" id="fests">
    <div class="wrap">
      <div class="fe-head">
        <h2>FESTS &amp; EVENTS</h2>
        <div class="bands" role="group" aria-label="Categories">
          {''.join(band(c) for c in CATS)}
        </div>
      </div>

      <div class="sub-head">
        <a class="sub-h" href="{BASE}/fests"><h3>Trending Fests</h3><span class="dot">{ic('arrow')}</span></a>
      </div>
      <div class="fests">
        {''.join(fest(f) for f in FESTS)}
      </div>

      <div class="sub-head sub-head-2">
        <a class="sub-h" href="{BASE}/events"><h3>Trending Events</h3><span class="dot">{ic('arrow')}</span></a>
      </div>
      <div class="lineup">
        {''.join(ev(t, i) for i, t in enumerate(EVENTS))}
      </div>
    </div>
    <div class="peek" aria-hidden="true"><img src="assets/img/fests/{EVENTS[0][7]}.jpg" alt=""></div>
  </section>

  <!-- ============ FAQ: ask the crew ============ -->
  <section class="faq" id="faq">
    <div class="wrap faq-grid">
      <div class="faq-side">
        <p class="eyebrow"><span></span>FAQs</p>
        <h2>QUESTIONS? WE'VE GOT ANSWERS.</h2>
        <p class="faq-p">Find quick answers to the most common questions about FestHey. Can't find what you're looking for? Reach out to us!</p>
        <a class="btn-ink" href="{BASE}/help">{ic('msg')}Contact Us</a>
        <div class="faq-list">
          {''.join(qa(i, q) for i, q in enumerate(FAQ))}
        </div>
      </div>
      <div class="phone-wrap" aria-hidden="true">
        <div class="chat" style="left:{sx0/PH['w']*100:.2f}%;top:{sy0/PH['h']*100:.2f}%;width:{(sx1-sx0)/PH['w']*100:.2f}%;height:{(sy1-sy0)/PH['h']*100:.2f}%">
          <div class="chat-head"><span class="chat-av"><img src="assets/img/favicon.svg" alt="" width="40" height="40"></span><b>FestHey</b></div>
          <div class="chat-body">
            <div class="bub bub-me">{e(FAQ[0][0])}</div>
            <div class="bub bub-bot">{FAQ[0][1]}</div>
          </div>
          <div class="chat-bar"><span class="chat-input"></span><span class="chat-send">{ic('send','ic ic-s')}</span></div>
        </div>
        <img class="phone" src="assets/img/v2/phone.png" alt="" width="{PH['w']}" height="{PH['h']}">
      </div>
    </div>
  </section>

  <!-- ============ JOIN THE PIT ============ -->
  <section class="pit" id="pit">
    <div class="beams" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
    <div class="wrap pit-wrap">
      <div class="pit-copy">
        <p class="eyebrow eyebrow-l"><span></span>Backstage Access</p>
        <h2>JOIN THE <span class="hl">PIT.</span></h2>
        <p class="pit-p">The hottest festivals. The exclusive drops.<br>The earliest tickets. All in your inbox.</p>
        <div class="joined"><span class="avs">{AV}</span><span class="joined-t"><span>Joined by</span><b>2,000+ Students</b></span></div>
      </div>
      <div class="rig-pit">
        <div class="pass pass--access" data-k="5.5" data-max="0.42">
          <div class="p-arm">
            <div class="strap" style="height:170px"><img src="assets/img/lanyard-strap.png" alt="" width="30" height="333"></div>
            <div class="p-card">
              <span class="p-slot"></span>
              <div class="acc-band"></div>
              <div class="acc-top"><img class="p-logo" src="assets/img/logo.svg" alt="FestHey" width="96" height="29"><img class="bc" src="assets/img/barcode.svg" alt="" width="110" height="22"></div>
              <h3 class="acc-h">YOUR<br>MISSION<br>CONTROL</h3>
              <p class="acc-sub">// Enter your credentials to proceed</p>
              <form class="acc-form" action="#" novalidate>
                <label class="fld">{ic('mail')}<input type="email" name="email" placeholder="Email address" aria-label="Email address" autocomplete="email"></label>
                <button class="btn-acc" type="submit"><span class="acc-ic">{ic('lock')}{ic('check','ic ic-ok')}</span>Secure Access</button>
              </form>
              <p class="acc-note">No Spam. No Noise. Just the Music.</p>
              <span class="sheen"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="crowd" aria-hidden="true">{''.join(hand(h) for h in CROWD)}</div>
    <canvas class="confetti" aria-hidden="true"></canvas>
  </section>
</main>

<!-- ============ FOOTER: the venue wall after dark ============ -->
<footer class="foot" id="foot">
  <img class="foot-wall" src="assets/img/v2/wall.jpg" alt="" width="1536" height="1024">
  <div class="foot-glow"></div>
  <div class="wrap foot-in">
    <div class="sign">
      {NEON}
      <img class="neon-static" src="assets/img/logo.svg" alt="FestHey" width="1024" height="309">
      <button class="switch is-on" aria-pressed="true" aria-label="Neon sign on or off"><span class="switch-plate"><span class="switch-screw"></span><span class="switch-lever"></span><span class="switch-screw"></span></span></button>
    </div>
    <div class="posters">
      <div class="poster pz-snow" style="--r:-2.4deg"><img class="ptape pt-l" src="assets/img/v2/tape1.png" alt=""><img class="ptape pt-r" src="assets/img/v2/tape2.png" alt="">
        <p class="pz-tag">India's premier campus event discovery platform. Your mission control for the ultimate college experience.</p>
        <div class="socials">
          <a href="{BASE}/" aria-label="Instagram">{ic('insta')}</a>
          <a href="{BASE}/" aria-label="LinkedIn">{ic('linkedin')}</a>
          <a href="{BASE}/" aria-label="YouTube">{ic('youtube')}</a>
          <a href="{BASE}/" aria-label="Email">{ic('mail')}</a>
        </div>
      </div>
      <div class="poster pz-sun" style="--r:1.8deg"><img class="ptape pt-c" src="assets/img/v2/tape4.png" alt="">
        <h5>For Hosts</h5><a href="{BASE}/organizer/dashboard/fests/new">Host a Fest</a><a href="{BASE}/auth/register/organizer">Onboard Organisers</a><a href="{BASE}/organizer/dashboard/fests">Manage Fests</a>
      </div>
      <div class="poster pz-orange" style="--r:-1.2deg"><img class="ptape pt-l" src="assets/img/v2/tape5.png" alt=""><img class="ptape pt-r" src="assets/img/v2/tape3.png" alt="">
        <h5>For Students</h5><a href="{BASE}/events">Browse Events</a><a href="{BASE}/fests">Browse Fests</a><a href="{BASE}/account/my-registrations">My Registration</a><a href="{BASE}/how-it-works">How It Works</a>
      </div>
      <div class="poster pz-snow2" style="--r:2.6deg"><img class="ptape pt-c" src="assets/img/v2/tape6.png" alt="">
        <h5>Company</h5><a href="{BASE}/about">About Us</a><a href="{BASE}/privacy-policy">Privacy Policy</a><a href="{BASE}/refund-policy">Refund Policy</a><a href="{BASE}/help">Help</a>
      </div>
    </div>
    <div class="foot-bot">
      <span>&copy; 2026 FestHey</span>
      <span class="foot-legal"><a href="{BASE}/privacy-policy">Privacy Policy</a><a href="{BASE}/terms">Terms of Service</a></span>
      <a class="to-top" href="#top" aria-label="Back to top">{ic('up')}</a>
    </div>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
'''
open(OUT, 'w').write(page)
bad = [ch for ch in ('—', '–') if ch in page]
print('wrote', OUT, len(page), 'dashes:', bad)
