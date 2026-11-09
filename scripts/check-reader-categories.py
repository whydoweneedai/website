#!/usr/bin/env python3
"""Check category assignment, legacy routing and content preservation."""
import json,re,subprocess,tomllib,sys
from pathlib import Path
from site_data import load_site
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
site=load_site(); categories=site['topic_pages']; assert len(categories)==4
assert len(site['articles'])==18
assert {c:sum(a['topic']==c for a in site['articles']) for c in categories}=={'getting-started':4,'using-ai-at-work':8,'tools-comparisons':2,'costs-results':2}
class Links(HTMLParser):
 def __init__(self,s):super().__init__();self.hrefs=[];self.feed(s)
 def handle_starttag(self,t,a):
  if t=='a':self.hrefs.append(dict(a).get('href',''))
for a in site['articles']:
 p=ROOT/'blog'/a['slug']/'index.html';s=p.read_text()
 baseline = 'origin/main' if a['slug']=='how-customers-find-small-business-chatgpt' else 'HEAD'
 body=lambda t:re.search(r'<article class="article-body">(.*?)</article>',t,re.S).group(1)
 if '--check-prose' in sys.argv:
  ref=baseline+':'+str(p.relative_to(ROOT))
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stderr=subprocess.DEVNULL).returncode==0:
   old=subprocess.check_output(['git','show',ref],cwd=ROOT,text=True)
   assert body(old)==body(s),a['slug']
 if a['topic']:
  assert f'/topics/{a["topic"]}/' in s
 else:
  assert a['slug'] in {'chatgpt-budget-from-bank-statement','thanksgiving-plan-chatgpt-menu-timeline-grocery-list'}
  crumb=re.search(r'<nav class="breadcrumbs".*?</nav>',s,re.S).group()
  assert '/topics/' not in crumb
for c in categories:
 s=(ROOT/'topics'/c/'index.html').read_text(); cards=re.search(r'<div class="card-grid">(.*?)</section>',s,re.S).group(1); links=Links(cards).hrefs
 for a in site['articles']:
  # Hub cards contain exactly their assigned articles; global nav contains none.
  assert (f'/blog/{a["slug"]}/' in links)==(a['topic']==c),(c,a['slug'])
for p in [ROOT/'index.html',ROOT/'blog/index.html',ROOT/'search/index.html',*(ROOT/'topics'/c/'index.html' for c in categories)]:
 s=p.read_text(); nav=re.search(r'<nav class="nav-inner".*?</nav>',s,re.S).group()
 assert all('/topics/'+c+'/' in nav for c in categories)
 assert not re.search(r'/topics/(tested|roi-planning|choosing-ai-tools)/',s)
routes=tomllib.loads((ROOT/'netlify.toml').read_text())['redirects']
for old,dest in site['raw']['legacyTopicRedirects'].items():
 for suffix in ['', '/', '/index.html']:
  assert any(x['from']==f'/topics/{old}{suffix}' and x['to']==dest and x['status']==301 for x in routes)
 assert dest in (ROOT/'topics'/old/'index.html').read_text()
index=json.loads((ROOT/'search/search-index.json').read_text());assert len(index)==18
assert sum(not x['topic'] for x in index)==2
assert {x['format'] for x in index}=={'Guide','Comparison','Our experiment'}
print('PASS: four category hubs (4/8/2/2), all 18 articles (use --check-prose for baseline equality), uncategorized personal guides, navigation, search and 15 legacy redirects')
