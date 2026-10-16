**file**: docs/requirements/requirement-python-error-handling.md
**Status**: Active (Version 1.3.0)
**Area**: python
**Key**: `requirement-python-error-handling`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define how HtmlDownloader detects, reports, and recovers from errors during the text menu, download, and serve without deleting a saved page that already exists.

Console sentences in this file stay required. Durable status, once the logger exists, is `requirement-python-cli-logging`. ChronicleLogger is required. It is not optional.

### 1.1 Human-facing

**In one sentence:** When a download or a serve cannot finish, HtmlDownloader tells you why and leaves saved pages in place.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who typed a bad URL or a missing page | You see the reason and can try again or stop |
| The other role | The status file | The same fact is written by ChronicleLogger after `main` has constructed it |
| Not this file | The menu frame, and the page folder | `requirement-python-tui`, `requirement-domain-videojoin` |

| Includes | Excludes |
|----------|----------|
| A readable failure sentence. An existing page left in place | A silent success after a failed download |
| Ask again when the number is not on the list | Treating that number as a page |
| The missing-library sentence, printed before any logger exists | Sending that one line through `log_message` |

| Surface | What you open | What for |
|---------|---------------|----------|
| Download and serve questions | Menu region above the box | The reason, without leaving the board when the board is already open |
| `html-downloader download` without `--url` | Message, non-zero exit | Nothing new is claimed as saved |
| Console before the logger exists | Missing ChronicleLogger | The pip next step |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Pick a number that is not in the list | The question stays. | A bad number, then a listed one |
| Serve a name that was not saved | You see why. No server starts. | `html-downloader serve --page-name missing` |
| Run without the logger library | The console names the pip next step and the program returns non-zero. | `html-downloader` |

## 2. Core Rules (Mandatory)

### 2.1 Fail-closed principles

1. **MUST NOT** silently ignore a failed download or a failed serve when the product claims success.
2. **MUST NOT** treat invalid user input as success.
3. **MUST** prefer clear human-readable messages over stack traces for expected user mistakes.
4. **MUST** leave an existing saved page in place on a failed resume. **MUST NOT** delete files outside that page folder.

### 2.2 Required error categories

| Category | Detection | Required action |
|----------|-----------|-----------------|
| Bad URL or page name | Not http or https, or not one file name | Message. Direct `download` exits non-zero. Do not claim a save |
| Page was not saved | `serve` name has no `index.html` | Message. Do not bind. Do not delete a folder |
| Port rejected | Not a number from 1 to 65535, or the port is taken | Message. Do not claim the server started |
| Invalid menu number | Not on the current list | Ask again. Do not proceed |
| Download failed | `PageDownloadError` | Report the sentence. Do not claim success. Keep files already saved |
| ChronicleLogger missing | import fails inside `def main` | Console next step from `requirement-python-cli-logging`. Return non-zero. That line cannot use `log_message` |
| Empty argv with no terminal | stdout is not a terminal | Help text. Return 0. This is not a failure |

### 2.3 Cleanup on failure

5. A failed download **MUST NOT** delete files outside that page folder.
6. A non-empty `index.html` that already existed **MUST** stay. That page URL is not fetched again.
7. A failed serve **MUST NOT** delete the saved page.
8. An unfinished temp is not the result. Discard it, and log that discard before the unlink when the logger exists (`requirement-python-cli-logging`).

### 2.4 Logging and the console

9. Once `def main` has constructed ChronicleLogger, durable status **MUST** go through that logger. The logger is required (`requirement-python-packaging`).
10. **MUST** still show the user-visible failure reason. On the text screen it sits in the menu region. Off the text screen it is a console line. A quiet logger mirror is not a substitute for that sentence.
11. **MUST NOT** log secrets. This product has none.
12. **MUST NOT** hang on `input()` when stdout is not a terminal.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Download errors** | `PageDownloadError` in `page_download.py`. The sentence is the failure |
| **Serve errors** | `PageServeError` in `page_serve.py`. A missing page or a bad port does not bind |
| **Open errors** | `PageOpenError` when the tool or the file is missing. The menu hides a missing tool |
| **Invalid menu number** | Stay on the board |
| **ChronicleLogger** | Required. Missing import is a console sentence and a non-zero return, before any `log_message` |
| **No terminal** | Empty argv prints help and returns 0. `download` and `serve` still run |
| **Running tree** | `Cli.report_error` prints the sentence and logs it when the logger exists |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Fail closed on a bad URL, a missing page, and a failed download.
- **Principle 11 – Temps**: Cleanup without destroying sources.
- **Principle 12 – Traceability**: The operator still sees the failure when the log mirror is quiet.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, failure sentences are for the normal user who started `html-downloader`. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to report an error or to clean a temp. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** An invalid selection does not download or serve.
- **Intentional:** The category table is the failure contract.
- **Anti-fragile:** Cleanup is best-effort and does not hide the first error.
- **Over-protect:** An existing saved page stays in place.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Swallow a download or serve error without a user-visible failure.
2. Delete a saved page on error.
3. Claim success after a failed download or a failed serve.
4. Replace clear messages with a silent pass.
5. Log credentials or tokens.
6. Call the logger optional, or send the missing-library line through `log_message`.
7. Hang on a prompt when there is no terminal.

**Violating this rule is a critical safety regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | An invalid menu number does not download or serve |
| AC-2 | A bad URL or a missing `--name` surfaces a message and a non-zero exit |
| AC-3 | An existing saved page remains after a failed resume |
| AC-4 | A failed serve does not delete the page folder |
| AC-5 | A missing saved page does not bind |
| AC-6 | A failed download does not present itself as success |
| AC-7 | Missing ChronicleLogger is a console next step and a non-zero return |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-video-ffmpeg-pipeline` | Retired |
| `requirement-python-cli-interface` | Verb exits |
| `requirement-python-tui` | Where the sentence sits on the screen |
| `requirement-python-cli-logging` | Durable status after the construct |
| `requirement-runtime-prerequisites` | The logger floor. No encoder |
| `requirement-domain-videojoin` | Session outcomes |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ERR-01** | `tests/test_download.py` | have | A bad URL and `hello` do not save a page |
| **TP-ERR-02** | `tests/test_serve.py` | have | A missing page and a bad port do not serve |
| **TP-LOG-01** | `tests/test_logging.py` | todo | Peer: missing library is a console line, not `log_message` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial error-handling law for HtmlDownloader |
| 2026-08-09 | Active 1.1.0 | Fail-closed fallback and unique temp cleanup notes |
| 2026-10-04 | Active 1.2.0 | ChronicleLogger is required for durable status. Console sentences stay. Missing library is a console line. Empty argv off a terminal is help, return 0 |
| 2026-10-16 | Active 1.3.0 | Failures are download and serve. No encoder errors. An existing page stays |

---

**Last Updated**: 2026-10-16
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
