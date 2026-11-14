#!/usr/bin/env python3
"""FestHey auth: login, register (student / organiser), verify (OTP), org-verify, forgot, reset.
Run: python3 assets/src/auth_pages.py"""
import os, runpy
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
D = runpy.run_path(os.path.join(ROOT, 'assets/src/dash_pages.py'))
ix, ic, HEAD, AV = D['ix'], D['ic'], D['HEAD'], D['B']['AV']
COLLEGES = D['COLLEGES']
CSS = ''.join(f'<link rel="stylesheet" href="assets/{x}.css">' for x in ('fests', 'app', 'dash', 'auth')) + '\n'
JS = '<script src="assets/auth.js"></script>\n</body>\n</html>\n'
STATES = ['Karnataka', 'Maharashtra', 'Delhi', 'Tamil Nadu', 'Telangana', 'West Bengal']

def art(l1, l2, lead):
    return f'''<aside class="au-art"><span class="grain" aria-hidden="true"></span>
    <a class="au-logo" href="index.html"><img src="assets/img/logo.svg" alt="FestHey" width="132" height="40"></a>
    <div class="au-tix" aria-hidden="true"><span class="au-tk au-tk--1"><b>Utsav Winter</b><small>Dec 12 &middot; BMSCE</small></span><span class="au-tk au-tk--2"><b>8th Mile</b><small>Dec 5 &middot; RVCE</small></span><span class="au-tk au-tk--3"><b>Brain Wars</b><small>Dec 30 &middot; MSRIT</small></span></div>
    <div class="au-copy"><p class="eyebrow eyebrow--ink"><span></span>FestHey</p><h1 class="au-h">{l1}<br><mark class="mark">{l2}</mark></h1><p class="au-lead">{lead}</p>
    <div class="joined"><span class="avs">{AV}</span><span class="joined-t"><span>Joined by</span><b>2,000+ students</b></span></div></div>
  </aside>'''

def page(title, artp, form, wide=False):
    return HEAD.format(title=f'{title} | FestHey') + CSS + f'''<div class="au{" au--wide" if wide else ""}">
  {artp}
  <main class="au-main">
    <a class="au-x icon-btn icon-btn--sm" href="index.html" aria-label="Close and go home">{ix('close')}</a>
    <div class="au-form">{form}</div>
  </main>
</div>
<div class="fd-toast" role="status" aria-live="polite"></div>
''' + JS

def fl(label, icon, ph, typ='text', name='', extra='', hint=''):
    ico = ix(icon) if icon else ''
    return f'<div class="df"><label class="m-label" for="{name}">{label}</label><label class="fld">{ico}<input id="{name}" name="{name}" type="{typ}" placeholder="{ph}" {extra}></label>{hint}</div>'
def pw(label, name, ph='At least 8 characters', meter=False):
    m = '<div class="pw-meter" aria-live="polite"><span class="pw-bars"><i></i><i></i><i></i><i></i></span><small>Use 8+ characters with a number and a symbol</small></div>' if meter else ''
    return f'<div class="df"><label class="m-label" for="{name}">{label}</label><label class="fld">{ix("lock")}<input id="{name}" name="{name}" type="password" placeholder="{ph}" autocomplete="new-password" required><button type="button" class="pw-eye" aria-label="Show password" aria-pressed="false">{ix("eye", "ic ic-s")}{ix("eyeoff", "ic ic-s")}</button></label>{m}</div>'
def sel(label, name, opts, ph):
    return f'<div class="df"><label class="m-label" for="{name}">{label}</label><label class="sel dsel"><select id="{name}" name="{name}"><option value="">{ph}</option>' + ''.join(f'<option>{o}</option>' for o in opts) + f'</select>{ix("chev", "ic ic-s")}</label></div>'
def otp():
    return '<div class="otp" role="group" aria-label="6-digit code">' + ''.join(f'<input inputmode="numeric" maxlength="1" aria-label="Digit {i + 1}" autocomplete="one-time-code">' for i in range(6)) + '</div><p class="au-resend">Didn&rsquo;t get it? <button type="button" class="dlink" data-resend disabled>Resend in <span>30</span>s</button></p>'
def head(eb, h, sub=''):
    return f'<p class="eyebrow"><span></span>{eb}</p><h2 class="au-t">{h}</h2>' + (f'<p class="au-sub">{sub}</p>' if sub else '')
GOOGLE = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" stroke="none" d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3Z"/><path fill="#34A853" stroke="none" d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22Z"/><path fill="#FBBC05" stroke="none" d="M6.4 14c-.2-.6-.3-1.3-.3-2s.1-1.4.3-2V7.4H3.1a10 10 0 0 0 0 9.2L6.4 14Z"/><path fill="#EA4335" stroke="none" d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.4L6.4 10C7.2 7.7 9.4 6 12 6Z"/></svg>'

login = page('Log in', art('WELCOME', 'BACK.', 'The hottest fests. The earliest tickets. Your whole squad, one link away.'), f'''
  {head('Welcome back', 'LOG IN TO FESTHEY', 'Students and organisers use the same login.')}
  <form class="au-f" action="me.html" data-auth="login" novalidate>
    {fl('Email', 'mail', 'you@college.edu', 'email', 'email', 'autocomplete="email" required')}
    {pw('Password', 'password', 'Your password')}
    <div class="au-row"><label class="ck"><input type="checkbox" checked><span class="ck-box">{ic('check')}</span><span class="ck-t">Remember me</span></label><a class="dlink" href="forgot.html">Forgot password?</a></div>
    <button class="btn btn--primary btn--block">Log In<span class="dot">{ic('arrow')}</span></button>
    <p class="au-or"><span>or</span></p>
    <a class="btn btn--light btn--block au-g" href="me.html">Continue with Google<span class="dot dot--still">{GOOGLE}</span></a>
  </form>
  <p class="au-alt">New to FestHey? <a class="dlink" href="register.html">Create an account</a></p>''')

reg_form = f'''
  {head('Welcome aboard', 'CREATE YOUR ACCOUNT')}
  <div class="seg au-role" role="radiogroup" aria-label="Account type"><button type="button" class="is-on" data-role="student" role="radio" aria-checked="true">{ix('cap', 'ic ic-s')}I&rsquo;m a student</button><button type="button" data-role="organiser" role="radio" aria-checked="false">{ix('school', 'ic ic-s')}I run fests</button></div>
  <p class="au-sub au-rsub" data-for="student">Register for fests, build teams and keep every ticket in one place.</p>
  <p class="au-sub au-rsub" data-for="organiser" hidden>List your college, publish fests and run the gate. We verify every organiser.</p>
  <form class="au-f" action="verify.html" data-auth="register" novalidate>
    <div class="fgrid">
      {fl('Full name', 'user', 'Your full name', 'text', 'name', 'autocomplete="name" required')}
      {fl('Email', 'mail', 'you@college.edu', 'email', 'remail', 'autocomplete="email" required', '<p class="m-hint" data-for="organiser" hidden>' + ix('info', 'ic ic-xs') + '<span>Use your official college email to verify instantly.</span></p>')}
      {sel('State', 'state', STATES, 'Select state')}
      {fl('City', 'pin', 'e.g. Bengaluru', 'text', 'city')}
      <div class="df df--full"><label class="m-label" for="college">College</label><label class="fld">{ix('search')}<input id="college" list="colleges" placeholder="Search your college" required></label><datalist id="colleges">{''.join(f'<option value="{c[0]}"></option>' for c in COLLEGES)}</datalist></div>
      <div data-for="student" class="df">{sel('Graduation year', 'grad', ['2026', '2027', '2028', '2029', '2030'], 'Select year')}</div>
      <div data-for="organiser" class="df" hidden>{fl('College website', 'link', 'e.g. msrit.edu', 'url', 'site')}</div>
      <div class="df"><label class="m-label" for="phone">Phone</label><label class="fld fld--tel"><span class="tel-cc">+91</span><input id="phone" type="tel" inputmode="numeric" maxlength="10" placeholder="98765 43210" autocomplete="tel-national"></label></div>
      <div data-for="organiser" class="df df--full" hidden>{sel('Your role at the college', 'role', ['Faculty coordinator', 'Student council', 'Fest committee head', 'Club lead'], 'Select role')}</div>
      {pw('Password', 'pw1', 'At least 8 characters', True)}
      {pw('Confirm password', 'pw2', 'Type it again')}
    </div>
    <p class="note note--s" data-for="organiser" hidden>{ix('shield', 'ic ic-s')}<span>After signing up you&rsquo;ll prove you belong to your college. An admin unlocks your dashboard, usually within a day.</span></p>
    <label class="ck"><input type="checkbox" required data-terms><span class="ck-box">{ic('check')}</span><span class="ck-t">I agree to the <a href="privacy.html">Terms</a> and <a href="privacy.html">Privacy Policy</a></span></label>
    <button class="btn btn--primary btn--block">Create Account<span class="dot">{ic('arrow')}</span></button>
  </form>
  <p class="au-alt">Already registered? <a class="dlink" href="login.html">Log in</a></p>'''
register = page('Create account', art('JOIN THE', 'PIT.', 'Thousands of students across India find, register and squad up for fests here.'), reg_form, True)

verify = page('Confirm your email', art('ALMOST', 'IN.', 'One quick check so your tickets and team invites reach the right inbox.'), f'''
  <span class="au-badge">{ix('mailok')}</span>
  {head('Step 2 of 2', 'CONFIRM YOUR EMAIL', 'Enter the 6-digit code we sent to <b data-mask>ro&middot;&middot;&middot;&middot;@festhey.in</b>.')}
  <form class="au-f" action="me.html" data-auth="otp" novalidate>
    {otp()}
    <button class="btn btn--primary btn--block is-off" data-otp-go>Verify Email<span class="dot">{ic('arrow')}</span></button>
  </form>
  <p class="au-alt">Wrong email? <a class="dlink" href="register.html">Go back</a></p>''')

org_verify = page('Verify your college', art('HOST YOUR', 'FEST.', 'Verified organisers publish fests, run the gate scanner and get paid on time.'), f'''
  <div class="ov-form">
  {head('Organiser verification', 'PROVE YOU BELONG TO MSRIT', 'Either option below is enough on its own. Pick the easiest.')}
  <div class="ov-pick" role="radiogroup" aria-label="Verification method">
    <label class="rcard2"><input type="radio" name="ov" value="email" checked><span><b>College email</b><small>Fastest. Unlocks instantly.</small></span><span class="tile-ic">{ix('mail', 'ic ic-s')}</span></label>
    <label class="rcard2"><input type="radio" name="ov" value="doc"><span><b>Upload a document</b><small>ID card or authorisation letter. Reviewed within a day.</small></span><span class="tile-ic">{ix('upload', 'ic ic-s')}</span></label>
  </div>
  <form class="au-f" action="org-verify.html" data-auth="orgv" novalidate>
    <input type="hidden" name="state" value="sent">
    <div data-ov="email">
      <div class="df"><label class="m-label" for="cemail">Official college email</label><div class="code-row"><label class="fld">{ix('mail')}<input id="cemail" type="email" placeholder="you@msrit.edu"></label><button type="button" class="btn btn--ink" data-send>Send Code<span class="dot dot--still">{ix('send')}</span></button></div></div>
      <div class="df ov-code" hidden><label class="m-label">Code from your inbox</label>{otp()}</div>
    </div>
    <div data-ov="doc" hidden>
      <div class="df"><label class="m-label">Document type</label><label class="sel dsel"><select><option>College ID card</option><option>Authorisation letter on letterhead</option><option>Faculty ID</option></select>{ix('chev', 'ic ic-s')}</label></div>
      <div class="df"><label class="m-label">Upload</label><label class="drop"><input type="file" accept="image/*,application/pdf" hidden><span class="drop-ic">{ix('upload')}</span><b>Click or drop your document</b><small>JPG, PNG or PDF, up to 10 MB</small><img class="drop-img" alt="" hidden></label></div>
    </div>
    <button class="btn btn--primary btn--block">Submit for Verification<span class="dot">{ic('arrow')}</span></button>
  </form>
  </div>
  <div class="ov-done" hidden>
    <span class="au-badge au-badge--sun">{ix('hourglass')}</span>
    {head('Submitted', 'YOU&rsquo;RE IN THE QUEUE', 'We&rsquo;ll email you the moment an admin approves MSRIT. Most requests clear within a day.')}
    <ol class="ov-tl"><li class="is-done"><span>{ic('check', 'ic ic-xs')}</span><b>Account created</b></li><li class="is-done"><span>{ic('check', 'ic ic-xs')}</span><b>Proof submitted</b></li><li class="is-now"><span>3</span><b>Admin review</b></li><li><span>4</span><b>Dashboard unlocked</b></li></ol>
    <a class="btn btn--ink btn--block" href="org.html">Preview the Dashboard<span class="dot">{ic('arrow')}</span></a>
    <p class="au-alt">Questions? <a class="dlink" href="help.html">Visit the help center</a></p>
  </div>''')

forgot = page('Forgot password', art('HAPPENS TO', 'THE BEST.', 'We&rsquo;ll get you back to your tickets in under a minute.'), f'''
  <a class="au-back" href="login.html">{ic('left', 'ic ic-s')}Back to log in</a>
  <span class="au-badge">{ix('key')}</span>
  {head('Reset', 'FORGOT YOUR PASSWORD?', 'Enter your email and we&rsquo;ll send a 6-digit reset code.')}
  <form class="au-f" action="reset.html" data-auth="forgot" novalidate>
    {fl('Email', 'mail', 'you@college.edu', 'email', 'femail', 'autocomplete="email" required')}
    <button class="btn btn--primary btn--block">Send Reset Code<span class="dot dot--still">{ix('send')}</span></button>
  </form>''')

reset = page('Reset password', art('FRESH', 'START.', 'Pick something you&rsquo;ll remember. Your tickets are waiting.'), f'''
  <a class="au-back" href="forgot.html">{ic('left', 'ic ic-s')}Back</a>
  <span class="au-badge">{ix('lock')}</span>
  {head('Reset', 'SET A NEW PASSWORD', 'Enter the code we emailed you, then choose a new password.')}
  <form class="au-f" action="login.html" data-auth="reset" novalidate>
    <input type="hidden" name="reset" value="1">
    <div class="df"><label class="m-label">6-digit code</label>{otp()}</div>
    {pw('New password', 'np1', 'At least 8 characters', True)}
    {pw('Confirm password', 'np2', 'Type it again')}
    <p class="m-hint pw-match" hidden>{ix('info', 'ic ic-xs')}<span>Passwords don&rsquo;t match yet</span></p>
    <button class="btn btn--primary btn--block is-off" data-reset-go>Reset Password<span class="dot">{ic('arrow')}</span></button>
  </form>''')

for fn, pg in (('login.html', login), ('register.html', register), ('verify.html', verify), ('org-verify.html', org_verify), ('forgot.html', forgot), ('reset.html', reset)):
    open(os.path.join(ROOT, fn), 'w').write(pg)
    print('wrote', fn, len(pg), 'dashes:', [c for c in ('—', '–') if c in pg])
