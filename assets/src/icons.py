"""Lucide icon library (lucide-static, pinned). SVGs are vendored in assets/icons/ and inlined at build time,
so pages stay static and Figma-import safe. Missing icons are fetched once from the pinned package."""
import os, re, urllib.request
ROOT = '/Users/durgesh/Desktop/WFT/festhey'
VER = '0.469.0'
DIR = os.path.join(ROOT, 'assets/icons')
# FestHey short names -> Lucide names
MAP = {
 'arrow': 'arrow-up-right', 'up': 'arrow-up', 'left': 'arrow-left', 'right': 'arrow-right', 'lock': 'lock', 'check': 'check',
 'mail': 'mail', 'msg': 'message-circle', 'menu': 'menu', 'insta': 'instagram', 'linkedin': 'linkedin', 'youtube': 'youtube',
 'send': 'send', 'search': 'search', 'filter': 'sliders-horizontal', 'pin': 'map-pin', 'user': 'user', 'bookmark': 'bookmark',
 'chev': 'chevron-down', 'reset': 'rotate-ccw', 'clock': 'clock', 'share': 'share-2', 'cal': 'calendar', 'ticket': 'ticket',
 'nav': 'navigation', 'close': 'x', 'users': 'users', 'userplus': 'user-plus', 'trophy': 'trophy', 'star': 'star', 'wifi': 'wifi',
 'coffee': 'coffee', 'drop': 'droplet', 'snow': 'snowflake', 'zap': 'zap', 'copy': 'copy', 'download': 'download', 'info': 'info',
 'wa': 'message-circle', 'shield': 'shield-check', 'book': 'book-open', 'medal': 'medal', 'crown': 'crown', 'party': 'party-popper',
 'sparkles': 'sparkles', 'quote': 'quote', 'cap': 'graduation-cap', 'qr': 'qr-code', 'card': 'credit-card', 'link': 'link',
 'okc': 'circle-check', 'gift': 'gift', 'plug': 'plug-zap', 'flag': 'flag', 'mic': 'mic', 'music': 'music', 'gauge': 'gauge',
 'receipt': 'receipt', 'hourglass': 'hourglass', 'hand': 'hand-heart', 'eye': 'eye', 'heart': 'heart', 'school': 'school',
 'plus': 'plus', 'minus': 'minus', 'camera': 'camera', 'calcheck': 'calendar-check', 'rupee': 'indian-rupee', 'bolt': 'bolt',
}
_cache = {}
def inner(n):
    name = MAP.get(n, n)
    if name in _cache:
        return _cache[name]
    p = os.path.join(DIR, name + '.svg')
    if not os.path.exists(p):
        os.makedirs(DIR, exist_ok=True)
        url = f'https://unpkg.com/lucide-static@{VER}/icons/{name}.svg'
        data = urllib.request.urlopen(url, timeout=20).read().decode()
        open(p, 'w').write(data)
    s = open(p).read()
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    body = re.sub(r'\s+', ' ', body).strip()
    _cache[name] = body
    return body
def svg(n, c='ic'):
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{inner(n)}</svg>'
