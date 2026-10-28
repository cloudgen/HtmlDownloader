**file**: docs/requirements/requirement-python-cli-debug.md
**Status**: Active (Version 1.0.2)
**Area**: python
**Key**: `requirement-python-cli-debug`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns debug status for HtmlDownloader and the catalog of values printed when that status is on. `requirement-python-cli-logging` still owns the ChronicleLogger construct and still shows how to ask that object for debug mode. This file does not construct the logger and does not add a `--debug` flag.

The running `src/HtmlDownloader/cli.py` already prints the catalog below inside `if logger.isDebug()`, before the argument parser. The allowed end state is this file.

### 1.1 Human-facing

**In one sentence:** Set `DEBUG` before `html-downloader` starts, and a run that does not open the text screen prints four identity lines, including `debug mode`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person running `html-downloader` | `DEBUG=1 html-downloader version` shows who this build is before the version line |
| The other role | ChronicleLogger, asked only through `isDebug()` and `log_message` | The library remembers the first answer and writes the daily file |
| Not this file | How the logger is constructed, and how the menu is drawn | `requirement-python-cli-logging`, `requirement-python-tui` |

| Includes | Excludes |
|----------|----------|
| The environment switch, the four printed values, which runs show them on the console, and the ban on `--debug` | A second logger, `logging.basicConfig`, reading `DEBUG` again after construct, a version integer triple |
| The daily file still receiving those lines when the text screen is open | Painting those lines over the text screen |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/HtmlDownloader/cli.py` | `def main`, inside `if logger.isDebug()` | The four `log_message` calls |
| `html-downloader` | console script | Shows the catalog on a non-screen run when debug status is on |
| Resolved `logDir()` | daily `.log` file | The same lines after the process exits, including a text-screen run |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Turn debug status on | `DEBUG` or `debug` is already `1`, `true`, or `show` before `ChronicleLogger(...)`. Product code asks `logger.isDebug()` and does not read the variable again. | `DEBUG=1 html-downloader version` |
| Read the four lines | On `version`, `help`, `download`, `serve`, and the pip verbs, the console shows the catalog. Empty argv on a terminal, and `about` on a terminal, keep the console quiet. The daily file still has the lines. | `DEBUG=1 html-downloader version` |
| Leave debug status off | Unset `DEBUG` and `debug`. Those four lines stay off the console and off the daily file. | `html-downloader version` |

## 2. Core Rules (Mandatory)

**Value owner.** The table in rule 4 is the only catalog of messages printed for debug status. `requirement-python-cli-logging` calls `log_message` for that catalog. It does not keep a second list.

### 2.0 When this law applies

1. **MUST** treat debug status as an environment fact already set before `ChronicleLogger(...)`.
2. **MUST NOT** add `--debug`. The parser stays on `requirement-python-cli-interface`.
3. **MUST NOT** use this file as the law for editing the ChronicleLogger library.

### 2.1 Switch

4. **MUST** ask `logger.isDebug()` for whether debug status is on. **MUST NOT** read `DEBUG` or `debug` again in product code. `isDebug()` remembers the first answer on that instance.
5. `DEBUG` or `debug` **MUST** already be `1`, `true`, or `show` (any letter case) **before** `ChronicleLogger(...)`. Any other value, or an unset variable, means debug status is off.
6. The identity block **MUST** run only inside `if logger.isDebug():`, and `main` **MUST** run that block before the argument parser. Each call is `log_message` with `component="main"`. When `isDebug()` is false, the four messages **MUST NOT** be displayed. A line with `level="DEBUG"` **MUST** sit inside that same `if`.

### 2.2 Values that must be printed

7. When debug status is on, `main` **MUST** display these four messages, in this order, and no others as product debug identity. **MUST NOT** type the library version by hand. **MUST NOT** add `MAJOR` / `MINOR` / `PATCH` integers. The package version is the single string `__version__`.

| # | Message | Level | component |
|---|---------|-------|-----------|
| 1 | `{resolved logName()} v{package __version__} ({path of this file})` | INFO (omitted `level`) | `main` |
| 2 | `Using {ChronicleLogger.class_version()}` | INFO (omitted `level`) | `main` |
| 3 | `Base {baseDir()}` | `DEBUG` | `main` |
| 4 | `debug mode` | INFO (omitted `level`) | `main` |

8. `logName()`, `baseDir()`, and `logDir()` are read before the first of these calls. The constructor string is not message 1. How to construct the logger and how to call `log_message` stay on `requirement-python-cli-logging`.
9. The library may prepend one extra file header, `@logger Using {logfile path}`, when debug status is on and the daily file rotates. That header is library behavior. It is not a fifth product message and product code **MUST NOT** print it by hand.
10. INFO lines that are not in the table (`instantiated`, temp write, publish, discard, and any later thread operation) **MUST NOT** sit inside `if logger.isDebug():`. Those lines stay on `requirement-python-cli-logging`.

### 2.3 Console mirror

11. When this run will open the text screen, and that fact is known before construct, `main` **MUST** pass `is_quiet=True` into `ChronicleLogger(...)`. The runs that open the text screen are: empty argv on a terminal, and `about` on a terminal. `download`, `serve`, `help`, `version`, and the pip verbs do not open it. A small argv peek may decide `is_quiet` before the constructor. `ArgumentParser.parse_args` runs after the constructor and after the debug block.
12. A run that does not open the text screen **MUST** leave `is_quiet` false, so the operator sees the four messages on the console when debug status is on. The text screen **MUST** keep that mirror off the console. The same lines still go to the daily file. `quiet(True)` after the constructor returns **MUST NOT** be the only quiet for a text-screen run. This product does not claim `--json` and does not claim `--verbose`.
13. The `version` verb prints `{product name} {__version__}` (`HtmlDownloader 1.1.1` today). That sentence is not message 1. Message 1 uses the resolved `logName()` and a `v` before the version.

### 2.4 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Switch** | Environment `DEBUG` or `debug`, already `1`, `true`, or `show`, before `ChronicleLogger(...)`. No `--debug` flag |
| **Ask** | `logger.isDebug()` only. Product code does not read the environment again |
| **Site** | `def main` in `src/HtmlDownloader/cli.py`, after `logName()` / `baseDir()` / `logDir()` read-back, before `Cli(logger)` and before the parser |
| **logname passed in** | `HtmlDownloader` |
| **Resolved name** | `html-downloader` from `logName()`. Message 1 starts `html-downloader v` |
| **Package version** | `__version__` in `src/HtmlDownloader/__init__.py`, currently `1.1.1`, same string as `pyproject.toml`. Not typed a second time. Not a `MAJOR` / `MINOR` / `PATCH` triple |
| **Message 1 path** | Path of `src/HtmlDownloader/cli.py` (`__file__` at the call) |
| **Message 2** | `Using` plus `ChronicleLogger.class_version()`. The library string shape is `{CLASSNAME} v{MAJOR}.{MINOR}.{PATCH}`. Product code does not type that version |
| **Message 3** | `Base` plus `baseDir()`, `level="DEBUG"`, `component="main"` |
| **Message 4** | The message is exactly `debug mode`. Omitted level means INFO |
| **Console** | `is_quiet=True` for empty argv on a terminal and for `about` on a terminal. `version`, `help`, `download`, `serve`, and the pip verbs leave it false |
| **Sample** | `DEBUG=1 html-downloader version` |
| **Proof** | `TP-DBG-01`, `TP-DBG-02`, `TP-DBG-03` in `tests/test_debug.py`. `TP-LOG-02` is not a second primary |

### 2.5 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT of output**: one catalog names the four debug messages.
- **Principle 1 – Caution**: debug status cannot be turned on by a flag the help text does not own, and the text screen does not paint these lines.
- **Principle 2 – Intentional**: each message, its level, and `component="main"` are named.
- **Principle 12 – Traceability**: the daily file still receives the lines while the text screen is quiet.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, setting `DEBUG` is an environment assignment for this login. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to turn debug status on. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Ask `isDebug()`. Do not re-read `DEBUG`. Do not mirror the catalog onto the text screen.
- **Intentional:** Four messages, one order, one component.
- **Anti-fragile:** The version string is `__version__`. A library rotation header is not a fifth product line.
- **Over-protect:** No `--debug` flag and no second catalog on the logging requirement.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

1. Add `--debug`, or read `DEBUG` again after `ChronicleLogger(...)`.
2. Print the four messages outside `if logger.isDebug():`, or drop one of them.
3. Type the library version by hand, or add `MAJOR` / `MINOR` / `PATCH` integers for this product.
4. Copy this catalog into `requirement-python-cli-logging` as a second owner. That file shows the `log_message` calls and points here.
5. Put `instantiated`, temp, publish, or discard lines inside `if logger.isDebug():`.
6. Treat `quiet(True)` after construct as the only quiet for a text-screen run.
7. Mark `TP-DBG-*` have before `tests/test_debug.py` asserts them.
8. Claim `--verbose` or `--json` on this product in order to show these lines.

**Violating this rule is a critical debug-status regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Debug status is `DEBUG` or `debug` already set to `1`, `true`, or `show` before construct. There is no `--debug` flag |
| AC-2 | Product code asks `logger.isDebug()` and does not read the environment again |
| AC-3 | The four messages in rule 7 appear, in order, only inside `if logger.isDebug():`, each with `component="main"` |
| AC-4 | A non-screen run shows them on the console. A text-screen run keeps them off the console and still writes the daily file |
| AC-5 | Unset `DEBUG` and `debug` display none of the four messages |
| AC-6 | `requirement-python-cli-logging` names this key and still shows the `ChronicleLogger` calls for this mode |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-logging` | Construct, `isDebug()`, and the `log_message` calls. This file owns the values |
| `requirement-python-cli-interface` | No `--debug` flag. Parser runs after this block |
| `requirement-python-tui` | Text screen that must stay quiet |
| `requirement-python-oop` | `main` passes the logger into `Cli` after this block |
| `requirement-python-packaging` | `__version__` string |
| `requirement-class-software-dev` | Residual pointer |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-DBG-01** | `tests/test_debug.py` | have | `DEBUG=1` and `main(["version"], basedir, logdir)` shows the four values on stdout |
| **TP-DBG-02** | `tests/test_debug.py` | have | `DEBUG` and `debug` unset. Those strings are absent |
| **TP-DBG-03** | `tests/test_debug.py` | have | A text-screen run keeps the lines off the console. The daily file still has them |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Project requirements.** Product law is the finished must/should rules for this product. They are complete for this product. They are not blank forms, not agent procedures, and not a glossary.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form in a stationery shop is not.

**Chronicle logger.** The one process status logger. `def main` writes `ChronicleLogger(...)` in that function before any product object. Each class stores that same object. It is not `print`, not a second logger, and not a thread pool. The log folder is the one `logDir()` returns. Product code does not copy that ladder and does not type the path. Debug status asks `isDebug()` on that object. The four messages in this file are what that question is allowed to print.

**Daily-life example:** You buy a kettle and write “kettle arrived” in the household book. Later you write “moved kettle, box to shelf.” Guests in the dining room do not hear that line. The book still has it. A separate card on the fridge lists the four lines you add only when you are checking the house.

**Debug mode.** The short status that those four lines are allowed. It is an environment fact set before the logger exists. It is not a command flag.

**Daily-life example:** You leave a note on the door, “checking the house,” before you walk in. You do not invent a new doorbell button for that note.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.2 | The version sentence uses the current package string **1.1.1**. The four values are unchanged |
| 2026-10-28 | Active 1.0.1 | `TP-DBG-01`, `TP-DBG-02`, and `TP-DBG-03` are have. `python3 -m unittest tests.test_debug` passed. Product version stays **1.1.0** |
| 2026-10-28 | Active 1.0.0 | Debug status and the four printed values leave `requirement-python-cli-logging`. That file still shows the ChronicleLogger calls. Product version stays **1.1.0** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
