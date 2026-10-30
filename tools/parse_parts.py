"""Ukraine phase 2 parts: one corpus.d part per code, from saved zakon.rada.gov.ua pages (archive captures, since the
site refuses traffic from outside Ukraine). Reads .cache only; writes corpus.d/<part>.json atomically.

Usage: python -X utf8 parse_parts.py [part ...]
"""
import hashlib, html, json, os, re, sys
from pathlib import Path

here = Path(__file__).parent
CACHE = here / '.cache'


def norm(s):
    s = html.unescape(s).replace('\xa0', ' ').replace('’', "'").replace('‘', "'").replace('ʼ', "'")
    s = s.replace('–', '-').replace('—', '-').replace('“', '"').replace('”', '"')
    s = s.replace('«', '"').replace('»', '"')
    return re.sub(r'\s+', ' ', s).strip()


def strip_notes(t):
    # editorial notes in braces, possibly nested once
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r'\s*\{[^{}]*\}', '', t)
    return t.strip()


TRANS = re.compile(r'(ПРИКІНЦЕВІ|ПЕРЕХІДНІ)', re.I)


def paragraphs(raw):
    """Every <p> in the article body: (data-tree, normalised text)."""
    h = raw.decode('utf8')
    h = h[h.index('<div id="article"'):]
    end = h.find('<div id="cut_off"')
    for m in re.finditer(r'<p\b([^>]*)>(.*?)</p>', h, flags=re.S):
        attrs, inner = m.group(1), m.group(2)
        dt = re.search(r'data-tree="([^"]*)"', attrs + inner)
        t = norm(re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>', ' ', inner)))
        yield (dt.group(1) if dt else ''), t


def parse(raw, pad):
    units = {}
    cur = None
    for tree, t in paragraphs(raw):
        if not t:
            continue
        t = strip_notes(t)
        if not t or re.fullmatch(r'\d+\.?', t):
            continue
        am = re.match(r'^Стаття ([\d\s\-]+?)\.\s*(.*)$', t) if re.match(r'^st\d', tree) else None
        if am:
            num = tree[2:]
            parts = num.split('-')
            key = 'art-' + '-'.join([parts[0].zfill(pad)] + parts[1:])
            if key in units:
                raise SystemExit('duplicate ' + key)
            cur = {'label': 'Ст. ' + num, 'kind': 'art', 'lines': [], 'head': '# Стаття ' + num}
            units[key] = cur
            if am.group(2):
                cur['lines'].append(am.group(2))
            continue
        if re.match(r'^(rz|kn|gl|pr\b|ro|pd|fr)', tree) or (
                not tree.startswith(('pu', 'st', 'ch', 'pp', 'cm')) and
                re.match(r'^(Розділ|Книга|ЗАГАЛЬНА ЧАСТИНА|ОСОБЛИВА ЧАСТИНА|Глава|Параграф|Підрозділ)\b', t)):
            mt = TRANS.search(t)
            if mt and 'ПОЛОЖЕННЯ' in t.upper() and (tree.startswith(('rz', 'gl')) or t.upper().startswith(('РОЗДІЛ', 'ГЛАВА', 'ПРИКІНЦЕВІ', 'ПЕРЕХІДНІ'))):
                up = t.upper()
                fin, per = 'ПРИКІНЦЕВІ' in up, 'ПЕРЕХІДНІ' in up
                if fin and per:
                    key, label = 'prykintsevi-ta-perekhidni-polozhennia', 'Прикінцеві та перехідні положення'
                elif fin:
                    key, label = 'prykintsevi-polozhennia', 'Прикінцеві положення'
                else:
                    key, label = 'perekhidni-polozhennia', 'Перехідні положення'
                if key in units:
                    key += '-2'
                cur = {'label': label, 'kind': 'transitional', 'lines': [], 'head': '# ' + label}
                units[key] = cur
            elif cur is not None and cur['kind'] == 'transitional':
                # sub-headings inside final or transitional provisions (Розділ I, Розділ II) are part of that text
                cur['lines'].append(t)
            else:
                cur = None
            continue
        if cur is None:
            continue
        cur['lines'].append(t)
    out = {}
    for k, u in units.items():
        if not u['lines']:
            continue
        out[k] = {'label': u['label'], 'kind': u['kind'], 'text': u['head'] + '\n' + ''.join(l + '\n' for l in u['lines'])}
    return out


def verify(raw, units):
    """Independent check against the page: every body paragraph that is not a heading or an editorial note is found
    in the units (article headings by their title), and every unit line is a paragraph of the page.
    Returns (page paragraphs not in the units, unit lines not on the page)."""
    page = []
    for tree, t in paragraphs(raw):
        t = strip_notes(t)
        if not t or re.fullmatch(r'\d+\.?', t):
            continue
        m = re.match(r'^Стаття [\d\s\-]+\.\s*(.*)$', t)
        if m:
            t = m.group(1)
            if not t:
                continue
        page.append(t)
    lines = set()
    for u in units.values():
        lines.update(u['text'].split('\n')[1:-1])
    pageset = set(page)
    missing = [t for t in page if t not in lines and not re.match(
        r'^(Розділ|РОЗДІЛ|Глава|ГЛАВА|Книга|Параграф|Підрозділ|§|ЗАГАЛЬНА|ОСОБЛИВА|КРИМІНАЛЬНИЙ|КОДЕКС|Кодекс|ВІДОМОСТІ|\(Відомості|Президент|м\. Київ|\d+ \w+ \d{4} року|N |№ )', t)]
    notfound = [l for l in lines if l not in pageset]
    return missing, notfound


CODES = {
    '10-criminal-code': dict(
        slug='criminal-code', file='2341-14.html', ts='20261009072950', pad=3, short='КК',
        title='Кримінальний кодекс України (Закон № 2341-III від 5 квітня 2001 року)',
        url='https://zakon.rada.gov.ua/laws/show/2341-14', vfrom='2026-09-18',
        basis='Редакція від 18.09.2026, підстава - 4986-IX'),
    '15-civil-code': dict(
        slug='civil-code', file='435-15.html', ts='20261023023036', pad=4, short='ЦК',
        title='Цивільний кодекс України (Закон № 435-IV від 16 січня 2003 року)',
        url='https://zakon.rada.gov.ua/laws/show/435-15', vfrom='2026-08-05',
        basis='Редакція від 05.08.2026, підстава - 2541-IX'),
    '20-criminal-procedure-code': dict(
        slug='criminal-procedure-code', file='4651-17@20261013044159.html', ts='20261013044159', pad=3, short='КПК',
        title='Кримінальний процесуальний кодекс України (Закон № 4651-VI від 13 квітня 2012 року)',
        url='https://zakon.rada.gov.ua/laws/show/4651-17', vfrom='2026-07-21',
        basis='Визнання неконституційними окремих положень від 21.07.2026, підстава - v008p710-26 (Конституційний Суд України)'),
    '30-labour-code': dict(
        slug='labour-code', file='322-08@20261016024229.html', ts='20261016024229', pad=3, short='КЗпП',
        title='Кодекс законів про працю України (затверджений Законом № 322-VIII від 10 грудня 1971 року)',
        url='https://zakon.rada.gov.ua/laws/show/322-08', vfrom='2026-07-31',
        basis='Редакція від 31.07.2026, підстава - 4742-IX'),
}


def main(only):
    (here / 'corpus.d').mkdir(exist_ok=True)
    for part in only:
        c = CODES[part]
        raw = (CACHE / c['file']).read_bytes()
        units = parse(raw, c['pad'])
        missing, notfound = verify(raw, units)
        d = c['vfrom']
        act = {'slug': c['slug'], 'short': c['short'], 'title': c['title'], 'url': c['url'], 'first_law': None,
               'earlier_laws': [],
               'versions': [{'from': d, 'source_url': c['url'], 'sha256': hashlib.sha256(raw).hexdigest(),
                             'units': units, 'credits': {},
                             'note': f"Current revision as the Verkhovna Rada shows it ({c['basis']}); the single "
                                     f"version is dated to that revision."}]}
        obj = {'acts': [act],
               'sources': [{'name': 'Verkhovna Rada: ' + c['title'] + ' (zakon.rada.gov.ua)', 'url': c['url'],
                            'retrieved': '2026-10-30',
                            'licence': 'official text of a law; open data of the Verkhovna Rada is CC BY 4.0',
                            'notes': f"Read from an Internet Archive capture of {c['ts'][:4]}-{c['ts'][4:6]}-{c['ts'][6:8]}, "
                                     "since zakon.rada.gov.ua refuses traffic from outside Ukraine."}],
               'decisions': [f"{c['slug']}: one 'oldest version available', dated to the revision the Verkhovna Rada "
                             f"shows ({d}); earlier revisions are not built. Chapter and section headings and the "
                             "editorial notes in braces are left out; each article is one file, with its title as the "
                             "first line."]}
        p = here / 'corpus.d' / f'{part}.json'
        tmp = p.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding='utf-8')
        os.replace(tmp, p)
        print(part, len(units), 'units', sum(len(u['text']) for u in units.values()), 'chars;',
              'page paragraphs not in units:', len(missing), '; unit lines not on page:', len(notfound))
        for t in missing[:15]:
            print('   MISSING', t[:140])
        for t in notfound[:5]:
            print('   NOTFOUND', t[:140])


if __name__ == '__main__':
    main(sys.argv[1:] or list(CODES))
