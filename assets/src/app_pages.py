#!/usr/bin/env python3
"""FestHey app pages: event.html, team.html, blog.html, article.html (+ 3 modals).
Run: python3 assets/src/app_pages.py"""
import os, runpy, html, random
import runpy as _rp
_LU = _rp.run_path('/Users/durgesh/Desktop/WFT/festhey/assets/src/icons.py')
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
B = runpy.run_path(os.path.join(ROOT, 'assets/src/build.py'))
L = runpy.run_path(os.path.join(ROOT, 'assets/src/fests_page.py'))
FP = runpy.run_path(os.path.join(ROOT, 'assets/src/fest_page.py'))
ic, btn, HEAD, NAV, EVENTS, BASE, evc, AV = B['ic'], B['btn'], B['HEAD'], B['NAV'], B['EVENTS'], B['BASE'], B['evc'], B['AV']
icx, FOOT, PIT, icy = L['icx'], L['FOOT'], L['PIT'], FP['icy']
e = html.escape
def ix(n, c='ic'):
    return _LU['svg'](n, c)
def css(*f):
    return ''.join(f'<link rel="stylesheet" href="assets/{x}.css">' for x in f) + '\n'
SCRIPTS = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="assets/site.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
'''
def fact(icon, label, val, cls=''):
    return f'<div class="fd-fact {cls}"><span class="fd-fact-ic">{icon}</span><span><small>{label}</small><b>{val}</b></span></div>'
def checks(items):
    return '<ul class="ok-list">' + ''.join(f'<li><span class="perk-ic">{ic("check")}</span>{t}</li>' for t in items) + '</ul>'
def crumb(*parts):
    out = []
    for i, (t, h) in enumerate(parts):
        out.append(f'<a href="{h}">{e(t)}</a>' if h else f'<span>{e(t)}</span>')
    return '<nav class="fd-crumb" aria-label="Breadcrumb">' + ic('right', 'ic ic-xs').join(out) + '</nav>'

EV = dict(name='Line Follower Sprint', fest='Brain Wars', fest_href='fest.html', college='M S Ramaiah Institute of Technology', short='MSRIT',
          venue='Main Grounds, MSRIT', date='Dec 30, 2026', time='9:00 AM to 10:30 AM', deadline='Dec 26, 2026', fee=349, team=3, cat='Technical', img='event-robotics-demo')
ELIG = ['Open to undergraduate students of any college in India.', 'A valid college ID card is mandatory for on-campus entry.', 'Teams of exactly 3 members; cross-college teams are allowed.', 'All participants must follow the event code of conduct.']
RULES = ['Robots must be autonomous; no remote control during the run.', 'Maximum robot size 25 by 25 cm, any power source up to 12 V.', 'Each team gets two timed runs; the best run counts.', 'Judges’ decision on track faults is final.']

# ======================= shared bits =======================
import math
def rosette(label, cls=''):
    pts = []
    for k in range(32):
        r = 50 if k % 2 == 0 else 43
        a = math.pi * 2 * k / 32
        pts.append(f'{50 + r * math.cos(a):.1f}% {50 + r * math.sin(a):.1f}%')
    return f'<span class="ros {cls}" aria-hidden="true"><span class="ros-t ros-t1"></span><span class="ros-t ros-t2"></span><span class="ros-b" style="clip-path:polygon({",".join(pts)})"></span><span class="ros-in">{label}</span></span>'
def tiles(items, cls=''):
    return f'<div class="tiles {cls}">' + ''.join(f'<div class="tile"><span class="tile-ic">{ix(i, "ic ic-s")}</span><span><small>{l}</small><b>{v}</b></span></div>' for i, l, v in items) + '</div>'
def avatar(i):
    return f'assets/img/av{i % 4 + 1}.jpg'
FEE_TILES = [('users', 'Team size', f"{EV['team']} members"), ('rupee', 'Fee', f"&#8377;{EV['fee']} / member"), ('cal', 'Event day', EV['date'])]
CONFETTI = ''.join(f'<i style="left:{x}%;top:{y}%;transform:rotate({r}deg)" class="cf cf{c}"></i>' for x, y, r, c in
                   [(4, 18, 20, 1), (12, 70, -30, 2), (22, 30, 60, 3), (78, 22, -14, 1), (88, 64, 40, 2), (94, 30, -50, 3), (48, 8, 12, 2), (62, 86, -24, 1), (34, 88, 34, 3), (70, 46, 70, 3)])

# ======================= modals =======================
AD = f'''
<div class="modal" id="m-ad" role="dialog" aria-modal="true" aria-labelledby="m-ad-h" hidden>
  <div class="modal-back" data-close></div>
  <div class="modal-card modal-ad">
    <img src="assets/img/fests/ad-fest-music.jpg" alt="" width="1280" height="720">
    <span class="modal-ad-shade"></span>
    <div class="m-ad-chips"><span class="chip chip--ink">AD</span><span class="chip chip--light">Three nights, Dec 2026</span></div>
    <button class="modal-x modal-x--glass" data-close aria-label="Close">{ix('close')}</button>
    <div class="m-ad-body">
      <span class="chip chip--sun">{ix('pin', 'ic ic-xs')}B M S College of Engineering</span>
      <h2 id="m-ad-h">Utsav Winter Edition</h2>
      <p>Three nights of music and dance. 7+ events, stand-ups and a headline pro-night.</p>
      <a class="btn btn--primary btn--block" href="fest.html">Check it out<span class="dot">{ic('arrow')}</span></a>
    </div>
  </div>
</div>'''

CREATE = f'''
<div class="modal" id="m-team" role="dialog" aria-modal="true" aria-labelledby="m-team-h" hidden>
  <div class="modal-back" data-close></div>
  <form class="modal-card modal-form" action="team.html" novalidate>
    <button type="button" class="modal-x" data-close aria-label="Close">{ix('close')}</button>
    <p class="eyebrow"><span></span>Step 1 of 2</p>
    <h2 id="m-team-h">NAME YOUR SQUAD</h2>
    <p class="m-sub">You&rsquo;re registering for <b>{EV['name']}</b>. Pick a team name, then invite your members with a link.</p>
    {tiles(FEE_TILES, 'm-tiles')}
    <label class="m-label" for="tn">Team name</label>
    <label class="fld">{ix('users')}<input id="tn" name="team" placeholder="e.g. SpiderTrack" maxlength="24" autocomplete="off" required><span class="fld-n"><b class="m-left">24</b></span></label>
    <p class="m-hint">{ix('lock', 'ic ic-xs')}<span>Team names are locked once created.</span></p>
    <button class="btn btn--primary btn--block m-go" type="submit">Create Team<span class="dot">{ic('arrow')}</span></button>
  </form>
</div>'''

INVITE = f'''
<div class="modal" id="m-invite" role="dialog" aria-modal="true" aria-labelledby="m-inv-h" hidden>
  <div class="modal-back" data-close></div>
  <div class="modal-card modal-invite">
    <div class="inv-top">
      <span class="grain" aria-hidden="true"></span>
      <button class="modal-x modal-x--glass" data-close aria-label="Close">{ix('close')}</button>
      <div class="inv-from"><img src="{avatar(0)}" alt="" width="40" height="40"><span><b>Rohan Verma</b> invited you to join</span></div>
      <h2 id="m-inv-h">SPIDERTRACK</h2>
      <span class="chip chip--sun">{ix('ticket', 'ic ic-xs')}{EV['name']} &middot; {EV['fest']}</span>
    </div>
    <div class="inv-cut" aria-hidden="true"></div>
    <div class="inv-body">
      <div class="inv-squad">
        <span class="inv-sl"><img src="{avatar(0)}" alt="" width="56" height="56"><small>Rohan</small></span>
        <span class="inv-sl"><img src="{avatar(1)}" alt="" width="56" height="56"><small>Sai</small></span>
        <span class="inv-sl inv-you"><span>{ix('plus')}</span><small>You</small></span>
      </div>
      <p class="inv-left">1 spot left in this team</p>
      {tiles([('cal', 'Event day', EV['date']), ('rupee', 'Your share', f"&#8377;{EV['fee']}")], 'm-tiles m-tiles--2')}
      <a class="btn btn--primary btn--block" href="team.html?state=complete">Join SpiderTrack<span class="dot">{ic('arrow')}</span></a>
      <p class="m-secure">{ix('shield', 'ic ic-xs')}You&rsquo;ll pay your share securely after joining</p>
    </div>
  </div>
</div>'''
MODALS = AD + CREATE + INVITE

# ======================= event page =======================
others = ''.join(evc(t, i) for i, t in enumerate(EVENTS[1:7]))
REVIEWS = [('Ananya Kulkarni', 'BMSCE', 5, 'Track was clean and the judges explained every fault on the spot. Second-run timing felt completely fair, and the crowd at the finish line was unreal.', 'Winner, 2025'),
           ('Mohit Sharma', 'RVCE', 5, 'Quick check-in and a well-run pit. Bring spare batteries; the charging queue got long before the finals.', 'Finalist'),
           ('Divya Rao', 'PES University', 4, 'Loved the surprise section. Wish the practice track had opened an hour earlier.', 'Participant')]
def stars(n):
    return '<span class="stars" aria-label="' + str(n) + ' out of 5">' + ''.join(ix('star', 'ic ic-xs' + (' off' if k >= n else '')) for k in range(5)) + '</span>'
reviews = ''.join(f'''<article class="rv{' rv--big' if k == 0 else ''}"><span class="rv-q">{ix('quote')}</span>{stars(s)}<p>{t}</p><div class="rv-by"><img src="{avatar(k + 1)}" alt="" width="40" height="40"><span><b>{n}</b><small>{c}</small></span><span class="chip chip--light">{tag}</span></div></article>''' for k, (n, c, s, t, tag) in enumerate(REVIEWS))
DIST = [(5, 78), (4, 16), (3, 4), (2, 2), (1, 0)]
dist = ''.join(f'<li><span>{n}</span>{ix("star", "ic ic-xs")}<span class="bar"><i style="width:{p}%"></i></span><small>{p}%</small></li>' for n, p in DIST)
EV_FAQ = [('Can I register alone for a team event?', 'Create a team with just yourself, then share the invite link. Your spot is held once you pay your share, and the team locks when it is full.'),
          ('What if a teammate never joins?', 'If your team is not full by the registration deadline, unpaid shares are released and paid members are refunded to their original payment method.'),
          ('Can members be from different colleges?', 'Yes. Cross-college teams are welcome; every member needs their own valid college ID at the venue.'),
          ('Is the fee refundable?', 'Fees are refundable up to 48 hours before the event. After that the organiser&rsquo;s refund policy applies.')]

ev_page = HEAD.format(title=f"{EV['name']} | {EV['fest']} | FestHey") + css('fests', 'fest', 'app') + NAV + f'''
<main class="fd ev" data-state="open">
  <section class="fd-hero">
    <img class="fd-hero-img" src="assets/img/fests/{EV['img']}.jpg" alt="" width="1280" height="720">
    <span class="fd-hero-shade"></span><span class="grain" aria-hidden="true"></span>
    <div class="wrap fd-hero-in">
      {crumb(('Fests', 'fests.html'), (EV['fest'], EV['fest_href']), (EV['name'], None))}
      <div class="fd-hero-copy">
        <p class="eyebrow fd-loc"><span></span>{EV['venue']}</p>
        <h1 class="hero-h">{EV['name']}</h1>
        <div class="fd-tags"><span class="chip chip--sun">{EV['cat']}</span><span class="chip chip--glass">{icy('cal', 'ic ic-xs')}{EV['date']}</span><span class="chip chip--glass">{ix('users', 'ic ic-xs')}Team of {EV['team']}</span></div>
      </div>
      <div class="fd-actions">
        <button class="fd-iconbtn fd-save" aria-pressed="false">{icx('bookmark', 'ic ic-s')}<span>Save</span></button>
        <button class="fd-iconbtn fd-share">{icy('share', 'ic ic-s')}<span>Share</span></button>
      </div>
    </div>
  </section>

  <div class="wrap fd-facts-wrap">
    <div class="fd-facts">
      {fact(icx('clock', 'ic ic-s'), 'Registration closes', EV['deadline'], 'fd-fact--hot')}
      {fact(ix('users', 'ic ic-s'), 'Team size', f"{EV['team']} members")}
      {fact(icy('cal', 'ic ic-s'), 'Time', EV['time'])}
      {fact(icy('ticket', 'ic ic-s'), 'Fee', f"&#8377;{EV['fee']}.00 / Member")}
      <button class="btn btn--primary fd-cta st-open" data-open="m-team">Register<span class="dot">{ic('arrow')}</span></button>
      <a class="btn btn--sun fd-cta st-pending" href="team.html">Complete Registration<span class="dot">{ic('arrow')}</span></a>
      <a class="btn btn--ink fd-cta st-done" href="team.html?state=complete">View Ticket<span class="dot">{ic('arrow')}</span></a>
    </div>
    <p class="st-banner st-pending">{ix('info', 'ic ic-s')}<span>Your team <b>SpiderTrack</b> has 1 of 3 members. Invite your squad and pay before Dec 26 to lock your spot.</span></p>
  </div>

  <section class="wrap fd-sec ev-grid">
    <div class="ev-main">
      <p class="eyebrow"><span></span>About the event</p>
      <h2>BUILD IT. RACE IT.</h2>
      <p class="ev-lead">Bring an autonomous robot that follows a black line through curves, crossings and a surprise section. The fastest clean run takes the trophy.</p>
      <div class="chips ev-amen"><span class="chip">{ix('coffee', 'ic ic-s')}Breakfast</span><span class="chip">{ix('wifi', 'ic ic-s')}Free Wi-Fi</span><span class="chip">{ix('drop', 'ic ic-s')}Drinking water</span><span class="chip">{ix('snow', 'ic ic-s')}Air-conditioned pit area</span><span class="chip">{ix('plug', 'ic ic-s')}Charging points</span></div>
      <div class="ev-two">
        <div><h3 class="ev-h">Eligibility</h3>{checks(ELIG)}</div>
        <div><h3 class="ev-h">Rules</h3>{checks(RULES)}</div>
      </div>
    </div>
    <aside class="ev-side">
      <div class="ev-fee">
        <div class="ev-fee-top">
          <span class="chip chip--sun">{ix('hourglass', 'ic ic-xs')}Closes {EV['deadline']}</span>
          <small>Registration fee</small>
          <p class="ev-price"><b>&#8377;{EV['fee']}</b><span>per member</span></p>
          <p class="ev-team">{ix('users', 'ic ic-xs')}Team of {EV['team']} &middot; &#8377;{EV['fee'] * EV['team']:,} for the full team</p>
        </div>
        <div class="ev-fee-cut" aria-hidden="true"></div>
        <div class="ev-fee-bot">
          <ul class="ev-fee-rows"><li><span class="tile-ic">{ix('pin', 'ic ic-xs')}</span>{EV['venue']}</li><li><span class="tile-ic">{ix('cal', 'ic ic-xs')}</span>{EV['date']}</li><li><span class="tile-ic">{ix('clock', 'ic ic-xs')}</span>{EV['time']}</li></ul>
          <button class="btn btn--primary btn--block st-open" data-open="m-team">Register as a team<span class="dot">{ic('arrow')}</span></button>
          <a class="btn btn--sun btn--block st-pending" href="team.html">Complete Registration<span class="dot">{ic('arrow')}</span></a>
          <a class="btn btn--ink btn--block st-done" href="team.html?state=complete">View Ticket<span class="dot">{ic('arrow')}</span></a>
          <button class="ev-invite-demo" data-open="m-invite">{ix('link', 'ic ic-xs')}Got an invite link? Join a team</button>
        </div>
      </div>
      <a class="ev-fest" href="{EV['fest_href']}"><img src="assets/img/fests/gallery-stage.jpg" alt="" width="1280" height="720"><span><small>Part of</small><b>{EV['fest']}</b><em class="chip chip--sun">Dec 30 to Dec 31</em></span>{ic('arrow')}</a>
      <div class="ev-org"><span class="fd-org-av">MS</span><span><small>Organised by</small><b>{EV['college']}</b></span></div>
    </aside>
  </section>

  <section class="ev-prize" id="prizes">
    <span class="grain" aria-hidden="true"></span>
    <span class="ev-rays" aria-hidden="true"></span>
    <div class="ev-conf" aria-hidden="true">{CONFETTI}</div>
    <div class="ev-tape" aria-hidden="true"><div>{'<span>Prize pool &#8377;75,000</span><span>&#9733;</span><span>Trophies</span><span>&#9733;</span><span>Internship interviews</span><span>&#9733;</span>' * 4}</div></div>
    <div class="wrap ev-prize-in">
      <div class="ev-prize-head"><p class="eyebrow eyebrow--ink"><span></span>Prize pool</p><h2>RACE FOR <mark class="mark mark--snow">&#8377;75,000</mark></h2></div>
      <div class="prizes">
        <div class="prz prz--2">{rosette('2<sup>nd</sup>', 'ros--snow')}<small>Runner up</small><b>&#8377;15,000</b><p>Merch kit and cloud credits</p></div>
        <div class="prz prz--1">{rosette(ix('crown'), 'ros--orange')}<small>Grand prize</small><b>&#8377;50,000</b><p>Golden trophy and internship interviews</p><span class="prz-stamp">Winner takes all</span></div>
        <div class="prz prz--3">{rosette('3<sup>rd</sup>', 'ros--snow')}<small>Third place</small><b>&#8377;10,000</b><p>Tech goodies and certificates</p></div>
      </div>
      <p class="ev-prize-note">{ix('medal', 'ic ic-xs')}Every finisher gets a participation certificate. Terms and conditions apply.</p>
    </div>
  </section>

  <section class="wrap fd-sec ev-rv">
    <div class="rv-sum">
      <p class="eyebrow"><span></span>Reviews</p>
      <h2>WHAT TEAMS SAID</h2>
      <div class="rv-score-big"><b>4.7</b><span>{stars(5)}<small>38 reviews from 2025</small></span></div>
      <ul class="rv-dist">{dist}</ul>
      <a class="btn btn--ink btn--block" href="#">Add your review<span class="dot">{ix('star')}</span></a>
    </div>
    <div class="rv-grid">{reviews}</div>
  </section>

  <section class="fd-sec ev-more">
    <div class="wrap"><div class="fd-head"><div><p class="eyebrow"><span></span>Also at {EV['fest']}</p><h2>MORE EVENTS</h2></div>{btn('View Fest', EV['fest_href'], 'ink', 'sm')}</div></div>
    <div class="ev-track"><div class="ev-row v-ticket">{others}</div></div>
  </section>
{B['faq_block'](EV_FAQ, 'TEAM EVENT QUESTIONS', 'Everything about teams, invites and refunds for this event. Still unsure? Our team replies within a day.', 'faq')}
</main>
<div class="fd-dock st-open"><span><small>&#8377;{EV['fee']}.00 / Member</small><b>Closes {EV['deadline']}</b></span><button class="btn btn--primary btn--sm" data-open="m-team">Register<span class="dot">{ic('arrow')}</span></button></div>
<div class="fd-toast" role="status" aria-live="polite"></div>
{MODALS}
{FOOT}
''' + SCRIPTS

# ======================= team page =======================
def qr_svg(seed=7, n=25):
    random.seed(seed); cells = []
    def finder(x, y):
        return f'<rect x="{x}" y="{y}" width="7" height="7" fill="#140A04"/><rect x="{x+1}" y="{y+1}" width="5" height="5" fill="#fff"/><rect x="{x+2}" y="{y+2}" width="3" height="3" fill="#140A04"/>'
    for yy in range(n):
        for xx in range(n):
            if (xx < 8 and yy < 8) or (xx > n - 9 and yy < 8) or (xx < 8 and yy > n - 9):
                continue
            if random.random() < .48:
                cells.append(f'<rect x="{xx}" y="{yy}" width="1" height="1"/>')
    return f'<svg class="qr" viewBox="-2 -2 {n+4} {n+4}" role="img" aria-label="Entry QR code"><rect x="-2" y="-2" width="{n+4}" height="{n+4}" fill="#fff"/><g fill="#140A04">{"".join(cells)}</g>{finder(0,0)}{finder(n-7,0)}{finder(0,n-7)}</svg>'

MEM = [('Rohan Verma', 'Captain', 0), ('Sai Vani', 'Member', 1), ('Reshma Gouri', 'Member', 2)]
def seat(k):
    n, r, a = MEM[k]
    you = '<span class="seat-you">You</span>' if k == 0 else ''
    paid = f'<span class="seat-ok">{ix("check", "ic ic-xs")}</span>'
    filled = f'<div class="seat{" st-done" if k else ""}"><span class="seat-ph"><img src="{avatar(a)}" alt="" width="96" height="96">{paid}</span><b>{n}</b><small>{r}</small>{you}</div>'
    empty = '' if k == 0 else f'<button class="seat seat--open st-pending" data-copy="https://festhey.in/t/spidertrack-4kq9"><span class="seat-ph">{ix("plus")}</span><b>Spot {k + 1}</b><small>Tap to copy invite</small></button>'
    return filled + empty
link = 'festhey.in/t/spidertrack-4kq9'
STEPS = [('Team created', 'SpiderTrack is yours. The name is locked.', 'done'),
         ('Invite your squad', 'Share the link. 2 spots are still open.', 'now'),
         ('Everyone pays their share', '&#8377;349 each, before Dec 26.', 'next'),
         ('Get your entry pass', 'A QR pass for each member, sent by email.', 'next')]
steps = ''.join(f'<li class="step step--{st}"><span class="step-n">{ix("check", "ic ic-xs") if st == "done" else i + 1}</span><span><b>{t}</b><small>{d}</small></span></li>' for i, (t, d, st) in enumerate(STEPS))

team_page = HEAD.format(title='SpiderTrack | Team | FestHey') + css('fests', 'fest', 'app') + NAV + f'''
<main class="tm" data-state="pending">
  <section class="tm-hero">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap tm-hero-in">
      {crumb((EV['fest'], EV['fest_href']), (EV['name'], 'event.html'), ('Your team', None))}
      <div class="tm-title">
        <span class="chip chip--sun st-pending">{ix('hourglass', 'ic ic-xs')}Waiting for 2 members</span>
        <span class="chip chip--sun st-done">{ix('okc', 'ic ic-xs')}Registration confirmed</span>
        <h1 class="hero-h">SPIDERTRACK</h1>
        <p class="tm-sub">{ix('ticket', 'ic ic-xs')}{EV['name']} &middot; {EV['fest']} &middot; {EV['date']}</p>
      </div>
      <div class="squad">
        <div class="squad-h"><b><span class="st-pending">1</span><span class="st-done">3</span> of 3 joined</b><span class="st-pending">2 spots left</span><span class="st-done">Team locked</span></div>
        <div class="seats">{''.join(seat(k) for k in range(3))}</div>
        <span class="squad-bar"><i></i></span>
      </div>
    </div>
  </section>

  <section class="wrap tm-grid">
    <div class="tm-main">
      <div class="epass st-done">
        <div class="epass-main">
          <p class="eyebrow"><span></span>Entry pass</p>
          <h2>SEE YOU AT THE TRACK</h2>
          {tiles([('hash' if False else 'ticket', 'Registration ID', 'FH-BW-26-4KQ9'), ('receipt', 'Order ID', 'order_N7c2Xk91'), ('clock', 'Check-in', f"{EV['date']}, 8:30 AM"), ('pin', 'Venue', EV['venue'])], 'epass-tiles')}
        </div>
        <div class="epass-stub"><div class="tm-qr">{qr_svg()}</div><small>Show at the gate</small></div>
      </div>

      <div class="card st-pending">
        <div class="card-h"><h3 class="ev-h">Your next steps</h3><span class="chip chip--sun">Step 2 of 4</span></div>
        <ol class="steps">{steps}</ol>
        <div class="invite">
          <div class="copy"><span class="copy-ic">{ix('link', 'ic ic-s')}</span><span class="copy-url">{link}</span><button class="btn btn--ink btn--sm copy-btn" data-copy="https://{link}">Copy<span class="dot dot--still">{ix('copy')}</span></button></div>
          <div class="invite-cta"><a class="btn btn--wa" href="https://wa.me/?text=Join%20my%20team%20SpiderTrack%20on%20FestHey%3A%20https%3A%2F%2F{link}" target="_blank" rel="noopener">Share on WhatsApp<span class="dot dot--still">{ix('wa')}</span></a><button class="btn btn--light" data-open="m-invite">Preview invite<span class="dot dot--still">{ix('eye')}</span></button></div>
        </div>
      </div>

      <div class="card ev-card">
        <img src="assets/img/fests/{EV['img']}.jpg" alt="" width="1280" height="720">
        <div class="ev-card-in">
          <div class="card-h"><div><small class="ev-card-k">The event</small><h3 class="ev-h">{EV['name']}</h3></div>{btn('Event page', 'event.html', 'light', 'sm')}</div>
          {tiles([('school', 'College', EV['short']), ('pin', 'Venue', EV['venue']), ('cal', 'Date', EV['date']), ('clock', 'Time', EV['time'])], 'tiles--4')}
        </div>
      </div>
      <div class="ev-two"><div><h3 class="ev-h">Eligibility</h3>{checks(ELIG)}</div><div><h3 class="ev-h">Rules</h3>{checks(RULES)}</div></div>
    </div>

    <aside class="tm-side">
      <div class="pay">
        <div class="pay-h"><span class="tile-ic">{ix('receipt', 'ic ic-s')}</span><b class="st-pending">Your share</b><b class="st-done">Order summary</b><span class="chip chip--light st-done">Paid</span></div>
        <p class="pay-big st-pending"><b>&#8377;359.47</b><small>due by {EV['deadline']}</small></p>
        <dl class="sum">
          <div><dt>Registration</dt><dd><span class="st-pending">&#8377;349.00 &times; 1</span><span class="st-done">&#8377;349.00 &times; 3</span></dd></div>
          <div><dt>Convenience fee</dt><dd><span class="st-pending">&#8377;10.47</span><span class="st-done">&#8377;31.41</span></dd></div>
          <div class="st-done"><dt>Paid with</dt><dd>Razorpay, UPI</dd></div>
          <div class="sum-total st-done"><dt>Total</dt><dd>&#8377;1,078.41</dd></div>
        </dl>
        <a class="btn btn--primary btn--block st-pending" href="team.html?state=complete">Pay my share<span class="dot">{ic('arrow')}</span></a>
        <p class="m-secure st-pending">{ix('shield', 'ic ic-xs')}Each member pays their own share</p>
        <div class="dl st-done"><a class="btn btn--ink btn--block" href="#">Download Ticket<span class="dot dot--still">{ix('download')}</span></a><a class="btn btn--light btn--block" href="#">Download Receipt<span class="dot dot--still">{ix('download')}</span></a></div>
      </div>
      <div class="help"><span class="tile-ic">{ix('msg', 'ic ic-s')}</span><span><b>Need a hand?</b><small>Teams, refunds or payments</small></span><a class="lc-go" href="https://festhey.agpro.co.in/help" aria-label="Get help">{ic('arrow')}</a></div>
    </aside>
  </section>
</main>
<div class="fd-toast" role="status" aria-live="polite"></div>
{INVITE}
{FOOT}
''' + SCRIPTS

# ======================= blog =======================
POSTS = [
  ('cultural', 'Cultural', 'How to survive a three-night college fest', 'Sleep, snacks and squad plans: a practical guide to getting the most from Utsav, 8th Mile and every big fest in between.', 'pronite', 6),
  ('technical', 'Technical', 'Line follower robots: what wins on race day', 'We asked three winning teams what separates a clean run from a crash at the first crossing.', 'robo', 8),
  ('hackathon', 'Hackathon', 'Your first overnight hackathon, hour by hour', 'From idea at 10 PM to a demo at 8 AM: pacing, roles and the pitch that judges remember.', 'hack', 7),
  ('sports', 'Sports', 'Inter-college athletics: a beginner’s calendar', 'The meets worth training for this winter, and how registrations usually open.', 'hoops', 5),
  ('quiz', 'Quiz', 'The quiz circuit, explained', 'General, India, pop culture: how campus quizzes are formatted and how to build a team.', 'quiz', 6),
  ('cultural', 'Cultural', 'Picking the right fest for your crew', 'Location, duration, entry fees and vibe: a simple checklist before you register.', 'dance', 4),
  ('technical', 'Technical', 'What organisers wish participants knew', 'Deadlines, IDs, team rules and refunds, straight from the people running the fests.', 'fest-technical', 5),
]
def pimg(p):
    return f'assets/img/v4/{p}.jpg' if os.path.exists(os.path.join(ROOT, f'assets/img/v4/{p}.jpg')) else f'assets/img/fests/{p}.jpg'
def post(p, big=False):
    k, cat, t, d, img, mins = p
    return f'''<a class="post" href="article.html" data-cat="{k}" data-name="{e(t.lower())}"><span class="post-ph"><img src="{pimg(img)}" alt="" width="800" height="1200" loading="lazy"></span><span class="post-meta"><span class="chip chip--light">{cat}</span><small>{mins} min read</small></span><b class="post-t">{e(t)}</b><span class="post-d">{e(d)}</span></a>'''
feat = POSTS[0]
bchips = '<button class="chip is-on" data-cat="all" aria-pressed="true">All</button>' + ''.join(f'<button class="chip" data-cat="{k}" aria-pressed="false">{l}</button>' for k, l in [('cultural', 'Cultural'), ('technical', 'Technical'), ('sports', 'Sports'), ('quiz', 'Quiz'), ('hackathon', 'Hackathon')])
blog_page = HEAD.format(title='Blog | FestHey') + css('fests', 'fest', 'app') + NAV + f'''
<main class="bl">
  <section class="lh">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap lh-in bl-hero">
      <div class="lh-copy"><p class="eyebrow eyebrow--ink"><span></span>Stories from campus</p><h1 class="hero-h">BLOG &amp; <mark class="mark">ARTICLES</mark></h1><p class="lead lh-p">Guides, recaps and playbooks for students and organisers on India&rsquo;s fest circuit.</p></div>
      <a class="bl-feat" href="article.html"><img src="{pimg(feat[4])}" alt="" width="800" height="1200"><span class="lf-shade"></span><span class="bl-feat-body"><span class="chip chip--sun">Editor&rsquo;s pick</span><b>{e(feat[2])}</b><small>{feat[5]} min read</small></span></a>
    </div>
  </section>
  <section class="wrap lb bl-list">
    <div class="lb-bar"><label class="lb-search">{icx('search')}<input type="search" placeholder="Search articles" aria-label="Search articles"></label><div class="chips lb-chips" role="group" aria-label="Topics">{bchips}</div></div>
    <div class="bl-grid">{''.join(post(p) for p in POSTS[1:])}</div>
    <p class="lb-empty" hidden>No articles match yet.</p>
    <div class="lb-pager"><span class="lb-count">Showing <b class="lb-n">{len(POSTS) - 1}</b> articles</span><nav class="lb-pages" aria-label="Pages"><button class="icon-btn icon-btn--sm" disabled aria-label="Previous">{ic('left')}</button><button class="lb-pg is-on">1</button><button class="icon-btn icon-btn--sm" disabled aria-label="Next">{ic('right')}</button></nav></div>
  </section>
{PIT}</main>
<div class="fd-toast" role="status" aria-live="polite"></div>
{FOOT}
''' + SCRIPTS

# ======================= article =======================
SECTIONS = [
 ('sleep', 'Plan your nights before day one', ['Three-night fests are marathons. Pick the two headline nights you care most about and treat the third as optional. Most regret comes from burning out on night one.', 'Check the schedule on the fest page and add the events you want to your saved list, so reminders arrive on your registered email.']),
 ('squad', 'Sort the squad and the money', ['Team events need every member registered before checkout. Create the team early, share the invite link, and let each person pay their own share.', 'Where there is a fee, the amount and the convenience fee are shown before you pay, so there are no surprises.']),
 ('kit', 'Pack like a regular', ['College ID, a power bank, a refillable bottle and cash for food stalls. Many campuses ask for ID at every gate, not just the first one.']),
 ('after', 'After the last act', ['Plan the ride home before the pro-night ends. Campus gates get crowded, and cabs surge right after the final encore.', 'Leave a review of the events you joined. It helps organisers improve and helps next year’s students pick well.']),
]
toc = ''.join(f'<a href="#{i}">{t}</a>' for i, t, _ in SECTIONS)
body = ''.join(f'<h2 id="{i}">{t}</h2>' + ''.join(f'<p>{x}</p>' for x in ps) + ('<blockquote>&ldquo;The best fest weekend is the one you planned on Thursday.&rdquo;<cite>An organiser at Utsav</cite></blockquote>' if i == 'squad' else '') + ('<figure><img src="assets/img/v4/dance.jpg" alt="Students dancing on a college stage" width="800" height="1200"><figcaption>Day two at a Bengaluru cultural fest.</figcaption></figure>' if i == 'kit' else '') for i, t, ps in SECTIONS)
art_page = HEAD.format(title=f'{feat[2]} | FestHey Blog') + css('fests', 'fest', 'app') + NAV + f'''
<main class="ar">
  <div class="ar-progress"><i></i></div>
  <header class="ar-head wrap">
    {crumb(('Blog', 'blog.html'), ('Cultural', 'blog.html'))}
    <h1 class="hero-h">{e(feat[2])}</h1>
    <p class="lead">{e(feat[3])}</p>
    <div class="ar-by"><span class="avs"><img src="assets/img/av2.jpg" alt="" width="40" height="40"></span><span><b>FestHey Editorial</b><small>Updated Nov 4, 2026 &middot; {feat[5]} min read</small></span><button class="fd-iconbtn ar-share">{icy('share', 'ic ic-s')}<span>Share</span></button></div>
  </header>
  <div class="wrap"><img class="ar-cover" src="assets/img/v4/pronite.jpg" alt="A college fest pro-night crowd" width="800" height="1200"></div>
  <div class="wrap ar-grid">
    <nav class="ar-toc" aria-label="Table of contents"><p class="eyebrow"><span></span>On this page</p>{toc}<a class="ar-back" href="blog.html">{ic('left', 'ic ic-xs')}All articles</a></nav>
    <article class="ar-body"><p class="ar-intro">Big college fests run for days, across stages, labs and grounds. A little planning turns them from a blur into the best weekend of the semester.</p>{body}</article>
  </div>
  <section class="wrap fd-sec ar-related"><div class="fd-head"><div><p class="eyebrow"><span></span>Keep reading</p><h2>RELATED READS</h2></div>{btn('All Articles', 'blog.html', 'ink', 'sm')}</div><div class="bl-grid">{''.join(post(p) for p in POSTS[1:4])}</div></section>
</main>
<div class="fd-toast" role="status" aria-live="polite"></div>
{FOOT}
''' + SCRIPTS

for name, pg in (('event.html', ev_page), ('team.html', team_page), ('blog.html', blog_page), ('article.html', art_page)):
    open(os.path.join(ROOT, name), 'w').write(pg)
    print('wrote', name, len(pg), 'dashes:', [c for c in ('—', '–') if c in pg])
