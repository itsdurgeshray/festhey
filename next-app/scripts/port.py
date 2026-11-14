#!/usr/bin/env python3
"""Port the static FestHey pages into Next.js App Router routes.
Each ../*.html becomes app/<route>/page.jsx with real JSX (className, htmlFor, style objects,
defaultValue/defaultChecked), its own stylesheets, and its scripts loaded in order.
Run from next-app/: python3 scripts/port.py"""
import os, re, json, glob
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.dirname(HERE)
APP = os.path.join(HERE, 'app')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
ATTR = {'class': 'className', 'for': 'htmlFor', 'tabindex': 'tabIndex', 'readonly': 'readOnly', 'maxlength': 'maxLength',
        'minlength': 'minLength', 'autocomplete': 'autoComplete', 'inputmode': 'inputMode', 'novalidate': 'noValidate',
        'playsinline': 'playsInline', 'autoplay': 'autoPlay', 'crossorigin': 'crossOrigin', 'srcset': 'srcSet',
        'colspan': 'colSpan', 'rowspan': 'rowSpan', 'enctype': 'encType', 'viewbox': 'viewBox', 'preserveaspectratio': 'preserveAspectRatio',
        'stroke-width': 'strokeWidth', 'stroke-linecap': 'strokeLinecap', 'stroke-linejoin': 'strokeLinejoin', 'stroke-dasharray': 'strokeDasharray',
        'fill-rule': 'fillRule', 'clip-rule': 'clipRule', 'stop-color': 'stopColor', 'stop-opacity': 'stopOpacity', 'fill-opacity': 'fillOpacity',
        'stroke-opacity': 'strokeOpacity', 'xlink:href': 'xlinkHref', 'xmlns:xlink': 'xmlnsXlink', 'accept-charset': 'acceptCharset',
        'http-equiv': 'httpEquiv', 'datetime': 'dateTime', 'frameborder': 'frameBorder', 'allowfullscreen': 'allowFullScreen',
        'gradientunits': 'gradientUnits', 'gradienttransform': 'gradientTransform', 'patternunits': 'patternUnits', 'stddeviation': 'stdDeviation',
        'text-anchor': 'textAnchor', 'dominant-baseline': 'dominantBaseline', 'font-size': 'fontSize', 'font-family': 'fontFamily', 'font-weight': 'fontWeight',
        'letter-spacing': 'letterSpacing', 'clip-path': 'clipPath', 'mask-type': 'maskType', 'pathlength': 'pathLength', 'markerwidth': 'markerWidth',
        'markerheight': 'markerHeight', 'refx': 'refX', 'refy': 'refY', 'spellcheck': 'spellCheck', 'contenteditable': 'contentEditable'}
SVGTAG = {t.lower(): t for t in ['linearGradient', 'radialGradient', 'clipPath', 'textPath', 'feTurbulence', 'feColorMatrix', 'feGaussianBlur', 'feBlend', 'feComposite', 'feDisplacementMap', 'feOffset', 'feMerge', 'feMergeNode', 'feFlood', 'feDropShadow', 'foreignObject', 'animateTransform', 'animateMotion']}
BOOL = {'hidden', 'disabled', 'required', 'multiple', 'muted', 'novalidate', 'playsinline', 'autoplay', 'readonly', 'open', 'loop', 'controls', 'allowfullscreen'}

def route_of(fn):
    b = os.path.splitext(os.path.basename(fn))[0]
    return '' if b == 'index' else b

def fix_url(v):
    """page.html -> /page ; assets/... -> /assets/... ; keeps query and hash."""
    if re.match(r'^(https?:|mailto:|tel:|#|/|data:)', v):
        return v
    m = re.match(r'^([A-Za-z0-9_-]+)\.html(.*)$', v)
    if m:
        r = '' if m.group(1) == 'index' else m.group(1)
        return '/' + r + m.group(2)
    if v.startswith('assets/'):
        return '/' + v
    if v.startswith('?'):
        return v
    return v

def style_obj(s):
    out = {}
    for decl in s.split(';'):
        if ':' not in decl:
            continue
        k, v = decl.split(':', 1)
        k = k.strip(); v = v.strip()
        if not k:
            continue
        if not k.startswith('--'):
            k = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), k)
        v = re.sub(r'url\((["\']?)assets/', r'url(\1/assets/', v)
        out[k] = v
    return out

class Node:
    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.kids = tag, attrs, []

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root', []); self.stack = [self.root]
    # HTML implied end tags: a new <option>, <li>, <tr>... closes the previous open one,
    # and block elements close an open <p>. Mirrors what the browser parser does.
    IMPLIED = {'option': {'option'}, 'optgroup': {'option', 'optgroup'}, 'li': {'li'}, 'dt': {'dt', 'dd'}, 'dd': {'dt', 'dd'},
               'tr': {'tr', 'td', 'th'}, 'td': {'td', 'th'}, 'th': {'td', 'th'}}
    P_CLOSE = {'address', 'article', 'aside', 'blockquote', 'details', 'div', 'dl', 'fieldset', 'figcaption', 'figure', 'footer',
               'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'main', 'menu', 'nav', 'ol', 'p', 'pre', 'section', 'table', 'ul'}
    def _implied(self, tag):
        closes = self.IMPLIED.get(tag, set())
        if closes and self.stack[-1].tag in closes:
            self.stack.pop()
        if tag in self.P_CLOSE and self.stack[-1].tag == 'p':
            self.stack.pop()
    def handle_starttag(self, tag, attrs):
        self._implied(tag)
        n = Node(tag, attrs); self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.stack[-1].kids.append(Node(tag, attrs))
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return
    def handle_data(self, d):
        self.stack[-1].kids.append(d)

NO_WS = {'table', 'thead', 'tbody', 'tfoot', 'tr', 'colgroup', 'select', 'optgroup'}
def jtext(t, parent=''):
    """Keep text nodes exactly as in the HTML so inline spacing renders identically.
    React forbids whitespace-only text inside table rows and selects, so drop it there."""
    if not t.strip() and parent in NO_WS:
        return ''
    return '{' + json.dumps(t, ensure_ascii=False) + '}'

def jattrs(n, extra=None):
    out = []
    attrs = list(n.attrs)
    tag = n.tag
    for k, v in attrs:
        if tag == 'option' and k == 'selected':
            continue
        name = ATTR.get(k, k)
        if k == 'style':
            out.append(f'style={{{json.dumps(style_obj(v or ""))}}}')
            continue
        if tag in ('input',) and k == 'value' and not any(a == 'type' and b in ('hidden', 'radio', 'checkbox', 'submit', 'button') for a, b in attrs):
            name = 'defaultValue'
        if tag in ('input',) and k == 'checked':
            name = 'defaultChecked'
        if k in ('href', 'src', 'action', 'poster') and v:
            v = fix_url(v)
        if v is None or (k in BOOL and v in ('', k)):
            out.append(name if v is None or v == '' else f'{name}')
            continue
        if k.startswith('on'):
            continue
        out.append(f'{name}={json.dumps(v, ensure_ascii=False)}')
    if extra:
        out.extend(extra)
    return (' ' + ' '.join(out)) if out else ''

def jsx(n, depth=0, parent=''):
    if isinstance(n, str):
        return jtext(n, parent)
    if n.tag in ('script',):
        return ''
    extra = []
    kids = n.kids
    if n.tag == 'select':
        sel = None
        for o in kids:
            if isinstance(o, Node) and o.tag == 'option' and any(k == 'selected' for k, _ in o.attrs):
                val = dict(o.attrs).get('value')
                sel = val if val is not None else ''.join(x for x in o.kids if isinstance(x, str)).strip()
        if sel is not None:
            extra.append(f'defaultValue={json.dumps(sel, ensure_ascii=False)}')
    if n.tag == 'textarea':
        txt = ''.join(x for x in kids if isinstance(x, str))
        if txt:
            extra.append(f'defaultValue={json.dumps(txt, ensure_ascii=False)}')
        kids = []
    a = jattrs(n, extra)
    tag = SVGTAG.get(n.tag, n.tag)
    if n.tag in VOID or not kids:
        return f'<{tag}{a} />'
    inner = ''.join(jsx(k, depth + 1, n.tag) for k in kids)
    return f'<{tag}{a}>{inner}</{tag}>'

def port(fn):
    src = open(fn, encoding='utf-8').read()
    title = re.search(r'<title>(.*?)</title>', src, re.S).group(1)
    title = HTMLParser().unescape(title) if hasattr(HTMLParser, 'unescape') else __import__('html').unescape(title)
    head = src[:src.index('<body')]
    # every stylesheet the HTML page loads, in the same order (old versions load v1.css etc. instead of site.css)
    css = [__import__('html').unescape(m.group(1) or m.group(2)) for m in re.finditer(r'<link rel="stylesheet" href="([^"]+)"|<link href="([^"]+)" rel="stylesheet"', head)]
    # stylesheets linked inside body (pages that add css after HEAD)
    body = src[src.index('<body'):]
    body_css = re.findall(r'<link rel="stylesheet" href="([^"]+)">', body)
    css += [c for c in body_css if c not in css]
    # body scripts in document order: external files by src, inline blocks by their code
    scripts = []
    for m in re.finditer(r'<script(?: src="([^"]+)")?[^>]*>(.*?)</script>', body, re.S):
        if m.group(1):
            scripts.append(m.group(1))
        elif m.group(2).strip():
            scripts.append({'code': m.group(2)})
    body_html = body[body.index('>') + 1: body.rindex('</body>')]
    body_html = re.sub(r'<link rel="stylesheet" href="[^"]+">', '', body_html)
    body_html = re.sub(r'<script[^>]*>.*?</script>', '', body_html, flags=re.S)
    p = P(); p.feed(body_html)
    tree = ''.join(jsx(k, 0, 'body') for k in p.root.kids)
    # the first stylesheet is the page's design system (site.css, or v1.css for old versions); it always loads first
    # fonts first, then the page's design system (site.css, or v1.css for old versions), then page styles
    fonts = [c for c in css if c.startswith('http')]
    local = [c for c in css if not c.startswith('http')]
    links = ''.join(f'<link rel="stylesheet" href={json.dumps(c)} precedence="fonts" />' for c in fonts)
    links += ''.join(f'<link rel="stylesheet" href="{fix_url(c)}" precedence="{"base" if i == 0 else "page"}" />' for i, c in enumerate(local))
    route = route_of(fn)
    d = os.path.join(APP, route) if route else APP
    os.makedirs(d, exist_ok=True)
    scripts = [fix_url(x) if isinstance(x, str) else x for x in scripts]
    code = f'''// Generated by scripts/port.py from {os.path.basename(fn)}. Edit the source page, then re-run the port.
import {{ preload }} from 'react-dom';
import ScriptChain from '{'../' if route else './'}components/ScriptChain';

export const metadata = {{ title: {json.dumps(title, ensure_ascii=False)} }};

const SCRIPTS = {json.dumps(scripts)};

export default function Page() {{
  // start downloading the page scripts with the HTML, exactly like the static page's script tags
  SCRIPTS.forEach(src => typeof src === 'string' && preload(src, {{ as: 'script' }}));
  return (
    <>
      {links}
      {tree}
      <ScriptChain srcs={{SCRIPTS}} />
    </>
  );
}}
'''
    open(os.path.join(d, 'page.jsx'), 'w', encoding='utf-8').write(code)
    return route or '/', len(code)

if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(SRC, '*.html')))
    for f in files:
        r, n = port(f)
        print(f'{r:28s} {n:>8d} bytes')
    print(len(files), 'routes')
