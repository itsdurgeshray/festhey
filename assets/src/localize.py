#!/usr/bin/env python3
"""Point links to the live site at the pages built here. Run after any build script.
Links with no local page (login, policies, organiser dashboard, help) stay on the live site."""
import glob, os, re
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
B = re.escape('https://festhey.agpro.co.in')
RULES = [
    (B + r'/fests/[^"#?]+', 'fest.html'),
    (B + r'/fests(?=["#?])', 'fests.html'),
    (B + r'/events(?:/[^"#?]+)?(?=["#?])', 'event.html'),
    (B + r'/blogs?(?:/[^"#?]+)?(?=["#?])', 'blog.html'),
    (B + r'/colleges(?=["#?])', 'colleges.html'),
    (B + r'/help(?=["#?])', 'help.html'),
    (B + r'/about(?=["#?])', 'about.html'),
    (B + r'/privacy-policy(?=["#?])', 'privacy.html'),
    (B + r'/refund-policy(?=["#?])', 'refund.html'),
    (B + r'/terms(?=["#?])', 'privacy.html'),
    (B + r'/account/my-registrations', 'me-registrations.html'),
    (B + r'/auth/login[^"]*', 'login.html'),
    (B + r'/auth/register/organizer', 'register.html?role=organiser'),
    (B + r'/auth/register[^"]*', 'register.html'),
    (B + r'/organizer/dashboard/fests/new', 'org-create-fest.html'),
    (B + r'/organizer/dashboard/fests', 'org-fests.html'),
    (B + r'/organizer/dashboard[^"]*', 'org.html'),
    (B + r'/how-it-works', 'about.html'),
    (B + r'/?(?=")', 'index.html'),
]
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f).read(); n0 = s
    for pat, to in RULES:
        s = re.sub(pat, to, s)
    if s != n0:
        open(f, 'w').write(s)
    print(os.path.basename(f), 'remaining live links:', len(re.findall(B, s)))
