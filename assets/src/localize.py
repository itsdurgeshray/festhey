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
    (B + r'/colleges(?=["#?])', 'fests.html'),
    (B + r'/account/my-registrations', 'team.html?state=complete'),
    (B + r'/?(?=")', 'index.html'),
]
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f).read(); n0 = s
    for pat, to in RULES:
        s = re.sub(pat, to, s)
    if s != n0:
        open(f, 'w').write(s)
    print(os.path.basename(f), 'remaining live links:', len(re.findall(B, s)))
