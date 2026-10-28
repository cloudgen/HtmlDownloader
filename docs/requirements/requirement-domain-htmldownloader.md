**file**: docs/requirements/requirement-domain-htmldownloader.md
**Status**: Active (Version 1.5.3)
**Area**: domain
**Key**: `requirement-domain-htmldownloader`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the domain surface Single Source of Truth for HtmlDownloader: download one HTML page, list the pages already saved, and serve one saved page on this computer. The save itself (folders, resume, caps) is `requirement-html-page-download`.

Typed verbs and empty argv are owned by `requirement-python-cli-interface`. The screen that shows the front board is owned by `requirement-python-tui`. The about page is `requirement-python-about`. Class homes are `requirement-python-oop`.

This file remains the sole Active `requirement-domain-*`. The file key stays `requirement-domain-htmldownloader`. Headings and pictures in the root user document are `requirement-python-readme`.

### 1.1 Human-facing

**In one sentence:** HtmlDownloader downloads one HTML page and the stylesheets, scripts, and images that page links to, lists saved page names, and serves one saved page on this computer.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who wants a page saved or served | `html-downloader download --url URL --name PAGENAME` |
| The other role | The text menu, rows 1, 2, and 3 | `requirement-python-tui` |
| Not this file | The rounded menu frame, pip install, and the log folder | TUI, packaging, and logging requirements |

| Includes | Excludes |
|----------|----------|
| One saved page at `~/.app/HtmlDownloader/output/<pagename>/<html file>`, default `index.html` | Joining media, an encoder, a scan of the working directory for files |
| Typed `download`, which needs `--url`. `--name` may be omitted when the URL recommends the folder. `--html` is optional. The verb does not draw the menu | `hello`, `join`, and `list-videos` as verbs |
| Menu row 1 **download**, menu row 2 **list downloaded**, menu row 3 **serve** | A front-board row that lists files in the folder |
| Help and about as real pages | A downloaded-script installer advertised on the about page |

| Surface | What you open | What for |
|---------|---------------|----------|
| `html-downloader download --url URL --name PAGENAME` | The terminal | Save the page. No menu |
| Menu row 1 | The text menu | A numbered list of `page name: URL`, or a URL, a page name, and an HTML file name |
| Menu row 2 | The text menu | Saved page names, then edit or view when the tool is installed |
| Menu row 3, or `html-downloader serve --page-name PAGENAME` | This computer | Serve that page folder on `127.0.0.1` |
| `html-downloader about` | About page | Name, version, what the product does, how to start it |
| `html-downloader help` | Help page | The same capabilities, including what this product does not do |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Save a page | The HTML file defaults to `index.html` under that page name. `--html FILENAME` chooses another name. Linked stylesheets, scripts, and images are saved beside it. The process does not draw the menu. | `html-downloader download --url https://example.com/ --name example` |
| Continue a save | When the stored HTML file is already there and not empty, that page URL is not fetched again. A different name moves that file. Missing stylesheets, scripts, and images are fetched. Files already saved are kept. | The same command again |
| List saved pages | On a terminal, open the menu and choose **2**. The list is page names by number. | `html-downloader`, then `2` |
| Serve a page | The page folder is the site root. `/` is the stored HTML file, which defaults to `index.html`. An empty port uses **5000**. Ctrl+C stops the server and prints `Stopped <name>.` | `html-downloader serve --page-name example` |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Download

D-01 and D-02 route the save. Folder shape, resume, caps, fonts, and saved-HTML cleanup are `requirement-html-page-download`.

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| D-01 | Save a page | typed verb `download` with `--url`, optional `--name`, and optional `--html` | One page folder from the save law. Return 0 when the save finishes. The menu does not open | this file + CLI + save law |
| D-02 | Save from the menu | menu row 1, kind `download` | The same page folder. The menu lists saved `page name: URL` pairs, or accepts a URL, a page name, and an HTML file name | this file + TUI + save law |

**Routing:** `html-downloader download --url URL --name PAGENAME` **MUST** run D-01 and **MUST NOT** draw the menu. Front-board row 1 **MUST** run D-02. Bare `html-downloader` on a terminal opens the front board and **MUST NOT** run D-01.

**Non-goals:** joining media, calling FFmpeg or any other encoder, listing files in the working directory, `join`, `list-videos`, `hello`, a welcome line, a folder prompt, a shell installer, a `crawl` verb, following `<a href>` to more HTML pages.

Complete invocation sample this pillar owns:

```text
html-downloader download --url https://example.com/ --name example
```

That command saves the page and returns 0 when the save finishes, with or without a terminal. It does not draw the menu. A missing `--url` exits non-zero. `--name` may be omitted when the URL ends with `.html`, `.htm`, or a folder name such as `xxx`. Otherwise a missing `--name` exits non-zero. `--html page.html` stores that file name. An empty `--html` keeps the stored name, or the name recommended from the URL.

### 2.2 Pillar B — List downloaded

Menu row **2** **MUST** list saved page names by number. After a page is chosen, **21 edit** opens the stored HTML file in Visual Studio Code when the `code` command or the Visual Studio Code desktop entry is installed, and **22 view** opens it in the default browser when one is set. That file defaults to `index.html`. A missing tool is left off that menu. **0** returns to the page list, then to the main menu. `list downloaded` is not an argv verb. The short stays English.

### 2.3 Pillar C — Serve

`html-downloader serve --page-name PAGENAME` **MUST** serve `~/.app/HtmlDownloader/output/<pagename>/` on `127.0.0.1` until Ctrl+C. `--port` defaults to **5000**. The stored HTML file is `/`. That file defaults to `index.html`. The typed verb does not draw the menu.

Menu row **3** lists saved page names by number, then asks `Port [5000]:`. An empty answer uses **5000**.

Ctrl+C **MUST** return 0 and print `Stopped <name>.` The server **MUST NOT** listen on an address other than `127.0.0.1`. A name that is not a saved page **MUST** fail with a message and **MUST NOT** delete that folder.

### 2.4 Pillar D — What this product does not do

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Download, list, serve | The three surfaces above. The save mechanics are the peer save law | this file + `requirement-html-page-download` |
| No media join | **MUST NOT** concatenate, re-encode, or publish a media file | this file |
| No file list | **MUST NOT** scan the working directory to list files for the person | this file |
| No encoder | **MUST NOT** require or invoke `ffmpeg` | this file |
| No welcome | **MUST NOT** offer `hello` or a welcome line. Menu row 1 is download | this file |

### 2.5 Pillar E — Help and about

`html-downloader help` and `python -m HtmlDownloader --help` **MUST** list download and serve and **MUST NOT** list `hello`, `join`, `list-videos`, or an encoder. Help is a typed verb. It is not a numbered menu row.

The domain sentence on the about page is `Download a page and its stylesheets, scripts, and images`. The page, the host check, and the star box are `requirement-python-about`.

| Field | Content |
|-------|---------|
| Product name | HtmlDownloader |
| Version | `__version__`, the same string as `pyproject.toml` (current `1.1.0`) |
| Domain summary | Download a page and its stylesheets, scripts, and images |

The page **MUST** use that domain sentence. The runtime-tools line **MUST** be `none`. It **MUST NOT** name FFmpeg.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `HtmlDownloader` |
| **Console script** | `html-downloader` |
| **Page class** | `PageDownload` in `src/HtmlDownloader/page_download.py` |
| **Serve class** | `PageServe` in `src/HtmlDownloader/page_serve.py`. Bind `127.0.0.1`. Default port **5000** |
| **Open class** | `PageOpen` in `src/HtmlDownloader/page_open.py`. Rows **21** and **22** |
| **Menu rows** | Front row 1 kind `download`. Front row 2 kind `list-downloaded`. Front row 3 kind `serve` |
| **Page folder** | `requirement-html-page-download` — `~/.app/HtmlDownloader/output/<pagename>/<html file>`, default `index.html` |
| **Map** | `requirement-html-page-download` — `output/url-map.json` |
| **VERSION** | `1.1.0` (`__init__.py` and `pyproject.toml`) |
| **Absent** | `src/HtmlDownloader/join.py`, verbs `hello`, `join`, and `list-videos`, FFmpeg |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **Screen** | `requirement-python-tui` |
| **User docs** | Root `README.md` |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Download, list, and serve are explicit. Empty argv does not download a page.
- **Principle 5 – SSOT**: One Active domain file. The page folder has one shape.
- **Principle 1 – Caution**: Join, file listing, a welcome line, and an encoder stay non-goals.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, download, list, and serve run as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to save or serve a page. Do not pipe a downloaded script into a shell.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not scan the working directory in order to download a page.
- **Intentional:** One page folder. Resume keeps the stored HTML file. Serve listens only on this computer.
- **Anti-fragile:** README, help, about, the terminal, and rows 1–3 name the same job.
- **Over-protect:** Keep the sole Active domain file. Keep this file key.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Add `join`, `list-videos`, `hello`, FFmpeg, or a working-directory file listing back without an explicit user order and a new revision of this file.
2. Add a shell installer or root elevation as silent domain behavior.
3. Create a second Active `requirement-domain-*` without superseding this one.
3a. Copy asset caps, flat-folder rules, or resume rules back into this file. Those stay on `requirement-html-page-download`.
3b. Add a `crawl` verb to this product.
4. Rename this file’s key without a registry update in the same change.
5. Make empty argv download a page or start a media job.
6. Serve on an address other than `127.0.0.1`.
7. Recreate `requirement-domain-videojoin`. The user confirmed its removal on 2026-10-28. A later Retired predecessor is a suggestion for removal. Ask the user to confirm before deleting that later file and its registry row.

**Violating this rule is a critical domain regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `html-downloader download --url URL --name PAGENAME` saves `output/<pagename>/index.html` and does not draw the menu. `--html FILENAME` saves that file name |
| AC-2 | When the stored HTML file already exists and is not empty, the page URL is not fetched again |
| AC-3 | Menu row 1 is `download`. Menu row 2 is `list downloaded`. Menu row 3 is `serve` |
| AC-4 | `serve` listens on `127.0.0.1`. The default port is 5000. Ctrl+C prints `Stopped <name>.` and returns 0 |
| AC-5 | `hello`, `join`, and `list-videos` are unknown verbs |
| AC-6 | Help and about use the download domain sentence and do not describe a join or an encoder |
| AC-7 | This file stays the sole Active domain SSOT |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-html-page-download` | One page, assets, resume, and caps |
| `requirement-python-cli-interface` | Typed `download` and `serve` |
| `requirement-python-about` | About page. This file keeps the domain sentence |
| `requirement-python-tui` | Rows 1, 2, and 3 |
| `requirement-python-oop` | `PageDownload`, `PageServe`, `PageOpen` |
| `requirement-runtime-prerequisites` | ChronicleLogger. No encoder |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-readme` | Headings and pictures in the user document |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| Download behavior | `tests/test_download.py` | have | The suite saves a page, resumes, drops `<base>`, and rejects `hello`. It does not use a `TP-HELLO` id |
| Serve behavior | `tests/test_serve.py` | have | The suite serves the page folder, rejects a missing page, and asks the menu for a port |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Domain requirements.** The one Active domain file is this product’s extra-job catalog: verbs, features, help lines, and about lines. A specialized product keeps exactly one Active file as that catalog.

**Daily-life example:** A café’s extra-job binder lists how takeout works, with a filled sample ticket. Opening and closing the shop is a different binder.

**Project requirements.** Product law is the finished must/should rules for this product. They are not blank forms and not agent procedures.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form is not.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for HtmlDownloader interactive two-file join |
| 2026-10-04 | Active 1.1.2 | Pillar D kept the join domain sentence. Product version **1.0.5** |
| 2026-10-05 | Active 1.2.0 | The domain is the welcome line. Join, file listing, and FFmpeg are non-goals |
| 2026-10-16 | Active 1.3.0 | The domain is download, list downloaded, and serve. Version **1.0.0**. The file key is unchanged |
| 2026-10-28 | Active 1.4.0 | Pillar A keeps routing. Folders, resume, and caps moved to `requirement-html-page-download`. No `crawl` verb |
| 2026-10-28 | Active 1.4.1 | Download can name the HTML file. The default stays `index.html`. Serve, edit, and view use the stored file |
| 2026-10-28 | Active 1.4.2 | The URL can recommend the page folder and the HTML file. `guide.html` saves `guide/guide.html`. `xxx` saves `xxx/index.html` |
| 2026-10-28 | Active 1.5.0 | Renamed from `requirement-domain-videojoin`. That file is Retired. This file is the sole Active domain SSOT |
| 2026-10-28 | Active 1.5.1 | A Retired predecessor is a suggestion for removal. Ask the user to confirm before deleting it |
| 2026-10-28 | Active 1.5.2 | The user confirmed. `requirement-domain-videojoin` is removed. Do not recreate that key |
| 2026-10-28 | Active 1.5.3 | The human box matches the omit-name sentence in this file. Product version **1.1.0** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
