"""Ukraine phase 2: adds codes to the constitution-only corpus (tmp/corpus.base.json) from the saved zakon.rada.gov.ua pages
(Internet Archive captures, since the site blocks traffic from outside Ukraine). Reads .cache only."""
import hashlib, html, json, re, sys
from pathlib import Path
here = Path(__file__).parent
base = json.load(open(here/'tmp'/'corpus.base.json', encoding='utf8'))

def norm(s):
    s = html.unescape(s).replace(' ', ' ').replace('’', "'").replace('‘', "'").replace('ʼ', "'")
    s = s.replace('–', '-').replace('—', '-').replace('“', '"').replace('”', '"').replace('«', '"').replace('»', '"')
    return re.sub(r'\s+', ' ', s).strip()

def parse(fname):
    raw = (here/'.cache'/fname).read_bytes()
    h = raw.decode('utf8')
    h = h[h.index('<div id="article"'):]
    h = re.sub(r'<em>.*?</em>', '', h, flags=re.S)
    units = {}; cur = None; stop = False
    for m in re.finditer(r'<p\b[^>]*>(.*?)</p>', h, flags=re.S):
        inner = m.group(1)
        dt = re.search(r'data-tree="([^"]*)"', inner)
        t = norm(re.sub(r'<[^>]+>', ' ', re.sub(r'<br\s*/?>', ' ', inner)))
        if not t or t.startswith('{'): continue
        tree = dt.group(1) if dt else ''
        if t.startswith('Президент України') or stop: stop = True; break
        am = re.match(r'^Стаття ([\d\s\-]+?)\.\s*(.*)$', t) if re.match(r'^st\d', tree) else None
        if am:
            num = tree[2:]
            key = 'art-' + '-'.join(p.zfill(4 if 'civil' in fname or '435' in fname else 3) if i == 0 else p for i, p in enumerate(num.split('-')))
            if key in units: raise SystemExit('dup '+key)
            label = 'Ст. ' + num
            cur = {'label': label, 'kind': 'art', 'lines': [], 'head': '# Стаття ' + num}
            units[key] = cur
            if am.group(2): cur['lines'].append(am.group(2))
            continue
        if re.match(r'^(rz|kn|gl|pr|ro|pd)', tree) or re.match(r'^(Розділ|Книга|ЗАГАЛЬНА ЧАСТИНА|ОСОБЛИВА ЧАСТИНА|Глава|Параграф|Підрозділ)\b', t) and not tree.startswith(('pu', 'st')):
            if re.search(r'ПРИКІНЦЕВІ|ПЕРЕХІДНІ', t, re.I):
                key = 'prykintsevi-polozhennia' if 'ПРИКІНЦЕВІ' in t.upper() else 'perekhidni-polozhennia'
                if key in units: key += '-2'
                cur = {'label': 'Прикінцеві положення' if 'prykin' in key else 'Перехідні положення', 'kind': 'transitional', 'lines': [], 'head': '# ' + ('Прикінцеві положення' if 'prykin' in key else 'Перехідні положення')}
                units[key] = cur
            elif re.match(r'^Розділ [IVXL]+', t) or tree.startswith(('rz', 'kn')):
                cur = None if not (cur and cur['kind'] == 'transitional' and not re.match(r'^Розділ', t)) else cur
            continue
        if cur is None: continue
        cur['lines'].append(t)
    out = {}
    for k, u in units.items():
        u['lines'] = [x for x in (re.sub(r'\s*\{[^{}]*\}', '', l).strip() for l in u['lines']) if x and not re.fullmatch(r'\d+\.?', x)]
        if not u['lines']: continue
        out[k] = {'label': u['label'], 'kind': u['kind'], 'text': u['head'] + '\n' + ''.join(l + '\n' for l in u['lines'])}
    return raw, out

CODES = {
 'criminal-code': dict(file='2341-14.html', short='КК', title='Кримінальний кодекс України (Закон № 2341-III від 5 квітня 2001 року)', url='https://zakon.rada.gov.ua/laws/show/2341-14', vfrom='2026-09-18', basis='4986-20', label='Закон № 4986-IX'),
 'civil-code': dict(file='435-15.html', short='ЦК', title='Цивільний кодекс України (Закон № 435-IV від 16 січня 2003 року)', url='https://zakon.rada.gov.ua/laws/show/435-15', vfrom='2026-08-05', basis='2541-20', label='Закон № 2541-IX'),
}
# The codes moved to corpus.d parts (parse_parts.py, 2026-10-30); corpus.json now holds the constitution only.
only = sys.argv[1:]
for slug in only:
    c = CODES[slug]
    raw, units = parse(c['file'])
    base['acts'].append({'slug': slug, 'short': c['short'], 'title': c['title'], 'url': c['url'], 'first_law': None, 'earlier_laws': [],
        'versions': [{'from': c['vfrom'], 'source_url': c['url'], 'sha256': hashlib.sha256(raw).hexdigest(), 'units': units, 'credits': {},
                      'note': f"Current revision (Редакція від {c['vfrom'][8:]}.{c['vfrom'][5:7]}.{c['vfrom'][:4]}, basis: {c['label']}, https://zakon.rada.gov.ua/laws/show/{c['basis']}); the single version is dated to that revision."}]})
    base['sources'].append({'name': 'Verkhovna Rada: ' + c['title'] + ' (zakon.rada.gov.ua)', 'url': c['url'], 'retrieved': '2026-10-30', 'licence': 'official text of a law; open data of the Verkhovna Rada is CC BY 4.0',
        'notes': 'zakon.rada.gov.ua blocks traffic from outside Ukraine, so the page was read from an Internet Archive capture.'})
    base['decisions'].append(f"{slug}: one 'oldest version available', dated to the revision the Verkhovna Rada shows ({c['vfrom']}); earlier revisions are not built. Chapter and section headings and the editorial notes in braces are left out; each article is one file, with its title as the first line.")
    print(slug, len(units), sum(len(u['text']) for u in units.values()))
import os
json.dump(base, open(here/'corpus.json.tmp', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
os.replace(here/'corpus.json.tmp', here/'corpus.json')
