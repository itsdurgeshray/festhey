#!/usr/bin/env python3
"""FestHey info pages: colleges.html, college.html, help.html, privacy.html, refund.html, about.html.
Run: python3 assets/src/info_pages.py  (then assets/src/localize.py)"""
import os, runpy, html
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
A = runpy.run_path(os.path.join(ROOT, 'assets/src/app_pages.py'))
B, ix, ic, btn, HEAD, NAV, FOOT, PIT, crumb, FESTS = A['B'], A['ix'], A['ic'], A['btn'], A['HEAD'], A['NAV'], A['FOOT'], A['PIT'], A['crumb'], A['B']['FESTS']
card = A['L']['card']
e = html.escape
SCRIPTS = A['SCRIPTS'].replace('<script src="assets/app.js"></script>', '<script src="assets/app.js"></script>\n<script src="assets/info.js"></script>')
def css(*f):
    return ''.join(f'<link rel="stylesheet" href="assets/{x}.css">' for x in f) + '\n'
CSS = css('fests', 'fest', 'app', 'info')
def page(title, body, main_cls):
    return HEAD.format(title=title) + CSS + NAV + f'<main class="{main_cls}">{body}</main>\n<div class="fd-toast" role="status" aria-live="polite"></div>\n{FOOT}\n' + SCRIPTS

# ======================= colleges =======================
# name, short, city, state, img, upcoming fests, fests hosted, est, type
COLLEGES = [
 ('R V College of Engineering', 'RV', 'Bengaluru', 'Karnataka', 'v4/pronite', 3, 12, 1963, 'engineering'),
 ('B M S College of Engineering', 'BM', 'Bengaluru', 'Karnataka', 'fests/ad-fest-music', 2, 9, 1946, 'engineering'),
 ('M S Ramaiah Institute of Technology', 'MS', 'Bengaluru', 'Karnataka', 'fests/event-robotics-demo', 2, 8, 1962, 'engineering'),
 ('Christ University', 'CU', 'Bengaluru', 'Karnataka', 'fests/fest-sports', 3, 14, 1969, 'university'),
 ('PES University', 'PE', 'Bengaluru', 'Karnataka', 'v4/hack', 1, 6, 1972, 'university'),
 ('St Joseph’s University', 'SJ', 'Bengaluru', 'Karnataka', 'v4/dance', 0, 4, 1882, 'university'),
 ('Mithibai College', 'MC', 'Mumbai', 'Maharashtra', 'fests/gallery-stage', 1, 7, 1961, 'arts'),
 ('IIT Bombay', 'IB', 'Mumbai', 'Maharashtra', 'v4/robo', 2, 11, 1958, 'engineering'),
 ('St Stephen’s College', 'SS', 'Delhi', 'Delhi', 'v4/quiz', 0, 5, 1881, 'arts'),
]
def cc(c, i):
    name, sh, city, st, img, up, hosted, est, typ = c
    tag = f'<span class="chip chip--sun cc-up">{ix("party", "ic ic-xs")}{up} upcoming fest{"s" if up != 1 else ""}</span>' if up else '<span class="chip chip--light cc-up">No fests right now</span>'
    return f'''
        <article class="cc" data-name="{e(name.lower())}" data-city="{city.lower()}" data-up="{1 if up else 0}" data-type="{typ}">
          <a class="cc-ph" href="college.html"><img src="assets/img/{img}.jpg" alt="" width="800" height="1200" loading="lazy">{tag}</a>
          <button class="lc-save cc-save" aria-label="Follow {e(name)}" aria-pressed="false">{ix('bookmark', 'ic ic-s')}</button>
          <div class="cc-body">
            <span class="cc-av">{sh}</span>
            <a class="cc-name" href="college.html">{e(name)}</a>
            <p class="cc-meta">{ix('pin', 'ic ic-xs')}{city}, {st}</p>
            <div class="cc-foot"><span><b>{hosted}</b><small>Fests hosted</small></span><span><b>{est}</b><small>Established</small></span><a class="lc-go" href="college.html" aria-label="Explore {e(name)}">{ic('arrow')}</a></div>
          </div>
        </article>'''
cities = sorted({c[2] for c in COLLEGES})
colleges_body = f'''
  <section class="lh">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap lh-in">
      <div class="lh-copy">
        <p class="eyebrow eyebrow--ink"><span></span>College directory 2026</p>
        <h1 class="hero-h">THE CAMPUS <mark class="mark">HUB</mark></h1>
        <p class="lead lh-p">Find the colleges behind India&rsquo;s biggest fests. Follow a campus to hear the moment its next fest opens for registration.</p>
      </div>
      <div class="lh-art" aria-hidden="true">
        <span class="lh-sq"></span><span class="lh-sun"></span>
        <img class="lh-img" src="assets/img/v4/hosts.jpg" alt="" width="800" height="1200">
        <img class="lh-img2" src="assets/img/fests/gallery-stage.jpg" alt="" width="1280" height="720">
      </div>
    </div>
  </section>
  <section class="wrap lb cl">
    <div class="cl-bar">
      <label class="lb-search">{ix('search')}<input type="search" placeholder="Search colleges" aria-label="Search colleges"></label>
      <label class="sel"><select class="cl-city" aria-label="City"><option value="all">All cities</option>{''.join(f'<option value="{c.lower()}">{c}</option>' for c in cities)}</select>{ix('chev', 'ic ic-s')}</label>
      <div class="chips cl-chips" role="group" aria-label="Type">
        <button class="chip is-on" data-type="all" aria-pressed="true">All</button><button class="chip" data-type="engineering" aria-pressed="false">Engineering</button><button class="chip" data-type="university" aria-pressed="false">University</button><button class="chip" data-type="arts" aria-pressed="false">Arts &amp; Science</button>
      </div>
      <label class="tog"><input type="checkbox" class="cl-live"><span class="tog-t"></span>Fests open now</label>
    </div>
    <p class="cl-count"><b class="cl-n">{len(COLLEGES)}</b> colleges</p>
    <div class="cl-grid">{''.join(cc(c, i) for i, c in enumerate(COLLEGES))}</div>
    <p class="lb-empty" hidden>No colleges match. <button class="lb-reset cl-reset">Clear filters</button></p>
    <div class="lb-pager"><span class="lb-count">Showing <b>1 to {len(COLLEGES)}</b> of 48 colleges</span><nav class="lb-pages" aria-label="Pages"><button class="icon-btn icon-btn--sm" disabled aria-label="Previous">{ic('left')}</button><button class="lb-pg is-on">1</button><button class="lb-pg">2</button><button class="lb-pg">3</button><span class="lb-dots">&hellip;</span><button class="lb-pg">6</button><button class="icon-btn icon-btn--sm" aria-label="Next">{ic('right')}</button></nav></div>
  </section>
  <section class="wrap host-cta">
    <span class="grain" aria-hidden="true"></span>
    <div><p class="eyebrow eyebrow--ink"><span></span>For colleges</p><h2>DON&rsquo;T SEE YOUR CAMPUS?</h2><p class="lead">Organisers can list a college and publish their first fest in under ten minutes.</p></div>
    {btn('List Your College', 'https://festhey.agpro.co.in/auth/register/organizer', 'ink')}
  </section>
{PIT}'''

# ======================= college detail =======================
C = COLLEGES[0]
up_fests = ''.join(card(f, i + 2) for i, f in enumerate([FESTS[0], FESTS[6], FESTS[7]]))
PAST = [('8th Mile 2025', 'Dec 2025', '24 events', 'v4/pronite'), ('Hack RVCE 2025', 'Mar 2025', '1 event', 'v4/hack'), ('RVCE Sports Meet', 'Feb 2025', '9 events', 'v4/hoops'), ('Robo Rumble', 'Sep 2024', '4 events', 'v4/robo')]
past = ''.join(f'<a class="pf" href="fest.html"><img src="assets/img/{img}.jpg" alt="" width="800" height="1200" loading="lazy"><span><b>{n}</b><small>{d} &middot; {ev}</small></span>{ic("arrow", "ic ic-s")}</a>' for n, d, ev, img in PAST)
GAL = ['v4/pronite', 'v4/dance', 'v4/hoops', 'v4/quiz', 'v4/hack', 'v4/robo']
gal = ''.join(f'<figure class="fd-g fd-g{i+1}"><img src="assets/img/{g}.jpg" alt="" width="800" height="1200" loading="lazy"></figure>' for i, g in enumerate(GAL))
sim = ''.join(cc(c, i) for i, c in enumerate(COLLEGES[1:4]))
college_body = f'''
  <section class="fd-hero">
    <img class="fd-hero-img" src="assets/img/v4/hosts.jpg" alt="" width="800" height="1200">
    <span class="fd-hero-shade"></span><span class="grain" aria-hidden="true"></span>
    <div class="wrap fd-hero-in">
      {crumb(('Colleges', 'colleges.html'), (C[0], None))}
      <div class="fd-hero-copy">
        <p class="eyebrow fd-loc"><span></span>{C[2]}, {C[3]}</p>
        <h1 class="hero-h">{C[0]}</h1>
        <div class="fd-tags"><span class="chip chip--sun">Engineering</span><span class="chip chip--glass">{ix('cap', 'ic ic-xs')}Est. {C[7]}</span><span class="chip chip--glass">{ix('party', 'ic ic-xs')}{C[5]} upcoming fests</span></div>
      </div>
      <div class="fd-actions">
        <button class="fd-iconbtn fol" aria-pressed="false">{ix("bookmark", "ic ic-s")}<span>Follow</span></button>
        <button class="fd-iconbtn fd-share">{ix('share', 'ic ic-s')}<span>Share</span></button>
      </div>
    </div>
  </section>
  <div class="wrap fd-facts-wrap">
    <div class="fd-facts">
      <div class="fd-fact fd-fact--hot"><span class="fd-fact-ic">{ix('party', 'ic ic-s')}</span><span><small>Next fest</small><b>8th Mile, Dec 5</b></span></div>
      <div class="fd-fact"><span class="fd-fact-ic">{ix('trophy', 'ic ic-s')}</span><span><small>Fests hosted</small><b>{C[6]} on FestHey</b></span></div>
      <div class="fd-fact"><span class="fd-fact-ic">{ix('users', 'ic ic-s')}</span><span><small>Followers</small><b>4,280 students</b></span></div>
      <div class="fd-fact"><span class="fd-fact-ic">{ix('star', 'ic ic-s')}</span><span><small>Fest rating</small><b>4.6 from 212</b></span></div>
      <button class="btn btn--primary fd-cta cg-follow" aria-pressed="false">Follow for alerts<span class="dot dot--still">{ix('plus')}</span></button>
    </div>
  </div>

  <section class="wrap fd-sec cg-about">
    <div>
      <p class="eyebrow"><span></span>About the campus</p>
      <h2>WHERE 8TH MILE <mark class="mark">LIVES.</mark></h2>
      <p class="fd-about-p">RVCE is one of Bengaluru&rsquo;s oldest engineering colleges and home to 8th Mile, a two-day fest that draws students from across South India. The campus hosts technical events in its labs, cultural shows on the main stage and sports on the open grounds off Mysore Road.</p>
      <div class="fd-expect">
        <div class="fx fx--o"><span class="fx-ic">{ix('mic')}</span><b>Main stage</b><small>Pro-nights and cultural finals</small></div>
        <div class="fx fx--s"><span class="fx-ic">{ix('zap')}</span><b>Innovation labs</b><small>Robotics, hackathons and builds</small></div>
        <div class="fx fx--i"><span class="fx-ic">{ix('trophy')}</span><b>Sports complex</b><small>Courts, track and indoor arena</small></div>
        <div class="fx fx--w"><span class="fx-ic">{ix('coffee')}</span><b>Food street</b><small>Stalls open through every fest</small></div>
      </div>
    </div>
    <aside class="cg-map">
      <div class="fd-map" aria-hidden="true"><span class="fd-map-grid"></span><span class="fd-pin">{ix('pin')}</span><span class="chip chip--light fd-map-tag">RVCE Campus</span></div>
      <div class="cg-map-in">
        <p class="fd-addr"><b>{C[0]}</b><span>Mysore Road, Bengaluru, Karnataka 560059</span></p>
        {btn('Show on Map', 'https://maps.google.com/?q=R+V+College+of+Engineering+Bengaluru', 'ink', 'sm')}
      </div>
    </aside>
  </section>

  <section class="wrap fd-sec" id="fests">
    <div class="fd-head"><div><p class="eyebrow"><span></span>Register now</p><h2>UPCOMING FESTS</h2></div>{btn('All Fests', 'fests.html', 'ink', 'sm')}</div>
    <div class="lb-cards">{up_fests}</div>
  </section>

  <section class="fd-sec cg-past">
    <div class="wrap"><div class="fd-head"><div><p class="eyebrow"><span></span>The archive</p><h2>PAST FESTS</h2></div></div><div class="pf-grid">{past}</div></div>
  </section>

  <section class="wrap fd-sec" id="gallery">
    <div class="fd-head"><div><p class="eyebrow"><span></span>Gallery</p><h2>LIFE AT RVCE</h2></div></div>
    <div class="fd-gallery">{gal}</div>
  </section>

  <section class="wrap fd-sec cg-sim">
    <div class="fd-head"><div><p class="eyebrow"><span></span>Nearby</p><h2>MORE COLLEGES IN BENGALURU</h2></div>{btn('All Colleges', 'colleges.html', 'ink', 'sm')}</div>
    <div class="cl-grid">{sim}</div>
  </section>'''

# ======================= help center =======================
HELP = [
 ('account', 'user', 'Account &amp; profile', 'Login, profile and settings', [
   ('How do I change my profile picture?', 'Open Account settings, tap your current avatar and choose Upload new image. PNG, JPG and WebP files up to 10 MB work.'),
   ('Can I delete my account?', 'Yes. Request deletion from Profile settings. This is permanent and removes your registration history.'),
   ('How do I reset my password?', 'Tap Forgot password on the login screen. We email a secure link to your registered address so you can set a new one.')]),
 ('register', 'ticket', 'Events &amp; teams', 'Registering, invites and tickets', [
   ('How do I join a team?', 'Open the invite link your team captain shared, or enter their invite code on the event page and tap Join team. You pay your share after joining.'),
   ('Where can I find my tickets?', 'Every active ticket is in My Registrations. You can view or download it and show the QR code at the gate.'),
   ('Can I cancel my registration?', 'Cancellation rules are set per event. If the organiser allows it, cancel from My Registrations and the refund follows their policy.')]),
 ('pay', 'card', 'Payments &amp; refunds', 'Methods, security and timing', [
   ('Which payment methods are supported?', 'Credit and debit cards, UPI (Google Pay, PhonePe and more) and net banking, through our payment partner Razorpay.'),
   ('Is my payment information secure?', 'Yes. We never store card details. Every transaction is encrypted and processed by an industry-standard gateway.'),
   ('How long do refunds take?', 'Once the organiser approves a refund it usually reaches your original payment method in 5 to 7 business days.')]),
 ('host', 'school', 'For organisers', 'Listing and managing fests', [
   ('How do I list my college fest?', 'Create an organiser account, add your college and publish the fest. Events, fees and team sizes can be edited until registrations open.'),
   ('When do organisers get paid?', 'Payouts for collected fees are settled to the college&rsquo;s bank account within 7 business days after the fest ends.')]),
]
qn = 0
def hq(q, a, cat):
    global qn; qn += 1
    return f'<div class="hq" data-cat="{cat}"><button class="hq-q" aria-expanded="false" aria-controls="hq{qn}"><span>{q}</span><span class="hq-ic">{ix("plus", "ic ic-s")}</span></button><div class="hq-a" id="hq{qn}" role="region"><div><p>{a}</p></div></div></div>'
hcards = ''.join(f'<button class="hc" data-cat="{k}" aria-pressed="false"><span class="hc-ic">{ix(i)}</span><b>{t}</b><small>{d}</small><span class="hc-n">{len(qs)} articles</span></button>' for k, i, t, d, qs in HELP)
hlist = ''.join(f'<div class="hgroup" data-cat="{k}"><h3 class="ev-h"><span class="hc-ic hc-ic--s">{ix(i, "ic ic-s")}</span>{t}</h3>' + ''.join(hq(q, a, k) for q, a in qs) + '</div>' for k, i, t, d, qs in HELP)
help_body = f'''
  <section class="lh hp-hero">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap hp-in">
      <p class="eyebrow eyebrow--ink eyebrow--c"><span></span>Help center</p>
      <h1 class="hero-h">HOW CAN WE <mark class="mark">HELP?</mark></h1>
      <label class="hp-search">{ix('search')}<input type="search" placeholder="Search for answers, like &ldquo;refund&rdquo; or &ldquo;join team&rdquo;" aria-label="Search help articles"></label>
      <div class="hp-pop"><span>Popular:</span><button data-q="team">Join a team</button><button data-q="ticket">Find my ticket</button><button data-q="refund">Refunds</button><button data-q="password">Reset password</button></div>
    </div>
  </section>
  <section class="wrap hp-cats" aria-label="Help topics">{hcards}</section>
  <section class="wrap fd-sec hp-body">
    <div class="hp-list">
      <div class="hp-list-h"><h2>ANSWERS</h2><button class="lb-reset hp-clear" hidden>{ix('reset', 'ic ic-xs')}Show all topics</button></div>
      {hlist}
      <div class="lb-empty hp-empty" hidden><b>No answers for that yet.</b><br>Try another word, or message our support crew below.</div>
    </div>
    <aside class="hp-side">
      <div class="hp-contact">
        <span class="grain" aria-hidden="true"></span>
        <p class="eyebrow eyebrow--ink"><span></span>Still stuck?</p>
        <h3>OUR CREW IS ON STANDBY 24/7</h3>
        <p>Most messages get a reply within 2 hours.</p>
        <a class="btn btn--ink btn--block" href="mailto:support@festhey.in">Contact Support<span class="dot dot--still">{ix('mail')}</span></a>
      </div>
      <a class="help" href="me-registrations.html"><span class="tile-ic">{ix('ticket', 'ic ic-s')}</span><span><b>My registrations</b><small>Tickets, QR and receipts</small></span>{ic('arrow', 'ic ic-s')}</a>
      <a class="help" href="refund.html"><span class="tile-ic">{ix('receipt', 'ic ic-s')}</span><span><b>Refund policy</b><small>Windows and timelines</small></span>{ic('arrow', 'ic ic-s')}</a>
      <a class="help" href="privacy.html"><span class="tile-ic">{ix('shield', 'ic ic-s')}</span><span><b>Privacy policy</b><small>How we handle your data</small></span>{ic('arrow', 'ic ic-s')}</a>
    </aside>
  </section>'''

# ======================= legal pages =======================
def legal(title_a, title_b, updated, summary, sections, cta):
    toc = ''.join(f'<a href="#s{i+1}"><span>{i+1:02d}</span>{t}</a>' for i, (t, _) in enumerate(sections))
    body = ''.join(f'<section class="lg-s" id="s{i+1}"><h2><span>{i+1:02d}</span>{t}</h2>{h}</section>' for i, (t, h) in enumerate(sections))
    sm = ''.join(f'<div class="lg-k"><span class="tile-ic">{ix(i, "ic ic-s")}</span><p>{t}</p></div>' for i, t in summary)
    return f'''
  <section class="lg-hero wrap">
    {crumb(('Help center', 'help.html'), (f'{title_a.title()} {title_b.title()}', None))}
    <h1 class="hero-h">{title_a} <mark class="mark">{title_b}</mark></h1>
    <p class="lg-date">{ix('cal', 'ic ic-xs')}Last updated {updated} &middot; {len(sections)} sections &middot; 4 min read</p>
  </section>
  <section class="wrap lg-short"><p class="eyebrow"><span></span>The short version</p><div class="lg-ks">{sm}</div></section>
  <div class="wrap lg-grid">
    <nav class="ar-toc lg-toc" aria-label="Sections"><p class="eyebrow"><span></span>On this page</p>{toc}</nav>
    <article class="lg-body">{body}{cta}</article>
  </div>'''

def lcta(h, p, label, href, icon):
    return f'<div class="lg-cta"><span class="grain" aria-hidden="true"></span><div><h3>{h}</h3><p>{p}</p></div><a class="btn btn--ink" href="{href}">{label}<span class="dot{" dot--still" if icon != "arrow" else ""}">{ix(icon) if icon != "arrow" else ic("arrow")}</span></a></div>'

REF_TIERS = '''<div class="tiers">
  <div class="tier tier--full"><span class="tier-tag">Full refund</span><b>100%</b><p>Cancelled within the organiser&rsquo;s free cancellation window.</p></div>
  <div class="tier tier--part"><span class="tier-tag">Partial refund</span><b>Varies</b><p>After the free window, before the event&rsquo;s refund deadline.</p></div>
  <div class="tier tier--none"><span class="tier-tag">No refund</span><b>0%</b><p>After the refund deadline, or once the event has started.</p></div>
</div>'''
refund_body = legal('REFUND', 'POLICY', 'May 26, 2026',
  [('flag', 'Each organiser sets the refund rules for their own event.'), ('ticket', 'Cancel from My Registrations; we handle the rest.'), ('hourglass', 'Approved refunds land in 5 to 7 business days.')],
  [('General refund terms', '<p>FestHey provides the infrastructure for event registration and payment. Every event on the platform may have its own refund policy, and it is your responsibility to review those terms before you pay.</p><p class="lg-note">' + ix('info', 'ic ic-s') + '<span>Refund rules are set by the individual event organisers. FestHey facilitates the process but does not set the rules for every event.</span></p>'),
   ('Cancellation by the organiser', '<p>If an organiser cancels an event, you are entitled to a full refund of the registration fee. FestHey works with the organiser to start that refund automatically; you don&rsquo;t need to do anything.</p>'),
   ('Cancelling it yourself', '<p>To cancel, go to My Registrations in your dashboard. Whether you get money back depends on when you cancel:</p>' + REF_TIERS),
   ('Processing time', '<p>Approved refunds go back to the original payment method. Allow 5 to 7 business days for the amount to appear, depending on your bank or card issuer.</p><ol class="lg-steps"><li><b>Request</b><span>Cancel in My Registrations</span></li><li><b>Approval</b><span>Organiser reviews, usually within 48 hours</span></li><li><b>Refund</b><span>5 to 7 business days to your account</span></li></ol>')],
  lcta('NEED TO REQUEST A REFUND?', 'Open your registrations to see the refund eligibility for each event.', 'Go to My Registrations', 'me-registrations.html', 'arrow'))

privacy_body = legal('PRIVACY', 'POLICY', 'June 9, 2026',
  [('lock', 'We collect only what we need to run your registrations.'), ('card', 'Payments go through Razorpay; we never store card details.'), ('shield', 'We don&rsquo;t sell your data to anyone, ever.')],
  [('Introduction', '<p>Welcome to FestHey. We are committed to protecting your personal information and your right to privacy. If you have questions or concerns about this notice or how we handle your information, please contact us.</p>'),
   ('Information we collect', '<p>We collect personal information you give us when you register, show interest in our products and services, take part in activities on the website or contact us.</p><div class="lg-cards"><div><span class="tile-ic">' + ix('user', 'ic ic-s') + '</span><b>Personal details</b><small>Name, email and phone number</small></div><div><span class="tile-ic">' + ix('card', 'ic ic-s') + '</span><b>Payment data</b><small>Processed by secure third-party gateways</small></div><div><span class="tile-ic">' + ix('link', 'ic ic-s') + '</span><b>Social login</b><small>Basic profile from the provider you choose</small></div></div>'),
   ('How we use your information', '<p>We use personal information for legitimate business purposes, to fulfil our contract with you, with your consent, or to meet legal obligations.</p><ul class="ok-list">' + ''.join(f'<li><span class="perk-ic">{ic("check")}</span>{t}</li>' for t in ['To create your account and log you in', 'To post testimonials and collect feedback', 'To manage your account and registrations', 'To send you administrative information']) + '</ul>'),
   ('Data security', '<p>We protect your personal information with organisational and technical security measures. These are designed to keep any information we process safe, but no online transmission can be guaranteed to be completely secure.</p>')],
  lcta('STILL HAVE QUESTIONS?', 'Email support@festhey.in or browse the help center.', 'Contact Support', 'help.html', 'msg'))

# ======================= about =======================
VALUES = [('o', 'flag', 'Our mission', 'Connect every student in India with the most exciting campus experiences and opportunities to grow.'),
          ('s', 'users', 'Community first', 'Built for students, by students. Every decision starts with the campus community.'),
          ('i', 'zap', 'Innovation', 'We keep improving so finding and joining a fest takes seconds, not group chats.'),
          ('w', 'heart', 'Passion', 'We love college fests, and want every registration to feel as exciting as the event itself.')]
vals = ''.join(f'<div class="val val--{k}"><span class="fx-ic">{ix(i)}</span><h3>{t}</h3><p>{d}</p></div>' for k, i, t, d in VALUES)
STEPS = [('search', 'Discover', 'Browse fests and events by city, category or date.'), ('ticket', 'Register', 'Pay securely, solo or as a team with one invite link.'), ('qr', 'Show up', 'Scan your QR pass at the gate and you&rsquo;re in.')]
hsteps = ''.join(f'<li class="hw"><span class="hw-n">{n+1:02d}</span><span class="hw-ic">{ix(i)}</span><b>{t}</b><p>{d}</p></li>' for n, (i, t, d) in enumerate(STEPS))
about_body = f'''
  <section class="lh ab-hero">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap lh-in">
      <div class="lh-copy">
        <p class="eyebrow eyebrow--ink"><span></span>About FestHey</p>
        <h1 class="hero-h">THE HEART OF <mark class="mark">CAMPUS</mark></h1>
        <p class="lead lh-p">India&rsquo;s event discovery platform for college fests, bridging the gap between organisers and the students who make every fest come alive.</p>
      </div>
      <div class="ab-note">
        <span class="ab-pin" aria-hidden="true"></span>
        <p class="eyebrow"><span></span>Who we are</p>
        <p>Founded in 2024, FestHey started as a small project to fix the chaos of fest registrations in a few local colleges. Today we connect thousands of students across the country to the fests they love.</p>
        <span class="ab-sign">Since 2024</span>
      </div>
    </div>
  </section>
  <section class="wrap ab-stats" aria-label="FestHey in numbers">
    <div><b>500+</b><span>Colleges</span></div><div><b>2,000+</b><span>Events</span></div><div><b>50K+</b><span>Students</span></div><div><b>4.7</b><span>Average rating</span></div>
  </section>
  <section class="wrap fd-sec">
    <div class="fd-head"><div><p class="eyebrow"><span></span>What drives us</p><h2>BUILT FOR THE CROWD</h2></div></div>
    <div class="vals">{vals}</div>
  </section>
  <section class="fd-sec ab-how">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap ab-how-in">
      <div><p class="eyebrow eyebrow--ink"><span></span>How it works</p><h2>THREE STEPS TO THE FRONT ROW</h2></div>
      <ol class="hws">{hsteps}</ol>
    </div>
  </section>
  <section class="wrap fd-sec ab-story">
    <div class="ab-ph"><img src="assets/img/v4/hosts.jpg" alt="Students at a campus fest" width="800" height="1200"><img src="assets/img/v4/dance.jpg" alt="" width="800" height="1200"></div>
    <div>
      <p class="eyebrow"><span></span>Our story</p>
      <h2>FROM GROUP CHATS TO ONE TAP</h2>
      <p class="fd-about-p">Fest registrations used to live in spreadsheets, payment screenshots and forwarded forms. We built FestHey so students could find every fest in one place, register in a tap, and bring their whole team along.</p>
      <ul class="ab-time"><li><b>2024</b><span>First fest goes live with 3 colleges in Bengaluru</span></li><li><b>2025</b><span>Team registrations and QR passes launch</span></li><li><b>2026</b><span>500+ colleges across India</span></li></ul>
    </div>
  </section>
  <section class="wrap ab-join">
    <span class="grain" aria-hidden="true"></span>
    <div class="ab-join-in">
      <p class="eyebrow eyebrow--ink eyebrow--c"><span></span>Join the revolution</p>
      <h2>LET&rsquo;S BUILD CAMPUS LIFE <mark class="mark mark--snow">TOGETHER</mark></h2>
      <p class="lead">Whether you&rsquo;re an organiser or a student leader, we&rsquo;re always looking for people who love fests as much as we do.</p>
      <div class="ab-ctas">{btn('Partner With Us', 'https://festhey.agpro.co.in/auth/register/organizer', 'ink')}{btn('Explore Fests', 'fests.html', 'light')}</div>
    </div>
  </section>'''

for name, title, body, cls in (
    ('colleges.html', 'Colleges | FestHey', colleges_body, 'lp cl-page'),
    ('college.html', f'{C[0]} | FestHey', college_body, 'fd cg'),
    ('help.html', 'Help Center | FestHey', help_body, 'hp'),
    ('refund.html', 'Refund Policy | FestHey', refund_body, 'lg'),
    ('privacy.html', 'Privacy Policy | FestHey', privacy_body, 'lg'),
    ('about.html', 'About | FestHey', about_body, 'ab')):
    pg = page(title, body, cls)
    open(os.path.join(ROOT, name), 'w').write(pg)
    print('wrote', name, len(pg), 'dashes:', [c for c in ('—', '–') if c in pg])
