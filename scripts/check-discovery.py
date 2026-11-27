#!/usr/bin/env python3
"""Regression checks for generated search metadata, feeds, links and privacy."""
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from site_data import load_site
ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://whydoweneedai.com'
ORG=ORIGIN+'/#organization'
PERSON=ORIGIN+'/about/#ross-c'
site=load_site()
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
NOINDEX=re.compile(r'<meta name="robots" content="noindex')
live=[a for a in site['ordered'] if (ROOT/'blog'/a['slug']/'index.html').exists()]
assert len(urls)==len(set(urls)),'duplicate sitemap entries'
assert all(ORIGIN+'/blog/'+a['slug']+'/' in urls for a in live),'live post missing from sitemap'
assert not any(NOINDEX.search((ROOT/u.removeprefix(ORIGIN).strip('/')/'index.html').read_text()) for u in urls),'noindex page in sitemap'
# Thin topic hubs (fewer than 5 posts) and the quiz stay live but out of search.
for slug in site['topic_pages']:
 hub=(ROOT/'topics'/slug/'index.html').read_text();thin=sum(a['topic']==slug for a in site['articles'])<5
 assert bool(NOINDEX.search(hub))==thin and ((ORIGIN+'/topics/'+slug+'/') in urls)!=thin,slug
quiz=(ROOT/'ai-readyscore/index.html').read_text()
assert NOINDEX.search(quiz) and 'adsbygoogle' not in quiz and 'google-adsense-account' not in quiz
assert ORIGIN+'/ai-readyscore/' not in urls
assert ORIGIN+'/how-we-test/' not in urls and ORIGIN+'/search/' not in urls
assert not any(r['slug'] in u for r in site['raw']['retiredArticles'] for u in urls)
for url in urls:
 rel=url.removeprefix(ORIGIN).strip('/')
 p=ROOT/rel/'index.html';s=p.read_text();page=Page(s)
 assert len([1 for t,a in page.tags if t=='h1'])==1,rel
 assert len([1 for t,a in page.tags if t=='link' and a.get('rel')=='canonical' and a.get('href')==url])==1,rel
 nodes=[]
 for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S):
  data=json.loads(raw);nodes.extend(data.get('@graph',[data]))
 orgs=[n for n in nodes if n.get('@type')=='Organization'];people=[n for n in nodes if n.get('@type')=='Person']
 assert len(orgs)==1 and orgs[0]['@id']==ORG and orgs[0]['name']=='Why Do We Need AI',rel
 assert orgs[0]['sameAs']==['https://x.com/whydoweneedai']
 assert len(people)==1 and people[0]['@id']==PERSON and people[0]['name']=='Ross C',rel
 assert 'sameAs' not in people[0],rel
 assert len([1 for t,a in page.tags if t=='meta' and a.get('property')=='og:image'])==1,rel
 assert len([1 for t,a in page.tags if t=='link' and a.get('type')=='application/rss+xml'])==1,rel
 for t,a in page.tags:
  link=a.get('href') if t in ['a','link'] else a.get('src') if t in ['img','script'] else None
  if not link:continue
  u=urlsplit(link)
  if u.netloc or u.scheme or not u.path:continue
  target=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)
  if target.is_dir():target/='index.html'
  assert target.exists(),(rel,link)
 if rel.startswith('blog/'):
  art=site['by_slug'][rel.split('/')[1]]
  posting=next(n for n in nodes if n.get('@type')=='BlogPosting')
  assert posting['publisher']=={'@id':ORG} and posting['author']=={'@id':PERSON},rel
  assert posting['dateModified']==art.get('dateModified',art['date']),rel
  assert '| Why Do We Need AI' not in re.search(r'<title>(.*?)</title>',s,re.S).group(1)
  assert any(n.get('@type')=='BreadcrumbList' for n in nodes),rel
 if rel=='blog' or rel.startswith('topics/'):
  collection=next(n for n in nodes if n.get('@type')=='CollectionPage')
  count=len(site['articles']) if rel=='blog' else sum(a['topic']==rel.split('/')[1] for a in site['articles'])
  assert len(collection['mainEntity']['itemListElement'])==count,rel
feed=ET.parse(ROOT/'feed.xml');items=feed.findall('channel/item')
assert len(items)==len(site['ordered']) and len({x.findtext('guid') for x in items})==len(items)
assert [x.findtext('link') for x in items]==[ORIGIN+'/blog/'+a['slug']+'/' for a in site['ordered']]
assert 'noindex' in (ROOT/'search/index.html').read_text()
assert 'Allow: /' in (ROOT/'robots.txt').read_text()
print(f'PASS: {len(urls)} sitemap pages (no noindex pages), entity graph, {len(live)} article breadcrumbs/dates, collection lists, {len(items)} feed items, social defaults, links and privacy')
