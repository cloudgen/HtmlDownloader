**file**: docs/requirements/requirement-domain-htmlcrawler.md
**Status**: Active (Version 1.0.3)
**Area**: domain
**Key**: `requirement-domain-htmlcrawler`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the domain surface Single Source of Truth for HtmlCrawler: crawl one site, list saved sites, and serve one saved site on this computer.

One HTML document and its stylesheets, scripts, images, and fonts are `requirement-html-page-download`. The walk, the depth, the page cap, and robots are `requirement-html-site-crawl`. Typed flags are `requirement-python-cli-interface`. This file is the only Active `requirement-domain-*` on HtmlCrawler.

### 1.1 Human-facing

**In one sentence:** HtmlCrawler saves a same-site set of pages from one start URL, lists those sites, and serves one saved site on this computer.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who wants a site saved | `html-crawler crawl --url URL --name SITENAME --depth N --max-pages N` |
| The other role | The text menu for list and serve | `requirement-python-tui` |
| Not this file | Asset caps and the link-walk engine | The page-download and site-crawl requirements |

| Includes | Excludes |
|----------|----------|
| Typed `crawl` with a required depth and page cap | An unbounded crawl |
| Typed `download` for one page | Following links inside `download` |
| List saved names and serve one folder on `127.0.0.1` | A public bind address |

| Surface | What you open | What for |
|---------|---------------|----------|
| `html-crawler crawl --url URL --name SITENAME --depth N --max-pages N` | The terminal | Save that site. No menu |
| `html-crawler download --url URL --name PAGENAME` | The terminal | Save one page. No menu |
| Menu row 2 | The text menu | Saved names |
| Menu row 3 | This computer | Serve one saved folder |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Crawl a site | Pages on that host, up to the depth and the page cap | `html-crawler crawl --url https://example.com/ --name example --depth 1 --max-pages 20` |
| Save one page | One HTML file, `index.html` unless `--html` names another, and its assets. No further HTML pages | `html-crawler download --url https://example.com/ --name example` |
| Serve | The folder is the site root on `127.0.0.1` | `html-crawler serve --page-name example` |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Crawl

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| C-01 | Crawl a site | typed verb `crawl` with `--url`, `--name`, `--depth`, `--max-pages` | A site folder. Return 0 when the walk finishes. The menu does not open | this file + CLI + site-crawl law |
| C-02 | Save one page | typed verb `download` with `--url`. `--name` and `--html` may be omitted | One page. The menu does not open | this file + CLI + page-download law |

**Routing:** Bare `html-crawler` on a terminal opens the front board and **MUST NOT** crawl and **MUST NOT** download.

### 2.2 Pillar B — List and serve

Menu row **2** lists saved names by number. Menu row **3** and `html-crawler serve --page-name NAME` serve that folder on `127.0.0.1`. `--port` defaults to **5000**. Ctrl+C returns 0 and prints `Stopped <name>.`

`list downloaded` is not an argv verb. `language` is not an argv verb.

### 2.3 Pillar C — Help

`html-crawler help` **MUST** list `crawl` and `download` and `serve`. It **MUST** show that `crawl` requires `--url`, `--name`, `--depth`, and `--max-pages`.

### 2.4 Pillar D — About

The domain sentence on the about page is `Crawl a same-site set of pages, and save one page on its own.` The runtime-tools line **MUST** be `none`.

### 2.5 Ship-unit gap (this pass)

The dispatcher accepts `crawl` and hands it to `SiteCrawl`. Empty argv does not crawl. The about sentence in §2.4 is on the about page. The remaining gap is the package directory `src/HtmlDownloader`, the console script `html-downloader`, and `Cli.APP_NAME`. The intended names stay `html-crawler`, `python -m HtmlCrawler`, and `HtmlCrawler`. `crawl` is not a menu row.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product** | `HtmlCrawler` |
| **Intended console script** | `html-crawler` |
| **Copied tree this pass** | Package directory `src/HtmlDownloader`. Console script in packaging is still `html-downloader` until the ship-unit pass |
| **Origin URL** | Still `https://github.com/cloudgen/HtmlDownloader` until you confirm a new remote |
| **Save engine** | `requirement-html-page-download` |
| **Walk engine** | `requirement-html-site-crawl` |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Crawl is the domain. One-page save stays a separate verb.
- **Principle 5 – SSOT**: One Active domain file. Engine rules stay on their own files.
- **Principle 1 – Caution**: Empty argv does not crawl.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, crawl, download, list, and serve run as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to crawl or to serve. Do not pipe a downloaded script into a shell.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A crawl names its depth and its page cap.
- **Intentional:** List and serve stay on the menu. Crawl is a typed verb.
- **Anti-fragile:** One-page save stays on `download` while `crawl` is its own verb.
- **Over-protect:** This file stays the only Active domain file.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Open a second Active domain file beside this one.
2. Put asset caps or robots rules in this file. Those stay on the engine requirements.
3. Make empty argv crawl.
4. Treat the package rename as already done. The gap in §2.5 stays the package directory and the console script until that rename is ordered.
5. Copy this domain back onto HtmlDownloader.

**Violating this rule is a critical domain regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | This file is the only Active domain requirement |
| AC-2 | `crawl` requires `--url`, `--name`, `--depth`, and `--max-pages` |
| AC-3 | `download` remains one page and does not take `--depth` or `--max-pages` |
| AC-4 | Help lists `crawl`, `download`, and `serve` |
| AC-5 | The dispatcher accepts `crawl`. §2.5 names the remaining package and console-script gap |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-html-site-crawl` | Walk, scope, robots, delay, site folder |
| `requirement-html-page-download` | One page and its assets |
| `requirement-python-cli-interface` | Typed verbs and flag fences |
| `requirement-python-tui` | Menu rows for list and serve |
| `requirement-python-about` | About page. This file keeps the domain sentence |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CRAWL-01** | `tests/test_crawl.py` | have | Missing `--depth` or `--max-pages` exits non-zero |
| **TP-PAGE-01** | `tests/test_download.py` | have | The copied suite still saves one page |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Domain requirements.** The one Active domain file is this product’s extra-job catalog: verbs, features, help lines, and about lines. A second Active domain file is not allowed.

**Daily-life example:** A café’s extra-job binder lists how takeout works. Opening the shop is a different binder. The café keeps one current extra-job binder.

**CLI routed-verb.** A command word the dispatcher accepts and hands to a handler.

**Daily-life example:** If saying “toast” at the counter really gets you toast, toast is a routed verb.

**CLI gap name.** A command word the law names and the dispatcher still rejects.

**Daily-life example:** The menu board lists “rye” for next month, and the counter still says it does not serve rye. Rye is a gap name until the counter accepts it.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.0 | HtmlCrawler domain. Crawl plus one-page download. Copied dispatcher does not accept `crawl` yet. |
| 2026-10-28 | Active 1.0.1 | This file stays the only domain file |
| 2026-10-28 | Active 1.0.2 | The dispatcher accepts `crawl`. The remaining gap is the package name and the console script |
| 2026-10-28 | Active 1.0.3 | `download` may omit `--name` and may pass `--html`. Product version **1.1.1** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
