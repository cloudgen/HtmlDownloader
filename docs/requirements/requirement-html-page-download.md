**file**: docs/requirements/requirement-html-page-download.md
**Status**: Active (Version 1.0.2)
**Area**: download
**Key**: `requirement-html-page-download`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the save law for one HTML page and the stylesheets, scripts, images, and fonts that page links to.

The typed verb `download` and menu row 1 stay on `requirement-domain-htmlcrawler`. Empty argv and the flag fence stay on `requirement-python-cli-interface`. This file is not a second domain file.

### 1.1 Human-facing

**In one sentence:** One download stores the page as `index.html` and stores the stylesheets, scripts, images, and fonts that page links to beside it.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who asked for one page | `html-crawler download --url URL --name PAGENAME` |
| The other role | The save inside that command | This file |
| Not this file | Which verb is typed, the menu picture, and serving the folder | Domain, CLI, and TUI requirements |

| Includes | Excludes |
|----------|----------|
| One `index.html` and flat `assets/css`, `assets/js`, and `assets/img` | A second HTML page reached from `<a href>` |
| Resume when `index.html` is already there | Fetching that page URL again |
| Fonts in `assets/css` | Running JavaScript to discover more links |

| Surface | What you open | What for |
|---------|---------------|----------|
| `download --url URL --name PAGENAME` | The terminal | Save that one page |
| Menu row 1 | The text menu | The same save after a URL and a page name |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Save a page | `index.html` plus linked assets land under that page name | `html-crawler download --url https://example.com/ --name example` |
| Save again | `index.html` stays. Missing assets are fetched. Files already there stay. | The same command again |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 One page

1. The save **MUST** store one HTML document for the URL it was given.
2. It **MUST NOT** follow `<a href>` to another HTML document.
3. It **MUST** fetch linked stylesheets, scripts, images, and font files named by that document and by stylesheet `url()` and `@import`.
4. It **MUST** ignore `data:`, `javascript:`, `mailto:`, and `blob:` references.
5. The URL **MUST** start with `http://` or `https://`, **MUST** have a host, and **MUST NOT** contain a username or password.
6. The save **MUST** run as the normal user. It **MUST NOT** use administrator privilege.

### 2.2 Folder

The page is `~/.app/HtmlCrawler/output/<pagename>/index.html`. Stylesheets and fonts go in `output/<pagename>/assets/css/`. Scripts go in `output/<pagename>/assets/js/`. Images go in `output/<pagename>/assets/img/`. Those three folders stay flat. `output/url-map.json` remembers each URL and page name.

7. The page name **MUST** be one file name. `/`, `\`, and an empty name **MUST** fail.
8. The names `assets` and `url-map.json` **MUST** stay reserved.
9. The page folder **MUST** stay inside `output/`.

### 2.3 Resume and saved HTML

10. When `index.html` exists and is not empty, the page URL **MUST NOT** be fetched again.
11. An asset file already in the page folder **MUST** be kept. A missing asset **MUST** be fetched.
12. After local links are written, the saved HTML **MUST** drop `<base>`, `xml:base`, `<link rel="canonical">`, and HTML comments.
13. A failed page fetch **MUST** stop and name the URL. A failed asset **MUST** be listed. Files already saved **MUST** stay.

### 2.4 Caps

| Bound | Value |
|-------|--------|
| Response body | 15 MiB (`15 * 1024 * 1024` bytes) |
| Request timeout | 30 seconds |
| Stylesheets | 40 |
| Stylesheet `@import` depth | 4 |
| Scripts | 40 |
| Images | 400 |
| Fonts | 80 |

14. Hitting a cap **MUST** stop that class of fetch and **MUST** say so. A body past the byte cap **MUST NOT** be kept.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product** | `HtmlCrawler` |
| **Class** | `PageDownload` in `src/HtmlDownloader/page_download.py` (copied tree; package rename waits) |
| **Page folder** | `~/.app/HtmlCrawler/output/<pagename>/index.html` |
| **Map** | `~/.app/HtmlCrawler/output/url-map.json` |
| **Verb owner** | `requirement-domain-htmlcrawler` (typed `download`, menu row 1) |
| **Flag owner** | `requirement-python-cli-interface` (`--url` and `--name` only) |
| **Crawl** | Not this file. The walk is `requirement-html-site-crawl`. This save still does not follow `<a href>` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: The save has one owner, separate from the menu and the verb list.
- **Principle 1 – Caution**: Scheme, size, and name are checked. A bad page fetch stops.
- **Principle 5 – SSOT**: Asset folders and caps live here. The domain file does not copy them.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the save runs as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to fetch a page or to create `~/.app/HtmlCrawler`. Do not pipe a downloaded script into a shell.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A URL that is not `http` or `https` does not save a page.
- **Intentional:** One page, then the assets that page names.
- **Anti-fragile:** Resume keeps `index.html` and files already stored.
- **Over-protect:** Anchors to other HTML pages stay out of this save.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Follow `<a href>` to more HTML documents from this requirement.
2. Turn this file into a second Active `requirement-domain-*`.
3. Remove the byte cap, the resume rule, or the reserved names.
4. Add the crawl walk to this file. The walk is `requirement-html-site-crawl`. This file stays one page.

**Violating this rule is a critical save-law regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `download --url URL --name PAGENAME` writes `output/<pagename>/index.html` and the linked assets |
| AC-2 | When `index.html` exists and is not empty, that page URL is not fetched again |
| AC-3 | A URL that is not `http` or `https`, or a page name with a slash, does not save a page |
| AC-4 | Saved HTML drops `<base>`, `xml:base`, the canonical link, and HTML comments |
| AC-5 | The save does not enqueue another HTML document from `<a href>` |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-domain-htmlcrawler` | Owns the `download` verb and menu row 1 |
| `requirement-python-cli-interface` | Owns `--url` and `--name` |
| `requirement-python-error-handling` | A failed fetch stays visible |
| `requirement-python-oop` | Class `PageDownload` |
| `requirement-python-coding-style` | Publish with `shutil.move` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PAGE-01** | `tests/test_download.py` | have | The suite saves one page and its assets |
| **TP-PAGE-02** | `tests/test_download.py` | have | A bad URL or a bad page name does not save a page |
| **TP-PAGE-03** | `tests/test_download.py` | have | Resume keeps `index.html` and fills missing assets |
| **TP-PAGE-04** | `tests/test_download.py` | todo | A response over 15 MiB is refused |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Project requirements.** Product law is the finished must/should rules for this product. They are complete for this product. They are not blank forms, not agent procedures, and not a glossary.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form in a stationery shop is not.

**Domain requirements.** The one Active domain file is the catalog for this product’s extra job: the verbs, the features, the help lines, and the about lines. The save of stylesheets and scripts is engine law in this file. The domain file names the verb and points here.

**Daily-life example:** A café’s extra-job binder lists how takeout works. The recipe card for one sandwich is a different card. The binder still says which order uses that card.

**CLI routed-verb.** A command word the dispatcher accepts and hands to a handler. A word the dispatcher rejects is not a routed verb.

**Daily-life example:** If saying “toast” at the counter really gets you toast, toast is a routed verb. A word only printed on a poster is not.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.0 | Save law moved out of the domain file. One page, flat assets, resume, caps |
| 2026-10-28 | Active 1.0.1 | Product name HtmlCrawler. The walk stays on `requirement-html-site-crawl` |
| 2026-10-28 | Active 1.0.2 | Verb owner is `requirement-domain-htmlcrawler` |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
