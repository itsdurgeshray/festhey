#!/usr/bin/env python3
"""FestHey fest detail page (fest.html). Run: python3 assets/src/fest_page.py"""
import os, runpy, html
import runpy as _rp
_LU = _rp.run_path('/Users/durgesh/Desktop/WFT/festhey/assets/src/icons.py')
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
B = runpy.run_path(os.path.join(ROOT, 'assets/src/build.py'))
L = runpy.run_path(os.path.join(ROOT, 'assets/src/fests_page.py'))
ic, btn, HEAD, NAV, FESTS, EVENTS, FAQ, BASE, evc, qa = B['ic'], B['btn'], B['HEAD'], B['NAV'], B['FESTS'], B['EVENTS'], B['FAQ'], B['BASE'], B['evc'], B['qa']
icx, card, FOOT = L['icx'], L['card'], L['FOOT']
e = html.escape
ICY = {
 'share': '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
 'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 'ticket': '<path d="M2 9a3 3 0 0 0 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 0 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2M13 17v2M13 11v2"/>',
 'nav': '<path d="m3 11 19-9-9 19-2-8-8-2z"/>',
}
def icy(n, c='ic'):
    return _LU['svg'](n, c)

F = FESTS[0]  # 8th Mile Encore
TABS = [('events', 'Events'), ('schedule', 'Schedule'), ('about', 'About'), ('venue', 'Venue'), ('gallery', 'Gallery'), ('faqs', 'FAQs')]
DAYS = [('Day 1', 'Friday, Dec 5', [('10:00', 'Inauguration and opening act', 'Main Stage'), ('11:30', EVENTS[1][1], EVENTS[1][3]), ('14:00', EVENTS[2][1], EVENTS[2][3]), ('19:00', 'Pro-night', 'Main Grounds')]),
        ('Day 2', 'Saturday, Dec 6', [('10:00', EVENTS[0][1], EVENTS[0][3]), ('13:00', EVENTS[4][1], EVENTS[4][3]), ('16:00', EVENTS[3][1], EVENTS[3][3]), ('18:30', 'Prize distribution', 'Main Stage')])]
GALLERY = ['pronite', 'dance', 'hoops', 'quiz', 'hack', 'robo']

TABHTML = ''.join(('<a href="#%s" class="on">%s</a>' if i == 'events' else '<a href="#%s">%s</a>') % (i, t) for i, t in TABS)

def fact(icon, label, val, cls=''):
    return f'<div class="fd-fact {cls}"><span class="fd-fact-ic">{icon}</span><span><small>{label}</small><b>{val}</b></span></div>'

events = ''.join(evc(t, i) for i, t in enumerate(EVENTS[:6]))
sched = ''.join(f'''<div class="fd-day"><div class="fd-day-h"><span class="chip chip--ink">{d}</span><b>{date}</b></div>
          <ol class="fd-tl">{''.join(f'<li><time>{t}</time><span><b>{e(n)}</b><small>{e(v)}</small></span></li>' for t, n, v in items)}</ol></div>''' for d, date, items in DAYS)
gallery = ''.join(f'<figure class="fd-g fd-g{i+1}"><img src="assets/img/v4/{g}.jpg" alt="" width="800" height="1200" loading="lazy"></figure>' for i, g in enumerate(GALLERY))
similar = ''.join(card(f, i + 1) for i, f in enumerate(FESTS[1:4]))

page = HEAD.format(title=f'{F[0]} | FestHey') + '<link rel="stylesheet" href="assets/fests.css"><link rel="stylesheet" href="assets/fest.css">\n' + NAV + f'''
<main class="fd">
  <!-- ============ HERO ============ -->
  <section class="fd-hero">
    <img class="fd-hero-img" src="assets/img/fests/{F[5]}.jpg" alt="" width="1280" height="720">
    <span class="fd-hero-shade"></span><span class="grain" aria-hidden="true"></span>
    <div class="wrap fd-hero-in">
      <nav class="fd-crumb" aria-label="Breadcrumb"><a href="fests.html">Fests</a>{ic('right', 'ic ic-xs')}<span>{e(F[0])}</span></nav>
      <div class="fd-hero-copy">
        <p class="eyebrow fd-loc"><span></span>Bengaluru, Karnataka</p>
        <h1 class="hero-h">{e(F[0])}</h1>
        <div class="fd-tags"><span class="chip chip--sun">Cultural</span><span class="chip chip--glass">{icy('cal', 'ic ic-xs')}{F[1]} to {F[2]}, 2026</span><span class="chip chip--glass">{F[3]} Events</span></div>
        <p class="lead fd-intro">Two days of music, dance, poetry and pro-nights at one of Bengaluru's biggest campus fests.</p>
      </div>
      <div class="fd-actions">
        <button class="fd-iconbtn fd-save" aria-pressed="false">{icx('bookmark', 'ic ic-s')}<span>Save</span></button>
        <button class="fd-iconbtn fd-share">{icy('share', 'ic ic-s')}<span>Share</span></button>
      </div>
    </div>
  </section>

  <!-- ============ KEY FACTS ============ -->
  <div class="wrap fd-facts-wrap">
    <div class="fd-facts">
      {fact(icx('clock', 'ic ic-s'), 'Registration closes', 'Dec 4, 2026', 'fd-fact--hot')}
      {fact(icy('cal', 'ic ic-s'), 'Starts', 'Dec 5, 2026')}
      {fact(icy('cal', 'ic ic-s'), 'Ends', 'Dec 6, 2026')}
      {fact(icy('ticket', 'ic ic-s'), 'Entry', 'From ₹0 / Member')}
      <a class="btn btn--primary fd-cta" href="#events">View Events<span class="dot">{ic('arrow')}</span></a>
    </div>
  </div>

  <!-- ============ IN-PAGE TABS ============ -->
  <nav class="fd-tabs" aria-label="On this page"><div class="wrap fd-tabs-in">{TABHTML}</div></nav>

  <!-- ============ EVENTS ============ -->
  <section class="wrap fd-sec" id="events">
    <div class="fd-head"><div><p class="eyebrow"><span></span>Fest Events</p><h2>PICK YOUR STAGE</h2></div><span class="fd-count"><b class="fd-n">6</b> events</span></div>
    <div class="fd-bar">
      <label class="lb-search">{icx('search')}<input type="search" placeholder="Search events" aria-label="Search events"></label>
      <label class="sel"><select class="fd-cat" aria-label="Category"><option value="all">All Categories</option><option value="cultural">Cultural</option><option value="technical">Technical</option><option value="quiz">Quiz</option></select>{icx('chev', 'ic ic-s')}</label>
      <label class="sel"><select class="fd-sort" aria-label="Sort by"><option value="date">Sort by date</option><option value="price">Price, low to high</option><option value="name">Name, A to Z</option></select>{icx('chev', 'ic ic-s')}</label>
      <label class="fd-free"><input type="checkbox"><span class="ck-box">{ic('check')}</span>Free only</label>
    </div>
    <div class="ev-row v-ticket fd-events">{events}</div>
    <p class="lb-empty" hidden>No events match. Try another category.</p>
  </section>

  <!-- ============ SCHEDULE ============ -->
  <section class="fd-band" id="schedule">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap fd-sec-in">
      <div class="fd-head"><div><p class="eyebrow eyebrow--ink"><span></span>Schedule</p><h2>TWO DAYS, ZERO CHILL.</h2></div></div>
      <div class="fd-days">{sched}</div>
    </div>
  </section>

  <!-- ============ ABOUT + ORGANISER ============ -->
  <section class="wrap fd-sec fd-about" id="about">
    <div class="fd-about-copy">
      <p class="eyebrow"><span></span>About the fest</p>
      <h2>TWO DAYS. {F[3]} EVENTS. <mark class="mark">ONE CAMPUS.</mark></h2>
      <p class="fd-about-p">8th Mile Encore brings students from colleges across Bengaluru together for competitions, performances and late-night music. Register for as many events as you like, as long as their schedules don&rsquo;t clash.</p>
      <div class="fd-expect">
        <div class="fx fx--o"><span class="fx-ic">{icy('trophy')}</span><b>Competitions</b><small>Robotics, hackathons and quizzes with cash prizes</small></div>
        <div class="fx fx--s"><span class="fx-ic">{icy('mic')}</span><b>Performances</b><small>Dance battles, slam poetry and stand-up sets</small></div>
        <div class="fx fx--i"><span class="fx-ic">{icy('music')}</span><b>Pro-nights</b><small>Headline music to close both days</small></div>
        <div class="fx fx--w"><span class="fx-ic">{icy('users')}</span><b>Team events</b><small>Invite your squad by link before checkout</small></div>
      </div>
      <ul class="fd-highs">
        <span class="grain" aria-hidden="true"></span>
        <li><b>{F[3]}</b><span>Events</span></li><li><b>2</b><span>Days</span></li><li><b>&#8377;0</b><span>Lowest entry</span></li><li><b>2</b><span>Pro-nights</span></li>
      </ul>
    </div>
    <aside class="fd-org">
      <div class="fd-org-ph"><img src="assets/img/fests/gallery-stage.jpg" alt="" width="1280" height="720"><span class="chip chip--sun">Host college</span></div>
      <div class="fd-org-in">
        <div class="fd-org-top"><span class="fd-org-av">RV</span><span><b>R V College of Engineering</b><small>{icx('pin', 'ic ic-xs')}Bengaluru, Karnataka</small></span></div>
        <p class="fd-org-p">Questions about an event, refunds or teams? The organising college handles them directly.</p>
        <div class="fd-org-cta">{btn('Contact Organiser', BASE + '/help', 'ink', 'sm')}<a class="fd-link" href="{BASE}/colleges">View college{ic('arrow', 'ic ic-xs')}</a></div>
      </div>
    </aside>
  </section>

  <!-- ============ VENUE ============ -->
  <section class="wrap fd-sec fd-venue" id="venue">
    <div class="fd-map" aria-hidden="true"><span class="fd-map-grid"></span><span class="fd-pin">{icx('pin')}</span><span class="chip chip--light fd-map-tag">Main Grounds</span></div>
    <div class="fd-venue-copy">
      <p class="eyebrow"><span></span>Venue</p>
      <h2>HOW TO GET THERE</h2>
      <p class="fd-addr"><b>R V College of Engineering</b><span>Mysore Road, Bengaluru, Karnataka</span></p>
      <ul class="fd-tips"><li>Carry your college ID and the registration email for entry.</li><li>Gates open 30 minutes before the first event each day.</li><li>Event venues inside campus are listed on each event card.</li></ul>
      {btn('Get Directions', 'https://maps.google.com/?q=R+V+College+of+Engineering+Bengaluru', 'ink')}
    </div>
  </section>

  <!-- ============ GALLERY ============ -->
  <section class="wrap fd-sec" id="gallery">
    <div class="fd-head"><div><p class="eyebrow"><span></span>Gallery</p><h2>LAST YEAR AT THE FEST</h2></div></div>
    <div class="fd-gallery">{gallery}</div>
  </section>

  <!-- ============ FAQS ============ -->
{B['faq_block']([FAQ[1], FAQ[2], FAQ[3], FAQ[6]], 'BEFORE YOU REGISTER', 'Quick answers about registering, teams and refunds for this fest. Still stuck? Our team replies within a day.', 'faqs')}

  <!-- ============ SIMILAR ============ -->
  <section class="wrap fd-sec" id="similar">
    <div class="fd-head"><div><p class="eyebrow"><span></span>Keep exploring</p><h2>SIMILAR FESTS</h2></div>{btn('All Fests', 'fests.html', 'ink', 'sm')}</div>
    <div class="lb-cards">{similar}</div>
  </section>
</main>

<div class="fd-dock"><span><small>Registration closes</small><b>Dec 4, 2026</b></span><a class="btn btn--primary btn--sm" href="#events">View Events<span class="dot">{ic('arrow')}</span></a></div>
<div class="fd-toast" role="status" aria-live="polite"></div>

{FOOT}

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="assets/site.js"></script>
<script src="assets/fest.js"></script>
</body>
</html>
'''
open(os.path.join(ROOT, 'fest.html'), 'w').write(page)
print('wrote fest.html', len(page), 'dashes:', [c for c in ('—', '–') if c in page])
