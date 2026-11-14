#!/usr/bin/env python3
"""FestHey design system page. Reuses the live components from build.py.
Run: python3 assets/src/ds_page.py  (writes design-system.html and system.html)"""
import os, runpy
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
B = runpy.run_path(os.path.join(ROOT, 'assets/src/build.py'))
ic, btn, fest, evc, fcard, qa, cat = B['ic'], B['btn'], B['fest'], B['evc'], B['fcard'], B['qa'], B['cat']
FESTS, EVENTS, ADS, FAQ, CATS, AV, HEAD, NAV = B['FESTS'], B['EVENTS'], B['ADS'], B['FAQ'], B['CATS'], B['AV'], B['HEAD'], B['NAV']

NAVS = [('principles', 'Principles'), ('colour', 'Colour'), ('type', 'Typography'), ('space', 'Spacing'),
        ('layout', 'Layout and grid'), ('radius', 'Radius and borders'), ('depth', 'Elevation'), ('texture', 'Texture'),
        ('icons', 'Icons'), ('motion', 'Motion'), ('buttons', 'Buttons'), ('chips', 'Chips and tags'),
        ('forms', 'Form fields'), ('cards', 'Cards'), ('lists', 'Lists and FAQ'), ('navigation', 'Navigation'),
        ('patterns', 'Section patterns'), ('voice', 'Copy rules'), ('tokens', 'Token reference')]

def sec(id_, num, title, intro, body):
    return f'''
    <section class="dsx-sec" id="{id_}">
      <p class="eyebrow"><span></span>{num}</p>
      <h2>{title}</h2>
      <p class="dsx-intro">{intro}</p>
      {body}
    </section>'''

def spec(label, value):
    return f'<span class="dsx-spec"><b>{label}</b>{value}</span>'

COLOURS = [
  ('Orange', '--orange', '#FF5A14', 'snow', 'Primary brand. Hero ground, primary buttons, live dots, accents.'),
  ('Orange 700', '--orange-700', '#E2470A', 'snow', 'Text on light grounds where orange must read (tags, hovers).'),
  ('Sun', '--sun', '#FFD400', 'ink', 'Accent. Marker highlight, stickers, the FAQ ground, date blocks.'),
  ('Snow', '--snow', '#F7F5F0', 'ink', 'Page ground. Light button fill.'),
  ('Paper', '--paper', '#FFFFFF', 'ink', 'Cards and raised surfaces.'),
  ('Ink', '--ink', '#140A04', 'snow', 'Text, dark buttons, outlines. Never pure black.'),
  ('Ink 75', '--ink-75', 'rgba(20,10,4,.75)', 'snow', 'Secondary paragraphs.'),
  ('Ink 60', '--ink-60', 'rgba(20,10,4,.6)', 'snow', 'Meta text: venues, colleges, captions.'),
  ('Line', '--line', 'rgba(20,10,4,.12)', 'ink', 'Hairlines and chip outlines.'),
  ('Line 2', '--line-2', 'rgba(20,10,4,.2)', 'ink', 'Dividers on yellow and dashed tear lines.'),
]
PAIRS = [('Ink on Snow', 'ink', 'snow', '17.9 : 1', 'AAA'), ('Ink on Sun', 'ink', 'sun', '14.6 : 1', 'AAA'),
         ('Ink on Orange', 'ink', 'orange', '6.3 : 1', 'AA'), ('Snow on Orange', 'snow', 'orange', '2.9 : 1', 'Large text only'),
         ('Snow on Ink', 'snow', 'ink', '17.9 : 1', 'AAA'), ('Orange 700 on Snow', 'orange-700', 'snow', '3.6 : 1', 'Large or bold 14+')]

TYPE = [
  ('H1', 'Hero title', 'Clash Display 700', '64 / 72', 'Phones 48 / 56', 't-h1', "India's <mark class='mark'>college fests</mark>"),
  ('H2', 'Section heading', 'Clash Display 600', '48 / 56', 'All widths', 't-h2', 'FESTS &amp; EVENTS'),
  ('H3', 'Eyebrow', 'Satoshi 700, caps, +8% tracking', '12 / 20', 'Above every H2', 't-eb', '<span class="eyebrow" style="margin:0"><span></span>Backstage Access</span>'),
  ('Title L', 'Card title', 'Clash Display 600', '24 / 32', 'Fest cards, featured fests', 't-h3', '8th Mile Encore'),
  ('Title M', 'Small title, lead', 'Clash Display 600 / Satoshi 500', '20 / 28', 'Event cards, intro paragraphs', 't-h4', 'Line Follower Sprint'),
  ('Body 16', 'Paragraph, buttons', 'Satoshi 400 to 700', '16 / 24', 'Long reading 16 / 32', 't-16', 'Open the fest, pick any event inside it, and hit Register.'),
  ('Body 14', 'Meta, nav, chips', 'Satoshi 500 to 700', '14 / 22', 'Relaxed 14 / 30', 't-14', 'Main Grounds, MSRIT'),
  ('Body 12', 'Labels, tags, captions', 'Satoshi 700', '12 / 20', 'Relaxed 12 / 28', 't-12', 'Bengaluru'),
]
SPACE = [2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 140]
RADII = [('r-sm', 12, 'Image insets, date blocks'), ('r-md', 16, 'Photos inside cards, fields'), ('r-lg', 24, 'Cards'), ('r-pill', 100, 'Buttons, chips, nav')]
MOTION = [('--ease', 'cubic-bezier(.2,.8,.2,1)', 'Reveals, slides, fades'), ('--spring', 'cubic-bezier(.3,1.5,.5,1)', 'Hovers, tilts, button dots'),
          ('Fast', '.3s', 'Colour and shadow changes'), ('Base', '.6s', 'Cards lifting, chips filtering'), ('Slow', '1.2s', 'Section reveals, photo zooms')]
ICONS = ['arrow', 'right', 'left', 'up', 'check', 'mail', 'lock', 'msg', 'menu', 'send', 'insta', 'linkedin', 'youtube']

body = []
body.append(sec('principles', '01 Foundations', 'Principles', 'Four rules every screen follows. If a choice breaks one, it is the wrong choice.', '''
      <div class="dsx-grid4">
        <div class="dsx-card"><b>Say it in a second</b><p>Lead with what FestHey is: college fests, all in one place. The headline and first image must explain the product without scrolling.</p></div>
        <div class="dsx-card"><b>Real things, real people</b><p>Use photographed cut-outs of real objects (lanyards, phones, hands, tape, paper) and real campus photos. Never draw what can be photographed.</p></div>
        <div class="dsx-card"><b>Loud colour, calm layout</b><p>Orange and sun carry the energy. Layouts stay simple: one message and one action per section, clean grids, generous space.</p></div>
        <div class="dsx-card"><b>Everything on the 2px grid</b><p>Every size, space, radius and border is a multiple of 2. Line height is the font size plus 8 or plus 16.</p></div>
      </div>'''))

body.append(sec('colour', '02 Foundations', 'Colour', 'Five core colours plus four ink tints. Orange leads, sun accents, snow and paper keep it light, ink does the reading.',
  '<div class="dsx-swatches">' + ''.join(f'<div class="dsx-sw"><span class="dsx-swc" style="background:var({v});color:var(--{t})">Aa</span><b>{n}</b><code>{v}</code><code>{h}</code><small>{u}</small></div>' for n, v, h, t, u in COLOURS) + '</div>'
  + '<h3 class="dsx-h">Proportion</h3><div class="dsx-prop"><span style="flex:44;background:var(--snow)">Snow 44%</span><span style="flex:22;background:var(--orange);color:var(--snow)">Orange 22%</span><span style="flex:12;background:var(--paper)">Paper 12%</span><span style="flex:12;background:var(--sun)">Sun 12%</span><span style="flex:10;background:var(--ink);color:var(--snow)">Ink 10%</span></div>'
  + '<h3 class="dsx-h">Contrast pairs</h3><div class="dsx-pairs">' + ''.join(f'<div class="dsx-pair" style="background:var(--{bg});color:var(--{fg})"><b>{n}</b><span>{r}</span><small>{g}</small></div>' for n, fg, bg, r, g in PAIRS) + '</div>'))

body.append(sec('type', '03 Foundations', 'Typography', 'Two families. Clash Display for headings and numbers, Satoshi for everything you read or tap. Line height is always the size plus 8 (plus 16 for long reading).',
  '<div class="dsx-fonts"><div class="dsx-font"><span class="dsx-aa" style="font-family:var(--fd);font-weight:700">Aa</span><b>Clash Display</b><small>500, 600, 700. Headings, card titles, prices, dates.</small></div><div class="dsx-font"><span class="dsx-aa" style="font-family:var(--fb);font-weight:500">Aa</span><b>Satoshi</b><small>400, 500, 700, 900. Body, buttons, chips, nav, labels.</small></div></div>'
  + '<div class="dsx-type">' + ''.join(f'<div class="dsx-trow"><div class="dsx-tmeta"><b>{t}</b><small>{r}</small>{spec("Font", f)}{spec("Size / line", sz)}{spec("Note", nt)}</div><div class="dsx-{c}">{sample}</div></div>' for t, r, f, sz, nt, c, sample in TYPE) + '</div>'
  + '<h3 class="dsx-h">Highlight</h3><div class="dsx-two"><div class="dsx-card"><div class="dsx-t-h2">India\'s <mark class="mark">college fests</mark></div><p class="dsx-ok">Do: a straight marker band behind 1 to 3 words, ink text on sun.</p></div><div class="dsx-card"><div class="dsx-t-h2"><span style="display:inline-block;background:var(--sun);transform:rotate(-3deg);padding:0 8px">college fests</span></div><p class="dsx-no">Don\'t: tilted blocks, or more than one highlight per heading.</p></div></div>'))

body.append(sec('space', '04 Foundations', 'Spacing', 'An even scale on the 2px grid. Pick from the scale; never invent a value in between.',
  '<div class="dsx-space">' + ''.join(f'<div class="dsx-srow"><code>{n}</code><span class="dsx-bar" style="width:{n * 4}px"></span><small>{u}</small></div>' for n, u in zip(SPACE, ['Hairline nudges', 'Icon to text', 'Tight gaps, chip rows', 'Card inner padding', 'Default gap', 'Heading to text', 'Between groups', 'Between sub-sections', 'Large blocks', 'Section padding on phones', 'Section padding on desktop'])) + '</div>'))

body.append(sec('layout', '05 Foundations', 'Layout and grid', 'A 12-column grid, 1440 wide, with a gutter that grows from 16 to 56. Sections stack with 96 to 140 of air.',
  '<div class="dsx-cols">' + '<span></span>' * 12 + '</div>'
  + '<div class="dsx-grid4">' + ''.join(f'<div class="dsx-card"><b>{a}</b><p>{b}</p></div>' for a, b in [('Desktop 1440', '12 columns, 56 gutter, 24 gap. Cards run 4 across.'), ('Laptop 1180', '12 columns, 48 gutter. Cards run 3 across.'), ('Tablet 768', '6 columns, 32 gutter. Cards 2 across, hero stacks.'), ('Phone 375', '4 columns, 16 gutter. Rows swipe sideways with snap.')]) + '</div>'))

body.append(sec('radius', '06 Foundations', 'Radius and borders', 'Four radii and one border weight. Borders are 2px and always wrap all four sides: never a one-sided accent line or divider. Separate items with space or a tint instead. Tickets tear along a row of dots.',
  '<div class="dsx-row">' + ''.join(f'<div class="dsx-box" style="border-radius:{v}px"><b>{n}</b><code>{v}</code><small>{u}</small></div>' for n, v, u in RADII)
  + '<div class="dsx-box" style="border-radius:16px;box-shadow:inset 0 0 0 2px var(--ink)"><b>Border</b><code>2 solid</code><small>Outlines, chips</small></div><div class="dsx-box" style="border-radius:16px"><b>Tear line</b><span class="dsx-dots"></span><code>4px dots</code><small>Tickets, stubs</small></div><div class="dsx-box" style="border-radius:16px;background:var(--snow)"><b>No dividers</b><code>space or tint</code><small>Never a single-side border</small></div></div>'))

body.append(sec('depth', '07 Foundations', 'Elevation', 'Two shadows, both warm. Objects that hang or are taped get a soft drop; nothing glows.',
  '<div class="dsx-row"><div class="dsx-box" style="box-shadow:var(--sh-1)"><b>sh-1</b><small>Cards, nav pills</small></div><div class="dsx-box" style="box-shadow:var(--sh-2)"><b>sh-2</b><small>Lifted, featured</small></div></div>'))

body.append(sec('texture', '08 Foundations', 'Texture', 'Grain is part of the brand. A light grain over the whole page, a heavier one on orange and yellow sections.',
  '<div class="dsx-row"><div class="dsx-tex" style="background:var(--snow)"><span class="grain" style="opacity:.12"></span><b>Page grain</b><small>12% over everything</small></div><div class="dsx-tex" style="background:var(--orange);color:var(--snow)"><span class="grain"></span><b>Section grain</b><small>42% on orange, sun, pit</small></div><div class="dsx-tex" style="background:url(assets/img/v2/paper-orange.jpg) center/cover"><b>Paper</b><small>Host card, posters</small></div><div class="dsx-tex" style="background:url(assets/img/v2/wall-day.jpg) center/cover"><b>Campus wall</b><small>Footer ground</small></div></div>'))

body.append(sec('icons', '09 Foundations', 'Icons', 'One line set, 2 stroke, round caps, drawn on a 24 grid and shown at 16, 18 or 20. Arrows sit in a round dot inside buttons.',
  '<div class="dsx-icons">' + ''.join(f'<div class="dsx-ic">{ic(n)}<small>{n}</small></div>' for n in ICONS) + '</div>'))

body.append(sec('motion', '10 Foundations', 'Motion', 'Physical, never decorative. Things hang, swing, tilt and settle on springs. Every animation has a static state for Figma and reduced motion.',
  '<div class="dsx-motion">' + ''.join(f'<div class="dsx-mrow"><code>{n}</code><span>{v}</span><small>{u}</small></div>' for n, v, u in MOTION) + '</div>'
  + '<div class="dsx-row"><div class="dsx-box dsx-demo dsx-demo-spring"><b>Hover me</b><small>spring lift</small></div><div class="dsx-box dsx-demo dsx-demo-tilt"><b>Hover me</b><small>hang tilt</small></div></div>'))

body.append(sec('buttons', '11 Components', 'Buttons', 'Every button is solid with an arrow dot. Two heights: 56 and 44. One primary action per view.',
  '<div class="dsx-stage"><div class="dsx-row">' + btn('Primary', '#', 'primary') + btn('Ink', '#', 'ink') + btn('Small', '#', 'ink', 'sm') + '</div></div>'
  + '<div class="dsx-stage dsx-stage--orange"><div class="dsx-row">' + btn('Light', '#', 'light') + btn('Ink on orange', '#', 'ink') + '</div></div>'
  + '<div class="dsx-row"><button class="icon-btn" aria-label="Previous">' + ic('left') + '</button><button class="icon-btn" aria-label="Next">' + ic('right') + '</button><a class="icon-btn icon-btn--ink" href="#" aria-label="Top">' + ic('up') + '</a></div>'
  + '<div class="dsx-specs">' + spec('Height', '56 / 44') + spec('Padding', '24 left, 8 right / 18 left, 6 right') + spec('Dot', '40 / 32') + spec('Type', '16 / 24 Satoshi 700, 14 / 22 on small') + spec('Hover', 'Fill shifts one step, dot turns 45 degrees') + '</div>'))

body.append(sec('chips', '12 Components', 'Chips and tags', 'Filters are 42 high with a 2 outline; tags on photos are 32 high and filled.',
  '<div class="dsx-row">' + ''.join(cat(c) for c in CATS[:4]) + '</div>'
  + '<div class="dsx-row"><span class="chip chip--light">Dec 5 to Dec 6</span><span class="chip chip--ink">AD</span><span class="dsx-photo"><span class="chip chip--glass">Bengaluru</span></span><span class="dsx-ticker-demo"><span class="live"></span>MSRIT Sports Meet</span></div>'))

body.append(sec('forms', '13 Components', 'Form fields', 'One field style: 56 high, 16 radius, 2 outline. Focus adds an ink outline and a sun offset shadow.',
  f'''<div class="dsx-two"><div class="dsx-card"><label class="fld">{ic("mail")}<input type="email" placeholder="Email address" aria-label="Email address"></label><small class="dsx-cap">Default</small></div>
      <div class="dsx-card"><label class="fld dsx-focus">{ic("mail")}<input type="email" value="student@college.edu" aria-label="Email address"></label><small class="dsx-cap">Focus</small></div></div>'''))

body.append(sec('cards', '14 Components', 'Cards', 'Five cards, one family: paper or brand-colour grounds, 24 radius, photo inset at 16, Clash titles, an action at the foot.',
  '<div class="dsx-cards">'
  + '<div class="dsx-cardcell"><div class="fests dsx-one">' + fest(FESTS[0]) + '</div><small class="dsx-cap">Fest pass</small></div>'
  + '<div class="dsx-cardcell"><div class="fests dsx-one">' + fest(FESTS[3]) + '</div><small class="dsx-cap">Fest pass, orange</small></div>'
  + '<div class="dsx-cardcell dsx-on-orange"><div class="dsx-fcard">' + fcard(0, ADS[0]).replace('fcard is-c', 'fcard is-c dsx-static') + '</div><small class="dsx-cap">Featured fest (hero)</small></div>'
  + '<div class="dsx-cardcell"><div class="ev-row v-ticket dsx-one">' + evc(EVENTS[0], 0) + '</div><small class="dsx-cap">Event ticket</small></div>'
  + '<div class="dsx-cardcell"><div class="ev-row v-calendar dsx-one">' + evc(EVENTS[3], 3) + '</div><small class="dsx-cap">Event calendar</small></div>'
  + '<div class="dsx-cardcell"><div class="ev-row v-poster dsx-one">' + evc(EVENTS[5], 5) + '</div><small class="dsx-cap">Event poster</small></div>'
  + '</div>'))

body.append(sec('lists', '15 Components', 'Lists and FAQ', 'FAQ rows are 2-ruled lines; the open row inverts to ink. On desktop answers arrive as chat bubbles.',
  '<div class="dsx-two"><div class="dsx-faq">' + ''.join(qa(i, q) for i, q in enumerate(FAQ[:3])) + '</div><div class="dsx-chat"><div class="bub bub-me">What is FestHey?</div><div class="bub bub-bot">' + FAQ[0][1] + '</div></div></div>'))

body.append(sec('navigation', '16 Components', 'Navigation', 'A ticker of featured fests, a logo tab hanging from it, pill links on the left and Get Started on the right. It hides on scroll down and returns on scroll up.',
  '<div class="dsx-navdemo">' + NAV.replace('class="nav"', 'class="nav dsx-nav"') + '</div>'
  + '<div class="dsx-specs">' + spec('Ticker', '32 high, 12 / 20 bold') + spec('Logo tab', '240 by 64, logo 40 high') + spec('Links', '14 / 22 bold, 10 by 18 padding') + spec('Phones', 'Menu left, tab centre, Get Started right') + '</div>'))

body.append(sec('patterns', '17 Patterns', 'Section patterns', 'Every section opens the same way: eyebrow, H2, then an optional lead. Grounds alternate so the page has rhythm.',
  '''<div class="dsx-two"><div class="dsx-card"><p class="eyebrow"><span></span>FAQs</p><h2>QUESTIONS? WE'VE GOT ANSWERS.</h2><p class="lead" style="margin-top:24px;color:var(--ink-75)">Find quick answers to the most common questions about FestHey.</p></div>
      <div class="dsx-card"><b>Section order and grounds</b><ol class="dsx-ol"><li><span style="background:var(--orange)"></span>Hero, orange + grain</li><li><span style="background:var(--sun)"></span>Category tape</li><li><span style="background:var(--snow)"></span>Fests and Events, snow</li><li><span style="background:var(--sun)"></span>FAQ, sun + grain</li><li><span style="background:var(--orange)"></span>Join the Pit, orange + grain</li><li><span style="background:#E9E2D6"></span>Footer, campus wall</li></ol></div></div>'''))

body.append(sec('voice', '18 Content', 'Copy rules', 'Short, energetic, student-first. These hold on every page.',
  '<div class="dsx-two"><div class="dsx-card"><p class="dsx-ok">Do</p><ul class="dsx-ul"><li>Use the client\'s words for fests, events and FAQs</li><li>Sentence case for body; caps only for H2 and eyebrows</li><li>Prices as ₹349.00 / Member, dates as Dec 5 to Dec 6</li><li>One highlighted phrase per heading at most</li></ul></div>'
  '<div class="dsx-card"><p class="dsx-no">Don\'t</p><ul class="dsx-ul"><li>Em or en dashes anywhere in visible copy</li><li>Italics</li><li>Decorative text scattered behind sections</li><li>Outline-only buttons</li></ul></div></div>'))

TOK = [('--orange', '#FF5A14'), ('--orange-700', '#E2470A'), ('--sun', '#FFD400'), ('--snow', '#F7F5F0'), ('--paper', '#FFFFFF'), ('--ink', '#140A04'),
       ('--h1 / --h1-lh', '64 / 72'), ('--h2 / --h2-lh', '48 / 56'), ('--eb / --eb-lh', '12 / 20'), ('--h3 / --h3-lh', '24 / 32'), ('--h4 / --h4-lh', '20 / 28'),
       ('--b16 / --b16-lh', '16 / 24'), ('--b14 / --b14-lh', '14 / 22'), ('--b12 / --b12-lh', '12 / 20'),
       ('--r-sm / md / lg / pill', '12 / 16 / 24 / 100'), ('--pad', 'clamp(16, 4vw, 56)'), ('--sec', 'clamp(96, 10vw, 140)'), ('--max', '1440'),
       ('--sh-1', '0 2 0, 0 20 38 -26 ink 45%'), ('--sh-2', '0 34 60 -30 ink 55%')]
body.append(sec('tokens', '19 Reference', 'Token reference', 'Every value lives as a CSS custom property in assets/site.css. Use the token, never the raw number.',
  '<div class="dsx-tokens">' + ''.join(f'<div><code>{a}</code><span>{b}</span></div>' for a, b in TOK) + '</div>'))

page = HEAD.format(title='FestHey Design System') + '<link rel="stylesheet" href="assets/ds.css">' + f'''
<header class="dsx-hero">
  <span class="grain" aria-hidden="true"></span>
  <div class="wrap dsx-hero-in">
    <img class="dsx-logo" src="assets/img/logo.svg" alt="FestHey" width="1024" height="309">
    <p class="eyebrow eyebrow--ink"><span></span>Version 5, November 2026</p>
    <h1 class="hero-h">Design <mark class="mark">system</mark></h1>
    <p class="lead">Foundations, components and patterns behind the FestHey landing page. Built on a 2px grid with a strict type scale.</p>
    <div class="dsx-hero-specs">{spec('Grid', '2px')}{spec('Type', '64 / 48 / 12 / 16 / 14 / 12')}{spec('Line height', 'size + 8 or + 16')}{spec('Fonts', 'Clash Display + Satoshi')}</div>
  </div>
</header>
<div class="wrap dsx-layout">
  <nav class="dsx-side" aria-label="Design system sections">{''.join(f'<a href="#{i}">{t}</a>' for i, t in NAVS)}<a class="dsx-back" href="index.html">Back to the page</a></nav>
  <main class="dsx-main">{''.join(body)}</main>
</div>
<script>
(function(){{var links=[].slice.call(document.querySelectorAll('.dsx-side a[href^="#"]'));
var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{links.forEach(function(l){{l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id)}})}}}})}},{{rootMargin:'-40% 0px -55% 0px'}});
document.querySelectorAll('.dsx-sec').forEach(function(s){{io.observe(s)}});
document.querySelectorAll('.qa-q').forEach(function(b){{b.addEventListener('click',function(){{var q=b.parentNode,on=q.classList.contains('is-on');document.querySelectorAll('.dsx-faq .qa').forEach(function(o){{o.classList.remove('is-on')}});if(!on)q.classList.add('is-on')}})}});
}})();
</script>
</body>
</html>
'''
for name in ('design-system.html', 'system.html'):
    open(os.path.join(ROOT, name), 'w').write(page)
print('wrote design-system.html', len(page), 'dashes:', [c for c in ('—', '–') if c in page])
