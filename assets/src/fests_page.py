#!/usr/bin/env python3
"""FestHey Fest listing page (fests.html), built on the landing-page design system.
Run: python3 assets/src/fests_page.py"""
import os, runpy, html
import runpy as _rp
_LU = _rp.run_path('/Users/durgesh/Desktop/WFT/festhey/assets/src/icons.py')
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
B = runpy.run_path(os.path.join(ROOT, 'assets/src/build.py'))
ic, btn, HEAD, NAV, FESTS, ADS, BASE = B['ic'], B['btn'], B['HEAD'], B['NAV'], B['FESTS'], B['ADS'], B['BASE']
e = html.escape
AV = B['AV']
index = B['page']
PIT = index[index.index('  <!-- ============ JOIN THE PIT'):index.index('</main>')]
FOOT = index[index.index('<!-- ============ FOOTER'):index.index('</footer>') + 9]

ICX = {
 'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 'filter': '<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
 'pin': '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 'user': '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
 'bookmark': '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/>',
 'chev': '<path d="m6 9 6 6 6-6"/>',
 'reset': '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
}
def icx(n, c='ic'):
    return _LU['svg'](n, c)

CATS = [('cultural', 'Cultural'), ('technical', 'Technical'), ('sports', 'Sports'), ('quiz', 'Quiz'), ('hackathon', 'Hackathon'), ('other', 'Other')]
MONTH = {'Nov': 11, 'Dec': 12}
# registration closes the day before each fest starts (placeholder until the real deadlines come from the API)
def close_day(d):
    m, n = d.split()
    return f'{m} {int(n) - 1}'

def card(f, i):
    name, d1, d2, evs, att, img, slug, catg, tone = f
    ad = '<span class="chip chip--ink lc-ad">AD</span>' if i in (1, 6) else ''
    m = MONTH[d1.split()[0]]
    return f'''
        <article class="lc" data-cat="{catg}" data-month="{m}" data-name="{e(name.lower())}" data-city="bengaluru">
          <a class="lc-ph" href="{BASE}/fests/{slug}">
            <img src="assets/img/fests/{img}.jpg" alt="" width="1280" height="720" loading="lazy">
            {ad}<span class="chip chip--light lc-date">{d1} to {d2}</span>
            <span class="chip chip--sun lc-city">{icx('pin', 'ic ic-xs')}Bengaluru</span>
            <span class="lc-tip" role="tooltip"><span>{icx('clock', 'ic ic-xs')}Last day for registration</span><b>{close_day(d1)}, 2026</b></span>
          </a>
          <div class="lc-body">
            <a class="lc-name" href="{BASE}/fests/{slug}">{e(name)}</a>
            <p class="lc-meta">{evs} Events</p>
            <div class="lc-foot">
              <span class="lc-att">{icx('user', 'ic ic-s')}{att} Attending</span>
              <button class="lc-save" aria-label="Save {e(name)}" aria-pressed="false">{icx('bookmark', 'ic ic-s')}</button>
              <a class="lc-go" href="{BASE}/fests/{slug}" aria-label="Explore {e(name)}">{ic('arrow')}</a>
            </div>
          </div>
        </article>'''

def feat(a, i):
    return f'''
        <a class="lf" href="{BASE}{a['href']}">
          <img src="assets/img/fests/{a['img']}.jpg" alt="" width="1280" height="720">
          <span class="lf-shade"></span>
          <span class="chip chip--ink lf-ad">AD</span>
          <span class="lf-body"><span class="chip chip--sun">{e(a['tag'])}</span><b>{e(a['name'])}</b><small>{e(a['col'])}</small></span>
          <span class="btn btn--light btn--sm lf-btn">Explore Event<span class="dot">{ic('arrow')}</span></span>
        </a>'''

checks = ''.join(f'<label class="ck"><input type="checkbox" name="cat" value="{k}"><span class="ck-box">{ic("check")}</span>{l}</label>' for k, l in CATS)
radios = ''.join(f'<label class="rd"><input type="radio" name="when" value="{v}"{" checked" if v == "all" else ""}><span class="rd-dot"></span>{l}</label>'
                 for v, l in [('all', 'All Dates'), ('month', 'This Month'), ('three', 'Next 3 Months')])
chips = '<button class="chip is-on" data-cat="all" aria-pressed="true">All Categories</button>' + ''.join(f'<button class="chip" data-cat="{k}" aria-pressed="false">{l}</button>' for k, l in CATS)

page = HEAD.format(title='Explore Fests | FestHey') + '<link rel="stylesheet" href="assets/fests.css">\n' + NAV + f'''
<main class="lp">
  <!-- ============ HERO ============ -->
  <section class="lh">
    <span class="grain" aria-hidden="true"></span>
    <div class="wrap lh-in">
      <div class="lh-copy">
        <p class="eyebrow eyebrow--ink"><span></span>Discover</p>
        <h1 class="hero-h">EXPLORE <mark class="mark">FESTS</mark></h1>
        <p class="lead lh-p">Browse college fests from across India. Filter by category, city, or duration to find the ones that match your vibe.</p>
      </div>
      <div class="lh-art" aria-hidden="true">
        <img class="lh-img3" src="assets/img/v4/dance.jpg" alt="" width="800" height="1200">
        <img class="lh-img2" src="assets/img/fests/blog-fest-season-crowd.jpg" alt="" width="1280" height="720">
        <img class="lh-img" src="assets/img/v4/pronite.jpg" alt="" width="800" height="1200">
        <span class="host-stick lh-stick"><span class="avs">{AV}</span><b>2,000+ Students</b></span>
      </div>
    </div>
  </section>

  <!-- ============ FEATURED ============ -->
  <section class="wrap lfeat" aria-label="Featured fests">
    {feat(ADS[1], 0)}{feat(ADS[2], 1)}
  </section>

  <!-- ============ BROWSE ============ -->
  <section class="wrap lb" id="browse">
    <div class="lb-bar">
      <label class="lb-search">{icx('search')}<input type="search" placeholder="Search fests" aria-label="Search fests"></label>
      <div class="chips lb-chips" role="group" aria-label="Categories">{chips}</div>
    </div>
    <div class="lb-grid">
      <aside class="lb-side" aria-label="Sort and filter">
        <p class="lb-side-h"><span class="lb-ic">{icx('filter', 'ic ic-xs')}</span>Sort &amp; Filter</p>
        <p class="eyebrow">Location</p>
        <label class="sel"><select aria-label="Location"><option value="all">All Locations</option><option value="bengaluru">Bengaluru</option></select>{icx('chev', 'ic ic-s')}</label>
        <p class="eyebrow">Category</p>
        <div class="lb-checks">{checks}</div>
        <p class="eyebrow">Date Range</p>
        <div class="lb-radios">{radios}</div>
        <button class="btn btn--ink btn--sm btn--block lb-apply" type="button">Apply Filters<span class="dot">{ic('check')}</span></button>
        <button class="lb-reset" type="button">{icx('reset', 'ic ic-xs')}Reset All</button>
      </aside>
      <div class="lb-main">
        <div class="lb-cards">{''.join(card(f, i) for i, f in enumerate(FESTS))}</div>
        <p class="lb-empty" hidden>No fests match these filters yet. <button class="lb-reset">Reset all</button></p>
        <div class="lb-pager">
          <span class="lb-count">Showing <b class="lb-n">{len(FESTS)}</b> of {len(FESTS)} fests</span>
          <nav class="lb-pages" aria-label="Pages"><button class="icon-btn icon-btn--sm" aria-label="Previous page" disabled>{ic('left')}</button><button class="lb-pg is-on" aria-current="page">1</button><button class="icon-btn icon-btn--sm" aria-label="Next page" disabled>{ic('right')}</button></nav>
        </div>
      </div>
    </div>
  </section>

{PIT}</main>

{FOOT}

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="assets/site.js"></script>
<script src="assets/fests.js"></script>
</body>
</html>
'''
open(os.path.join(ROOT, 'fests.html'), 'w').write(page)
print('wrote fests.html', len(page), 'dashes:', [c for c in ('—', '–') if c in page])
