#!/usr/bin/env python3
"""FestHey v4: builds index.html and system.html as static markup (Figma-import safe).
Run: python3 assets/src/build.py"""
import html, json, math
import runpy as _rp
_LU = _rp.run_path('/Users/durgesh/Desktop/WFT/festhey/assets/src/icons.py')

ROOT = '/Users/durgesh/Desktop/WFT/festhey'
BASE = 'https://festhey.agpro.co.in'
META = json.load(open(f'{ROOT}/assets/img/v2/meta.json'))
e = html.escape

I = {
 'arrow': '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
 'up': '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
 'left': '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
 'right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
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
    return _LU['svg'](n, c)
def btn(label, href, v='primary', size='', icon='arrow', extra=''):
    sz = f' btn--{size}' if size else ''
    return f'<a class="btn btn--{v}{sz}{extra}" href="{href}">{label}<span class="dot">{ic(icon)}</span></a>'

STAR = '<svg class="star" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0l2.6 8.2L23 6.5l-6.3 5.5L23 17.5l-8.4-1.7L12 24l-2.6-8.2L1 17.5l6.3-5.5L1 6.5l8.4 1.7z"/></svg>'
AV = ''.join(f'<img src="assets/img/av{i}.jpg" alt="" width="40" height="40">' for i in range(1, 5))

# ---------------- data (client copy, word for word) ----------------
ADS = [
  dict(name='MSRIT Sports Meet', href='/fests/msrit-sports-meet', tag='Football, Basketball and More', col='M S Ramaiah Institute of Technology', img='ad-event-basketball'),
  dict(name='Utsav Winter Edition', href='/fests/utsav-winter-edition', tag='Three Nights of Music and Dance at BMSCE', col='B M S College of Engineering', img='ad-fest-music'),
  dict(name='Hack RVCE Winter', href='/fests/hack-rvce-winter', tag='Overnight Builds, ₹75K in Prizes', col='R V College of Engineering', img='ad-event-hackathon'),
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
CROWD = [(9,-2,430,0,0,1),(4,6,380,.25,1,1),(10,13,470,.1,0,0),(13,22,400,.35,0,1),(15,30,460,.05,0,0),(1,39,390,.3,1,1),
         (11,46,450,.15,0,0),(16,54,420,.4,1,1),(12,61,470,.2,1,0),(5,69,390,.05,0,1),(14,76,440,.3,1,0),(10,84,400,.1,1,1),
         (3,90,460,.35,1,0),(9,97,410,.2,0,1)]

# ---------------- hero: the three featured fests, fanned ----------------
POSES = ['is-c', 'is-r', 'is-l']
def fcard(i, a):
    return f'''
        <a class="fcard {POSES[i]}" href="{BASE}{a['href']}" data-i="{i}" draggable="false">
          <span class="fcard-ph"><img src="assets/img/fests/{a['img']}.jpg" alt="" width="1280" height="720" draggable="false"><span class="chip chip--ink fcard-ad">AD</span></span>
          <span class="fcard-tag">{e(a['tag'])}</span>
          <span class="fcard-name">{e(a['name'])}</span>
          <span class="fcard-col">{e(a['col'])}</span>
          <span class="btn btn--ink btn--sm btn--block">Explore Event<span class="dot">{ic('arrow')}</span></span>
        </a>'''

def ticker_run():
    return ''.join(f'<a href="{BASE}{a["href"]}"><span class="live"></span>{e(a["name"])}</a>{STAR}' for a in ADS)

NOTCH = '<svg class="notch-bg" viewBox="0 0 240 64" aria-hidden="true"><path d="M0 0H240C224 0 216 4 214 16L210 40C208 56 196 64 180 64H60C44 64 32 56 30 40L26 16C24 4 16 0 0 0Z"/></svg>'

# ---------------- builders ----------------
def cat(c):
    k, label = c
    on = k == 'all'
    return f'<button class="chip{" is-on" if on else ""}" data-cat="{k}" aria-pressed="{"true" if on else "false"}">{label}</button>'

def fest(f):
    name, d1, d2, evs, att, img, slug, catg, tone = f
    return f'''
        <a class="fest fest--{tone}" href="{BASE}/fests/{slug}" data-cat="{catg}">
          <span class="slot"></span>
          <span class="f-ph"><img src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720"><span class="chip chip--light f-date">{d1} to {d2}</span><span class="chip chip--glass f-city">Bengaluru</span></span>
          <span class="f-name">{e(name)}</span>
          <span class="f-stats"><span><b>{evs}</b>Events</span><span><b>{att}</b>Attending</span></span>
          <span class="btn btn--ink btn--block f-cta">Explore<span class="dot">{ic('arrow')}</span></span>
        </a>'''

def evc(t, i):
    festn, name, day, venue, price, slug, catg, img = t
    return f'''
          <a class="evc" href="{BASE}/events/{slug}" data-cat="{catg}" draggable="false">
            <span class="evc-rings"><span></span><span></span></span>
            <span class="evc-ph"><img src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720" draggable="false"><span class="evc-shade"></span></span>
            <span class="evc-date"><b>{day}</b><small>December</small></span>
            <span class="chip chip--light evc-fest">{e(festn)}</span>
            <span class="evc-body"><span class="evc-name">{e(name)}</span><span class="evc-venue">{e(venue)}</span></span>
            <span class="evc-cut"><span></span><span></span></span>
            <span class="evc-foot"><span class="evc-price"><b>{price}</b> / Member</span><span class="btn btn--ink btn--sm">Register<span class="dot">{ic('arrow')}</span></span></span>
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
            f'style="left:{left}%;--hh:{hh}px;--d:{d}s" width="{META[f"hand{n}"]["w"]}" height="{META[f"hand{n}"]["h"]}">')

def tape_run():
    return ''.join(f'<span>{w}</span>{STAR}' for w in ['Cultural', 'Technical', 'Sports', 'Quiz', 'Hackathon', 'Other'])

PH = META['phone2']; sx0, sy0, sx1, sy1 = PH['screen']

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.">
<meta name="theme-color" content="#FF5A14">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600,700&amp;f[]=satoshi@400,500,700,900&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script>(function(){{var f=/[?&]figma/.test(location.search)||navigator.webdriver;document.documentElement.className=f?'figma':'anim';}})();</script>
</head>
<body>
<div class="noise" aria-hidden="true"></div>
'''

NAV = f'''
<header class="nav">
  <div class="ticker"><div class="ticker-run">{ticker_run() * 6}</div></div>
  <div class="wrap nav-row">
    <nav class="nav-links" aria-label="Main">
      <a href="{BASE}/colleges">Colleges</a>
      <a href="{BASE}/fests">Fests</a>
      <a href="{BASE}/blogs">Blogs</a>
    </nav>
    <button class="nav-menu" aria-label="Menu" aria-expanded="false">{ic('menu')}</button>
    <a class="notch" href="{BASE}/" aria-label="FestHey home">{NOTCH}<img src="assets/img/logo.svg" alt="FestHey" width="132" height="40"></a>
    <div class="nav-end">{btn('Get Started', BASE + '/auth/login?redirect=%2F', 'ink', 'sm')}</div>
  </div>
  <div class="wrap"><div class="nav-sheet">
    <a href="{BASE}/colleges">Colleges</a>
    <a href="{BASE}/fests">Fests</a>
    <a href="{BASE}/blogs">Blogs</a>
  </div></div>
</header>
'''

HOST_PERKS = ['Fest and event pages in minutes', 'Registrations, team invites and payments', 'Confirmations and reminders by email', 'A live dashboard for every registration']

def faq_block(items, h2="QUESTIONS? WE'VE GOT ANSWERS.", lead="Find quick answers to the most common questions about FestHey. Can't find what you're looking for? Reach out to us!", sid='faq'):
    """Shared FAQ: question list + phone chat on desktop, accordion below 1025px. Used on every page."""
    return f'''  <!-- ============ FAQ ============ -->
  <section class="sec faq" id="{sid}">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap faq-grid">
      <div class="faq-head">
        <p class="eyebrow"><span></span>FAQs</p>
        <h2>{h2}</h2>
        <p class="lead faq-p">{lead}</p>
      </div>
      <div class="faq-list">
        {''.join(qa(i, q) for i, q in enumerate(items))}
        <a class="btn btn--ink faq-btn" href="{BASE}/help">Contact Us<span class="dot dot--still">{ic('msg')}</span></a>
      </div>
      <div class="phone-wrap" aria-hidden="true">
        <div class="chat" style="left:{sx0/PH['w']*100:.2f}%;top:{sy0/PH['h']*100:.2f}%;width:{(sx1-sx0)/PH['w']*100:.2f}%;height:{(sy1-sy0)/PH['h']*100:.2f}%">
          <div class="chat-head"><span class="chat-av"><img src="assets/img/favicon.svg" alt="" width="40" height="40"></span><b>FestHey</b></div>
          <div class="chat-body">
            <div class="bub bub-me">{e(items[0][0])}</div>
            <div class="bub bub-bot">{items[0][1]}</div>
          </div>
          <div class="chat-bar"><span class="chat-input"></span><span class="chat-send">{ic('send','ic ic-s')}</span></div>
        </div>
        <img class="phone" src="assets/img/v2/phone2.png" alt="" width="{PH['w']}" height="{PH['h']}">
      </div>
    </div>
  </section>

'''

page = HEAD.format(title='FestHey | Discover College Fests &amp; Events Across India') + NAV + f'''
<main>
  <!-- ============ HERO ============ -->
  <section class="hero" id="top">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap hero-in">
      <div class="hero-copy">
        <h1 class="hero-h"><span class="ln">India's</span> <span class="ln"><mark class="mark">college fests</mark>,</span> <span class="ln">all in one place.</span></h1>
        <p class="lead hero-p">Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.</p>
        <div class="hero-cta">
          {btn('Explore Fests', '#fests', 'light')}
          {btn('Host a Fest', BASE + '/organizer/dashboard/fests/new', 'ink')}
        </div>
        <div class="joined joined--light"><span class="avs">{AV}</span><span class="joined-t"><span>Joined by</span><b>2000+ Students</b></span></div>
      </div>
      <div class="trio" aria-label="Featured fests">
        {''.join(fcard(i, a) for i, a in enumerate(ADS))}
        <div class="trio-dots" aria-hidden="true"><span class="on"></span><span></span><span></span></div>
      </div>
    </div>
  </section>

  <div class="tapes" aria-hidden="true">
    <div class="tape"><div class="tape-run">{tape_run()*4}</div></div>
  </div>

  <!-- ============ FESTS & EVENTS ============ -->
  <section class="sec fe" id="fests">
    <div class="wrap">
      <div class="sec-head">
        <h2>FESTS &amp; EVENTS</h2>
        <div class="chips" role="group" aria-label="Categories">
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
            <button class="icon-btn ev-prev" aria-label="Previous events">{ic('left')}</button>
            <button class="icon-btn ev-next" aria-label="More events">{ic('right')}</button>
          </div>
        </div>
      </div>
      <div class="ev-track">
        <div class="ev-row v-ticket">
          {''.join(evc(t, i) for i, t in enumerate(EVENTS))}
        </div>
      </div>
    </div>
  </section>

{faq_block(FAQ)}
  <!-- ============ JOIN THE PIT ============ -->
  <section class="pit" id="pit">
    <span class="grain" aria-hidden="true"></span>
    <div class="beams" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
    <div class="wrap pit-wrap">
      <div class="pit-copy">
        <p class="eyebrow eyebrow--ink"><span></span>Backstage Access</p>
        <h2>JOIN THE <mark class="mark mark--snow">PIT.</mark></h2>
        <p class="lead pit-p">The hottest festivals. The exclusive drops.<br>The earliest tickets. All in your inbox.</p>
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
                <button class="btn btn--primary btn--block" type="submit">Secure Access<span class="dot dot--still acc-ic">{ic('lock')}{ic('check','ic ic-ok')}</span></button>
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

<!-- ============ FOOTER: the campus wall, with a call for hosts ============ -->
<footer class="foot" id="foot">
  <img class="foot-wall" src="assets/img/v2/wall-day.jpg" alt="" width="1536" height="1024">
  <div class="wrap foot-in">
    <div class="host">
      <div class="host-card">
        <img class="ptape pt-l" src="assets/img/v2/tape1.png" alt=""><img class="ptape pt-r" src="assets/img/v2/tape3.png" alt="">
        <p class="eyebrow eyebrow--ink"><span></span>For Hosts</p>
        <h2>HOSTING A FEST? BRING IT TO <mark class="mark mark--snow">FESTHEY.</mark></h2>
        <p class="lead host-p">Publish your fest, take registrations and payments, and reach students across India from one dashboard.</p>
        <ul class="perks">{''.join(f'<li><span class="perk-ic">{ic("check")}</span>{p}</li>' for p in HOST_PERKS)}</ul>
        <div class="host-cta">
          {btn('Host a Fest', BASE + '/organizer/dashboard/fests/new', 'ink')}
          {btn('Onboard Organisers', BASE + '/auth/register/organizer', 'light')}
        </div>
      </div>
      <div class="host-photo">
        <img class="ptape pt-c" src="assets/img/v2/tape2.png" alt="">
        <img class="host-img" src="assets/img/v4/hosts.jpg" alt="A college fest team at the registration desk" width="1400" height="933">
        <span class="host-stick"><span class="avs">{AV}</span><b>2,000+ Students</b></span>
      </div>
    </div>
    <div class="posters">
      <div class="poster pz-snow" style="--r:-2deg"><img class="ptape pt-c" src="assets/img/v2/tape4.png" alt="">
        <p class="pz-tag">India's premier campus event discovery platform. Your mission control for the ultimate college experience.</p>
        <div class="socials">
          <a href="{BASE}/" aria-label="Instagram">{ic('insta')}</a>
          <a href="{BASE}/" aria-label="LinkedIn">{ic('linkedin')}</a>
          <a href="{BASE}/" aria-label="YouTube">{ic('youtube')}</a>
          <a href="{BASE}/" aria-label="Email">{ic('mail')}</a>
        </div>
      </div>
      <div class="poster pz-sun" style="--r:1.6deg"><img class="ptape pt-c" src="assets/img/v2/tape5.png" alt="">
        <h5>For Hosts</h5><a href="{BASE}/organizer/dashboard/fests/new">Host a Fest</a><a href="{BASE}/auth/register/organizer">Onboard Organisers</a><a href="{BASE}/organizer/dashboard/fests">Manage Fests</a>
      </div>
      <div class="poster pz-snow2" style="--r:-1.2deg"><img class="ptape pt-c" src="assets/img/v2/tape6.png" alt="">
        <h5>For Students</h5><a href="{BASE}/events">Browse Events</a><a href="{BASE}/fests">Browse Fests</a><a href="{BASE}/account/my-registrations">My Registration</a><a href="{BASE}/how-it-works">How It Works</a>
      </div>
      <div class="poster pz-snow3" style="--r:2.2deg"><img class="ptape pt-c" src="assets/img/v2/tape1.png" alt="">
        <h5>Company</h5><a href="{BASE}/about">About Us</a><a href="{BASE}/privacy-policy">Privacy Policy</a><a href="{BASE}/refund-policy">Refund Policy</a><a href="{BASE}/help">Help</a>
      </div>
    </div>
    <div class="mural"><img src="assets/img/logo.svg" alt="FestHey" width="1024" height="309"></div>
    <div class="foot-bot">
      <span>&copy; 2026 FestHey</span>
      <span class="foot-legal"><a href="{BASE}/privacy-policy">Privacy Policy</a><a href="{BASE}/terms">Terms of Service</a></span>
      <a class="icon-btn icon-btn--ink to-top" href="#top" aria-label="Back to top">{ic('up')}</a>
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

# ---------------- design system page ----------------
SW = [('--orange', '#FF5A14', 'Orange', 'Primary. Hero, primary buttons, live states.'),
      ('--sun', '#FFD400', 'Sun', 'Accent. Highlights, stickers, FAQ ground.'),
      ('--snow', '#F7F5F0', 'Snow', 'Page background.'),
      ('--paper', '#FFFFFF', 'Paper', 'Cards and surfaces.'),
      ('--ink', '#140A04', 'Ink', 'Text, dark buttons, outlines.'),
      ('--ink-60', 'rgba(20,10,4,.6)', 'Ink 60', 'Secondary text.')]
TYPE = [('t-h1', 'H1 hero', 'Clash Display 700, 64 / 68 (48 / 52 on phones)', "India's college fests"),
        ('t-h2', 'H2 section', 'Clash Display 600, 48 / 52', 'FESTS &amp; EVENTS'),
        ('t-h3', 'Heading 24', 'Clash Display 600, 24 / 28', 'Trending Events'),
        ('t-h4', 'Heading 20', 'Clash Display 600 or Satoshi 700, 20 / 24, lead 20 / 28', 'What is FestHey?'),
        ('t-16', 'Body 16', 'Satoshi 400 to 700, 16 / 24', 'Open the fest, pick any event inside it, and hit Register.'),
        ('t-14', 'Body 14', 'Satoshi 500 to 700, 14 / 18 or 14 / 22', 'Main Grounds, MSRIT'),
        ('t-12', 'Body 12', 'Satoshi 700, 12 / 16', 'Bengaluru')]
system = HEAD.format(title='FestHey Design System') + f'''
<main class="ds">
  <header class="ds-hero">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap">
      <img class="ds-logo" src="assets/img/logo.svg" alt="FestHey" width="1024" height="309">
      <h1 class="hero-h">Design <mark class="mark">system</mark></h1>
      <p class="lead">Tokens and components behind the FestHey landing page. Every section is built from these pieces.</p>
    </div>
  </header>
  <section class="ds-sec"><div class="wrap">
    <p class="eyebrow"><span></span>01 Colour</p>
    <div class="ds-swatches">{''.join(f'<div class="ds-sw"><span class="ds-chip" style="background:{v}"></span><b>{n}</b><code>{t}</code><code>{v}</code><small>{u}</small></div>' for t, v, n, u in SW)}</div>
  </div></section>
  <section class="ds-sec"><div class="wrap">
    <p class="eyebrow"><span></span>02 Type</p>
    <div class="ds-type">{''.join(f'<div class="ds-row"><div class="ds-meta"><b>{n}</b><small>{d}</small></div><div class="ds-{c}">{s}</div></div>' for c, n, d, s in TYPE)}</div>
    <div class="ds-row"><div class="ds-meta"><b>Highlight</b><small>.mark: a straight marker band behind the words, never tilted</small></div><div class="ds-t-h2">India's <mark class="mark">college fests</mark></div></div>
    <div class="ds-row"><div class="ds-meta"><b>Rules</b><small>Every size, space, radius and border is a multiple of 2. Line height is font size + 4 or + 8.</small></div><div class="ds-t-14">12 / 16 &nbsp; 14 / 18 &nbsp; 16 / 24 &nbsp; 20 / 24 &nbsp; 24 / 28 &nbsp; 48 / 52 &nbsp; 64 / 68</div></div>
  </div></section>
  <section class="ds-sec"><div class="wrap">
    <p class="eyebrow"><span></span>03 Buttons and chips</p>
    <div class="ds-comp">
      {btn('Primary', '#', 'primary')} {btn('Ink', '#', 'ink')} <span class="ds-on-orange">{btn('Light', '#', 'light')}</span> {btn('Small', '#', 'ink', 'sm')}
      <button class="icon-btn" aria-label="Previous">{ic('left')}</button><button class="icon-btn icon-btn--ink" aria-label="Next">{ic('right')}</button>
    </div>
    <div class="ds-comp">
      <span class="chip">Cultural</span><span class="chip is-on">All Categories</span><span class="chip chip--light">Dec 5 to Dec 6</span><span class="ds-on-photo"><span class="chip chip--glass">Bengaluru</span></span><span class="chip chip--ink">AD</span>
    </div>
  </div></section>
  <section class="ds-sec"><div class="wrap">
    <p class="eyebrow"><span></span>04 Radius, shadow, spacing</p>
    <div class="ds-comp ds-boxes">
      <div class="ds-box" style="border-radius:var(--r-sm)"><b>r-sm</b>12</div>
      <div class="ds-box" style="border-radius:var(--r-md)"><b>r-md</b>16</div>
      <div class="ds-box" style="border-radius:var(--r-lg)"><b>r-lg</b>24</div>
      <div class="ds-box" style="border-radius:var(--r-pill)"><b>pill</b>100</div>
      <div class="ds-box" style="box-shadow:var(--sh-1)"><b>sh-1</b>cards</div>
      <div class="ds-box" style="box-shadow:var(--sh-2)"><b>sh-2</b>lifted</div>
    </div>
    <p class="ds-note">Spacing steps: 4, 8, 12, 16, 24, 32, 48, 64, 96, 140. Sections breathe at 96 to 140. Content max width 1440 with a 16 to 56 gutter. Borders are 2.</p>
  </div></section>
  <section class="ds-sec"><div class="wrap">
    <p class="eyebrow"><span></span>05 Cards</p>
    <div class="ds-cards">
      <div class="fests ds-one">{fest(FESTS[0])}</div>
      <div class="ev-row v-ticket ds-one">{evc(EVENTS[0], 0)}</div>
      <div class="ev-row v-calendar ds-one">{evc(EVENTS[3], 3)}</div>
      <div class="ev-row v-poster ds-one">{evc(EVENTS[5], 5)}</div>
    </div>
  </div></section>
  <section class="ds-sec"><div class="wrap">
    <p class="eyebrow"><span></span>06 Texture and motion</p>
    <p class="ds-note">A fine grain sits over the whole page and a heavier grain over the orange and yellow sections. Real-world objects (lanyards, phones, hands, paper, tape, pegs) are photographed cut-outs, never illustrations of them. Motion is physical: things hang, swing and settle with springs; nothing slides in without a reason.</p>
  </div></section>
</main>
</body>
</html>
'''

for name, html_ in (('index.html', page), ('system.html', system)):
    open(f'{ROOT}/{name}', 'w').write(html_)
    bad = [ch for ch in ('—', '–') if ch in html_]
    print('wrote', name, len(html_), 'dashes:', bad)
