# How this repository was made (Ukraine)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Verkhovna Rada: Конституція України (zakon.rada.gov.ua), revision of 01.01.2020 | <https://zakon.rada.gov.ua/laws/show/254%D0%BA/96-%D0%B2%D1%80> | 2026-10-29 | official text of a law; open data of the Verkhovna Rada is CC BY 4.0 |
| Verkhovna Rada: Кримінальний кодекс України (Закон № 2341-III від 5 квітня 2001 року) (zakon.rada.gov.ua) | <https://zakon.rada.gov.ua/laws/show/2341-14> | 2026-10-30 | official text of a law; open data of the Verkhovna Rada is CC BY 4.0 |
| Verkhovna Rada: Цивільний кодекс України (Закон № 435-IV від 16 січня 2003 року) (zakon.rada.gov.ua) | <https://zakon.rada.gov.ua/laws/show/435-15> | 2026-10-30 | official text of a law; open data of the Verkhovna Rada is CC BY 4.0 |
| Verkhovna Rada: Кримінальний процесуальний кодекс України (Закон № 4651-VI від 13 квітня 2012 року) (zakon.rada.gov.ua) | <https://zakon.rada.gov.ua/laws/show/4651-17> | 2026-10-30 | official text of a law; open data of the Verkhovna Rada is CC BY 4.0 |
| Verkhovna Rada: Кодекс законів про працю України (затверджений Законом № 322-VIII від 10 грудня 1971 року) (zakon.rada.gov.ua) | <https://zakon.rada.gov.ua/laws/show/322-08> | 2026-10-30 | official text of a law; open data of the Verkhovna Rada is CC BY 4.0 |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Конституція України (прийнята 28 червня 1996 року), чинна редакція | 1 | 2020-01-01 to 2020-01-01 |
| `criminal-code` | Кримінальний кодекс України (Закон № 2341-III від 5 квітня 2001 року) | 1 | 2026-09-18 to 2026-09-18 |
| `civil-code` | Цивільний кодекс України (Закон № 435-IV від 16 січня 2003 року) | 1 | 2026-08-05 to 2026-08-05 |
| `criminal-procedure-code` | Кримінальний процесуальний кодекс України (Закон № 4651-VI від 13 квітня 2012 року) | 1 | 2026-07-21 to 2026-07-21 |
| `labour-code` | Кодекс законів про працю України (затверджений Законом № 322-VIII від 10 грудня 1971 року) | 1 | 2026-07-31 to 2026-07-31 |

The build made 5 commits:

| Commits | Kind |
| ---: | --- |
| 5 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 5 tags.

## Dates

Each commit is dated at noon (Europe/Kyiv) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Zakon.rada.gov.ua dates each revision of an act from the day the amending law takes effect; this text is the revision of 01.01.2020 (basis: Law No. 27-IX of 3 September 2019). https://zakon.rada.gov.ua/laws/show/254%D0%BA/96-%D0%B2%D1%80

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `9e13de93ba50c1a1e3dbdbd96e65725f004e201ba7d696893f93a59dfdb29795` (5986135 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

5 versions of 5 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 5 history commits and 5 tags (history tip `380def55540cc6e20ef2c9361375106e39e217dd`).

## Decisions made by hand

- Ukrainian is the language of the act; it is built in Ukrainian.
- One version, the oldest available (first_law null), credited to the Verkhovna Rada as publisher. It is dated 2020-01-01, the date of the revision the site shows ("Редакція від 01.01.2020"). The site lists earlier revisions (1996, 2006, 2010, 2011, 2013, 2014, 2016, 2019); they were not fetched in this first build.
- The page was read from an Internet Archive capture of 23 October 2026.
- Unit files: preamble, one per article (art-NNN, with art-129-1 style keys for articles such as 129-1), and the transitional provisions of Chapter XV; chapter headings, amendment notes in braces, the amending-law list, the footer and the "***" line are left out. Articles 121-123 were repealed with Chapter VII in 2016 and are not in the text.
- criminal-code: one 'oldest version available', dated to the revision the Verkhovna Rada shows (2026-09-18); earlier revisions are not built. Chapter and section headings and the editorial notes in braces are left out; each article is one file, with its title as the first line.
- civil-code: one 'oldest version available', dated to the revision the Verkhovna Rada shows (2026-08-05); earlier revisions are not built. Chapter and section headings and the editorial notes in braces are left out; each article is one file, with its title as the first line.
- criminal-procedure-code: one 'oldest version available', dated to the revision the Verkhovna Rada shows (2026-07-21); earlier revisions are not built. Chapter and section headings and the editorial notes in braces are left out; each article is one file, with its title as the first line.
- labour-code: one 'oldest version available', dated to the revision the Verkhovna Rada shows (2026-07-31); earlier revisions are not built. Chapter and section headings and the editorial notes in braces are left out; each article is one file, with its title as the first line.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code wrote the code and chose the source; it did not write or alter any legal text. The code is deterministic and runs no model.
