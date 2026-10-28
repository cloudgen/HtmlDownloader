**file**: docs/requirements/requirement-python-cli-interface.md
**Status**: Active (Version 1.2.7)
**Area**: python
**Key**: `requirement-python-cli-interface`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official command-line entry points, empty-argv behavior, and typed verbs for the HtmlDownloader Python package.

The text-menu picture is `requirement-python-tui`. Download, list, and serve are `requirement-domain-htmldownloader`. The page folder, resume, and caps are `requirement-html-page-download`. The about page is `requirement-python-about`. The domain sentence stays on the domain file. The logger construct is `requirement-python-cli-logging`. Debug values are `requirement-python-cli-debug`. Class homes are `requirement-python-oop`. This program does not call an encoder.

`def main` writes `ChronicleLogger(...)` and then constructs `Cli`. The argument parser runs after that construct and after the debug block. The running `src/HtmlDownloader/cli.py` still starts the prompt session. The allowed end state is this file. This pass does not change `src/`.

### 1.1 Human-facing

**In one sentence:** `html-downloader` with no words opens the numbered menu on a terminal, and with no terminal it prints help and stops.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at the keyboard or in a script | `html-downloader` or `html-downloader download --url URL --name PAGENAME` |
| The other role | The menu picture and the page facts | `requirement-python-tui`, `requirement-domain-htmldownloader` |
| Not this file | How the frame is drawn, and where the page is saved | TUI and domain requirements |

| Includes | Excludes |
|----------|----------|
| Console script, module entry, typed verbs, empty-argv menu or help | A shell installer on empty argv. Flags that scan the working directory |
| `download` and `serve` as typed verbs, also owned by the domain file | A numbered row for `help`. `hello`, `join`, and `list-videos` are not verbs |
| Pip verbs `version-check`, `self-update`, `self-install`, `self-uninstall`, also owned by the text menu | `sudo` pip, or a downloaded script piped into a shell |

| Surface | What you open | What for |
|---------|---------------|----------|
| `html-downloader` on a terminal | Front board | Menu. Does not download a page |
| `html-downloader` with no terminal | Help text | Exit 0 |
| `html-downloader download --url URL --name PAGENAME` | The terminal | Saves the page. Does not draw the menu |
| `html-downloader help` | Help text | Verb list. Does not draw the menu |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal | The front board opens. Pip does not run. | `html-downloader` |
| Start in a script | Help text, exit 0. | `html-downloader` |
| Save a page | Needs `--url`. `--name` is the page folder. Omit it when the URL ends with `.html`, `.htm`, or a folder name such as `xxx`. `--html` chooses the HTML file. An empty value keeps a stored name, or the name recommended from the URL. The menu does not open. | `html-downloader download --url URL` |
| Serve a saved page | Needs `--page-name`. `--port` defaults to 5000. Listens on `127.0.0.1`. | `html-downloader serve --page-name PAGENAME` |
| Check or change the install | Pip runs only when you ask. Empty argv does not. | `html-downloader version-check` |

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose a console script entry named `html-downloader` pointing at `HtmlDownloader.cli:main` (declared in packaging SSOT).
2. **MUST** support module execution: `python -m HtmlDownloader`.
3. **MUST** keep `def main` in `src/HtmlDownloader/cli.py` as the single runtime entry. `main` writes `ChronicleLogger(...)` before it constructs `Cli` (`requirement-python-cli-logging`, `requirement-python-oop`).
4. **MUST NOT** require root or sudo to run the CLI.

### 2.2 Empty argv

5. On a terminal, bare invocation (`html-downloader` with no args, or `python -m HtmlDownloader` with no args) **MUST** open the front board in `requirement-python-tui`. It **MUST NOT** start a download. It **MUST NOT** run pip.
6. When stdout is not a terminal, bare invocation **MUST** print help and return 0. It **MUST NOT** draw the text screen and **MUST NOT** wait.
7. **MUST NOT** default empty argv to a shell-channel install or to self-update.

### 2.3 Typed verbs

8. `ArgumentParser.parse_args` **MUST** run after `ChronicleLogger(...)` and after the debug block.
9. The typed verbs are `help`, `version`, `about`, `download`, `serve`, `self-install`, `version-check`, `self-update`, and `self-uninstall`. Each one is operational. **MUST NOT** add a verb whose only purpose is a test. **MUST NOT** add `hello`, `join`, or `list-videos`. `language` is not a typed verb. Menu row 7 owns it (`requirement-python-cli-language`). **MUST NOT** add `language` to `PRODUCT_VERBS`.
10. **MUST NOT** invent flags that scan the working directory. `download` accepts `--url`, `--name`, and `--html` only. `--url` is required. `--name` and `--html` may be omitted. The omitted names come from the URL, as `requirement-html-page-download` states. An empty `--html` keeps the stored HTML file name when the page is already saved. `serve` accepts `--page-name` and `--port` only. `--force` belongs only to `self-uninstall`. **MUST NOT** add `crawl`, `--depth`, or `--max-pages` on this product.
11. On a terminal, `download` and `serve` **MUST NOT** draw the text screen. `about` **MUST** open the about page.
12. With no terminal, `about` **MUST** print the about page and return 0. It does not draw the text screen. `download` and `serve` still run. They do not need a terminal.
13. `help` **MUST NOT** draw the text screen and returns 0. `download` needs `--url`. `--name` is the page folder and may be omitted when the URL recommends one. `--html` names the HTML file inside the page folder. `serve` needs `--page-name`. `--port` defaults to 5000. Menu row 1 is download. It is not a welcome line.
14. `version` **MUST** print `__version__` and **MUST NOT** call pip and **MUST NOT** draw the text screen.
15. `version-check`, `self-update`, `self-install`, and `self-uninstall` **MUST NOT** open the text screen. The commands are:

| Verb | Command |
|------|---------|
| `version-check` | `python -m pip index versions HtmlDownloader` |
| `self-update` | `python -m pip install --upgrade HtmlDownloader` |
| `self-install` | `python -m pip install HtmlDownloader` |
| `self-uninstall` | `python -m pip uninstall -y HtmlDownloader` only when `--force` is also present |

`self-uninstall` without `--force` **MUST** print the next step and return non-zero. The package stays installed. These commands **MUST NOT** use `sudo` and **MUST NOT** use `curl`. Empty argv **MUST NOT** run `self-install` or `self-update`.

Every typed verb is named again by its topic owner. Help text is not that second mention.

| Verb | Second mention |
|------|----------------|
| `help`, `version` | This file for `help`. `version` is also row 61 on `requirement-python-tui` |
| `about` | `requirement-python-about` and row 62. The domain sentence stays on `requirement-domain-htmldownloader` |
| `download`, `serve` | `requirement-domain-htmldownloader` for the verb. `requirement-html-page-download` for the save. Menu rows 1 and 3 |
| `self-install`, `version-check`, `self-update`, `self-uninstall` | Rows 63–66 on `requirement-python-tui` |

`language` is not in this table. The second mention of that ban is `requirement-python-cli-language`.

Complete invocation samples:

```text
html-downloader
html-downloader help
html-downloader version
html-downloader about
html-downloader download --url URL --name PAGENAME
html-downloader serve --page-name PAGENAME
html-downloader self-install
html-downloader version-check
html-downloader self-update
html-downloader self-uninstall --force
python -m HtmlDownloader
```

### 2.4 Download and serve

These rules are the `download` and `serve` verbs. The text screen draws the menu forms (`requirement-python-tui`). The domain file owns the page folder. They are not what empty argv does.

16. `download` **MUST** require `--url`. A missing `--url` exits non-zero and names the gap. `--name` may be omitted when the URL recommends the page folder, as `requirement-html-page-download` states. Otherwise a missing `--name` exits non-zero and names the gap. `--html` may be omitted. It **MUST NOT** scan the working directory. The save **MUST** obey `requirement-html-page-download`.
17. `serve` **MUST** require `--page-name`. `--port` defaults to **5000**. It **MUST** listen on `127.0.0.1` only.
18. A URL that does not start with `http://` or `https://`, or a page name that is not one file name, **MUST** fail with a message and **MUST NOT** claim success.
19. A `--page-name` that is not a saved page **MUST** fail with a message. It **MUST NOT** delete a folder.
20. On the text screen, a number that is not on the current list **MUST** stay on that list. **MUST NOT** proceed with that number.
21. Ctrl+C on `serve` **MUST** return 0 and print `Stopped <name>.`
22. **MUST NOT** follow this verb with an encoder check.
23. **MUST** show a clear success or failure outcome after the download attempt.

Esc on a menu question returns to the previous board and does not download.

### 2.5 Flags

24. The parser accepts the verbs in rule 9. `help` is also available as `--help`.
25. This product does not claim `--json`. **MUST NOT** add it in this file.
26. **MUST NOT** add `--debug`. Debug status is the environment gate on `requirement-python-cli-debug`. How to ask ChronicleLogger stays on `requirement-python-cli-logging`.
27. **MUST NOT** add flags that name two local media files.

### 2.6 Output behavior

28. Download and serve failures **MUST** be visible to the operator. On the text screen they are drawn in the menu region. Off the text screen they are console lines.
29. Durable status **MUST** go through ChronicleLogger once `main` has constructed it (`requirement-python-cli-logging`). The console failure sentence remains required.
30. **MUST NOT** mix a machine-only JSON mode into the session. This product does not claim `--json`.

### 2.7 No encoder

31. The front board **MUST** be allowed to open when `ffmpeg` is missing.
32. `download` and `serve` **MUST NOT** check for `ffmpeg`.
33. The about page says `Runtime tools: none` (`requirement-python-about`). It does not probe `PATH` and it does not install an encoder.

### 2.8 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `html-downloader = HtmlDownloader.cli:main` |
| **Module entry** | `src/HtmlDownloader/__main__.py` → `main()` |
| **CLI module** | `src/HtmlDownloader/cli.py` defines `Cli` and `def main` in the allowed end state |
| **Empty argv, terminal** | Front board. No download. No pip |
| **Empty argv, no terminal** | Help text. Return 0 |
| **Parser** | After ChronicleLogger and the debug block |
| **Quiet / JSON** | Text screen sets `is_quiet=True` on the logger construct. No `--json` |
| **Privilege** | user-level only |
| **Running tree** | `cli.py` dispatches `download` and `serve`. It does not call `ffmpeg` |
| **Product version** | `1.1.1` |
| **User docs** | Root `README.md` matches this contract |

### 2.9 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry, empty argv, and each typed verb are explicit.
- **Principle 16 – Interactive awareness**: A terminal opens the menu. No terminal prints help and returns 0.
- **Principle 5 – SSOT**: Verb names live here and on the topic owner. The picture lives on the TUI requirement.
- **Principle 10 – Least privilege**: Pip verbs do not use sudo.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the person runs `html-downloader` as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to start the program or to run the pip verbs. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

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
6. Add `hello`, `join`, or `list-videos` without a domain-law change.
7. Add file-operand flags, `--json`, or `--debug` in this file.
8. Treat help text as the second mention of a verb.
9. Add `language` as an argv verb. Row 7 is the menu language.
10. Add `crawl` to the typed verbs. This product saves one page.
11. Keep a Retired requirement on disk because an older line says the key stays. Suggest removal of that file and its registry row, and ask the user to confirm before deleting either one.

**Violating this rule is a critical CLI regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `html-downloader` entry declared in packaging |
| AC-2 | `python -m HtmlDownloader` reaches `main` |
| AC-3 | Empty argv on a terminal opens the front board and does not download and does not run pip |
| AC-4 | Empty argv with no terminal prints help and returns 0 |
| AC-5 | `download` without `--url` exits non-zero. Without `--name`, the URL must recommend the folder, or the command exits non-zero. `serve` without `--page-name` exits non-zero |
| AC-6 | A URL that is not http or https does not save a page. An unlisted menu number asks again |
| AC-7 | Pip verbs match the command table and do not use sudo or curl |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-tui` | Menu picture and numbered rows |
| `requirement-python-cli-language` | `language` is not an argv verb. Menu row 7 |
| `requirement-domain-htmldownloader` | Download, list, serve, and the about domain sentence |
| `requirement-html-page-download` | Page folder, assets, resume, and caps for `download` |
| `requirement-python-about` | The about page |
| `requirement-python-cli-logging` | Construct before the parser. How to ask ChronicleLogger |
| `requirement-python-cli-debug` | Environment gate and the printed values. No `--debug` flag |
| `requirement-python-oop` | `Cli` and `def main` |
| `requirement-python-packaging` | Console script name |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-runtime-prerequisites` | ChronicleLogger. No encoder |
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
| 2026-08-09 | Active 1.0.0 | Initial Python CLI interface law for HtmlDownloader |
| 2026-10-04 | Active 1.1.0 | Empty argv opens the text menu on a terminal and prints help off a terminal. Typed verbs. Join questions are the `join` verb |
| 2026-10-04 | Active 1.1.1 | `language` is not an argv verb. Menu row 4 owns it |
| 2026-10-04 | Active 1.1.2 | Verb `about` is `requirement-python-about`. Rule 33 no longer claims a live ffmpeg probe. Product version **1.0.5** |
| 2026-10-16 | Active 1.2.0 | Verbs are help, version, about, download, serve, and the pip verbs. No `hello`. Product version **1.0.0** |
| 2026-10-28 | Active 1.2.1 | `download` still takes `--url` and `--name` only. The save is `requirement-html-page-download`. `crawl` stays off this verb list |
| 2026-10-28 | Active 1.2.2 | `download` also accepts `--html`. An empty value keeps the stored HTML file name, or `index.html` |
| 2026-10-28 | Active 1.2.3 | `--name` may be omitted. The URL recommends the folder and the HTML file |
| 2026-10-28 | Active 1.2.4 | Rule 16 and AC-5 match rule 10. A Retired requirement is a suggestion for removal. Ask the user to confirm before deleting it |
| 2026-10-28 | Active 1.2.5 | Product version **1.1.0** |
| 2026-10-28 | Active 1.2.6 | Rule 26 points the environment gate at `requirement-python-cli-debug`. Logging still shows how to ask ChronicleLogger. Product version stays **1.1.0** |
| 2026-10-28 | Active 1.2.7 | Product version **1.1.1** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
