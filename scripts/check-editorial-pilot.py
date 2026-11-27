#!/usr/bin/env python3
"""Static regression checks for the homepage (the invoice pilot post was retired on 2026-11-27)."""
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]; self.h1=0; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='img': self.images.append(a)
for rel in ['index.html']:
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
for path in (ROOT/'images/editorial').glob('*.svg'): ET.parse(path)
print('PASS: homepage internal links, media, headings, IDs and SVG XML')
