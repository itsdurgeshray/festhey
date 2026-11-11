#!/usr/bin/env python3
"""Builds WFT/festhey/index.html as fully static markup (Figma-import safe)."""
import html

OUT = '/Users/durgesh/Desktop/WFT/festhey/index.html'
BASE = 'https://festhey.agpro.co.in'

I = {
 'arrow': '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
 'right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 'pin': '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 'cal': '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 'layers': '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
 'plus': '<path d="M5 12h14"/><path d="M12 5v14"/>',
 'lock': '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 'msg': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 'grab': '<path d="M18 11.5V9a2 2 0 0 0-2-2a2 2 0 0 0-2 2v1.4"/><path d="M14 10V8a2 2 0 0 0-2-2a2 2 0 0 0-2 2v2"/><path d="M10 9.9V9a2 2 0 0 0-2-2a2 2 0 0 0-2 2v5"/><path d="M6 14a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M18 11a2 2 0 1 1 4 0v3a8 8 0 0 1-8 8h-4a8 8 0 0 1-8-8 2 2 0 1 1 4 0"/>',
 'menu': '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
 'insta': '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
 'linkedin': '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
 'youtube': '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
}
def ic(n, c='ic'):
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{I[n]}</svg>'

STAR = '<svg class="star" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0l2.6 8.2L23 6.5l-6.3 5.5L23 17.5l-8.4-1.7L12 24l-2.6-8.2L1 17.5l6.3-5.5L1 6.5l8.4 1.7z"/></svg>'

e = html.escape

# ---------- data (copy kept word for word from festhey.agpro.co.in) ----------
PASSES = [
  dict(k='snow', tag='Football, Basketball and More', name='MSRIT SPORTS MEET', short='MSRIT Sports Meet',
       col='M S Ramaiah Institute of Technology', img='ad-event-basketball', href='/fests/msrit-sports-meet', x='2%', len=232),
  dict(k='sun', tag='Three Nights of Music and Dance at BMSCE', name='UTSAV WINTER EDITION', short='Utsav Winter Edition',
       col='B M S College of Engineering', img='ad-fest-music', href='/fests/utsav-winter-edition', x='29%', len=298),
  dict(k='ink', tag='Overnight Builds, ₹75K in Prizes', name='HACK RVCE WINTER', short='Hack RVCE Winter',
       col='R V College of Engineering', img='ad-event-hackathon', href='/fests/hack-rvce-winter', x='56%', len=250),
]

CATS = [('all','All Categories',None),('cultural','Cultural','obj-mic'),('technical','Technical','obj-robot'),
        ('sports','Sports','obj-ball'),('quiz','Quiz','obj-buzzer'),('hackathon','Hackathon','obj-laptop'),('other','Other','obj-popper')]

FESTS = [
  ('8TH MILE ENCORE','Dec 5','Dec 6','7+ Events','0 Attending','fest-cultural','8th-mile-encore','cultural'),
  ('BMSCE ESPORTS SHOWDOWN','Dec 12','Dec 13','5+ Events','0 Attending','event-esports','bmsce-esports-showdown','other'),
  ('BRAIN WARS','Dec 30','Dec 31','5+ Events','0 Attending','gallery-stage','brain-wars','quiz'),
  ('CHRIST CODE SPRINT','Dec 17','Dec 18','5+ Events','0 Attending','event-hackathon','christ-code-sprint','hackathon'),
  ('CHRIST INTER-COLLEGE ATHLETICS','Nov 20','Nov 22','7+ Events','0 Attending','fest-sports','christ-inter-college-athletics','sports'),
  ('CHRIST LIT FEST','Nov 13','Nov 14','5+ Events','0 Attending','blog-fest-season','christ-lit-fest','cultural'),
  ('HACK RVCE WINTER','Nov 14','Nov 15','7+ Events','0 Attending','ad-event-hackathon','hack-rvce-winter','hackathon technical'),
  ('HACK-A-THON BMS','Dec 26','Dec 27','5+ Events','1 Attending','fest-technical','hack-a-thon-bms','hackathon technical'),
]

EVENTS = [
  ('Brain Wars','LINE FOLLOWER SPRINT','30','Main Grounds, MSRIT','₹349.00','line-follower-sprint-ymdlgs','technical'),
  ('Brain Wars','SLAM POETRY','31','Electronics Lab, MSRIT','₹0','slam-poetry-xyhzfg','cultural'),
  ('Brain Wars','SCIENCE & TECH QUIZ','30','ESB Seminar Hall, MSRIT','₹0','science-tech-quiz-phiblg','quiz'),
  ('Brain Wars','GENERAL QUIZ','31','Main Grounds, MSRIT','₹199.00','general-quiz-hhbpkh','quiz'),
  ('Brain Wars','INDIA QUIZ','30','Electronics Lab, MSRIT','₹0','india-quiz-ww8o81','quiz'),
  ('Hack-a-Thon BMS','POP CULTURE QUIZ','26','PJA Auditorium, BMSCE','₹199.00','pop-culture-quiz-67epp3','quiz'),
  ('Hack-a-Thon BMS','IOT BUILD-OFF','27','Mechanical Seminar Hall, BMSCE','₹0','iot-build-off-fvihvz','technical'),
  ('Hack-a-Thon BMS','LINE FOLLOWER SPRINT','26','Football Ground, BMSCE','₹349.00','line-follower-sprint','technical'),
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

AV = ''.join(f'<img src="assets/img/av{i}.jpg" alt="" width="40" height="40">' for i in range(1,5))

def strap(length):
    return f'<div class="strap" style="height:{length}px"><img src="assets/img/lanyard-strap.png" alt="" width="30" height="333"></div>'

def hero_pass(i, p):
    return f'''
      <div class="pass pass--{p['k']}{' is-on' if i==0 else ''}" data-i="{i}" style="z-index:{5 if i==0 else (4 if i==1 else 3)};left:{p['x']}" data-href="{BASE}{p['href']}" data-name="{e(p['short'])}">
        <div class="p-arm">
          {strap(p['len'])}
          <div class="p-card" role="button" tabindex="0" aria-label="Feature {e(p['short'])}">
            <span class="p-slot"></span>
            <div class="p-top"><span class="p-ad">AD</span><img class="p-logo" src="assets/img/logo.svg" alt="FestHey" width="74" height="22"></div>
            <div class="p-ph"><img src="assets/img/duo/{p['img']}.jpg" alt="" width="640" height="360"></div>
            <p class="p-tag">{e(p['tag'])}</p>
            <h3 class="p-name">{e(p['name'])}</h3>
            <p class="p-col">{e(p['col'])}</p>
            <div class="p-foot"><img class="bc" src="assets/img/{'barcode-light' if p['k']=='ink' else 'barcode'}.svg" alt="" width="120" height="22"><span class="p-go">{ic('arrow')}</span></div>
            <span class="sheen"></span>
          </div>
        </div>
      </div>'''

def cat_tile(c):
    key, label, img = c
    art = f'<img class="cat-obj" src="assets/img/{img}.png" alt="" height="110">' if img else \
          '<span class="cat-all"><img class="cat-burst" src="assets/img/burst.svg" alt="" width="104" height="104"><img class="cat-flower" src="assets/img/flower.svg" alt="" width="66" height="66"></span>'
    on = ' is-on' if key == 'all' else ''
    return f'<button class="cat{on}" data-cat="{key}" aria-pressed="{"true" if on else "false"}">{art}<span class="cat-label">{label}</span></button>'

def fest_card(f):
    name, d1, d2, evs, att, img, slug, cat = f
    return f'''
        <a class="fest" href="{BASE}/fests/{slug}" data-cat="{cat}">
          <span class="slot"></span>
          <div class="ph">
            <img class="duo" src="assets/img/duo/{img}.jpg" alt="" width="1280" height="720">
            <img class="col" src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720">
            <span class="date">{d1} to {d2}</span>
            <span class="city">{ic('pin','ic ic-s')}Bengaluru</span>
          </div>
          <div class="fest-body">
            <h4>{e(name)}</h4>
            <div class="fest-meta"><span>{ic('layers','ic ic-s')}{evs}</span><span>{ic('users','ic ic-s')}{att}</span></div>
            <span class="btn-x">Explore<span class="dot">{ic('arrow')}</span></span>
          </div>
        </a>'''

def ticket(t, idx):
    fest, name, day, venue, price, slug, cat = t
    free = price == '₹0'
    tone = 'or' if fest == 'Brain Wars' else 'ink'
    return f'''
        <a class="ticket t-{tone}{' is-free' if free else ''}" href="{BASE}/events/{slug}" data-cat="{cat}">
          <div class="t-date"><span>December</span><b>{day}</b></div>
          <div class="t-main">
            <span class="t-fest">{e(fest)}</span>
            <h4>{e(name)}</h4>
            <span class="t-venue">{ic('pin','ic ic-s')}{e(venue)}</span>
          </div>
          <div class="t-stub">
            <span class="nt nt-a"></span><span class="nt nt-b"></span>
            <span class="t-price"><b>{price}</b> / Member</span>
            <span class="t-reg">Register{ic('arrow','ic ic-s')}</span>
            <img class="t-bc" src="assets/img/barcode.svg" alt="" width="120" height="18">
          </div>
        </a>'''

def faq_item(i, q):
    qq, a = q
    on = ' is-open' if i == 0 else ''
    return f'''
          <div class="qa{on}">
            <button class="qa-q" aria-expanded="{'true' if on else 'false'}" aria-controls="qa{i+1}" id="qq{i+1}">
              <span class="qa-n"><b>{i+1:02d}</b></span>
              <span class="qa-t">{e(qq)}</span>
              <span class="qa-i">{ic('plus')}</span>
            </button>
            <div class="qa-a" id="qa{i+1}" role="region" aria-labelledby="qq{i+1}"><div><div class="qa-body">{a}</div></div></div>
          </div>'''

TAPE_WORDS = ['Cultural','Technical','Sports','Quiz','Hackathon','Other']
def tape_run():
    return ''.join(f'<span>{w}</span>{STAR}' for w in TAPE_WORDS)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FestHey | Discover College Fests &amp; Events Across India</title>
<meta name="description" content="Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.">
<meta name="theme-color" content="#FF5A14">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
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
  <!-- ============ HERO ============ -->
  <section class="hero" id="top">
    <div class="hero-glow"></div>
    <img class="hero-burst" src="assets/img/burst.svg" alt="" width="760" height="760">
    <div class="wrap hero-wrap">
      <h1 class="hero-h">
        <span class="ln"><span>THE BEAT</span></span>
        <span class="ln ln-hl"><span class="hl">OF THE</span></span>
        <span class="ln"><span>CAMPUS</span></span>
      </h1>

      <div class="rig rig-hero" aria-label="Featured fests">
        <span class="rail"></span>
        {''.join(hero_pass(i,p) for i,p in enumerate(PASSES))}
      </div>

      <div class="hero-foot">
        <a class="feat" href="{BASE}{PASSES[0]['href']}"><span class="live"></span><span class="feat-name">MSRIT Sports Meet</span></a>
        <p class="hero-p">Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.</p>
        <div class="hero-cta">
          <a class="btn-sun" href="{BASE}{PASSES[0]['href']}">Explore Event<span class="dot">{ic('arrow')}</span></a>
          <div class="joined"><div class="avs">{AV}</div><p><span>Joined by</span><b>2000+ Students</b></p></div>
        </div>
      </div>
    </div>
    <div class="grain"></div>
  </section>

  <div class="tapes" aria-hidden="true">
    <div class="tape tape-ink"><div class="tape-run">{tape_run()*4}</div></div>
    <div class="tape tape-sun"><div class="tape-run">{tape_run()*4}</div></div>
  </div>

  <!-- ============ FESTS & EVENTS ============ -->
  <section class="sec fe" id="fests">
    <div class="wrap">
      <div class="sec-head">
        <h2>FESTS &amp; EVENTS</h2>
      </div>
      <div class="cats" role="group" aria-label="Categories">
        {''.join(cat_tile(c) for c in CATS)}
      </div>

      <div class="sub-head">
        <a class="sub-h" href="{BASE}/fests"><h3>Trending Fests</h3><span class="dot">{ic('arrow')}</span></a>
      </div>
      <div class="fests">
        {''.join(fest_card(f) for f in FESTS)}
      </div>

      <div class="sub-head sub-head-2">
        <a class="sub-h" href="{BASE}/events"><h3>Trending Events</h3><span class="dot">{ic('arrow')}</span></a>
      </div>
      <div class="tickets">
        {''.join(ticket(t,i) for i,t in enumerate(EVENTS))}
      </div>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section class="sec faq" id="faq">
    <div class="wrap faq-grid">
      <div class="faq-side">
        <p class="eyebrow">FAQs</p>
        <h2>QUESTIONS? WE'VE GOT ANSWERS.</h2>
        <p class="faq-p">Find quick answers to the most common questions about FestHey. Can't find what you're looking for? Reach out to us!</p>
        <a class="btn-ink" href="{BASE}/help">{ic('msg')}Contact Us</a>
      </div>
      <div class="faq-list">
        {''.join(faq_item(i,q) for i,q in enumerate(FAQ))}
      </div>
    </div>
  </section>

  <!-- ============ JOIN THE PIT ============ -->
  <section class="pit" id="pit">
    <div class="pit-bg"><img src="assets/img/crowd.jpg" alt="" width="1536" height="1024"></div>
    <div class="pit-shade"></div>
    <div class="wrap pit-wrap">
      <div class="pit-copy">
        <p class="eyebrow">Backstage Access</p>
        <h2>JOIN THE <span class="hl">PIT.</span></h2>
        <p class="pit-p">The hottest festivals. The exclusive drops.<br>The earliest tickets. All in your inbox.</p>
        <div class="joined joined-dark"><div class="avs">{AV}</div><p><span>Joined by</span><b>2,000+ Students</b></p></div>
      </div>
      <img class="pit-hand" src="assets/img/hand.png" alt="" width="495" height="1476">
      <div class="rig rig-pit">
        <div class="pass pass--access" data-k="5.5" data-max="0.42" style="left:0">
          <div class="p-arm">
            {strap(150)}
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
    <div class="grain"></div>
  </section>
</main>

<!-- ============ FOOTER ============ -->
<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <p class="foot-p">India's premier campus event discovery platform. Your mission control for the ultimate college experience.</p>
        <div class="socials">
          <a href="{BASE}/" aria-label="Instagram">{ic('insta')}</a>
          <a href="{BASE}/" aria-label="LinkedIn">{ic('linkedin')}</a>
          <a href="{BASE}/" aria-label="YouTube">{ic('youtube')}</a>
          <a href="{BASE}/" aria-label="Email">{ic('mail')}</a>
        </div>
      </div>
      <div class="foot-cols">
        <div><h5>For Hosts</h5><a href="{BASE}/organizer/dashboard/fests/new">Host a Fest</a><a href="{BASE}/auth/register/organizer">Onboard Organisers</a><a href="{BASE}/organizer/dashboard/fests">Manage Fests</a></div>
        <div><h5>For Students</h5><a href="{BASE}/events">Browse Events</a><a href="{BASE}/fests">Browse Fests</a><a href="{BASE}/account/my-registrations">My Registration</a><a href="{BASE}/how-it-works">How It Works</a></div>
        <div><h5>Company</h5><a href="{BASE}/about">About Us</a><a href="{BASE}/privacy-policy">Privacy Policy</a><a href="{BASE}/refund-policy">Refund Policy</a><a href="{BASE}/help">Help</a></div>
      </div>
    </div>
    <div class="foot-mark"><img src="assets/img/logo.svg" alt="FestHey" width="1024" height="309"></div>
    <div class="foot-bot">
      <span>&copy; 2026 FestHey</span>
      <span class="foot-legal"><a href="{BASE}/privacy-policy">Privacy Policy</a><a href="{BASE}/terms">Terms of Service</a></span>
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
print('wrote', OUT, len(page))
