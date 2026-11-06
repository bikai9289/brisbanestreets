"""Local browser and static-export checks; does not certify the live host or Google indexation."""
from pathlib import Path
from urllib.parse import urlsplit
from html.parser import HTMLParser
from xml.etree import ElementTree
from playwright.sync_api import sync_playwright
import json

class LocalPage(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links = [], []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
BASE = 'http://127.0.0.1:4311'
ROUTES = ['/', '/controls/', '/unblocked/', '/about/', '/privacy/']
report = {'pages': [], 'runtimeErrors': [], 'failedLocalRequests': []}
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', headless=True)
    page = browser.new_page()
    page.on('pageerror', lambda error: report['runtimeErrors'].append(str(error)))
    page.on('response', lambda response: report['failedLocalRequests'].append(response.url) if response.url.startswith(BASE) and response.status >= 400 else None)
    for width in [1440, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1000})
        for route in ROUTES:
            response = page.goto(BASE+route, wait_until='networkidle')
            assert response.status == 200
            result = page.evaluate('''() => {
              const visible = [...document.querySelectorAll('body *')].filter(e => e.getClientRects().length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
              return {overflow: document.documentElement.scrollWidth > innerWidth,
                minFont: Math.min(...visible.map(e => parseFloat(getComputedStyle(e).fontSize))),
                brokenImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).length,
                headings: document.querySelectorAll('h1').length,
                canonical: document.querySelector('link[rel="canonical"]').href,
                schemas: [...document.querySelectorAll('script[type="application/ld+json"]')].map(e => JSON.parse(e.textContent)),
                resources: [...document.querySelectorAll('[href],[src]')].flatMap(e => ['href','src'].map(a => e.getAttribute(a))).filter(v => v && v.startsWith('/'))};
            }''')
            assert not result['overflow'] and result['minFont'] >= 16 and not result['brokenImages'], (width, route, result)
            assert result['headings'] == 1 and result['canonical'] == 'https://brisbanestreets.online'+route
            for resource in result.pop('resources'):
                relative = urlsplit(resource).path.lstrip('/')
                local = P / relative
                if local.is_dir(): local = local / 'index.html'
                assert local.is_file(), resource
            report['pages'].append({'width': width, 'route': route, **result})
            if width in [1440, 390] and route == '/':
                page.screenshot(path=str(P / f'preview-{width}.png'), full_page=True)
    page.goto(BASE+'/controls/')
    page.get_by_role('tab', name='Mobile / touch').click()
    page.locator('#mobile').wait_for(state='visible')
    page.locator('#desktop').wait_for(state='hidden')
    page.get_by_role('tab', name='Mobile / touch').press('ArrowLeft')
    page.locator('#desktop').wait_for(state='visible')
    page.goto(BASE+'/controls/#mobile')
    page.locator('#mobile').wait_for(state='visible')
    page.goto(BASE+'/controls/#desktop')
    page.locator('#desktop').wait_for(state='visible')
    page.goto(BASE+'/')
    play_link = page.locator('#play').get_by_role('link', name='Open official game')
    assert play_link.get_attribute('href') == 'https://brisbane-streets.pages.dev/'
    assert play_link.get_attribute('target') == '_blank'
    assert 'noopener' in play_link.get_attribute('rel').split()
    assert page.locator('iframe').count() == 0
    for section in ['missions', 'map', 'tips']:
        assert page.locator('#'+section).is_visible()
    page.locator('summary').first.click()
    assert page.locator('details').first.get_attribute('open') is not None
    page.goto(BASE+'/404.html')
    assert 'noindex' in page.locator('meta[name="robots"]').get_attribute('content')
    nojs = browser.new_context(java_script_enabled=False)
    nojs_page = nojs.new_page()
    nojs_page.goto(BASE+'/controls/')
    assert nojs_page.locator('#desktop').is_visible() and nojs_page.locator('#mobile').is_visible()
    assert nojs_page.locator('[role="tablist"]').is_hidden()
    browser.close()

dist = ROOT / 'dist'
link_count = 0
for path in dist.rglob('*.html'):
    parsed = LocalPage(path)
    assert len(parsed.ids) == len(set(parsed.ids)), ('Duplicate ID', path)
    for href in parsed.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        target = dist / url.path.lstrip('/') if url.path.startswith('/') else path.parent / url.path if url.path else path
        if target.is_dir():
            target = target / 'index.html'
        assert target.is_file(), (path, href)
        if url.fragment:
            assert url.fragment in LocalPage(target).ids, (path, href)
        link_count += 1
for path in dist.rglob('*'):
    if path.is_file():
        relative = path.relative_to(dist)
        assert path.suffix not in ['.py', '.md', '.json'], relative
        assert 'designs' not in relative.parts, relative
        assert path.read_bytes() == (P / relative).read_bytes(), relative
xml = ElementTree.parse(dist/'sitemap.xml')
urls = [node.text for node in xml.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert set(urls) == {'https://brisbanestreets.online'+route for route in ROUTES}
for line in (dist/'_redirects').read_text().splitlines():
    source, target, status = line.split()
    assert status == '301' and (dist/target.lstrip('/')/'index.html').is_file()
assert not report['runtimeErrors'] and not report['failedLocalRequests']
report.update({'interactions':'passed', 'noJavaScriptFallback':'passed', 'cleanExport':'passed', 'sitemapAndRedirectTargets':'passed', 'localLinksAndFragments':link_count, 'outboundPlayEntrance':'passed', 'liveDeployment':'not tested'})
(P/'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(f"PASS: {len(report['pages'])} page/viewport checks; keyboard tabs, hashes, FAQ, no-JS, local links, metadata and clean export. Live host still needs verification.")
