**file**: docs/requirements/requirement-python-cli-interface.md
**Status**: Active (Version 1.3.3)
**Area**: python
**Key**: `requirement-python-cli-interface`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official command-line entry points, empty-argv behavior, and typed verbs for the HtmlCrawler Python package.

The text-menu picture is `requirement-python-tui`. Crawl, download, list, and serve are `requirement-domain-htmlcrawler`. The page folder, resume, and caps are `requirement-html-page-download`. The site walk is `requirement-html-site-crawl`. The about page is `requirement-python-about`. The domain sentence stays on the domain file. The logger construct is `requirement-python-cli-logging`. Class homes are `requirement-python-oop`.

`def main` writes `ChronicleLogger(...)` and then constructs `Cli`. The argument parser runs after that construct and after the debug block. The four messages in that block are `requirement-python-cli-debug`. Logging still calls ChronicleLogger. The running `src/HtmlDownloader/cli.py` dispatches `download`, `crawl`, and `serve`.

### 1.1 Human-facing

**In one sentence:** `html-crawler` with no words opens the numbered menu on a terminal, and with no terminal it prints help and stops.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at the keyboard or in a script | `html-crawler` or `html-crawler download --url URL --name PAGENAME` |
| The other role | The menu picture and the page facts | `requirement-python-tui`, `requirement-domain-htmlcrawler` |
| Not this file | How the frame is drawn, and where the page is saved | TUI and domain requirements |

| Includes | Excludes |
|----------|----------|
| Console script, module entry, typed verbs, empty-argv menu or help | A shell installer on empty argv |
| `download` and `serve` as typed verbs, also owned by the domain file | A numbered row for `help` |
| Pip verbs `version-check`, `self-update`, `self-install`, `self-uninstall`, also owned by the text menu | `sudo` pip, or a downloaded script piped into a shell |

| Surface | What you open | What for |
|---------|---------------|----------|
| `html-crawler` on a terminal | Front board | Menu. Does not download a page |
| `html-crawler` with no terminal | Help text | Exit 0 |
| `html-crawler download --url URL --name PAGENAME` | The terminal | Saves the page. Does not draw the menu |
| `html-crawler help` | Help text | Verb list. Does not draw the menu |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal | The front board opens. Pip does not run. | `html-crawler` |
| Start in a script | Help text, exit 0. | `html-crawler` |
| Save a page | Needs `--url` and `--name`. The menu does not open. | `html-crawler download --url URL --name PAGENAME` |
| Serve a saved page | Needs `--page-name`. `--port` defaults to 5000. Listens on `127.0.0.1`. | `html-crawler serve --page-name PAGENAME` |
| Check or change the install | Pip runs only when you ask. Empty argv does not. | `html-crawler version-check` |

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose a console script entry named `html-crawler` pointing at `HtmlCrawler.cli:main` (declared in packaging SSOT).
2. **MUST** support module execution: `python -m HtmlCrawler`.
3. **MUST** keep `def main` in `src/HtmlDownloader/cli.py` as the single runtime entry. `main` writes `ChronicleLogger(...)` before it constructs `Cli` (`requirement-python-cli-logging`, `requirement-python-oop`).
4. **MUST NOT** require root or sudo to run the CLI.

### 2.2 Empty argv

5. On a terminal, bare invocation (`html-crawler` with no args, or `python -m HtmlCrawler` with no args) **MUST** open the front board in `requirement-python-tui`. It **MUST NOT** start a download. It **MUST NOT** run pip.
6. When stdout is not a terminal, bare invocation **MUST** print help and return 0. It **MUST NOT** draw the text screen and **MUST NOT** wait.
7. **MUST NOT** default empty argv to a shell-channel install or to self-update.

### 2.3 Typed verbs

8. `ArgumentParser.parse_args` **MUST** run after `ChronicleLogger(...)` and after the debug block.
9. The typed verbs are `help`, `version`, `about`, `download`, `crawl`, `serve`, `self-install`, `version-check`, `self-update`, and `self-uninstall`. Each one is operational. **MUST NOT** add a verb whose only purpose is a test. `language` is not a typed verb. Menu row 7 owns it (`requirement-python-cli-language`). **MUST NOT** add `language` to `PRODUCT_VERBS`.
10. **MUST NOT** invent flags that scan the working directory. `download` accepts `--url` and `--name` only. `crawl` accepts `--url`, `--name`, `--depth`, and `--max-pages`, and all four are required. `serve` accepts `--page-name` and `--port` only. `--force` belongs only to `self-uninstall`. `--depth` and `--max-pages` **MUST NOT** be accepted on `download`.
11. On a terminal, `download`, `crawl`, and `serve` **MUST NOT** draw the text screen. `about` **MUST** open the about page.
12. With no terminal, `about` **MUST** print the about page and return 0. It does not draw the text screen. `download` and `serve` still run. They do not need a terminal.
13. `help` **MUST NOT** draw the text screen and returns 0. `download` needs `--url` and `--name`. `crawl` needs `--url`, `--name`, `--depth`, and `--max-pages`. `serve` needs `--page-name`. `--port` defaults to 5000. Menu row 1 is download. It is not a welcome line. `crawl` is not a menu row in this pass.
14. `version` **MUST** print `__version__` and **MUST NOT** call pip and **MUST NOT** draw the text screen.
15. `version-check`, `self-update`, `self-install`, and `self-uninstall` **MUST NOT** open the text screen. The commands are:

| Verb | Command |
|------|---------|
| `version-check` | `python -m pip index versions HtmlCrawler` |
| `self-update` | `python -m pip install --upgrade HtmlCrawler` |
| `self-install` | `python -m pip install HtmlCrawler` |
| `self-uninstall` | `python -m pip uninstall -y HtmlCrawler` only when `--force` is also present |

`self-uninstall` without `--force` **MUST** print the next step and return non-zero. The package stays installed. These commands **MUST NOT** use `sudo` and **MUST NOT** use `curl`. Empty argv **MUST NOT** run `self-install` or `self-update`.

Every typed verb is named again by its topic owner. Help text is not that second mention.

| Verb | Second mention |
|------|----------------|
| `help`, `version` | This file for `help`. `version` is also row 61 on `requirement-python-tui` |
| `about` | `requirement-python-about` and row 62. The domain sentence stays on `requirement-domain-htmlcrawler` |
| `download` | `requirement-domain-htmlcrawler` for the verb. `requirement-html-page-download` for the save |
| `crawl` | `requirement-domain-htmlcrawler` for the catalog. `requirement-html-site-crawl` for the walk |
| `serve` | `requirement-domain-htmlcrawler`. Menu row 3 |
| `self-install`, `version-check`, `self-update`, `self-uninstall` | Rows 63–66 on `requirement-python-tui` |

`language` is not in this table. The second mention of that ban is `requirement-python-cli-language`.

Complete invocation samples:

```text
html-crawler
html-crawler help
html-crawler version
html-crawler about
html-crawler download --url URL --name PAGENAME
html-crawler crawl --url URL --name SITENAME --depth N --max-pages N
html-crawler serve --page-name PAGENAME
html-crawler self-install
html-crawler version-check
html-crawler self-update
html-crawler self-uninstall --force
python -m HtmlCrawler
```

### 2.4 Download and serve

These rules are the `download` and `serve` verbs. The text screen draws the menu forms (`requirement-python-tui`). The domain file owns the page folder. They are not what empty argv does.

16. `download` **MUST** require `--url` and `--name`. A missing flag exits non-zero and names the gap. It **MUST NOT** scan the working directory. The save **MUST** obey `requirement-html-page-download`.
17. `serve` **MUST** require `--page-name`. `--port` defaults to **5000**. It **MUST** listen on `127.0.0.1` only.
18. A URL that does not start with `http://` or `https://`, or a page name that is not one file name, **MUST** fail with a message and **MUST NOT** claim success.
19. A `--page-name` that is not a saved page **MUST** fail with a message. It **MUST NOT** delete a folder.
20. On the text screen, a number that is not on the current list **MUST** stay on that list. **MUST NOT** proceed with that number.
21. Ctrl+C on `serve` **MUST** return 0 and print `Stopped <name>.`
22. **MUST** show a clear success or failure outcome after the download attempt.

Esc on a menu question returns to the previous board and does not download.

### 2.5 Flags

24. The parser accepts the verbs in rule 9. `help` is also available as `--help`.
25. This product does not claim `--json`. **MUST NOT** add it in this file.
26. **MUST NOT** add `--debug`. Debug status is the environment gate on `requirement-python-cli-debug`. Logging still calls ChronicleLogger for that list.

### 2.6 Output behavior

27. Download and serve failures **MUST** be visible to the operator. On the text screen they are drawn in the menu region. Off the text screen they are console lines.
28. Durable status **MUST** go through ChronicleLogger once `main` has constructed it (`requirement-python-cli-logging`). The console failure sentence remains required.
29. **MUST NOT** mix a machine-only JSON mode into the session. This product does not claim `--json`.

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `html-crawler = HtmlCrawler.cli:main` |
| **Module entry** | `src/HtmlDownloader/__main__.py` → `main()` |
| **CLI module** | `src/HtmlDownloader/cli.py` defines `Cli` and `def main` in the allowed end state |
| **Empty argv, terminal** | Front board. No download. No pip |
| **Empty argv, no terminal** | Help text. Return 0 |
| **Parser** | After ChronicleLogger and the debug block |
| **Quiet / JSON** | Text screen sets `is_quiet=True` on the logger construct. No `--json` |
| **Privilege** | user-level only |
| **Running tree** | `cli.py` dispatches `download`, `crawl`, and `serve` |
| **Copied console script** | `html-downloader` until the ship-unit rename |
| **Product version** | `1.0.1` |

Inside `_dispatch`, a bound that belongs to another verb fails closed. The crawl branch follows the download branch:

```python
if (args.depth is not None or args.max_pages is not None) and verb != "crawl":
    return self.report_error(
        "--depth and --max-pages are only for crawl.",
        "{0} crawl --url URL --name SITENAME --depth N --max-pages N".format(
            Cli.CONSOLE_NAME
        ),
    )
if verb == "crawl":
    return self._verb_crawl(args.url, args.name, args.depth, args.max_pages)
```

`_verb_crawl` is the method quoted on `requirement-html-site-crawl`. `--depth` uses `_depth_value` (integer ≥ 0). `--max-pages` uses `_max_pages_value` (integer ≥ 1).
| **User docs** | Root `README.md` matches this contract |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry, empty argv, and each typed verb are explicit.
- **Principle 16 – Interactive awareness**: A terminal opens the menu. No terminal prints help and returns 0.
- **Principle 5 – SSOT**: Verb names live here and on the topic owner. The picture lives on the TUI requirement.
- **Principle 10 – Least privilege**: Pip verbs do not use sudo.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the person runs `html-crawler` as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to start the program or to run the pip verbs. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A bad URL or a missing page name does not claim success. A number that is not on the list asks again.
- **Intentional:** Empty argv is the menu on a terminal and help off a terminal.
- **Anti-fragile:** Module entry and the console script both call `main`.
- **Over-protect:** Empty argv does not install, update, or download a page.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Change empty argv into a shell-channel install.
2. Make empty argv download a page or run pip.
3. Make empty argv off a terminal exit non-zero. That path prints help and returns 0.
4. Remove the console script or the module entry without a packaging and docs update.
5. Require root to download or serve a page.
6. Add `--json` or `--debug` in this file.
7. Treat help text as the second mention of a verb.
8. Add `language` as an argv verb. Row 7 is the menu language.
9. Drop `crawl` from the typed verbs, or accept `--depth` or `--max-pages` on `download`.

**Violating this rule is a critical CLI regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `html-crawler` entry declared in packaging |
| AC-2 | `python -m HtmlCrawler` reaches `main` |
| AC-3 | Empty argv on a terminal opens the front board and does not download and does not run pip |
| AC-4 | Empty argv with no terminal prints help and returns 0 |
| AC-5 | `download` without `--url` or `--name` exits non-zero. `crawl` without `--depth` or `--max-pages` exits non-zero. `serve` without `--page-name` exits non-zero |
| AC-6 | A URL that is not http or https does not save a page. An unlisted menu number asks again |
| AC-7 | Pip verbs match the command table and do not use sudo or curl |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-tui` | Menu picture and numbered rows |
| `requirement-python-cli-language` | `language` is not an argv verb. Menu row 7 |
| `requirement-domain-htmlcrawler` | Crawl, download, list, serve, and the about domain sentence |
| `requirement-html-site-crawl` | Depth, page cap, same host, robots |
| `requirement-html-page-download` | Page folder, assets, resume, and caps for `download` |
| `requirement-python-about` | The about page |
| `requirement-python-cli-logging` | Construct before the parser. Calls `isDebug()` and `log_message` |
| `requirement-python-cli-debug` | Owns the four debug messages. This file rejects `--debug` |
| `requirement-python-oop` | `Cli` and `def main` |
| `requirement-python-packaging` | Console script name |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-runtime-prerequisites` | ChronicleLogger |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CLI-01** | `tests/test_cli.py` | todo | Empty argv on a tty opens the front board |
| **TP-CLI-02** | `tests/test_download.py` | have | A bad URL or a bad page name does not save a page |
| **TP-CLI-03** | `tests/test_serve.py` | have | A missing saved page does not start the server |
| **TP-CLI-04** | `tests/test_cli.py` | optional | Empty argv off a tty prints help and returns 0 |
| **TP-TUI-07** | `tests/test_download.py` | have | `download` does not draw the menu |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**CLI routed-verb.** A command word the dispatcher accepts and hands to a handler. A word the dispatcher rejects is not a routed verb.

**Daily-life example:** If saying “toast” at the counter really gets you toast, toast is a routed verb. A word only printed on a poster is not.

**Project requirements.** Product law is the finished must/should rules for this product. They are not blank forms and not agent procedures.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form is not.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial Python CLI interface law for HtmlCrawler |
| 2026-10-04 | Active 1.1.0 | Empty argv opens the text menu on a terminal and prints help off a terminal. Typed verbs |
| 2026-10-04 | Active 1.1.1 | `language` is not an argv verb. Menu row 4 owns it |
| 2026-10-04 | Active 1.1.2 | Verb `about` is `requirement-python-about`. Product version **1.0.5** |
| 2026-10-16 | Active 1.2.0 | Verbs are help, version, about, download, serve, and the pip verbs. No `hello`. Product version **1.0.0** |
| 2026-10-28 | Active 1.2.1 | Inherited from HtmlDownloader. `crawl` was off that verb list |
| 2026-10-28 | Active 1.3.0 | `crawl` is a typed verb. `--depth` and `--max-pages` belong to `crawl` only. The copied dispatcher does not accept `crawl` yet |
| 2026-10-28 | Active 1.3.1 | Sections that named a media verb were removed |
| 2026-10-28 | Active 1.3.2 | `--debug` stays forbidden. The environment gate is `requirement-python-cli-debug` |
| 2026-10-28 | Active 1.3.3 | The running dispatcher accepts `crawl`. Product version **1.0.1** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
