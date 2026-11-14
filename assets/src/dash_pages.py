#!/usr/bin/env python3
"""FestHey dashboards: organiser (org*.html) and student (me*.html) on one shell.
Run: python3 assets/src/dash_pages.py  (then assets/src/localize.py)"""
import os, runpy, html
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
A = runpy.run_path(os.path.join(ROOT, 'assets/src/app_pages.py'))
I = runpy.run_path(os.path.join(ROOT, 'assets/src/info_pages.py'))
ix, ic, btn, HEAD, crumb = A['ix'], A['ic'], A['btn'], A['HEAD'], A['crumb']
B = A['B']; card = A['L']['card']; evc = B['evc']; FESTS, EVENTS = B['FESTS'], B['EVENTS']
cc, COLLEGES, qr_svg = I['cc'], I['COLLEGES'], A['qr_svg']
e = html.escape
CSS = ''.join(f'<link rel="stylesheet" href="assets/{x}.css">' for x in ('fests', 'fest', 'app', 'info', 'dash')) + '\n'
JS = '<script src="assets/app.js"></script>\n<script src="assets/dash.js"></script>\n</body>\n</html>\n'

def chip(label, kind):
    return f'<span class="pill pill--{kind}">{label}</span>'
STATUS = {'live': ('Live', 'live'), 'up': ('Upcoming', 'up'), 'draft': ('Draft', 'draft'), 'past': ('Past', 'past'),
          'pub': ('Published', 'up'), 'cancel': ('Cancelled', 'bad'), 'ok': ('Approved', 'ok'), 'pend': ('Pending', 'live'),
          'wait': ('Waitlisted', 'draft'), 'rej': ('Rejected', 'bad'), 'paid': ('Paid', 'ok'), 'refund': ('Refunded', 'draft')}
def st(k):
    return chip(*STATUS[k])
def stat(icon, label, value, note='', kind='', href=''):
    tag = 'a' if href else 'div'
    hr = f' href="{href}"' if href else ''
    go = f'<span class="stat-go">{ic("arrow", "ic ic-s")}</span>' if href else ''
    return f'<{tag} class="stat {kind}"{hr}><span class="stat-ic">{ix(icon, "ic ic-s")}</span><small>{label}</small><b>{value}</b>{f"<em>{note}</em>" if note else ""}{go}</{tag}>'
def tabs(items, name, active=0):
    return f'<div class="dtabs" role="tablist" data-tabs="{name}">' + ''.join(f'<button role="tab" data-tab="{k}" aria-selected="{"true" if i == active else "false"}">{l}{f"<span>{n}</span>" if n is not None else ""}</button>' for i, (k, l, n) in enumerate(items)) + '</div>'
def field(label, inner, cls=''):
    return f'<div class="df {cls}"><label class="m-label">{label}</label>{inner}</div>'
def inp(icon, ph, val='', typ='text', name=''):
    ico = ix(icon) if icon else ''
    return f'<label class="fld">{ico}<input type="{typ}" placeholder="{ph}" value="{val}" name="{name}"></label>'
def select(opts, sel=''):
    return '<label class="sel dsel"><select>' + ''.join(f'<option{" selected" if o == sel else ""}>{o}</option>' for o in opts) + f'</select>{ix("chev", "ic ic-s")}</label>'
def upload(title, hint, ratio='wide'):
    return f'<label class="drop drop--{ratio}"><input type="file" accept="image/*" hidden><span class="drop-ic">{ix("upload", "ic")}</span><b>{title}</b><small>{hint}</small><img class="drop-img" alt="" hidden></label>'
def stepper(label, val):
    return f'<div class="df"><label class="m-label">{label}</label><div class="stepper"><button type="button" aria-label="Decrease">{ix("minus", "ic ic-s")}</button><input type="number" value="{val}" min="0" aria-label="{label}"><button type="button" aria-label="Increase">{ix("plus", "ic ic-s")}</button></div></div>'

def shell(role, active, title, body, cls=''):
    links = '<a href="colleges.html">Colleges</a><a href="fests.html">Fests</a><a href="blog.html">Blog</a>'
    if role == 'org':
        NAV = [('org', 'Overview', 'dash', 'org.html'), ('fests', 'Fests &amp; Events', 'cal', 'org-fests.html'), ('gate', 'Gate scanner', 'scan', 'org-gate.html'),
               ('ads', 'Ads &amp; Sponsors', 'flag', 'org-ads.html'), ('plans', 'Subscription', 'card', 'org-plans.html'), ('college', 'College profile', 'school', 'org-college.html')]
        top = f'''<a class="side-org" href="college.html"><span class="grain" aria-hidden="true"></span><span class="side-org-av">MS</span><b>M S Ramaiah Institute of Technology</b><small>{ix('pin', 'ic ic-xs')}Bengaluru, Karnataka</small><span class="side-org-go">{ic('arrow', 'ic ic-s')}</span></a>
      <div class="side-me"><span class="side-av">RV</span><span><b>Rohan Verma</b><span class="side-chips"><span class="chip chip--sun">Organiser</span><span class="plan-chip plan-free">Free tier</span><span class="plan-chip plan-pro">Standard</span></span></span></div>'''
        menu_switch = '<a href="me.html">' + ix('user', 'ic ic-s') + 'Switch to student view</a>'
    else:
        NAV = [('me', 'My profile', 'user', 'me.html'), ('regs', 'My registrations', 'ticket', 'me-registrations.html'), ('saved', 'Saved', 'bookmark', 'me-saved.html'), ('pay', 'Payments', 'card', 'me-payments.html')]
        top = f'''<div class="side-me side-me--big"><img src="assets/img/av1.jpg" alt="" width="56" height="56"><span><b>Rohan Verma</b><small>R V College of Engineering</small><span class="side-chips"><span class="chip chip--sun">Student</span></span></span></div>
      <div class="side-next"><small>Next up</small><b>Line Follower Sprint</b><span>{ix('cal', 'ic ic-xs')}Dec 30 &middot; in 16 days</span></div>'''
        menu_switch = '<a href="org.html">' + ix('school', 'ic ic-s') + 'Switch to organiser view</a>'
    nav = ''.join(f'<a href="{h}" class="side-a{" is-on" if k == active else ""}"{" aria-current=page" if k == active else ""}>{ix(i, "ic ic-s")}<span>{l}</span></a>' for k, l, i, h in NAV)
    return HEAD.format(title=f'{title} | FestHey') + CSS + f'''<header class="dh">
  <div class="wrap dh-in">
    <a class="dh-logo" href="index.html"><img src="assets/img/logo.svg" alt="FestHey" width="132" height="40"></a>
    <nav class="dh-links" aria-label="Main">{links}</nav>
    <div class="dh-end">
      <button class="icon-btn icon-btn--sm dh-bell" aria-label="Notifications" data-menu="bell">{ix('bell', 'ic')}<i></i></button>
      <div class="dmenu-wrap"><button class="dh-me" data-menu="me" aria-haspopup="true" aria-expanded="false"><img src="assets/img/av1.jpg" alt="" width="36" height="36">{ix('chev', 'ic ic-s')}</button>
        <div class="dmenu" data-menu-for="me" hidden><p><b>Rohan Verma</b><small>rohan.v@festhey.in</small></p>{menu_switch}<a href="help.html">{ix('msg', 'ic ic-s')}Help center</a><a href="index.html" class="dmenu-out">{ix('logout', 'ic ic-s')}Log out</a></div>
      </div>
    </div>
  </div>
</header>
<div class="wrap dl {cls}">
  <aside class="side" aria-label="Dashboard">
    {top}
    <nav class="side-nav">{nav}</nav>
    <div class="side-foot"><a href="help.html" class="side-a">{ix('msg', 'ic ic-s')}<span>Help center</span></a><a href="index.html" class="side-a side-out">{ix('logout', 'ic ic-s')}<span>Log out</span></a></div>
  </aside>
  <main class="dm">{body}</main>
</div>
<div class="fd-toast" role="status" aria-live="polite"></div>
''' + JS

def head(parts, h1, sub='', actions='', pre=''):
    back = parts[-2][1] if len(parts) > 1 and parts[-2][1] else 'org.html'
    return f'''<div class="dm-head"><div><div class="dm-crumb"><a class="dm-back" href="{back}" aria-label="Back">{ic('left', 'ic ic-s')}</a>{crumb(*parts)}</div>{pre}<h1 class="dm-h">{h1}</h1>{f'<p class="dm-sub">{sub}</p>' if sub else ''}</div>{f'<div class="dm-act">{actions}</div>' if actions else ''}</div>'''

def modal(id_, title, body, size=''):
    return f'<div class="modal" id="{id_}" role="dialog" aria-modal="true" aria-labelledby="{id_}-h" hidden><div class="modal-back" data-close></div><div class="modal-card modal-form {size}"><button class="modal-x" data-close aria-label="Close">{ix("close")}</button><h2 id="{id_}-h">{title}</h2>{body}</div></div>'

# ============================ organiser data ============================
OF = [  # name, cat, date, venue, regs, cap, status, img
 ('ByteForce CTF', 'Technical', 'Dec 18, 2026', 'LHC Labs, MSRIT', 320, 500, 'live', 'fests/event-hackathon'),
 ('Cultfest 2026', 'Cultural', 'Dec 5, 2026', 'College Grounds', 718, 1200, 'live', 'v4/pronite'),
 ('Innovate X', 'Technical', 'Jan 15, 2027', 'Main Auditorium', 210, 400, 'up', 'fests/event-robotics-demo'),
 ('Rhythm Riot', 'Cultural', 'Feb 20, 2027', 'Open Air Theatre', 0, 600, 'draft', 'v4/dance'),
 ('Code Sprint 2025', 'Technical', 'Mar 8, 2025', 'CSE Block', 450, 450, 'past', 'v4/hack'),
]
def fest_row(f, actions=True):
    n, c, d, v, r, cap, s, img = f
    pct = round(r / cap * 100) if cap else 0
    act = f'<td class="t-act"><a class="btn btn--light btn--sm" href="org-fest.html">Manage<span class="dot">{ic("arrow")}</span></a></td>' if actions else ''
    return f'''<tr data-status="{s}"><td><a class="t-fest" href="org-fest.html"><img src="assets/img/{img}.jpg" alt="" width="64" height="44"><span><b>{n}</b><span class="chip chip--sun">{c}</span></span></a></td>
      <td><b class="t-b">{d}</b><small class="t-s">{v}</small></td><td><b class="t-b">{r:,} / {cap:,}</b><span class="bar t-bar"><i style="width:{pct}%"></i></span></td><td>{st(s)}</td>{act}</tr>'''
EVS = [  # name, cat, date, venue, status, regs
 ('Chords &amp; Chaos', 'Cultural', 'Dec 18, 2026', 'Main Stage Auditorium', 'live', '42 / 60', 'v4/dance'),
 ('Capture the Flag Finals', 'Technical', 'Dec 18, 2026', 'LHC Lab 2', 'pub', '28 / 40 teams', 'fests/event-hackathon'),
 ('Bug Bounty Blitz', 'Technical', 'Dec 19, 2026', 'LHC Lab 1', 'pub', '64 / 100', 'v4/hack'),
 ('Crypto Cipher Hunt', 'Quiz', 'Dec 19, 2026', 'Seminar Hall B', 'draft', '0 / 80', 'v4/quiz'),
 ('Web Exploit Arena', 'Technical', 'Dec 19, 2026', 'LHC Lab 3', 'cancel', '0 / 50', 'fests/event-robotics'),
]
STATUS_OPTS = [('live', 'Live'), ('pub', 'Published'), ('draft', 'Draft'), ('cancel', 'Cancelled')]
def ev_row(ev, scan=False):
    n, c, d, v, s, r, img = ev
    if scan:
        right = f'<a class="btn btn--primary btn--sm" href="org-gate.html">Scan<span class="dot dot--still">{ix("qr")}</span></a>'
    else:
        opts = ''.join(f'<option value="{k}"{" selected" if k == s else ""}>{l}</option>' for k, l in STATUS_OPTS)
        right = f'<label class="pill-sel pill--{STATUS[s][1]}"><select aria-label="Status for {n}" data-pill>{opts}</select>{ix("chev", "ic ic-xs")}</label><a class="icon-btn icon-btn--sm" href="org-event.html" aria-label="Open {n}">{ic("arrow")}</a>'
    return f'''<div class="erow" data-status="{s}"><img src="assets/img/{img}.jpg" alt="" width="120" height="80"><div class="erow-b"><span class="chip chip--sun">{c}</span><a href="org-event.html"><b>{n}</b></a><span class="erow-m"><span>{ix("cal", "ic ic-xs")}{d}</span><span>{ix("pin", "ic ic-xs")}{v}</span><span>{ix("users", "ic ic-xs")}{r}</span></span></div><div class="erow-r">{right}</div></div>'''

SCAN_MODAL = modal('m-scan', 'SCAN WHICH EVENT?', '<p class="m-sub">Pick the event at this gate. Only events happening today or tomorrow are listed.</p><div class="scan-list">' + ''.join(ev_row(x, True) for x in EVS[:3]) + '</div>', 'modal-wide')

# ---------- org overview ----------
attention = [('ok', 'users', '3 registrations need approval', 'Chords &amp; Chaos', 'org-event.html?tab=regs'),
             ('live', 'card', '&#8377;6,780 ready to withdraw', 'Wallet, RVCE Tech Event', 'org-event.html?tab=wallet'),
             ('up', 'camera', 'Add a gallery to Innovate X', 'Fests with photos get 2x saves', 'org-fest.html')]
att = ''.join(f'<a class="todo" href="{h}"><span class="todo-ic todo-ic--{k}">{ix(i, "ic ic-s")}</span><span><b>{t}</b><small>{s}</small></span>{ic("arrow", "ic ic-s")}</a>' for k, i, t, s, h in attention)
org_body = head([('Organiser', None), ('Overview', None)], 'GOOD EVENING, ROHAN', 'Two fests are live. Here&rsquo;s what&rsquo;s happening across MSRIT today.',
  f'<button class="btn btn--light" data-open="m-scan">Launch Scanner<span class="dot dot--still">{ix("qr")}</span></button><div class="dmenu-wrap"><button class="btn btn--primary" data-menu="create" aria-haspopup="true" aria-expanded="false">Create<span class="dot dot--still">{ix("plus")}</span></button><div class="dmenu dmenu--r" data-menu-for="create" hidden><a href="org-create-fest.html">{ix("party", "ic ic-s")}New fest</a><a href="org-create-event.html">{ix("ticket", "ic ic-s")}New event in a fest</a><a href="org-ad-new.html">{ix("flag", "ic ic-s")}New ad</a></div></div>') + f'''
<section class="stats">
  {stat('party', 'Total fests', '12', '2 live now', 'stat--o', 'org-fests.html')}
  {stat('zap', 'Live events', '4', 'Across 2 fests', '', 'org-fests.html')}
  {stat('users', 'Registrations', '1,342', '+18% vs last month', '', 'org-fests.html')}
  {stat('wallet', 'Revenue', '&#8377;2.48L', '&#8377;6,780 available', 'stat--s', 'org-event.html?tab=wallet')}
</section>
<div class="dgrid">
  <section class="dcard">
    <div class="dcard-h"><h2 class="dcard-t">Recent fests</h2><a class="dlink" href="org-fests.html">View all{ic('arrow', 'ic ic-xs')}</a></div>
    <div class="tscroll"><table class="dt"><thead><tr><th>Fest</th><th>Date &amp; venue</th><th>Registrations</th><th>Status</th></tr></thead><tbody>{''.join(fest_row(f, False) for f in OF[:3])}</tbody></table></div>
  </section>
  <aside class="dside">
    <section class="dcard"><div class="dcard-h"><h2 class="dcard-t">Needs attention</h2><span class="pill pill--live">3</span></div><div class="todos">{att}</div></section>
    <section class="dcard plan-card plan-free"><span class="grain" aria-hidden="true"></span><p class="eyebrow eyebrow--ink"><span></span>Free tier</p><b>1 of 1 fest used</b><span class="bar"><i style="width:100%"></i></span><b>3 of 5 events used</b><span class="bar"><i style="width:60%"></i></span><a class="btn btn--ink btn--block" href="org-plans.html">See Standard<span class="dot">{ic('arrow')}</span></a></section>
  </aside>
</div>
{SCAN_MODAL}'''

# ---------- gate controller ----------
HIST = [('Ananya Kulkarni', 'FH-CC-26-8QX1', '10:42 AM', 'ok'), ('Mohit Sharma', 'FH-CC-26-7LM3', '10:40 AM', 'ok'), ('Unknown ticket', 'FH-XX-00-0000', '10:37 AM', 'bad'), ('Divya Rao', 'FH-CC-26-2HB8', '10:31 AM', 'ok')]
hist = ''.join(f'<li class="hrow hrow--{k}"><span class="hrow-ic">{ix("check" if k == "ok" else "close", "ic ic-xs")}</span><span><b>{n}</b><small>{t}</small></span><time>{tm}</time></li>' for n, t, tm, k in HIST)
gate_body = head([('Organiser', 'org.html'), ('Gate scanner', None)], 'GATE CONTROLLER', '', f'<button class="btn btn--light btn--sm" data-open="m-scan">Switch event<span class="dot dot--still">{ix("reset")}</span></button>', f'<p class="dm-pre"><span class="pill pill--live">Live</span>Chords &amp; Chaos &middot; Main Stage Auditorium</p>') + f'''
{tabs([('scan', 'Scanner', None), ('manage', 'Manage', None)], 'gate')}
<section data-panel="scan" class="gate">
  <div class="gate-cam">
    <div class="seg" role="radiogroup" aria-label="Scan mode"><button class="is-on" data-mode="cam">{ix('camera', 'ic ic-s')}Live camera</button><button data-mode="code">{ix('ticket', 'ic ic-s')}Enter code</button></div>
    <div class="cam" data-cam>
      <video playsinline muted hidden></video>
      <span class="cam-frame" aria-hidden="true"><i></i><i></i><i></i><i></i><span class="cam-line"></span></span>
      <div class="cam-idle"><span class="cam-ic">{ix('camera')}</span><b>CAMERA STANDBY</b><p>Point the camera at an attendee&rsquo;s QR pass. Allow camera access when your browser asks.</p><button class="btn btn--primary btn--sm cam-start">Start Camera<span class="dot dot--still">{ix('camera')}</span></button></div>
      <p class="cam-err" hidden>{ix('info', 'ic ic-s')}<span>Camera blocked or in use. Allow access from your browser&rsquo;s address bar, or enter the code instead.</span></p>
    </div>
    <form class="code" hidden><label class="m-label" for="tcode">Registration ID</label><div class="code-row"><label class="fld">{ix('ticket')}<input id="tcode" placeholder="e.g. FH-CC-26-8QX1" autocomplete="off"></label><button class="btn btn--ink">Verify<span class="dot">{ic('arrow')}</span></button></div><p class="m-hint">{ix('info', 'ic ic-xs')}<span>Try FH-CC-26-4KQ9 for a valid pass.</span></p></form>
  </div>
  <div class="gate-side">
    <div class="res res--wait" aria-live="polite">
      <span class="res-ic">{ix('qr')}</span><b class="res-t">WAITING FOR SCAN</b><p class="res-p">Scan an attendee&rsquo;s QR pass to verify it at the gate.</p>
    </div>
    <div class="dcard"><div class="dcard-h"><h2 class="dcard-t">Check-in history</h2><span class="hcount"><b>38</b> / 60 in</span></div><ul class="hlist">{hist}</ul></div>
  </div>
</section>
<section data-panel="manage" hidden>
  <div class="stats stats--4">
    {stat('users', 'Total registrations', '60')}{stat('okc', 'Approved', '52', '', 'stat--ok')}{stat('calcheck', 'Checked in', '38', '73% of approved', 'stat--o')}{stat('hourglass', 'Still to arrive', '14')}
    {stat('info', 'Pending', '3', '', 'stat--s')}{stat('flag', 'Waitlisted', '4')}{stat('close', 'Rejected', '1')}{stat('trophy', 'Team capacity', '8 / 8', 'Full')}
  </div>
  <div class="dcard"><div class="dcard-h"><h2 class="dcard-t">Arrival progress</h2><b class="t-b">38 of 52</b></div><span class="bar bar--big"><i style="width:73%"></i></span><p class="dm-sub">Doors close at 11:30 AM. Late arrivals need organiser approval.</p></div>
</section>
{SCAN_MODAL}'''

# ---------- fests list ----------
counts = {s: sum(1 for f in OF if f[6] == s) for s in ('live', 'up', 'draft', 'past')}
fests_body = head([('Organiser', 'org.html'), ('Fests &amp; Events', None)], 'FESTS &amp; EVENTS', 'Every fest your college runs on FestHey, from drafts to the archive.', f'<a class="btn btn--primary" href="org-create-fest.html">Create Fest<span class="dot dot--still">{ix("plus")}</span></a>') + f'''
<div class="dbar">{tabs([('all', 'All', len(OF)), ('live', 'Live', counts['live']), ('up', 'Upcoming', counts['up']), ('draft', 'Draft', counts['draft']), ('past', 'Past', counts['past'])], 'filter')}<label class="lb-search">{ix('search')}<input type="search" placeholder="Search fests" aria-label="Search fests" data-search></label></div>
<section class="dcard dcard--flush"><div class="tscroll"><table class="dt dt--rows"><thead><tr><th>Fest</th><th>Date &amp; venue</th><th>Registrations</th><th>Status</th><th><span class="sr">Action</span></th></tr></thead><tbody>{''.join(fest_row(f) for f in OF)}</tbody></table></div><p class="lb-empty d-empty" hidden>No fests here yet.</p></section>'''

# ---------- fest detail ----------
GAL = ['v4/pronite', 'v4/hack', 'fests/event-hackathon', 'v4/quiz']
fest_body = head([('Organiser', 'org.html'), ('Fests', 'org-fests.html'), ('ByteForce CTF', None)], 'BYTEFORCE CTF', '', f'<button class="btn btn--light btn--sm" data-toast="Fest unpublished. It is hidden from students.">Unpublish<span class="dot dot--still">{ix("eye")}</span></button><a class="btn btn--light btn--sm" href="org-create-fest.html">Edit<span class="dot dot--still">{ix("edit")}</span></a><a class="btn btn--ink btn--sm" href="fest.html">View Live<span class="dot">{ic("arrow")}</span></a>', f'<p class="dm-pre"><span class="pill pill--live">Live</span>Udbhav 2026 &middot; Technical</p>') + f'''
<section class="fsum">
  <div class="fsum-img"><img src="assets/img/fests/event-hackathon.jpg" alt="" width="1280" height="720"><span class="chip chip--light">{ix('pin', 'ic ic-xs')}Bengaluru, Karnataka</span></div>
  <div class="fsum-tl">
    <p class="eyebrow"><span></span>Timeline</p>
    <ol class="tl"><li class="tl--done"><b>Registrations open</b><small>Nov 20, 2026</small></li><li class="tl--hot"><b>Deadline</b><small>Dec 15, 2026 &middot; in 1 day</small></li><li><b>Fest starts</b><small>Dec 18, 2026</small></li><li><b>Fest ends</b><small>Dec 19, 2026</small></li></ol>
  </div>
</section>
<section class="stats stats--3">
  {stat('ticket', 'Events', '28', '24 published')}{stat('users', 'Registrations', '3,248', '+18% vs last fest', 'stat--o')}{stat('rupee', 'Revenue', '&#8377;2,48,560', 'After platform fee', 'stat--s')}
</section>
<section class="dcard">
  <div class="dcard-h"><div><h2 class="dcard-t">Gallery</h2><p class="dm-sub">Add 10 to 20 photos. Fests with a gallery get twice the saves.</p></div><span class="pill pill--draft">4 / 20</span></div>
  <div class="gal-grid">{''.join(f'<figure><img src="assets/img/{g}.jpg" alt="" width="800" height="1200"><button class="gal-x" aria-label="Remove photo">{ix("close", "ic ic-xs")}</button></figure>' for g in GAL)}<label class="gal-add"><input type="file" accept="image/*" multiple hidden>{ix('plus')}<span>Add photos</span></label></div>
</section>
<section class="dsec">
  <div class="dcard-h"><h2 class="dsec-t">Events</h2><a class="btn btn--primary btn--sm" href="org-create-event.html">Create Event<span class="dot dot--still">{ix("plus")}</span></a></div>
  <div class="dbar">{tabs([('all', 'All', 5), ('live', 'Live', 1), ('pub', 'Published', 2), ('draft', 'Draft', 1), ('cancel', 'Cancelled', 1)], 'filter')}</div>
  <div class="elist">{''.join(ev_row(x) for x in EVS)}</div><p class="lb-empty d-empty" hidden>No events here yet.</p>
</section>'''

# ---------- event detail (tabs) ----------
REGS = [('SpiderTrack', 'Rohan Verma', 'rohan.v@festhey.in', 'R V College of Engineering', 'FH-RT-26-9934', 'pend', 1, 3),
        ('Bit Bandits', 'Ananya Kulkarni', 'ananya.k@festhey.in', 'BMSCE', 'FH-RT-26-1182', 'ok', 3, 3),
        ('Null Pointers', 'Mohit Sharma', 'mohit.s@festhey.in', 'RVCE', 'FH-RT-26-4410', 'wait', 2, 3),
        ('Kernel Panic', 'Divya Rao', 'divya.r@festhey.in', 'PES University', 'FH-RT-26-7720', 'ok', 3, 3),
        ('Root Access', 'Karan Mehta', 'karan.m@festhey.in', 'Christ University', 'FH-RT-26-3051', 'rej', 1, 3)]
REG_OPTS = [('pend', 'Pending'), ('ok', 'Approved'), ('wait', 'Waitlisted'), ('rej', 'Rejected')]
def reg_card(r, i):
    team, n, em, col, tid, s, have, need = r
    opts = ''.join(f'<option value="{k}"{" selected" if k == s else ""}>{l}</option>' for k, l in REG_OPTS)
    return f'''<div class="rcard" data-status="{s}"><label class="rc-ck"><input type="checkbox" aria-label="Select {n}"><span class="ck-box">{ic("check")}</span></label><img src="assets/img/av{i % 4 + 1}.jpg" alt="" width="48" height="48"><div class="rc-b"><span class="rc-team">{ix("users", "ic ic-xs")}Team {team} &middot; {have} of {need} joined</span><b>{n}</b><span class="rc-m"><span>{ix("mail", "ic ic-xs")}{em}</span><span>{ix("school", "ic ic-xs")}{col}</span><span>{ix("ticket", "ic ic-xs")}{tid}</span></span></div><label class="pill-sel pill--{STATUS[s][1]}"><select aria-label="Status for {n}" data-pill>{opts}</select>{ix("chev", "ic ic-xs")}</label></div>'''
ACT = [('In', 'Registration, Team Bit Bandits', 'Dec 12, 4:10 PM', '+ &#8377;300.00'), ('In', 'Registration, Team Kernel Panic', 'Dec 12, 1:02 PM', '+ &#8377;300.00'), ('Fee', 'Platform fee, December', 'Dec 1', '&minus; &#8377;420.00'), ('In', 'Registration, Team SpiderTrack', 'Nov 30, 9:45 AM', '+ &#8377;100.00')]
act = ''.join(f'<li class="tx"><span class="tx-ic tx-ic--{"in" if k == "In" else "out"}">{ix("download" if k == "In" else "receipt", "ic ic-s")}</span><span><b>{t}</b><small>{d}</small></span><b class="tx-amt {"is-in" if k == "In" else ""}">{a}</b></li>' for k, t, d, a in ACT)
DEL = modal('m-del', 'DELETE THIS EVENT?', f'<p class="m-sub">RVCE Tech Event and its 5 registrations will be removed. Registered students are refunded automatically and notified by email. This can&rsquo;t be undone.</p><label class="m-label" for="delc">Type <b>DELETE</b> to confirm</label><label class="fld"><input id="delc" autocomplete="off" data-confirm="DELETE"></label><button class="btn btn--primary btn--block m-go" disabled data-confirm-btn data-toast="Event deleted. Students are being refunded.">Delete Event<span class="dot dot--still">{ix("trash")}</span></button>')
event_body = head([('Organiser', 'org.html'), ('8th Mile 2026', 'org-fest.html'), ('RVCE Tech Event', None)], 'RVCE TECH EVENT', '', f'<a class="btn btn--light btn--sm" href="org-create-event.html">Edit<span class="dot dot--still">{ix("edit")}</span></a><button class="btn btn--light btn--sm" data-toast="Event unpublished">Unpublish<span class="dot dot--still">{ix("eye")}</span></button><button class="btn btn--light btn--sm btn--danger" data-open="m-del">Delete<span class="dot dot--still">{ix("trash")}</span></button>', f'<p class="dm-pre"><span class="pill pill--live">Live</span>8th Mile 2026 &middot; Technical</p>') + f'''
{tabs([('ov', 'Overview', None), ('regs', 'Registrations', 5), ('wallet', 'Wallet &amp; payouts', None)], 'event')}
<section data-panel="ov" class="evo">
  <div>
    <div class="tiles tiles--2x">{''.join(f'<div class="tile"><span class="tile-ic">{ix(i, "ic ic-s")}</span><span><small>{l}</small><b>{v}</b></span></div>' for i, l, v in [('clock', 'Registration deadline', 'Dec 15, 2026'), ('cal', 'Event day', 'Sat, Dec 19, 2026'), ('pin', 'Venue', 'Audi 1, RVCE'), ('flag', 'Category', 'Technical')])}</div>
    <div class="dcard"><p class="eyebrow"><span></span>About the event</p><p class="evo-p">A free event that tests your technical skills across three timed rounds. Come be a part of it and earn a chance to win the grand prize.</p></div>
    <a class="dcta" href="?tab=regs" data-goto="regs"><span class="tile-ic">{ix('users', 'ic ic-s')}</span><span><b>Registrations</b><small>3 waiting for your approval</small></span><span class="btn btn--ink btn--sm">Review<span class="dot">{ic('arrow')}</span></span></a>
  </div>
  <aside class="entry"><span class="grain" aria-hidden="true"></span><small>Entry fee</small><b class="entry-big">&#8377;100<span>/ member</span></b><div class="entry-rows"><span>{ix('users', 'ic ic-s')}<b>1 to 3</b> members a team</span><span>{ix('trophy', 'ic ic-s')}<b>7 of 8</b> team slots left</span></div><span class="bar"><i style="width:12%"></i></span></aside>
</section>
<section data-panel="regs" hidden>
  <div class="stats stats--4">{stat('users', 'Total', '5')}{stat('okc', 'Approved', '2', '', 'stat--ok')}{stat('info', 'Pending', '1', '', 'stat--s')}{stat('trophy', 'Slots left', '7 / 8')}</div>
  <div class="dbar">{tabs([('all', 'All', 5), ('pend', 'Pending', 1), ('ok', 'Approved', 2), ('wait', 'Waitlisted', 1), ('rej', 'Rejected', 1)], 'filter')}<label class="lb-search">{ix('search')}<input type="search" placeholder="Search name or team" aria-label="Search registrations" data-search></label></div>
  <div class="bulk" hidden><b><span data-bulk-n>0</span> selected</b><button class="btn btn--primary btn--sm" data-bulk="ok">Approve<span class="dot dot--still">{ic('check')}</span></button><button class="btn btn--light btn--sm" data-bulk="wait">Waitlist<span class="dot dot--still">{ix('hourglass')}</span></button></div>
  <div class="rlist">{''.join(reg_card(r, i) for i, r in enumerate(REGS))}</div><p class="lb-empty d-empty" hidden>No registrations match.</p>
</section>
<section data-panel="wallet" hidden>
  <div class="wallet"><span class="grain" aria-hidden="true"></span><div><small>Available to withdraw</small><b>&#8377;6,780.00</b><p>Settled to HDFC Bank &middot;&middot;&middot;&middot; 4421 within 2 business days.</p></div><button class="btn btn--ink" data-toast="Payout of &#8377;6,780 requested. You&rsquo;ll get an email when it lands.">Request Payout<span class="dot">{ic('arrow')}</span></button></div>
  <div class="stats stats--4">{stat('zap', 'Total revenue', '&#8377;8,400')}{stat('receipt', 'Platform fee', '&#8377;420')}{stat('hourglass', 'Pending', '&#8377;1,200', 'Clears after the event')}{stat('download', 'Withdrawn', '&#8377;0')}</div>
  <div class="dcard"><div class="dcard-h"><h2 class="dcard-t">Recent activity</h2><a class="dlink" href="#">Export CSV{ix('download', 'ic ic-xs')}</a></div><ul class="txs">{act}</ul></div>
</section>
{DEL}'''

# ---------- create fest ----------
create_fest_body = head([('Organiser', 'org.html'), ('Fests', 'org-fests.html'), ('Create fest', None)], 'CREATE FEST', 'Set up the fest first. You&rsquo;ll add events to it next.') + f'''
<div class="cf">
  <form class="dcard cf-form" action="org-fest.html" novalidate>
    <div class="fgrid">
      {field('Fest title', inp('party', 'e.g. Mood Indigo 2026', '', 'text', 'title'))}
      {field('Theme category', select(['Cultural', 'Technical', 'Sports', 'Quiz', 'Hackathon', 'Management'], 'Technical'))}
      {field('Tagline', inp('', 'A one-line pitch for your fest', '', 'text', 'tag'), 'df--full')}
      {field('Fest banner', upload('Click to upload banner', 'PNG, JPG or WebP, 16:9, up to 10 MB'), 'df--full')}
      {field('Registrations open', inp('cal', '', '', 'date'))}
      {field('Registration deadline', inp('clock', '', '', 'date'))}
      {field('Grand opening', inp('cal', '', '', 'date'))}
      {field('Finale', inp('cal', '', '', 'date'))}
    </div>
    <button class="btn btn--primary btn--block m-go">Create Fest<span class="dot">{ic('arrow')}</span></button>
  </form>
  <aside class="cf-prev"><p class="eyebrow"><span></span>Live preview</p><div class="prev"><div class="prev-img"><img alt="" hidden data-prev-img><span class="prev-ph">{ix('camera')}</span><span class="chip chip--light prev-date" data-prev-date>Dates appear here</span></div><div class="prev-b"><span class="chip chip--sun" data-prev-cat>Technical</span><b data-prev-title>Your fest title</b><small data-prev-tag>Your tagline shows up on cards across FestHey.</small></div></div><p class="m-hint">{ix('info', 'ic ic-xs')}<span>This is how students will see your fest in listings.</span></p></aside>
</div>'''

# ---------- create event wizard ----------
AMEN = [('coffee', 'Breakfast'), ('wifi', 'Free Wi-Fi'), ('drop', 'Drinking water'), ('snow', 'Air conditioning'), ('plug', 'Charging points'), ('gift', 'Goodies')]
def rep(name, ph1, ph2=None):
    two = f'<label class="fld"><input placeholder="{ph2}"></label>' if ph2 else ''
    return f'<div class="rep" data-rep="{name}"><div class="rep-row{" rep-row--2" if ph2 else ""}"><label class="fld"><input placeholder="{ph1}"></label>{two}<button type="button" class="icon-btn icon-btn--sm rep-x" aria-label="Remove">{ix("close")}</button></div></div>'
def rep_h(title, name, add):
    return f'<div class="rep-h"><span class="m-label">{title}</span><button type="button" class="btn btn--light btn--sm" data-add="{name}">{add}<span class="dot dot--still">{ix("plus")}</span></button></div>'
STEPS = ['Basics', 'Schedule', 'Prizes &amp; rules']
wizard_body = head([('Organiser', 'org.html'), ('ByteForce CTF', 'org-fest.html'), ('Create event', None)], 'CREATE EVENT', 'Three quick steps. Your progress is saved as a draft.') + f'''
<ol class="wsteps">{''.join(f'<li class="{"is-on" if i == 0 else ""}"><span>{i + 1}</span><b>{s}</b></li>' for i, s in enumerate(STEPS))}</ol>
<form class="wiz" action="org-fest.html" novalidate>
  <section class="dcard wstep" data-step="1">
    <h2 class="dcard-t">The basics</h2>
    <div class="fgrid">
      {field('Event title', inp('ticket', 'e.g. Robo Wars'))}
      {field('Category', select(['Cultural', 'Technical', 'Sports', 'Quiz', 'Hackathon'], 'Technical'))}
      {field('Amenities', '<div class="chips amen">' + ''.join(f'<button type="button" class="chip" aria-pressed="false">{ix(i, "ic ic-s")}{l}</button>' for i, l in AMEN) + '</div>', 'df--full')}
      {field('Who can register', '<div class="rcards"><label class="rcard2"><input type="radio" name="vis" checked><span><b>Public</b><small>Open to students from any college</small></span></label><label class="rcard2"><input type="radio" name="vis"><span><b>Intra-college</b><small>Only verified MSRIT students</small></span></label></div>', 'df--full')}
      {field('Short summary', '<label class="fld fld--area"><textarea rows="3" placeholder="Describe the energy in two lines"></textarea></label>', 'df--full')}
      {field('Event banner (16:9)', upload('Upload banner', 'PNG, JPG or WebP, up to 10 MB'))}
      {field('Listing poster (1:1)', upload('Upload poster', 'Square works best', 'sq'))}
    </div>
  </section>
  <section class="dcard wstep" data-step="2" hidden>
    <h2 class="dcard-t">When and where</h2>
    <div class="fgrid">
      {field('Event date', inp('cal', '', '', 'date'))}{field('Start time', inp('clock', '', '', 'time'))}
      {field('Registration deadline', inp('hourglass', '', '', 'date'))}{field('Venue', inp('pin', 'e.g. Main Stage'))}
    </div>
    <div class="rep-h"><span class="m-label">Schedule</span><button type="button" class="btn btn--light btn--sm" data-add="sched">Add slot<span class="dot dot--still">{ix("plus")}</span></button></div>
    <div class="rep" data-rep="sched"><div class="slot"><div class="fgrid fgrid--4"><label class="fld"><input placeholder="e.g. Opening ceremony"></label><label class="fld"><input placeholder="Venue (optional)"></label><label class="fld">{ix('clock')}<input type="time" aria-label="From"></label><label class="fld">{ix('clock')}<input type="time" aria-label="To"></label></div><button type="button" class="icon-btn icon-btn--sm rep-x" aria-label="Remove slot">{ix("close")}</button></div></div>
  </section>
  <section class="dcard wstep" data-step="3" hidden>
    <h2 class="dcard-t">Prizes and rules</h2>
    {field('Prize pool summary', inp('trophy', 'e.g. &#8377;1,00,000 plus hardware'), 'df--full')}
    {rep_h('Prizes', 'prize', 'Add prize')}{rep('prize', '1st place', 'e.g. &#8377;50,000')}
    {rep_h('Rules', 'rule', 'Add rule')}{rep('rule', 'e.g. Judges&rsquo; decisions are final')}
    {rep_h('Eligibility', 'elig', 'Add rule')}{rep('elig', 'e.g. A valid college ID is required')}
    <h3 class="dcard-t dcard-t--s">Teams and fees</h3>
    <div class="fgrid fgrid--4">{stepper('Min team size', 1)}{stepper('Max team size', 3)}{stepper('Team slots', 40)}{stepper('Entry fee (&#8377;)', 100)}</div>
  </section>
  <div class="wnav"><button type="button" class="btn btn--light" data-prev hidden>Previous<span class="dot dot--still">{ic('left')}</span></button><button type="button" class="btn btn--primary" data-next>Next<span class="dot">{ic('arrow')}</span></button><button class="btn btn--primary" data-create hidden>Create Event<span class="dot">{ic('arrow')}</span></button></div>
</form>'''

# ---------- college profile ----------
college_body = head([('Organiser', 'org.html'), ('College profile', None)], 'COLLEGE PROFILE', 'This is what students see on your public college page.', f'<a class="btn btn--light btn--sm" href="college.html">View Public Page<span class="dot">{ic("arrow")}</span></a><button class="btn btn--ink btn--sm" data-toast="Profile saved">Save Changes<span class="dot dot--still">{ic("check")}</span></button>') + f'''
<section class="cprof"><label class="cprof-banner"><input type="file" accept="image/*" hidden><img src="assets/img/v4/hosts.jpg" alt="" width="800" height="1200" class="drop-img"><span class="chip chip--light">{ix('camera', 'ic ic-xs')}Change banner</span></label><div class="cprof-id"><span class="cprof-av">MS</span><div><h2 class="dcard-t">M S Ramaiah Institute of Technology</h2><p class="dm-sub">{ix('pin', 'ic ic-xs')}Bengaluru, Karnataka 560054 &middot; msrit.edu</p></div><span class="pill pill--ok">{ix('shield', 'ic ic-xs')}Verified Jun 30, 2026</span></div></section>
<div class="dgrid dgrid--even">
  <section class="dcard"><h2 class="dcard-t">Details</h2><div class="fgrid fgrid--1">{field('Official name', inp('school', '', 'M S Ramaiah Institute of Technology'))}{field('City and PIN', inp('pin', '', 'Bengaluru, Karnataka 560054'))}{field('Website', inp('link', '', 'msrit.edu'))}</div></section>
  <section class="dcard"><h2 class="dcard-t">Point of contact</h2><div class="fgrid fgrid--1">{field('Full name', inp('user', '', 'Dr. Sanjay Gowda'))}{field('Email', inp('mail', '', 'sanjay.gowda@msrit.edu', 'email'))}{field('Mobile', inp('phone', '', '+91 98765 43212', 'tel'))}</div></section>
</div>
<section class="dcard"><div class="dcard-h"><div><h2 class="dcard-t">Campus gallery</h2><p class="dm-sub">Shown on your public page. 6 of 20 photos.</p></div></div><div class="gal-grid gal-grid--6">{''.join(f'<figure><img src="assets/img/{g}.jpg" alt="" width="800" height="1200"><button class="gal-x" aria-label="Remove photo">{ix("close", "ic ic-xs")}</button></figure>' for g in ['v4/pronite', 'v4/dance', 'v4/hoops', 'v4/quiz', 'v4/hack', 'v4/robo'])}<label class="gal-add"><input type="file" accept="image/*" multiple hidden>{ix('plus')}<span>Add photos</span></label></div></section>
<section class="dcard plan-strip"><span class="tile-ic">{ix('card', 'ic ic-s')}</span><span><small>Active plan</small><b class="plan-free">Free tier &middot; 1 fest, 5 events</b><b class="plan-pro">Standard &middot; unlimited fests and events</b></span><a class="btn btn--light btn--sm" href="org-plans.html">Manage Plan<span class="dot">{ic("arrow")}</span></a></section>'''

# ---------- ads & sponsors ----------
POS = [('1', 'Top banner', 'Full-width banner at the top of the home page.', '2,500', 'top'), ('2', 'Listing card', 'A featured card inside fest listings.', '500', 'list'), ('3', 'Pop-up', 'A pop-up shown once per visit on event pages.', '200', 'modal')]
def pos_vis(k):
    return f'<span class="pv pv--{k}" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'
MY_ADS = [('BeatWave 2026', 'Top banner', 'Jan 10 to Feb 25, 2027', 'live', '12,430', '842'), ('Cultfest 2026', 'Listing card', 'Dec 1 to Dec 5, 2026', 'live', '5,210', '390'), ('Innovate X', 'Pop-up', 'Jan 2 to Jan 14, 2027', 'up', '0', '0')]
ads = ''.join(f'<div class="adrow"><span class="pv-mini">{pos_vis(["top", "list", "modal"][i])}</span><div><b>{n}</b><small>{p} &middot; {d}</small></div><span class="ad-n"><b>{v}</b><small>Views</small></span><span class="ad-n"><b>{c}</b><small>Clicks</small></span><span class="ad-n"><b>{(round(int(c.replace(",", "")) / int(v.replace(",", "")) * 100, 1) if v != "0" else 0)}%</b><small>CTR</small></span>{st(s)}<button class="icon-btn icon-btn--sm" aria-label="Edit {n}">{ix("edit")}</button></div>' for i, (n, p, d, s, v, c) in enumerate(MY_ADS))
SPONS = [('Red Bull India', 'Beverages', 'Mumbai', 'Events above 500 attendees'), ('boAt', 'Consumer tech', 'Delhi', 'Music and cultural fests'), ('Unstop', 'Careers', 'Delhi', 'Hackathons and case comps'), ('Zomato', 'Food', 'Gurugram', 'Food stalls and pro-nights'), ('Devfolio', 'Developer tools', 'Bengaluru', 'Hackathons'), ('Swiggy', 'Food', 'Bengaluru', 'Cultural fests'), ('Coding Ninjas', 'Edtech', 'Delhi', 'Technical events'), ('Decathlon', 'Sports retail', 'Bengaluru', 'Sports meets')]
spons = ''.join(f'<article class="sp"><span class="sp-av">{"".join(w[0] for w in n.split()[:2])}</span><b>{n}</b><span class="chip chip--light">{c}</span><small>{ix("pin", "ic ic-xs")}{l}</small><p>{t}</p><a class="btn btn--sun btn--sm btn--block" href="mailto:partnerships@example.com">Contact<span class="dot dot--still">{ix("mail")}</span></a></article>' for n, c, l, t in SPONS)
LOCKS = ['Sponsor names', 'Company details', 'Websites', 'Locations', 'Sponsorship interests', 'Contact information']
ads_body = head([('Organiser', 'org.html'), ('Ads &amp; Sponsors', None)], 'ADS &amp; SPONSORS', 'Promote your fests across FestHey and find brands to back them.', f'<a class="btn btn--primary" href="org-ad-new.html">Create Ad<span class="dot dot--still">{ix("plus")}</span></a>') + f'''
{tabs([('ads', 'Ads', 3), ('sponsors', 'Sponsors', None)], 'ads')}
<section data-panel="ads">
  <div class="stats stats--3">{stat('eye', 'Ad views', '17,640', 'Last 30 days')}{stat('zap', 'Clicks', '1,232', '7.0% CTR', 'stat--o')}{stat('users', 'Registrations from ads', '214', '&#8377;21,400 revenue', 'stat--s')}</div>
  <section class="dcard"><div class="dcard-h"><h2 class="dcard-t">Your ads</h2></div><div class="adlist">{ads}</div></section>
  <h2 class="dsec-t">Ad positions</h2><p class="dm-sub">Each ad runs in one dedicated spot. Pick the one that fits your goal.</p>
  <div class="poss">{''.join(f'<a class="pos" href="org-ad-new.html?pos={k}">{pos_vis(v)}<span class="pill pill--draft">Position {k}</span><b>{n}</b><small>{d}</small><span class="pos-p">&#8377;{p} <small>per ad</small></span></a>' for k, n, d, p, v in POS)}</div>
</section>
<section data-panel="sponsors" hidden>
  <div class="sp-wrap">
    <div class="sp-grid">{spons}</div>
    <div class="sp-lock plan-free"><div class="lockc"><span class="lockc-ic">{ix('lock')}</span><h2 class="dcard-t">SPONSOR DETAILS ARE LOCKED</h2><p class="dm-sub">The sponsor directory is part of the Standard plan. Upgrade to see:</p><ul class="ok-list ok-list--2">{''.join(f'<li><span class="perk-ic">{ic("check")}</span>{t}</li>' for t in LOCKS)}</ul><a class="btn btn--primary btn--block" href="org-upgrade.html">Upgrade for &#8377;999 / year<span class="dot">{ic("arrow")}</span></a></div></div>
  </div>
</section>'''

# ---------- create ad ----------
ad_new_body = head([('Organiser', 'org.html'), ('Ads', 'org-ads.html'), ('Create ad', None)], 'CREATE AD', 'Ads are paid per placement, separately from your plan.') + f'''
<div class="cf">
  <form class="cf-form" action="org-ads.html" novalidate>
    <section class="dcard"><h2 class="dcard-t"><span class="nstep">1</span>Pick a position</h2><div class="poss poss--pick">{''.join(f'<label class="pos"><input type="radio" name="pos" value="{p}" data-price="{p.replace(",", "")}" data-name="{n}"{" checked" if k == "1" else ""}>{pos_vis(v)}<span class="pill pill--draft">Position {k}</span><b>{n}</b><small>{d}</small><span class="pos-p">&#8377;{p}</span></label>' for k, n, d, p, v in POS)}</div></section>
    <section class="dcard"><h2 class="dcard-t"><span class="nstep">2</span>What are you promoting?</h2>{select(['ByteForce CTF (fest)', 'Cultfest 2026 (fest)', 'Chords &amp; Chaos (event)', 'Innovate X (fest)'])}</section>
    <section class="dcard"><h2 class="dcard-t"><span class="nstep">3</span>Ad image <small class="opt">Optional</small></h2><p class="dm-sub">Skip it and we&rsquo;ll use your fest banner.</p>{upload('Upload ad image', 'PNG, JPG or WebP, up to 10 MB')}</section>
    <section class="dcard"><h2 class="dcard-t"><span class="nstep">4</span>Schedule</h2><div class="fgrid">{field('Start date', inp('cal', '', '', 'date'))}{field('End date', inp('cal', '', '', 'date'))}</div></section>
  </form>
  <aside class="cf-prev"><div class="dcard sumcard"><h2 class="dcard-t">Summary</h2><dl class="sum"><div><dt>Position</dt><dd data-sum-name>Top banner</dd></div><div><dt>Placement fee</dt><dd data-sum-fee>&#8377;2,500.00</dd></div><div><dt>GST (18%)</dt><dd data-sum-gst>&#8377;450.00</dd></div><div class="sum-total"><dt>Total</dt><dd data-sum-total>&#8377;2,950.00</dd></div></dl><a class="btn btn--primary btn--block" href="org-ads.html">Pay &amp; Publish<span class="dot dot--still">{ix("lock")}</span></a><p class="m-secure">{ix('shield', 'ic ic-xs')}Ads go live after a quick review, usually within 2 hours.</p></div></aside>
</div>'''

# ---------- plans ----------
FEAT = [('Fests', '1', 'Unlimited'), ('Events', 'Up to 5', 'Unlimited'), ('Organiser dashboard', 'yes', 'yes'), ('Gate scanner', 'yes', 'yes'), ('Create ads', 'yes', 'yes'), ('Publish ads', 'Paid per ad', 'Paid per ad'), ('Sponsor management', 'yes', 'yes'), ('Sponsor directory', 'no', 'yes')]
def cell(v):
    return f'<span class="yes">{ic("check", "ic ic-s")}</span>' if v == 'yes' else (f'<span class="no">{ix("lock", "ic ic-xs")}Locked</span>' if v == 'no' else v)
cmp_rows = ''.join(f'<tr><td>{a}</td><td>{cell(b)}</td><td>{cell(c)}</td></tr>' for a, b, c in FEAT)
FREE_L = ['1 fest', 'Up to 5 events', 'Organiser dashboard', 'Gate scanner', 'Create ads', 'Sponsor management']
PRO_L = ['Unlimited fests', 'Unlimited events', 'Everything in Free', 'Full sponsor directory', 'Sponsor contact details', 'Priority support']
HIST_R = [('Nov 12, 2026', 'Standard, yearly', '&#8377;1,178.82', 'paid'), ('Nov 12, 2025', 'Standard, yearly', '&#8377;1,178.82', 'paid'), ('Oct 2, 2025', 'Standard, yearly', '&#8377;1,178.82', 'refund')]
plans_body = head([('Organiser', 'org.html'), ('Subscription', None)], 'SUBSCRIPTION &amp; PLANS', 'Two plans. Upgrade when you need more fests or the sponsor directory.') + f'''
<div class="plans">
  <article class="planc"><p class="eyebrow"><span></span>Free</p><h2 class="planc-n">Free tier</h2><p class="planc-p"><b>&#8377;0</b><span>forever</span></p><ul class="ok-list">{''.join(f'<li><span class="perk-ic">{ic("check")}</span>{t}</li>' for t in FREE_L)}</ul><span class="btn btn--light btn--block plan-free planc-cur">Current Plan<span class="dot dot--still">{ic("check")}</span></span></article>
  <article class="planc planc--pro"><span class="grain" aria-hidden="true"></span><span class="planc-rec">Recommended</span><span class="pill pill--ok plan-pro planc-act">Active, renews Nov 12, 2027</span><p class="eyebrow eyebrow--ink"><span></span>Standard</p><h2 class="planc-n">Standard</h2><p class="planc-p"><b>&#8377;999</b><span>per year + GST</span></p><ul class="ok-list">{''.join(f'<li><span class="perk-ic">{ic("check")}</span>{t}</li>' for t in PRO_L)}</ul><a class="btn btn--ink btn--block plan-free" href="org-upgrade.html">Upgrade to Standard<span class="dot">{ic("arrow")}</span></a><button class="btn btn--light btn--block plan-pro" data-open="m-cancel">Cancel Subscription<span class="dot dot--still">{ix("close")}</span></button></article>
</div>
<div class="note">{ix('info', 'ic ic-s')}<p><b>Ads are paid separately.</b> Your plan unlocks features only. Publishing an ad needs a one-time payment for the position you choose, on either plan.</p></div>
<section class="dcard dcard--flush"><div class="dcard-h dcard-h--pad"><h2 class="dcard-t">Compare plans</h2></div><div class="tscroll"><table class="dt dt--cmp"><thead><tr><th>Feature</th><th>Free</th><th>Standard</th></tr></thead><tbody>{cmp_rows}</tbody></table></div></section>
<section class="dcard dcard--flush plan-pro"><div class="dcard-h dcard-h--pad"><h2 class="dcard-t">Billing history</h2></div><div class="tscroll"><table class="dt"><thead><tr><th>Date</th><th>Plan</th><th>Amount</th><th>Status</th><th>Invoice</th></tr></thead><tbody>{''.join(f'<tr><td>{d}</td><td>{p}</td><td><b class="t-b">{a}</b></td><td>{st(s)}</td><td><a class="dlink" href="#">Download{ix("download", "ic ic-xs")}</a></td></tr>' for d, p, a, s in HIST_R)}</tbody></table></div></section>
''' + modal('m-cancel', 'CANCEL STANDARD?', f'<p class="m-sub">Your plan stays active until <b>Nov 12, 2027</b>. After that your account moves to the Free tier:</p><ul class="ok-list ok-list--box">{"".join(f"<li><span class=perk-ic>{ic('check')}</span>{t}</li>" for t in FREE_L[:2])}<li><span class="perk-ic perk-ic--x">{ix("lock", "ic")}</span>Sponsor directory locks</li><li><span class="perk-ic perk-ic--x">{ix("lock", "ic")}</span>Extra fests become read-only</li></ul><a class="btn btn--ink btn--block m-go" href="org-plans.html">Cancel at Period End<span class="dot dot--still">{ix("close")}</span></a>')

# ---------- upgrade checkout ----------
METHODS = [('card', 'Credit or debit card', 'Visa, Mastercard, RuPay'), ('upi', 'UPI', 'Google Pay, PhonePe, Paytm'), ('nb', 'Net banking', 'All major banks')]
upgrade_body = head([('Organiser', 'org.html'), ('Subscription', 'org-plans.html'), ('Upgrade', None)], 'UPGRADE TO STANDARD', 'Unlimited fests, unlimited events and the full sponsor directory.') + f'''
<div class="cf">
  <form class="cf-form" action="org-plans.html" novalidate>
    <input type="hidden" name="plan" value="pro">
    <section class="upg"><span class="grain" aria-hidden="true"></span><div><p class="eyebrow eyebrow--ink"><span></span>Standard plan</p><p class="planc-p"><b>&#8377;999</b><span>per year</span></p><ul class="ok-list ok-list--2">{''.join(f'<li><span class="perk-ic">{ic("check")}</span>{t}</li>' for t in PRO_L)}</ul></div><span class="upg-crown">{ix('crown')}</span></section>
    <section class="dcard"><h2 class="dcard-t">Payment method</h2><div class="rcards rcards--col">{''.join(f'<label class="rcard2"><input type="radio" name="pm"{" checked" if i == 0 else ""}><span><b>{t}</b><small>{d}</small></span><span class="tile-ic">{ix(["card", "zap", "school"][i], "ic ic-s")}</span></label>' for i, (k, t, d) in enumerate(METHODS))}</div><p class="m-hint">{ix('shield', 'ic ic-xs')}<span>Payments are processed securely by Razorpay. FestHey never stores card details.</span></p></section>
  </form>
  <aside class="cf-prev"><div class="dcard sumcard"><h2 class="dcard-t">Billing summary</h2><dl class="sum"><div><dt>Standard, yearly</dt><dd>&#8377;999.00</dd></div><div><dt>GST (18%)</dt><dd>&#8377;179.82</dd></div><div class="sum-total"><dt>Total today</dt><dd>&#8377;1,178.82</dd></div></dl><label class="ck"><input type="checkbox" data-terms><span class="ck-box">{ic("check")}</span><span class="ck-t">I agree to the <a href="privacy.html">Terms</a> and <a href="privacy.html">Privacy Policy</a></span></label><a class="btn btn--primary btn--block m-go is-off" href="org-plans.html?plan=pro" data-pay aria-disabled="true">Pay &#8377;1,178.82<span class="dot dot--still">{ix("lock")}</span></a><p class="m-secure">Renews yearly. Cancel any time.</p></div></aside>
</div>'''

# ============================ student ============================
MYREGS = [  # event, fest, date, venue, status, img, fee, team
 ('Line Follower Sprint', 'Brain Wars', 'Dec 30, 2026', 'Main Grounds, MSRIT', 'conf', 'fests/event-robotics-demo', '&#8377;349 / member', 'Team SpiderTrack'),
 ('ByteForce CTF', 'Udbhav 2026', 'Dec 18, 2026', 'LHC Labs, MSRIT', 'pay', 'fests/event-hackathon', '&#8377;1.03 due', 'Team SpiderTrack, 1 of 3'),
 ('Slam Poetry', 'Brain Wars', 'Dec 31, 2026', 'Electronics Lab, MSRIT', 'conf', 'fests/blog-fest-season-crowd', 'Free', 'Solo'),
 ('General Quiz', 'Christ Lit Fest', 'Nov 13, 2026', 'Auditorium, Christ University', 'att', 'v4/quiz', '&#8377;99 / member', 'Team Know-It-Alls'),
 ('Hoops 3x3', 'Christ Athletics', 'Nov 20, 2026', 'Indoor Arena', 'cxl', 'v4/hoops', 'Refunded', 'Team Fast Break'),
]
RST = {'conf': ('Confirmed', 'ok', 'up'), 'pay': ('Payment due', 'live', 'up'), 'att': ('Attended', 'draft', 'att'), 'cxl': ('Cancelled', 'bad', 'cxl')}
def myreg(r):
    n, f, d, v, s, img, fee, team = r
    lab, kind, grp = RST[s]
    cta = {'conf': ('View Ticket', 'me-registration.html?state=done', 'ink'), 'pay': ('Complete Payment', 'me-registration.html', 'primary'), 'att': ('Leave a Review', 'event.html', 'light'), 'cxl': ('Find Similar', 'fests.html', 'light')}[s]
    return f'''<article class="mreg" data-status="{grp}"><a class="mreg-ph" href="me-registration.html"><img src="assets/img/{img}.jpg" alt="" width="800" height="1200"><span class="chip chip--light">{d}</span></a><div class="mreg-b"><span class="mreg-top">{chip(lab, kind)}<small>{f}</small></span><a href="me-registration.html"><b>{n}</b></a><span class="erow-m"><span>{ix("pin", "ic ic-xs")}{v}</span><span>{ix("users", "ic ic-xs")}{team}</span><span>{ix("rupee", "ic ic-xs")}{fee}</span></span></div><div class="mreg-cut" aria-hidden="true"></div><div class="mreg-r">{btn(cta[0], cta[1], cta[2], 'sm')}</div></article>'''
cnt = lambda g: sum(1 for r in MYREGS if RST[r[4]][2] == g)
regs_body = head([('My account', 'me.html'), ('Registrations', None)], 'MY REGISTRATIONS', 'Every event you&rsquo;ve signed up for, with tickets one tap away.', f'<a class="btn btn--primary" href="fests.html">Find Fests<span class="dot">{ic("arrow")}</span></a>') + f'''
<a class="nextup" href="me-registration.html?state=done"><span class="grain" aria-hidden="true"></span><img src="assets/img/fests/event-robotics-demo.jpg" alt="" width="1280" height="720"><div><p class="eyebrow eyebrow--ink"><span></span>Next up &middot; in 16 days</p><b>Line Follower Sprint</b><small>Dec 30, 9:00 AM &middot; Main Grounds, MSRIT</small></div><div class="nextup-qr">{qr_svg(3, 21)}</div></a>
<div class="dbar">{tabs([('all', 'All', len(MYREGS)), ('up', 'Upcoming', cnt('up')), ('att', 'Attended', cnt('att')), ('cxl', 'Cancelled', cnt('cxl'))], 'filter')}<label class="sel dsel dsel--sm"><select aria-label="Location"><option>All locations</option><option>Bengaluru</option></select>{ix("chev", "ic ic-s")}</label></div>
<div class="mregs">{''.join(myreg(r) for r in MYREGS)}</div><p class="lb-empty d-empty" hidden>Nothing here yet.</p>'''

# ---------- registration detail ----------
PROG = [('Team created', 'done'), ('Members joined', 'done'), ('Payment', 'now'), ('Confirmed', 'next')]
prog = ''.join(f'<li class="pg pg--{s}"><span>{ic("check", "ic ic-xs") if s == "done" else i + 1}</span><b>{t}</b></li>' for i, (t, s) in enumerate(PROG))
TEAM = [('Rohan Verma', 'Captain, you', 'pend', 0), ('Sai Vani', 'Member', 'pend', 1), ('Reshma Gouri', 'Invite sent', 'wait', 2)]
team = ''.join(f'<li class="tm-m"><img src="assets/img/av{a + 1}.jpg" alt="" width="40" height="40"><span><b>{n}</b><small>{r}</small></span>{chip({"pend": "Payment due", "wait": "Not joined"}[s], {"pend": "live", "wait": "draft"}[s])}</li>' for n, r, s, a in TEAM)
reg_body = head([('My registrations', 'me-registrations.html'), ('ByteForce CTF', None)], 'BYTEFORCE CTF', '', '', '<p class="dm-pre"><span class="chip chip--sun">Technical</span>Udbhav 2026 &middot; Dec 18, 2026 &middot; LHC Labs, MSRIT</p>') + f'''
<div class="dgrid dgrid--ticket">
  <div class="dcol">
    <section class="dcard"><div class="dcard-h"><h2 class="dcard-t">Registration progress</h2><span class="pill pill--live rp-pend">Step 3 of 4</span><span class="pill pill--ok rp-done">Complete</span></div><ol class="prog">{prog}</ol></section>
    <section class="dcard"><h2 class="dcard-t">Details</h2><div class="tiles tiles--2x">{''.join(f'<div class="tile"><span class="tile-ic">{ix(i, "ic ic-s")}</span><span><small>{l}</small><b>{v}</b></span></div>' for i, l, v in [('ticket', 'Ticket type', 'Team pass'), ('rupee', 'Your share', '&#8377;1.03'), ('cal', 'Registered on', 'Nov 24, 2026'), ('card', 'Payment', 'Pending')])}</div></section>
    <section class="dcard"><div class="dcard-h"><h2 class="dcard-t">Team SpiderTrack</h2><span class="pill pill--draft">2 of 3 joined</span></div><ul class="tm-list">{team}</ul><div class="copy"><span class="copy-ic">{ix('link', 'ic ic-s')}</span><span class="copy-url">festhey.in/t/spidertrack-4kq9</span><button class="btn btn--ink btn--sm" data-copy="https://festhey.in/t/spidertrack-4kq9">Copy Invite<span class="dot dot--still">{ix("copy")}</span></button></div></section>
  </div>
  <aside class="tk">
    <div class="tk-card">
      <div class="tk-top"><b>BYTEFORCE CTF</b><small>Udbhav 2026 &middot; Dec 18</small></div>
      <div class="tk-qr"><div class="tk-qr-in">{qr_svg(11, 25)}</div><span class="tk-lock">{ix('lock')}<b>Unlocks after payment</b></span></div>
      <div class="tk-cut" aria-hidden="true"></div>
      <div class="tk-id"><small>Registration ID</small><b>#C89BD861</b></div>
    </div>
    <p class="tk-note rp-pend">{ix('hourglass', 'ic ic-s')}<span>Pay your share by <b>Dec 15</b> to get your QR pass.</span></p>
    <a class="btn btn--primary btn--block rp-pend" href="me-registration.html?state=done">Pay &#8377;1.03 Now<span class="dot dot--still">{ix("lock")}</span></a>
    <a class="btn btn--ink btn--block rp-done" href="#">Download Ticket<span class="dot dot--still">{ix("download")}</span></a>
    <button class="tk-cancel" data-open="m-cxl">Cancel registration</button>
  </aside>
</div>
''' + modal('m-cxl', 'CANCEL REGISTRATION?', f'<p class="m-sub">You&rsquo;ll leave Team SpiderTrack. Anything you paid is refunded to your original payment method within 5 to 7 business days, following the <a class="dlink" href="refund.html">refund policy</a>.</p><a class="btn btn--ink btn--block m-go" href="me-registrations.html">Cancel My Registration<span class="dot dot--still">{ix("close")}</span></a>')

# ---------- saved ----------
saved_fests = ''.join(card(f, 2) for f in FESTS[:6])
saved_evs = '<div class="ev-row v-ticket saved-evs">' + ''.join(evc(t, i) for i, t in enumerate(EVENTS[:6])) + '</div>'
saved_cols = ''.join(cc(c, i) for i, c in enumerate(COLLEGES[:4]))
saved_body = head([('My account', 'me.html'), ('Saved', None)], 'SAVED STASH', 'Fests, events and colleges you&rsquo;re keeping an eye on. We&rsquo;ll ping you before deadlines.') + f'''
{tabs([('fests', 'Fests', 6), ('events', 'Events', 6), ('colleges', 'Colleges', 4)], 'saved')}
<section data-panel="fests"><div class="lb-cards">{saved_fests}</div></section>
<section data-panel="events" hidden>{saved_evs}</section>
<section data-panel="colleges" hidden><div class="cl-grid cl-grid--2">{saved_cols}</div></section>'''

# ---------- payments ----------
PAYS = [('Dec 2026', [('Line Follower Sprint', 'Brain Wars', 'Dec 2, 2026', 'UPI', '&#8377;359.47', 'paid', 'fests/event-robotics-demo')]),
        ('Nov 2026', [('General Quiz', 'Christ Lit Fest', 'Nov 8, 2026', 'Card &middot;&middot;&middot;&middot; 4421', '&#8377;101.97', 'paid', 'v4/quiz'), ('Hoops 3x3', 'Christ Athletics', 'Nov 4, 2026', 'UPI', '&#8377;299.00', 'refund', 'v4/hoops'), ('Slam Poetry', 'Brain Wars', 'Nov 1, 2026', 'Free', '&#8377;0.00', 'paid', 'fests/blog-fest-season-crowd')])]
pays = ''.join(f'<h3 class="pmonth">{m}</h3><div class="pays">' + ''.join(f'<div class="pay-r"><img src="assets/img/{img}.jpg" alt="" width="64" height="64"><span><b>{n}</b><small>{f} &middot; {d} &middot; {pm}</small></span>{st(s)}<b class="pay-amt">{a}</b><a class="btn btn--light btn--sm" href="#">Receipt<span class="dot dot--still">{ix("download")}</span></a></div>' for n, f, d, pm, a, s, img in rows) + '</div>' for m, rows in PAYS)
pay_body = head([('My account', 'me.html'), ('Payments', None)], 'PAYMENTS', 'Every transaction and receipt in one place. Handy for reimbursement claims.') + f'''
<div class="stats stats--3">{stat('rupee', 'Total spent', '&#8377;760.44', 'This year', 'stat--o')}{stat('receipt', 'Transactions', '4')}{stat('reset', 'Refunds', '&#8377;299.00', '1 refund processed', 'stat--s')}</div>
<section class="dcard">{pays}</section>'''

# ---------- profile ----------
INTERESTS = ['Cultural', 'Technical', 'Hackathon', 'Quiz', 'Sports', 'Music', 'Dance', 'Gaming']
ON = {'Technical', 'Hackathon', 'Quiz'}
NOTIF = [('Deadline reminders', 'A day before registrations close on saved fests', True), ('Team activity', 'When someone joins or pays in your team', True), ('New fests near me', 'Weekly picks from colleges in Bengaluru', False)]
profile_body = f'''<div class="pf-head">
  <label class="pf-av"><input type="file" accept="image/*" hidden><img src="assets/img/av1.jpg" alt="Rohan Verma" width="120" height="120" class="drop-img"><span class="pf-cam">{ix('camera', 'ic ic-s')}</span></label>
  <div><p class="dm-pre"><span class="chip chip--sun">Student</span>R V College of Engineering</p><h1 class="dm-h">ROHAN VERMA</h1><p class="dm-sub">{ix('mail', 'ic ic-xs')}rohan.v@festhey.in &middot; Member since Aug 2025</p></div>
  <div class="pf-meter"><svg viewBox="0 0 36 36" aria-hidden="true"><circle cx="18" cy="18" r="16"/><circle cx="18" cy="18" r="16" class="pf-arc" style="stroke-dasharray:80 100"/></svg><span><b>80%</b><small>Profile complete. Add your student ID to finish.</small></span></div>
</div>
<div class="stats stats--3">{stat('ticket', 'Registered', '5', '2 upcoming', 'stat--o', 'me-registrations.html')}{stat('calcheck', 'Attended', '1', '', '', 'me-registrations.html')}{stat('bookmark', 'Saved', '16', '', 'stat--s', 'me-saved.html')}</div>
<form class="pf-form" novalidate>
  <section class="dcard"><div class="dcard-h"><h2 class="dcard-t">Personal details</h2></div><div class="fgrid">{field('First name', inp('user', '', 'Rohan'))}{field('Last name', inp('user', '', 'Verma'))}{field('Email', inp('mail', '', 'rohan.v@festhey.in', 'email'))}{field('Phone', inp('phone', '', '+91 98450 12345', 'tel'))}</div></section>
  <section class="dcard"><h2 class="dcard-t">Academic details</h2><div class="fgrid">{field('College', select([c[0] for c in COLLEGES], 'R V College of Engineering'))}{field('Course and year', inp('cap', '', 'B.E. Computer Science, 3rd year'))}{field('Student ID card', upload('Upload your college ID', 'Needed for intra-college events. JPG or PDF.'), 'df--full')}</div></section>
  <section class="dcard"><h2 class="dcard-t">Your interests</h2><p class="dm-sub">We use these to recommend fests.</p><div class="chips amen">{''.join(f'<button type="button" class="chip{" is-on" if t in ON else ""}" aria-pressed="{"true" if t in ON else "false"}">{t}</button>' for t in INTERESTS)}</div></section>
  <section class="dcard"><h2 class="dcard-t">Notifications</h2><div class="nlist">{''.join(f'<label class="nrow"><span><b>{t}</b><small>{d}</small></span><span class="tog"><input type="checkbox"{" checked" if on else ""}><span class="tog-t"></span></span></label>' for t, d, on in NOTIF)}</div></section>
  <section class="dcard danger"><span><b>Delete account</b><small>Removes your profile and registration history for good.</small></span><button type="button" class="btn btn--light btn--sm" data-toast="We&rsquo;ve emailed you a link to confirm deletion">Delete<span class="dot dot--still">{ix("close")}</span></button></section>
  <div class="savebar" hidden><span>{ix('info', 'ic ic-s')}You have unsaved changes</span><button type="reset" class="btn btn--light btn--sm">Discard<span class="dot dot--still">{ix("reset")}</span></button><button type="submit" class="btn btn--primary btn--sm">Save Changes<span class="dot dot--still">{ic("check")}</span></button></div>
</form>'''

PAGES = [
 ('org.html', 'org', 'org', 'Organiser overview', org_body, ''),
 ('org-gate.html', 'org', 'gate', 'Gate controller', gate_body, ''),
 ('org-fests.html', 'org', 'fests', 'Fests and events', fests_body, ''),
 ('org-fest.html', 'org', 'fests', 'ByteForce CTF', fest_body, ''),
 ('org-event.html', 'org', 'fests', 'RVCE Tech Event', event_body, ''),
 ('org-create-fest.html', 'org', 'fests', 'Create fest', create_fest_body, ''),
 ('org-create-event.html', 'org', 'fests', 'Create event', wizard_body, ''),
 ('org-college.html', 'org', 'college', 'College profile', college_body, ''),
 ('org-ads.html', 'org', 'ads', 'Ads and sponsors', ads_body, ''),
 ('org-ad-new.html', 'org', 'ads', 'Create ad', ad_new_body, ''),
 ('org-plans.html', 'org', 'plans', 'Subscription', plans_body, ''),
 ('org-upgrade.html', 'org', 'plans', 'Upgrade to Standard', upgrade_body, ''),
 ('me.html', 'me', 'me', 'My profile', profile_body, ''),
 ('me-registrations.html', 'me', 'regs', 'My registrations', regs_body, ''),
 ('me-registration.html', 'me', 'regs', 'ByteForce CTF registration', reg_body, 'rp'),
 ('me-saved.html', 'me', 'saved', 'Saved', saved_body, ''),
 ('me-payments.html', 'me', 'pay', 'Payments', pay_body, ''),
]
for fn, role, act_, title, body, cls in PAGES:
    pg = shell(role, act_, title, body, cls)
    open(os.path.join(ROOT, fn), 'w').write(pg)
    print('wrote', fn, len(pg), 'dashes:', [c for c in ('—', '–') if c in pg])
