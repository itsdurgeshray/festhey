#!/usr/bin/env python3
"""FestHey app pages: event.html, team.html, blog.html, article.html (+ 3 modals).
Run: python3 assets/src/app_pages.py"""
import os, runpy, html, random
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
B = runpy.run_path(os.path.join(ROOT, 'assets/src/build.py'))
L = runpy.run_path(os.path.join(ROOT, 'assets/src/fests_page.py'))
FP = runpy.run_path(os.path.join(ROOT, 'assets/src/fest_page.py'))
ic, btn, HEAD, NAV, EVENTS, BASE, evc, AV = B['ic'], B['btn'], B['HEAD'], B['NAV'], B['EVENTS'], B['BASE'], B['evc'], B['AV']
icx, FOOT, PIT, icy = L['icx'], L['FOOT'], L['PIT'], FP['icy']
e = html.escape
X = {
 'close': '<path d="M18 6 6 18M6 6l12 12"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 'userplus': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/>',
 'trophy': '<path d="M6 9H4a2 2 0 0 1 0-4h2M18 9h2a2 2 0 0 0 0-4h-2M4 22h16M10 15v7M14 15v7M18 2H6v7a6 6 0 0 0 12 0Z"/>',
 'star': '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
 'wifi': '<path d="M5 13a10 10 0 0 1 14 0M8.5 16.5a5 5 0 0 1 7 0M2 8.8a15 15 0 0 1 20 0"/><circle cx="12" cy="20" r="1"/>',
 'coffee': '<path d="M17 8h1a4 4 0 0 1 0 8h-1M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><path d="M6 2v2M10 2v2M14 2v2"/>',
 'drop': '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5S12.5 5.5 12 2.5C11.5 5.5 10 7.9 8 9.5S5 13 5 15a7 7 0 0 0 7 7Z"/>',
 'snow': '<path d="M2 12h20M12 2v20M4.9 4.9l14.2 14.2M19.1 4.9 4.9 19.1"/>',
 'zap': '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
 'copy': '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
 'info': '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
 'wa': '<path d="M3 21l1.6-4.7A9 9 0 1 1 8 20Z"/><path d="M9 10c0 3 2 5 5 5l1.5-1.5-2-1-1 1c-1 0-2.5-1.5-2.5-2.5l1-1-1-2Z"/>',
 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>',
 'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-10 6L2 7"/>',
 'book': '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
}
def ix(n, c='ic'):
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{X[n]}</svg>'
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

# ======================= modals =======================
AD = f'''
<div class="modal" id="m-ad" role="dialog" aria-modal="true" aria-labelledby="m-ad-h" hidden>
  <div class="modal-back" data-close></div>
  <div class="modal-card modal-ad">
    <img src="assets/img/fests/ad-fest-music.jpg" alt="" width="1280" height="720">
    <span class="modal-ad-shade"></span>
    <span class="chip chip--ink m-ad-tag">AD</span>
    <span class="chip chip--light m-ad-date">Three nights, Dec 2026</span>
    <button class="modal-x modal-x--glass" data-close aria-label="Close">{ix('close')}</button>
    <div class="m-ad-body">
      <span class="chip chip--sun">{icx('pin', 'ic ic-xs')}B M S College of Engineering</span>
      <h2 id="m-ad-h">Utsav Winter Edition</h2>
      <p>Three Nights of Music and Dance at BMSCE</p>
      <div class="m-ad-cta"><button class="btn btn--light btn--sm" data-close>Maybe later<span class="dot dot--still">{ix('close')}</span></button>{btn('Check it out', BASE + '/fests/utsav-winter-edition', 'primary', 'sm')}</div>
    </div>
  </div>
</div>'''

CREATE = f'''
<div class="modal" id="m-team" role="dialog" aria-modal="true" aria-labelledby="m-team-h" hidden>
  <div class="modal-back" data-close></div>
  <form class="modal-card modal-form" action="team.html" novalidate>
    <button type="button" class="modal-x" data-close aria-label="Close">{ix('close')}</button>
    <p class="eyebrow"><span></span>Step 1 of 2 &middot; Create your team</p>
    <h2 id="m-team-h">NAME YOUR SQUAD</h2>
    <p class="m-sub">You are registering as a team for <b>{EV['name']}</b>. Name your team, then share the invite link with your members.</p>
    <div class="m-sum">
      <span><small>Team size</small><b>{EV['team']} members</b></span><span><small>Fee</small><b>&#8377;{EV['fee']}.00 / Member</b></span><span><small>Event day</small><b>{EV['date']}</b></span>
    </div>
    <label class="m-label" for="tn">Team name</label>
    <label class="fld">{ix('users')}<input id="tn" name="team" placeholder="e.g. SpiderTrack" maxlength="24" autocomplete="off" required></label>
    <p class="m-hint">{ix('info', 'ic ic-xs')}<span>Team names can&rsquo;t be changed later. <b class="m-left">24</b> characters left.</span></p>
    <div class="m-actions"><button type="button" class="btn btn--light" data-close>Cancel<span class="dot dot--still">{ix('close')}</span></button><button class="btn btn--ink" type="submit">Create Team<span class="dot">{ic('arrow')}</span></button></div>
  </form>
</div>'''

INVITE = f'''
<div class="modal" id="m-invite" role="dialog" aria-modal="true" aria-labelledby="m-inv-h" hidden>
  <div class="modal-back" data-close></div>
  <div class="modal-card modal-invite">
    <button class="modal-x" data-close aria-label="Close">{ix('close')}</button>
    <span class="m-inv-ic">{ix('mail')}<span>{ix('userplus', 'ic ic-xs')}</span></span>
    <p class="eyebrow eyebrow--c"><span></span>Team invitation</p>
    <h2 id="m-inv-h">YOU&rsquo;RE INVITED!</h2>
    <p class="m-sub"><b>Rohan Verma</b> invited you to join their team for <b>{EV['name']}</b> at {EV['fest']}.</p>
    <div class="m-inv-team"><span class="m-inv-av">ST</span><span><b>SpiderTrack</b><span class="chip chip--sun">{EV['short']}</span></span><span class="m-inv-fee"><b>&#8377;{EV['fee']}</b><small>/ Member</small></span></div>
    <div class="m-inv-slots"><span>{ix('users')}<b>2 of {EV['team']} spots filled</b></span><span class="bar"><i style="width:66%"></i></span></div>
    <a class="btn btn--ink btn--block" href="team.html?state=complete">Join Team<span class="dot">{ix('userplus', 'ic')}</span></a>
    <p class="m-secure">{ix('shield', 'ic ic-xs')}Secure checkout. Pay your share after joining.</p>
  </div>
</div>'''
MODALS = AD + CREATE + INVITE

# ======================= event page =======================
others = ''.join(evc(t, i) for i, t in enumerate(EVENTS[1:7]))
REVIEWS = [('Ananya K', 'BMSCE', 5, 'Track was clean and the judges explained every fault. Second run timing felt fair.'),
           ('Mohit S', 'RVCE', 5, 'Great crowd, quick check-in. Bring spare batteries; the queue for charging was long.'),
           ('Divya R', 'PES University', 4, 'Loved the format. Wish the practice track had opened an hour earlier.')]
reviews = ''.join(f'''<article class="rv"><div class="rv-top"><span class="rv-av">{n.split()[0][0]}{n.split()[1][0]}</span><span><b>{n}</b><small>{c}, Brain Wars 2025</small></span><span class="rv-score">{ix('star', 'ic ic-xs')}{s}.0</span></div><p>{t}</p></article>''' for n, c, s, t in REVIEWS)

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
    <p class="st-banner st-pending">{ix('info', 'ic ic-s')}Your team <b>SpiderTrack</b> has 1 of 3 members. Invite your squad and pay before Dec 26 to lock your spot.</p>
  </div>

  <section class="wrap fd-sec ev-grid">
    <div class="ev-main">
      <p class="eyebrow"><span></span>About the event</p>
      <h2>BUILD IT. RACE IT.</h2>
      <p class="ev-lead">Bring an autonomous robot that follows a black line through curves, crossings and a surprise section. The fastest clean run takes the trophy.</p>
      <div class="chips ev-amen"><span class="chip">{ix('coffee', 'ic ic-s')}Breakfast</span><span class="chip">{ix('wifi', 'ic ic-s')}Free Wi-Fi</span><span class="chip">{ix('drop', 'ic ic-s')}Drinking water</span><span class="chip">{ix('snow', 'ic ic-s')}Air-conditioned pit area</span><span class="chip">{ix('zap', 'ic ic-s')}Charging points</span></div>
      <div class="ev-two">
        <div><h3 class="ev-h">Eligibility</h3>{checks(ELIG)}</div>
        <div><h3 class="ev-h">Rules</h3>{checks(RULES)}</div>
      </div>
    </div>
    <aside class="ev-side">
      <div class="ev-fee">
        <small>Registration fee</small>
        <b>&#8377;{EV['fee']}.00</b><span>per team member</span>
        <div class="ev-fee-rows"><span>{icx('pin', 'ic ic-xs')}{EV['venue']}</span><span>{icy('cal', 'ic ic-xs')}{EV['date']}</span><span>{icx('clock', 'ic ic-xs')}{EV['time']}</span></div>
        <button class="btn btn--primary btn--block st-open" data-open="m-team">Register as a team<span class="dot">{ic('arrow')}</span></button>
        <a class="btn btn--sun btn--block st-pending" href="team.html">Complete Registration<span class="dot">{ic('arrow')}</span></a>
        <a class="btn btn--ink btn--block st-done" href="team.html?state=complete">View Ticket<span class="dot">{ic('arrow')}</span></a>
        <button class="ev-invite-demo" data-open="m-invite">Got an invite link? Join a team</button>
      </div>
      <a class="ev-fest" href="{EV['fest_href']}"><img src="assets/img/fests/gallery-stage.jpg" alt="" width="1280" height="720"><span><small>Part of</small><b>{EV['fest']}</b><em class="chip chip--sun">Dec 30 to Dec 31</em></span>{ic('arrow')}</a>
      <div class="ev-org"><span class="fd-org-av">MS</span><span><small>Organised by</small><b>{EV['college']}</b></span></div>
    </aside>
  </section>

  <section class="ev-prize" id="prizes">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap ev-prize-in">
      <div class="fd-head ev-prize-head"><div><p class="eyebrow eyebrow--ink"><span></span>Prize pool</p><h2>&#8377;75,000 UP FOR GRABS</h2></div><p class="ev-prize-note">The winning team takes the grand prize; runners-up and third place are rewarded too. Terms and conditions apply.</p></div>
      <div class="podium">
        <div class="pod pod--2"><span class="pod-rank">2</span><small>Runner up</small><b>&#8377;15,000</b><p>Merch kit and cloud credits</p></div>
        <div class="pod pod--1"><span class="pod-ic">{ix('trophy')}</span><small>Grand prize</small><b>&#8377;50,000</b><p>Golden trophy and internship interviews</p></div>
        <div class="pod pod--3"><span class="pod-rank">3</span><small>Third place</small><b>&#8377;10,000</b><p>Tech goodies and certificates</p></div>
      </div>
    </div>
  </section>

  <section class="wrap fd-sec">
    <div class="fd-head"><div><p class="eyebrow"><span></span>From last year</p><h2>WHAT TEAMS SAID</h2></div><span class="ev-rating"><b>4.7</b>{ix('star', 'ic ic-s')}<small>from 38 reviews</small></span></div>
    <div class="rv-grid">{reviews}</div>
  </section>

  <section class="fd-sec ev-more">
    <div class="wrap"><div class="fd-head"><div><p class="eyebrow"><span></span>Also at {EV['fest']}</p><h2>MORE EVENTS</h2></div>{btn('View Fest', EV['fest_href'], 'ink', 'sm')}</div></div>
    <div class="ev-track"><div class="ev-row v-ticket">{others}</div></div>
  </section>
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

MEM = [('RV', 'Rohan Verma', 'Team captain', True), ('SV', 'Sai Vani', 'Member', False), ('RG', 'Reshma Gouri', 'Member', False)]
slots = ''.join(f'''<div class="slot-c {'is-you' if you else ''} {'' if i == 0 else 'st-done'}"><span class="slot-av">{a}</span><b>{n}</b><small>{r}</small>{'<span class="chip chip--sun slot-you">You</span>' if you else ''}</div>''' for i, (a, n, r, you) in enumerate(MEM))
slots += ''.join(f'<div class="slot-c slot-empty st-pending"><span class="slot-av">{ix("userplus")}</span><b>Waiting for member {i}</b><small>Share the invite link</small></div>' for i in (2, 3))
INFO = [(icy('ticket', 'ic ic-s'), 'Event', EV['name']), (ix('book', 'ic ic-s'), 'College', EV['short']), (icx('pin', 'ic ic-s'), 'Venue', EV['venue']), (icy('cal', 'ic ic-s'), 'Date', EV['date'])]
info = ''.join(f'<div class="ti"><span class="fd-fact-ic">{a}</span><span><small>{b}</small><b>{c}</b></span></div>' for a, b, c in INFO)
link = 'festhey.in/t/spidertrack-4kq9'
team_page = HEAD.format(title='SpiderTrack | Team | FestHey') + css('fests', 'fest', 'app') + NAV + f'''
<main class="tm" data-state="pending">
  <section class="tm-hero">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap tm-hero-in">
      <div>
        {crumb((EV['fest'], EV['fest_href']), (EV['name'], 'event.html'), ('Team', None))}
        <div class="tm-name"><span class="tm-badge">{ix('zap')}</span><h1 class="hero-h">SPIDERTRACK</h1></div>
        <p class="tm-sub st-pending">Invite 2 more members and pay to confirm your team.</p>
        <p class="tm-sub st-done">You&rsquo;re in. Show the QR at the venue on {EV['date']}.</p>
      </div>
      <div class="tm-count">
        <span class="chip chip--sun tm-flag st-pending">2 spots left</span><span class="chip chip--sun tm-flag st-done">Confirmed</span>
        <span class="tm-count-ic">{ix('users')}</span>
        <span><b><span class="st-pending">1</span><span class="st-done">3</span> / 3</b><small>spots filled</small></span>
        <span class="bar"><i></i></span>
      </div>
    </div>
  </section>

  <section class="wrap tm-grid">
    <div class="tm-main">
      <div class="tm-ticket st-done">
        <div class="tm-qr">{qr_svg()}</div>
        <div class="tm-ticket-body">
          <p class="eyebrow"><span></span>Entry pass</p>
          <h2>SEE YOU AT THE TRACK</h2>
          <dl><div><dt>Registration ID</dt><dd>FH-BW-26-4KQ9</dd></div><div><dt>Order ID</dt><dd>order_N7c2Xk91</dd></div><div><dt>Check-in</dt><dd>{EV['date']}, 8:30 AM</dd></div></dl>
        </div>
      </div>

      <div class="tm-block">
        <div class="tm-block-h"><h3 class="ev-h">Your team</h3><span class="tm-step st-pending">Step 2 of 2 &middot; Fill your team</span></div>
        <div class="slots">{slots}</div>
      </div>

      <div class="tm-block"><h3 class="ev-h">Event information</h3><div class="ti-grid">{info}</div></div>
      <div class="ev-two tm-block"><div><h3 class="ev-h">Eligibility</h3>{checks(ELIG)}</div><div><h3 class="ev-h">Rules</h3>{checks(RULES)}</div></div>
    </div>

    <aside class="tm-side">
      <div class="side-card st-pending">
        <div class="side-h"><span class="side-ic">{ix('userplus', 'ic ic-s')}</span><b>Invite your squad</b></div>
        <p class="side-p">Send this link to your teammates. It opens the invite and lets them join in one tap.</p>
        <div class="copy"><span class="copy-url">{link}</span><button class="icon-btn icon-btn--sm copy-btn" aria-label="Copy invite link" data-copy="https://{link}">{ix('copy')}</button></div>
        <a class="btn btn--wa btn--block" href="https://wa.me/?text=Join%20my%20team%20SpiderTrack%20on%20FestHey%3A%20https%3A%2F%2F{link}" target="_blank" rel="noopener">Share on WhatsApp<span class="dot">{ix('wa')}</span></a>
        <button class="m-preview" data-open="m-invite">Preview what they&rsquo;ll see</button>
      </div>

      <div class="side-card">
        <div class="side-h"><span class="side-ic">{icy('ticket', 'ic ic-s')}</span><b class="st-pending">Team fee summary</b><b class="st-done">Order summary</b><span class="side-fee"><b>&#8377;{EV['fee']}</b><small>/ Member</small></span></div>
        <dl class="sum">
          <div><dt>Members joined</dt><dd><span class="st-pending">1</span><span class="st-done">3</span></dd></div>
          <div><dt>Registration subtotal</dt><dd><span class="st-pending">&#8377;349.00</span><span class="st-done">&#8377;1,047.00</span></dd></div>
          <div><dt>Convenience fee {ix('info', 'ic ic-xs')}</dt><dd><span class="st-pending">&#8377;10.47</span><span class="st-done">&#8377;31.41</span></dd></div>
          <div class="st-done"><dt>Paid with</dt><dd>Razorpay, UPI</dd></div>
        </dl>
        <div class="sum-total"><span>Total</span><b><span class="st-pending">&#8377;359.47</span><span class="st-done">&#8377;1,078.41</span></b></div>
        <a class="btn btn--primary btn--block st-pending" href="team.html?state=complete">Pay my share<span class="dot">{ic('arrow')}</span></a>
        <p class="m-secure st-pending">{ix('shield', 'ic ic-xs')}Each member pays their own share. Spots lock once everyone pays.</p>
        <a class="btn btn--ink btn--block st-done" href="event.html?state=done">View Event<span class="dot">{ic('arrow')}</span></a>
      </div>
      <div class="dl st-done"><a class="btn btn--light btn--block" href="#">Download Ticket PDF<span class="dot dot--still">{ix('download')}</span></a><a class="btn btn--light btn--block" href="#">Download Receipt PDF<span class="dot dot--still">{ix('download')}</span></a></div>
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
