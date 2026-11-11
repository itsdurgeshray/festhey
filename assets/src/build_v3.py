#!/usr/bin/env python3
"""FestHey v3: builds index.html as static markup (Figma-import safe). Run: python3 assets/src/build.py"""
import html, json, math

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
 'left': '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
 'right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 'send': '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
}
def ic(n, c='ic'):
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{I[n]}</svg>'

STAR = '<svg class="star" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0l2.6 8.2L23 6.5l-6.3 5.5L23 17.5l-8.4-1.7L12 24l-2.6-8.2L1 17.5l6.3-5.5L1 6.5l8.4 1.7z"/></svg>'
AV = ''.join(f'<img src="assets/img/av{i}.jpg" alt="" width="40" height="40">' for i in range(1, 5))

# ---------------- data (client copy, word for word) ----------------
ADS = [
  dict(name='MSRIT Sports Meet', href='/fests/msrit-sports-meet', img='ad-event-basketball'),
  dict(name='Utsav Winter Edition', href='/fests/utsav-winter-edition', img='ad-fest-music'),
  dict(name='Hack RVCE Winter', href='/fests/hack-rvce-winter', img='ad-event-hackathon'),
]
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
# crowd: (hand file, left %, height px, beat delay s, flip, back row). Mostly women's hands (9-16), mixed in.
CROWD = [(9,-2,430,0,0,1),(4,6,380,.25,1,1),(10,13,470,.1,0,0),(13,22,400,.35,0,1),(15,30,460,.05,0,0),(1,39,390,.3,1,1),
         (11,46,450,.15,0,0),(16,54,420,.4,1,1),(12,61,470,.2,1,0),(5,69,390,.05,0,1),(14,76,440,.3,1,0),(10,84,400,.1,1,1),
         (3,90,460,.35,1,0),(9,97,410,.2,0,1)]

# ---------------- ferris wheel ----------------
CABS = []
for a in ADS:
    CABS.append(dict(name=a['name'], sub=None, img=a['img'], href=BASE + a['href'], ad=True))
for f in FESTS:
    if f[0] in ('Hack RVCE Winter', 'Christ Lit Fest', 'Hack-a-Thon BMS'):
        continue
    CABS.append(dict(name=f[0], sub=f'{f[1]} to {f[2]}', img=f[5], href=f'{BASE}/fests/{f[6]}', ad=False))
# interleave ads around the wheel
order = [0, 3, 4, 1, 5, 6, 2, 7]
CABS = [CABS[i] for i in order]
N = len(CABS)
ROOFS = ['orange', 'ink', 'sun', 'orange', 'ink', 'sun', 'orange', 'ink']

def wheel_svg():
    p = []
    # truss between rims
    pts = []
    for i in range(0, 121):
        a = 2 * math.pi * i / 120
        r = 404 if i % 2 == 0 else 440
        pts.append(f'{r*math.sin(a):.1f},{-r*math.cos(a):.1f}')
    p.append(f'<polyline class="w-truss" points="{" ".join(pts)}"/>')
    # lattice + spokes
    S = 20
    for i in range(S):
        a = 2 * math.pi * i / S
        a2 = 2 * math.pi * (i + .5) / S
        x0, y0 = 66 * math.sin(a), -66 * math.cos(a)
        x1, y1 = 404 * math.sin(a), -404 * math.cos(a)
        p.append(f'<line class="w-spoke" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
        bx, by = 250 * math.sin(a), -250 * math.cos(a)
        cx2, cy2 = 404 * math.sin(a2), -404 * math.cos(a2)
        p.append(f'<line class="w-lat" x1="{bx:.1f}" y1="{by:.1f}" x2="{cx2:.1f}" y2="{cy2:.1f}"/>')
        dx2, dy2 = 250 * math.sin(a2), -250 * math.cos(a2)
        ex, ey = 404 * math.sin(a), -404 * math.cos(a)
        p.append(f'<line class="w-lat" x1="{dx2:.1f}" y1="{dy2:.1f}" x2="{ex:.1f}" y2="{ey:.1f}"/>')
    p.append('<circle class="w-rim" r="440"/><circle class="w-rim2" r="404"/><circle class="w-mid" r="250"/><circle class="w-in" r="124"/>')
    # bulbs
    B = 40
    for i in range(B):
        a = 2 * math.pi * (i + .5) / B
        p.append(f'<circle class="bulb b{i%2+1}" cx="{422*math.sin(a):.1f}" cy="{-422*math.cos(a):.1f}" r="6.5"/>')
    for i in range(12):
        a = 2 * math.pi * (i + .5) / 12
        p.append(f'<circle class="bulb b{i%2+1}" cx="{250*math.sin(a):.1f}" cy="{-250*math.cos(a):.1f}" r="5"/>')
    # cabin pins
    for i in range(N):
        a = 2 * math.pi * i / N
        p.append(f'<circle class="w-pin" cx="{440*math.sin(a):.1f}" cy="{-440*math.cos(a):.1f}" r="11"/>')
    return f'<svg class="wheel-svg" viewBox="-500 -500 1000 1000" aria-hidden="true"><g class="wheel-rot">{"".join(p)}</g></svg>'

LEGS = '''<svg class="wheel-legs" viewBox="-500 0 1000 1000" preserveAspectRatio="xMidYMin meet" aria-hidden="true">
          <path class="leg" d="M-26 0 L-330 860 M26 0 L330 860"/>
          <path class="leg-x" d="M-150 340 L150 340 M-240 600 L240 600 M-150 340 L240 600 M150 340 L-240 600"/>
        </svg>'''

def cabin(i, c):
    a = 2 * math.pi * i / N
    left = 50 + 44 * math.sin(a); top = 50 - 44 * math.cos(a)
    ad = '<span class="cab-ad">AD</span>' if c['ad'] else ''
    sub = f'<small>{e(c["sub"])}</small>' if c['sub'] else ''
    return f'''<a class="cab cab--{ROOFS[i]}{' is-ad' if c['ad'] else ''}" href="{c['href']}" data-i="{i}" style="left:{left:.2f}%;top:{top:.2f}%" draggable="false">
          <span class="cab-rod"></span><span class="cab-roof"></span>
          <span class="cab-body"><span class="cab-ph"><img src="assets/img/fests/{c['img']}.jpg" alt="" width="1280" height="720" draggable="false">{ad}</span><span class="cab-label"><b>{e(c['name'])}</b>{sub}</span></span>
        </a>'''

# ---------------- other builders ----------------
def cat(c):
    k, label = c
    on = k == 'all'
    return f'<button class="cat{" is-on" if on else ""}" data-cat="{k}" aria-pressed="{"true" if on else "false"}">{label}</button>'

def fest(f):
    name, d1, d2, evs, att, img, slug, catg, tone = f
    return f'''
        <a class="fest fest--{tone}" href="{BASE}/fests/{slug}" data-cat="{catg}">
          <span class="slot"></span>
          <span class="f-ph"><img src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720"><span class="f-date">{d1} to {d2}</span><span class="f-city">Bengaluru</span></span>
          <span class="f-name">{e(name)}</span>
          <span class="f-stats"><span><b>{evs}</b>Events</span><span><b>{att}</b>Attending</span></span>
          <span class="f-cta">Explore<span class="dot">{ic('arrow')}</span></span>
        </a>'''

# polaroids pegged on a string of fest lights; small resting tilts so the line feels hand-hung
TILT = [-2.5, 1.8, -1.2, 2.6, -2, 1.2, -2.8, 2]
def pol(t, i):
    festn, name, day, venue, price, slug, catg, img = t
    last = ' is-last' if i == len(EVENTS) - 1 else ''
    tail = '<span class="cord cord-tail"><svg viewBox="0 0 100 64" preserveAspectRatio="none" aria-hidden="true"><path d="M0 4 Q50 60 100 4"/></svg></span>' if i == len(EVENTS) - 1 else ''
    return f'''
          <div class="hang{last}" data-cat="{catg}" style="--tilt:{TILT[i]}deg">
            <span class="cord"><svg viewBox="0 0 100 64" preserveAspectRatio="none" aria-hidden="true"><path d="M0 4 Q50 60 100 4"/></svg><span class="bulb-l l1"></span><span class="bulb-l l2"></span><span class="bulb-l l3"></span></span>{tail}
            <a class="pol" href="{BASE}/events/{slug}" draggable="false" style="transform:rotate({TILT[i]}deg)">
              <img class="peg" src="assets/img/v2/peg.png" alt="" width="73" height="400" draggable="false">
              <span class="pol-ph"><img src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720" draggable="false"><span class="pol-fest">{e(festn)}</span></span>
              <span class="pol-name">{e(name)}</span>
              <span class="pol-meta">December {day}<i></i>{e(venue)}</span>
              <span class="pol-foot"><span class="pol-price"><b>{price}</b> / Member</span><span class="pol-reg">Register{ic('arrow', 'ic ic-s')}</span></span>
            </a>
          </div>'''

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
            f'style="left:{left}%;--hh:{hh}px;--d:{d}s" width="{META[f"hand{n}"]["w"]}" height="{META[f"hand{n}"]["h"]}">')

def tape_run():
    return ''.join(f'<span>{w}</span>{STAR}' for w in ['Cultural', 'Technical', 'Sports', 'Quiz', 'Hackathon', 'Other'])

PH = META['phone2']; sx0, sy0, sx1, sy1 = PH['screen']

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
<div class="noise" aria-hidden="true"></div>

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
  <!-- ============ HERO: the fest wheel ============ -->
  <section class="hero" id="top">
    <div class="wrap hero-in">
      <div class="hero-copy">
        <a class="feat" href="{BASE}{ADS[0]['href']}"><span class="live"></span><span class="feat-name">{ADS[0]['name']}</span>{ic('arrow','ic ic-s')}</a>
        <h1 class="hero-h">
          <span class="ln"><span class="w">HOP ON</span></span>
          <span class="ln"><span class="w hl">THE FEST</span></span>
          <span class="ln"><span class="w w-or">CIRCUIT.</span></span>
        </h1>
        <p class="hero-p">Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.</p>
        <div class="hero-cta">
          <a class="btn-or" href="{BASE}{ADS[0]['href']}">Explore Event<span class="dot">{ic('arrow')}</span></a>
          <div class="joined"><span class="avs">{AV}</span><span class="joined-t"><span>Joined by</span><b>2000+ Students</b></span></div>
        </div>
      </div>
    </div>
    <div class="wheel" id="wheel">
      <span class="sun"></span><span class="sun-ring"></span>
      {LEGS}
      {wheel_svg()}
      <span class="hub"><img src="assets/img/logo.svg" alt="" width="1024" height="309"></span>
      {''.join(cabin(i, c) for i, c in enumerate(CABS))}
    </div>
  </section>

  <div class="tapes" aria-hidden="true">
    <div class="tape tape-sun"><div class="tape-run">{tape_run()*4}</div></div>
  </div>

  <!-- ============ FESTS & EVENTS ============ -->
  <section class="fe" id="fests">
    <div class="wrap">
      <div class="fe-head">
        <h2>FESTS &amp; EVENTS</h2>
        <div class="cats" role="group" aria-label="Categories">
          {''.join(cat(c) for c in CATS)}
        </div>
      </div>

      <div class="sub-head">
        <a class="sub-h" href="{BASE}/fests"><h3>Trending Fests</h3><span class="dot">{ic('arrow')}</span></a>
      </div>
      <div class="fests">
        {''.join(fest(f) for f in FESTS)}
      </div>
    </div>

    <div class="events" id="events">
      <div class="wrap">
        <div class="sub-head">
          <a class="sub-h" href="{BASE}/events"><h3>Trending Events</h3><span class="dot">{ic('arrow')}</span></a>
          <div class="ev-nav">
            <button class="ev-btn ev-prev" aria-label="Previous events">{ic('left')}</button>
            <button class="ev-btn ev-next" aria-label="More events">{ic('right')}</button>
          </div>
        </div>
      </div>
      <div class="line-track">
        <div class="line">
          {''.join(pol(t, i) for i, t in enumerate(EVENTS))}
        </div>
      </div>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section class="faq" id="faq">
    <div class="wrap faq-grid">
      <div class="faq-head">
        <p class="eyebrow"><span></span>FAQs</p>
        <h2>QUESTIONS? WE'VE GOT ANSWERS.</h2>
        <p class="faq-p">Find quick answers to the most common questions about FestHey. Can't find what you're looking for? Reach out to us!</p>
      </div>
      <div class="faq-list">
        {''.join(qa(i, q) for i, q in enumerate(FAQ))}
        <a class="btn-ink" href="{BASE}/help">{ic('msg')}Contact Us</a>
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
        <img class="phone" src="assets/img/v2/phone2.png" alt="" width="{PH['w']}" height="{PH['h']}">
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

<!-- ============ FOOTER: the campus notice wall ============ -->
<footer class="foot" id="foot">
  <img class="foot-wall" src="assets/img/v2/wall-day.jpg" alt="" width="1536" height="1024">
  <div class="wrap foot-in">
    <div class="mural"><img src="assets/img/logo.svg" alt="FestHey" width="1024" height="309"></div>
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
