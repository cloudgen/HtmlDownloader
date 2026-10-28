**file**: docs/requirements/requirement-html-site-crawl.md
**Status**: Active (Version 1.0.2)
**Area**: crawl
**Key**: `requirement-html-site-crawl`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the walk law for HtmlCrawler: same-host HTML links, a required depth, a required page cap, robots, and a wait between requests.

Each saved document uses `requirement-html-page-download`. The verb is named here and on `requirement-domain-htmlcrawler` and `requirement-python-cli-interface`. This file is not a domain file.

### 1.1 Human-facing

**In one sentence:** A crawl starts at one URL, stays on that host, and stops at the depth and the page cap you set.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who set the bounds | `html-crawler crawl --url URL --name SITENAME --depth 1 --max-pages 20` |
| The other role | The walk | This file |
| Not this file | Stylesheets, scripts, images, and fonts inside one page | `requirement-html-page-download` |

| Includes | Excludes |
|----------|----------|
| `<a href>` on the same host | Links to another host |
| `robots.txt` for that host | A crawl when robots cannot be read |
| One second between requests | A zero wait |

| Surface | What you open | What for |
|---------|---------------|----------|
| `crawl` | The terminal | The walk. No menu |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Crawl | Depth and page cap are required. The start page is depth 0 | `html-crawler crawl --url https://example.com/ --name example --depth 1 --max-pages 20` |
| Omit a bound | The walk does not start | `html-crawler crawl --url URL --name example` |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Required arguments

1. `crawl` **MUST** take `--url`, `--name`, `--depth`, and `--max-pages`.
2. A missing flag **MUST** exit non-zero and name the flag.
3. `--depth` **MUST** be an integer ≥ 0. `--max-pages` **MUST** be an integer ≥ 1. Any other value **MUST** fail.
4. **MUST NOT** default either bound to unlimited.
5. `--depth` and `--max-pages` on `download` **MUST** fail.
6. The URL **MUST** be `http` or `https`, with a host, and without a username or password.
7. `--name` **MUST** be one file name. `assets` and `url-map.json` stay reserved.

### 2.2 Scope

8. The walk **MUST** enqueue an HTML link only when its host equals the start host after redirects.
9. Each absolute URL **MUST** be visited once.
10. Depth 0 is the start page only. A link from a page at depth D is depth D+1.
11. The walk **MUST** stop at `--depth` and at `--max-pages`, and **MUST** say which bound stopped it.
12. The walk **MUST NOT** run JavaScript. It reads `<a href>` in the HTML the server returns.
13. Each HTML document **MUST** be saved by `requirement-html-page-download`. This file **MUST NOT** restate asset caps.

### 2.3 Politeness

14. The walk **MUST** fetch `robots.txt` for the start host before any HTML page. A failed robots fetch **MUST** stop the crawl and **MUST NOT** fetch pages.
15. A path disallowed for `*` or for this product’s user agent **MUST** be skipped.
16. The wait between requests to that host **MUST** be 1 second.
17. The user agent **MUST** be `HtmlCrawler/` plus the product version.
18. The walk **MUST** run as the normal user.

### 2.4 Site folder

19. One crawl **MUST** write under the live app output root `~/.app/<app-name>/output/<sitename>/`. On this tree the app name is `HtmlDownloader`, so the folder is `~/.app/HtmlDownloader/output/<sitename>/`. List and serve read that same root.
20. The start URL’s path `/` or empty **MUST** save `<sitename>/index.html`.
21. Any other path **MUST** save `<sitename>/<path>/index.html`. The query and the fragment are dropped. `..` **MUST** fail that URL.
22. Each of those directories **MUST** hold its own `assets/css`, `assets/js`, and `assets/img`. Two HTML documents **MUST NOT** share one `index.html`.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product** | `HtmlCrawler` |
| **Intended verb** | `crawl` |
| **Delay** | 1 second |
| **Dispatcher** | Accepts `crawl` and calls `SiteCrawl`. See `requirement-domain-htmlcrawler` §2.5 |
| **Page engine** | `requirement-html-page-download`. `save_document` writes each HTML file |
| **Class home** | `SiteCrawl` in `src/HtmlDownloader/site_crawl.py`. `Cli._verb_crawl` constructs it. `PageDownloadError` is reused. There is no `SiteCrawlError` |
| **Output root** | `Cli.APP_NAME`, which is `HtmlDownloader` on this tree |
| **User agent** | `HtmlCrawler/` plus `__version__` |

`_verb_crawl` names each missing flag and constructs the walk at the call site:

```python
def _verb_crawl(self, url, name, depth, max_pages):
    """Walk one site. Does not draw the menu. Needs all four flags."""
    missing = []
    if not (url or "").strip():
        missing.append("--url")
    if not (name or "").strip():
        missing.append("--name")
    if depth is None:
        missing.append("--depth")
    if max_pages is None:
        missing.append("--max-pages")
    usage = "{0} crawl --url URL --name SITENAME --depth N --max-pages N".format(
        Cli.CONSOLE_NAME
    )
    if missing:
        return self.report_error("crawl needs {0}.".format(", ".join(missing)), usage)
    worker = SiteCrawl(Cli.APP_NAME, logger=self.logger)
    try:
        text = worker.crawl(url, name, depth, max_pages)
    except PageDownloadError as exc:
        return self.report_error(str(exc), usage)
    print(text)
    return 0
```

The walk sets the user agent, gates every fetch on that host, and unions robots rules for `*` and for a user agent that starts with `HtmlCrawler`:

```python
self.pages.user_agent = "{0}/{1}".format(self.CRAWL_PRODUCT, __version__)
self.pages.gate = self._gate

def _gate(self, url) -> None:
    key = self._host_key(url)
    if key is None:
        return
    now = self._clock()
    last = self._last.get(key)
    if last is not None:
        gap = self.DELAY_SECONDS - (now - last)
        if gap > 0:
            self._sleeper(gap)
            now = self._clock()
    self._last[key] = now

def _agents_apply(self, agents) -> bool:
    for agent in agents:
        token = agent.strip().lower()
        if token == "*":
            return True
        if token.startswith(self.CRAWL_PRODUCT.lower()):
            return True
    return False
```

`DELAY_SECONDS` is `1`. `CRAWL_PRODUCT` is `HtmlCrawler`. The stop line is `Stopped by --max-pages.`, `Stopped by --depth.`, `Stopped by --max-pages and --depth.`, or `Finished.` A root start calls `PageDownload._remember(start, name, pages.INDEX_NAME)` so menu row 2 and `serve` see the site. The map row stores `html` as `index.html`. A non-root start does not write a map row.

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Depth, page cap, same host, and robots bound the walk.
- **Principle 2 – Intentional**: The operator sets both bounds on every crawl.
- **Principle 3 – Anti-fragile**: Pages already saved stay if the walk stops.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the crawl runs as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to crawl. Do not pipe a downloaded script into a shell.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** No robots file means no crawl.
- **Intentional:** Depth and page cap are arguments, not hidden defaults.
- **Anti-fragile:** A stopped walk leaves saved pages in place.
- **Over-protect:** Another host is not queued.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Drop `--depth` or `--max-pages`, or default either to unlimited.
2. Follow a link onto another host.
3. Crawl when `robots.txt` could not be read.
4. Copy stylesheet, script, image, and font caps into this file.
5. Specialize this file onto HtmlDownloader.

**Violating this rule is a critical crawl-law regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `crawl` without `--depth` or `--max-pages` exits non-zero and names the gap |
| AC-2 | A link whose host differs from the start host is not saved |
| AC-3 | The walk stops at the page cap and says so |
| AC-4 | A disallowed robots path is skipped |
| AC-5 | A failed robots fetch saves no HTML page |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-domain-htmlcrawler` | Verb catalog, help, about |
| `requirement-html-page-download` | One document and its assets |
| `requirement-python-cli-interface` | Flag fence |
| `requirement-python-error-handling` | Failures stay visible |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CRAWL-01** | `tests/test_crawl.py` | have | Missing depth or page cap |
| **TP-CRAWL-02** | `tests/test_crawl.py` | have | Other host is not saved |
| **TP-CRAWL-03** | `tests/test_crawl.py` | have | Page cap stops the walk |
| **TP-CRAWL-04** | `tests/test_crawl.py` | have | Robots disallow and robots failure |

`./tests/run.sh` on 2026-10-28 is the proof run for these four rows. Hosts in that file are `127.0.0.1` and `127.0.0.1:9` only.

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Project requirements.** Product law is the finished must/should rules for this product. They are not blank forms and not agent procedures.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form is not.

**CLI gap name.** A command word the law names and the dispatcher still rejects.

**Daily-life example:** The board lists “rye” for next month, and the counter still says it does not serve rye. Rye is a gap name until the counter accepts it.

**Path-safe name.** A name that is safe to use as one path segment: no slash, no empty name, no parent-directory token.

**Daily-life example:** A folder label “receipts” is safe. A label “../receipts” is not, because it leaves the folder you meant.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.0 | Same-site walk. Required depth and page cap. One-second delay. Robots fail closed. Dispatcher wiring waits. |
| 2026-10-28 | Active 1.0.1 | `crawl` is routed. Output root is the live app name. `TP-CRAWL-01` through `TP-CRAWL-04` are have. |
| 2026-10-28 | Active 1.0.2 | A root start stores `html` as `index.html` in the url map. Product version **1.1.1** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
