import sys, re
from pathlib import Path
R = Path(__file__).parent.parent/'repo'
ROWS = {
 'criminal-code': ("| `criminal-code/` | Кримінальний кодекс України (Закон № 2341-III від 5 квітня 2001 року) | 1 | Oldest version available, dated 18 September 2026, the revision the Verkhovna Rada's site shows (basis: Law No. 4986-IX); about 540 articles |\n", 'Кримінальний кодекс України', 'https://zakon.rada.gov.ua/laws/show/2341-14', '2341-III of 5 April 2001'),
 'civil-code': ("| `civil-code/` | Цивільний кодекс України (Закон № 435-IV від 16 січня 2003 року) | 1 | Oldest version available, dated 5 August 2026, the revision the Verkhovna Rada's site shows (basis: Law No. 2541-IX); about 1,300 articles and the final provisions |\n", 'Цивільний кодекс України', 'https://zakon.rada.gov.ua/laws/show/435-15', '435-IV of 16 January 2003'),
}
s = (R/'README.md').read_text(encoding='utf8'); l = (R/'LICENSE').read_text(encoding='utf8')
s = re.sub(r'`criminal-code/`.*\n|`civil-code/`.*\n', '', s) if False else s
for slug in sys.argv[1:]:
    row, name, url, no = ROWS[slug]
    if f'`{slug}/`' in s: continue
    i = s.index('\n\n## Questions as git commands'); s = s[:i].rstrip('\n') + '\n' + row + s[i:]
    j = s.index('\n\nSee `LICENSE`'); s = s[:j].rstrip('\n') + f'\n| [Verkhovna Rada, Zakonodavstvo Ukrainy]({url}) | {name} ({no}), current revision | Official publication of the Verkhovna Rada; the site refuses traffic from outside Ukraine, so the page was read from an Internet Archive capture. |' + s[j:]
    l = l.replace('\n\nChanges made by Lexifina:', f'\n\nThe {name} ({no}) is likewise from {url}, read from an Internet Archive capture, retrieved 30 October 2026.\n\nChanges made by Lexifina:', 1)
s = s.replace('and no statute is built yet.', 'and only the statutes listed below are built.').replace('- **Statutes.** No Ukrainian statute is included yet.', '- **Statutes.** Only the codes listed in the table are included, each as one version (the revision in force); the Commercial Code (Господарський кодекс) is not included because it ceased to be in force on 28 August 2025.')
(R/'README.md').write_text(s, encoding='utf8'); (R/'LICENSE').write_text(l, encoding='utf8')
