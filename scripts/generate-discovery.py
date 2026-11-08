#!/usr/bin/env python3
"""Normalize discovery metadata after page generation; never infer publication dates."""
import html
import json
import re
import xml.etree.ElementTree as ET
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path
from site_data import load_site

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://whydoweneedai.com'
ORG = ORIGIN + '/#organization'
PERSON = ORIGIN + '/about/#ross-c'
LD = re.compile(r'<script(?: id="[^"]*")? type="application/ld\+json">(.*?)</script>', re.S)
IDENTITY = {
    '@context': 'https://schema.org', '@graph': [
        {'@type': 'Organization', '@id': ORG, 'name': 'Why Do We Need AI',
         'url': ORIGIN + '/', 'logo': ORIGIN + '/website_logo.png',
         'sameAs': ['https://x.com/whydoweneedai']},
        {'@type': 'Person', '@id': PERSON, 'name': 'Ross C', 'url': PERSON,
         'jobTitle': 'Editor', 'worksFor': {'@id': ORG},
         'description': 'Editor of Why Do We Need AI, a publication about practical AI and automation decisions for small-business owners.'}
    ]}


def script(data, id=None):
    attr = f' id="{id}"' if id else ''
    return f'<script{attr} type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('<', '\\u003c') + '</script>'


def normalize(value):
    if isinstance(value, list):
        return [normalize(x) for x in value if not (isinstance(x, dict) and x.get('@type') == 'Organization')]
    if not isinstance(value, dict):
        return value
    if value.get('@type') == 'Organization':
        return {'@id': ORG}
    if value.get('@type') == 'Person' and value.get('name') == 'Ross C':
        return {'@id': PERSON}
    return {k: normalize(v) for k, v in value.items()}


def set_meta(text, name, content, prop=False):
    key = 'property' if prop else 'name'
    tag = f'<meta {key}="{name}" content="{html.escape(content, quote=True)}">'
    pattern = rf'<meta {key}="{re.escape(name)}"[^>]*>'
    if re.search(pattern, text):
        return re.sub(pattern, lambda m: tag, text, count=1)
    return text.replace('</head>', tag + '\n</head>', 1)


def itemlist(articles):
    return {'@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'url': ORIGIN + '/blog/' + a['slug'] + '/', 'name': a['searchTitle']}
        for i, a in enumerate(articles, 1)]}


def main():
    site = load_site()
    articles = site['by_slug']
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [x.text for x in sitemap.findall('s:url/s:loc', ns)]
    if (ROOT / 'how-we-test/index.html').exists():
        urls.append(ORIGIN + '/how-we-test/')
    urls = list(dict.fromkeys(urls))
    for url in urls:
        rel = url.removeprefix(ORIGIN).strip('/')
        path = ROOT / rel / 'index.html'
        text = path.read_text()
        text = re.sub(r'<script id="discovery-[^"]*" type="application/ld\+json">.*?</script>\s*', '', text, flags=re.S)
        text = re.sub(r'<link rel="alternate" type="application/rss\+xml"[^>]*>\s*', '', text)
        art = articles.get(rel.removeprefix('blog/')) if rel.startswith('blog/') else None
        def replace_ld(match):
            data = normalize(json.loads(match.group(1)))
            if data.get('@type') == 'BlogPosting' and art:
                # Schema headline describes the visible headline, not a historical title.
                h1 = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
                data['headline'] = html.unescape(re.sub('<[^>]+>', '', h1.group(1)))
                data['dateModified'] = art.get('dateModified', art['date'])
                data['description'] = art.get('metaDescription', data.get('description', art['searchDek']))
            if data.get('@type') == 'CollectionPage' and rel.startswith('topics/'):
                selected = [a for a in site['ordered'] if a['topic'] == rel.split('/')[1]]
                data['mainEntity'] = itemlist(selected)
            return script(data)
        text = LD.sub(replace_ld, text)
        additions = [script(IDENTITY, 'discovery-identity')]
        if art:
            old_title = html.unescape(re.search(r'<title>(.*?)</title>', text, re.S).group(1))
            title = art.get('metaTitle') or re.sub(r'\s*\|\s*Why Do We Need AI\??$', '', old_title)
            text = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title) + '</title>', text, count=1, flags=re.S)
            if art.get('metaDescription'):
                for name, prop in [('description', False), ('og:description', True), ('twitter:description', False)]:
                    text = set_meta(text, name, art['metaDescription'], prop)
            text = set_meta(text, 'article:modified_time', art.get('dateModified', art['date']), True)
            crumbs = [('Home', ORIGIN + '/'), ('Archive', ORIGIN + '/blog/')]
            if art['topic']:
                crumbs.append((art['topicLabel'], ORIGIN + '/topics/' + art['topic'] + '/'))
            crumbs.append((art['searchTitle'], url))
            additions.append(script({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': i, 'name': name, 'item': target}
                for i, (name, target) in enumerate(crumbs, 1)]}, 'discovery-breadcrumbs'))
        elif rel == 'blog':
            additions.append(script({'@context': 'https://schema.org', '@type': 'CollectionPage',
                '@id': url, 'url': url, 'name': 'All articles', 'publisher': {'@id': ORG},
                'mainEntity': itemlist(site['ordered'])}, 'discovery-archive'))
        for name, prop in [('og:image', True), ('twitter:image', False)]:
            key = 'property' if prop else 'name'
            if f'{key}="{name}"' not in text:
                text = set_meta(text, name, ORIGIN + '/images/og/about.png', prop)
        if 'name="twitter:card"' not in text:
            text = set_meta(text, 'twitter:card', 'summary_large_image')
        additions.append('<link rel="alternate" type="application/rss+xml" title="Why Do We Need AI" href="/feed.xml">')
        text = text.replace('</head>', '\n'.join(additions) + '\n</head>', 1)
        path.write_text(text)
    # Explicit content-change dates, not the build clock. Unchanged page dates stay unchanged.
    dates = json.loads((ROOT / 'data/page-modified.json').read_text())
    for entry in sitemap.findall('s:url', ns):
        url = entry.find('s:loc', ns).text
        rel = url.removeprefix(ORIGIN)
        art = articles.get(rel.removeprefix('/blog/').strip('/'))
        date = art.get('dateModified', art['date']) if art else dates.get(rel)
        if date:
            el = entry.find('s:lastmod', ns)
            if el is None:
                el = ET.SubElement(entry, '{' + ns['s'] + '}lastmod')
            el.text = date
    for url in urls:
        if not any(x.text == url for x in sitemap.findall('s:url/s:loc', ns)):
            entry = ET.SubElement(sitemap.getroot(), '{' + ns['s'] + '}url')
            ET.SubElement(entry, '{' + ns['s'] + '}loc').text = url
            if dates.get(url.removeprefix(ORIGIN)):
                ET.SubElement(entry, '{' + ns['s'] + '}lastmod').text = dates[url.removeprefix(ORIGIN)]
    ET.register_namespace('', ns['s'])
    ET.indent(sitemap, space='  ')
    sitemap.write(ROOT / 'sitemap.xml', encoding='UTF-8', xml_declaration=True)
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    for tag, value in [('title', 'Why Do We Need AI'), ('link', ORIGIN + '/'), ('description', 'Practical AI guides and documented experiments for small-business owners.'), ('language', 'en')]:
        ET.SubElement(channel, tag).text = value
    for art in site['ordered']:
        item = ET.SubElement(channel, 'item')
        url = ORIGIN + '/blog/' + art['slug'] + '/'
        for tag, value in [('title', art['searchTitle']), ('link', url), ('description', art['searchDek']), ('pubDate', format_datetime(datetime.fromisoformat(art['date']).replace(tzinfo=timezone.utc)))]:
            ET.SubElement(item, tag).text = value
        ET.SubElement(item, 'guid', isPermaLink='true').text = url
    ET.indent(rss, space='  ')
    ET.ElementTree(rss).write(ROOT / 'feed.xml', encoding='UTF-8', xml_declaration=True)
    lines = ['# Why Do We Need AI', '', '> Practical AI and automation guidance for small-business owners, with documented experiments and explicit limits.', '', '## Start here', '', '- [About and editorial responsibility](' + ORIGIN + '/about/)', '- [How we test](' + ORIGIN + '/how-we-test/)', '- [Editorial policy](' + ORIGIN + '/editorial-policy/)', '- [All articles](' + ORIGIN + '/blog/)', '- [RSS feed](' + ORIGIN + '/feed.xml)', '', '## Reader sections', '']
    for topic in site['raw']['topics']:
        lines.append(f"- [{topic['name']}]({ORIGIN}/topics/{topic['slug']}/): {topic['intro']}")
    lines.extend(['', '## Documented experiments', ''])
    for art in site['ordered']:
        if art['format'] == 'Our experiment':
            lines.append(f"- [{art['searchTitle']}]({ORIGIN}/blog/{art['slug']}/): {art['searchDek']}")
    lines.extend(['', 'These small, task-specific experiments do not predict performance in other businesses. Read each method and its limits before using the result.', ''])
    (ROOT / 'llms.txt').write_text('\n'.join(lines))
    print(f'Discovery metadata, RSS and curated index: {len(urls)} pages')

if __name__ == '__main__':
    main()
