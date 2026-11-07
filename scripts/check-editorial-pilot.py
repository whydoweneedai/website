#!/usr/bin/env python3
"""Static regression checks for the homepage/invoice editorial pilot."""
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
ARTICLE = 'blog/can-ai-enter-invoices-spreadsheet-test/index.html'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]; self.h1=0; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='img': self.images.append(a)
for rel in ['index.html', ARTICLE]:
    text=(ROOT/rel).read_text(); page=Page(text)
    assert page.h1==1, (rel,'heading count')
    assert len(page.ids)==len(set(page.ids)), (rel,'duplicate IDs')
    for href in page.links:
        url=urlsplit(href)
        if url.scheme or url.netloc: continue
        path=ROOT/unquote(url.path).lstrip('/') if url.path.startswith('/') else (ROOT/rel).parent/unquote(url.path)
        if url.path:
            if path.is_dir(): path=path/'index.html'
            assert path.exists(), (rel,href)
        if url.fragment and not url.path: assert unquote(url.fragment) in page.ids, (rel,href)
    for img in page.images:
        assert 'alt' in img, (rel,'missing alt')
        assert (ROOT/img['src'].lstrip('/')).is_file(), (rel,img['src'])
        assert 'width' in img and 'height' in img, (rel,'missing dimensions')
old=subprocess.check_output(['git','show','origin/main:'+ARTICLE],cwd=ROOT,text=True)
new=(ROOT/ARTICLE).read_text()
assert set(Page(old).ids)<=set(Page(new).ids)
old_body = re.search(r'<article class="article-body">(.*?)</article>', old, re.S).group(1)
assert set(Page(old_body).links)<=set(Page(new).links)
for heading in ['what-we-tested','what-happened','limits','how-we-ran-this-test','sources']:
    section=re.search(r'<h2 id="'+heading+r'".*?</h2>(.*?)(?=<h2 |<aside class="inline-cta")',old,re.S).group(1)
    # Every original paragraph and list/table detail retained in these evidence sections.
    for fragment in re.findall(r'<p>.*?</p>|<li>.*?</li>|<table>.*?</table>',section,re.S):
        assert fragment in new, (heading,fragment[:80])
assert new.count('<details class="test-detail">')==6
assert 'this is not a screenshot' in new
for path in (ROOT/'images/editorial').glob('*.svg'): ET.parse(path)
print('PASS: internal links, media, headings, IDs, original evidence detail, disclosures and SVG XML')
