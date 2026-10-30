# Ukraine: law history in git

The law of Ukraine as a git history: one file per provision, one commit per law or decision on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a provision; `tools/on.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ua/`.

> **First build.** The text is the Constitution of Ukraine as published by the Verkhovna Rada on zakon.rada.gov.ua. This first build holds one version, the revision in force; the site lists earlier revisions (1996, 2006, 2010, 2011, 2013, 2014, 2016, 2019) that are not yet built, and only the statutes listed below are built.

Language: the text is in Ukrainian (the official language of the act); this README is in English.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Конституція України (1996), current revision | 1 | Oldest version available, dated 1 January 2020, the revision the Verkhovna Rada's site shows (basis: Law No. 27-IX of 3 September 2019); 161 articles with their numbered sub-articles and the transitional provisions |
| `criminal-code/` | Кримінальний кодекс України (Закон № 2341-III від 5 квітня 2001 року) | 1 | Oldest version available, dated 18 September 2026, the revision the Verkhovna Rada's site shows (basis: Law No. 4986-IX); about 540 articles and the final and transitional provisions |
| `civil-code/` | Цивільний кодекс України (Закон № 435-IV від 16 січня 2003 року) | 1 | Oldest version available, dated 5 August 2026, the revision the Verkhovna Rada's site shows (basis: Law No. 2541-IX); about 1,300 articles and the final provisions |
| `criminal-procedure-code/` | Кримінальний процесуальний кодекс України (Закон № 4651-VI від 13 квітня 2012 року) | 1 | Oldest version available, dated 21 July 2026, the revision the Verkhovna Rada's site shows (a Constitutional Court decision of that day declaring provisions unconstitutional); about 680 articles and the final and transitional provisions |
| `labour-code/` | Кодекс законів про працю України (1971) | 1 | Oldest version available, dated 31 July 2026, the revision the Verkhovna Rada's site shows (basis: Law No. 4742-IX); about 290 articles and the final provisions |

## Questions as git commands

| Question | Command |
| --- | --- |
| The whole act on a date | `python tools/on.py 2024-01-01 constitution` |
| One provision on a date | `python tools/on.py 2024-01-01 constitution <unit>` (unit = file name without `.md`) |
| Which law wrote each line of a provision? | `git blame constitution/<unit>.md` |
| Every change to a provision, word by word | `git log -p --word-diff constitution/<unit>.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## What it does not show

- **One version.** Only the current revision is built. The Constitution as adopted in 1996 and the revisions of 2006, 2010, 2011, 2013, 2014, 2016 and 2019 are not shown as separate versions; the single version is dated 1 January 2020 and credited to the publisher ("oldest version available").
- **Apparatus.** Chapter headings, the list of amending laws, editorial notes in braces and the site's footer are left out. Articles 121-123 were repealed with Chapter VII in 2016 and are not in the text.
- **Statutes.** Only the codes listed in the table are included, each as one version (the revision in force); the Commercial Code (Господарський кодекс) is not included because it ceased to be in force on 28 August 2025.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

Lexifina's code reads the saved Constitution page and writes `corpus.json`; `parse_parts.py` reads the saved code pages and writes one `corpus.d/` part per code. The shared builder turns `corpus.json` into the commits; `REPRODUCE.md` lists the sources, commands and decisions, and the result of the checks (every version read back from git on its in-force day and the day before, trailers parsed, no merge commits, dates never going backwards).

## Sources

| Source | What | Notes |
| --- | --- | --- |
| [Verkhovna Rada, Zakonodavstvo Ukrainy](https://zakon.rada.gov.ua/laws/show/254%D0%BA/96-%D0%B2%D1%80) | Constitution of Ukraine, revision of 01.01.2020 | Open data of the Rada is CC BY 4.0. |
| [Verkhovna Rada, Zakonodavstvo Ukrainy](https://zakon.rada.gov.ua/laws/show/2341-14) | Кримінальний кодекс України (2341-III of 5 April 2001), current revision | – |
| [Verkhovna Rada, Zakonodavstvo Ukrainy](https://zakon.rada.gov.ua/laws/show/435-15) | Цивільний кодекс України (435-IV of 16 January 2003), current revision | – |
| [Verkhovna Rada, Zakonodavstvo Ukrainy](https://zakon.rada.gov.ua/laws/show/4651-17) | Кримінальний процесуальний кодекс України (4651-VI of 13 April 2012), current revision | – |
| [Verkhovna Rada, Zakonodavstvo Ukrainy](https://zakon.rada.gov.ua/laws/show/322-08) | Кодекс законів про працю України (322-VIII of 10 December 1971), current revision | – |

See `LICENSE` for the attribution.
