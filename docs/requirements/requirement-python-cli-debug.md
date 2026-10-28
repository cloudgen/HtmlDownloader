**file**: docs/requirements/requirement-python-cli-debug.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-cli-debug`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file names the four lines HtmlCrawler prints when debug mode is on. It does not construct ChronicleLogger. `requirement-python-cli-logging` still writes `ChronicleLogger(...)` inside `def main`, still calls `logger.isDebug()` and `log_message` for this list, and still shows that call. This file is not a new routed verb and not a `--debug` flag.

The running `src/HtmlDownloader/cli.py` does not yet print these four lines. The allowed end state is this file. This pass does not change `src/`.

### 1.1 Human-facing

**In one sentence:** With `DEBUG` already on, a run that does not open the text menu prints four status lines, and with `DEBUG` off those four lines stay off.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person running `html-crawler` | You set `DEBUG` in the same shell, then run a command |
| The other role | The logger’s debug gate | `logger.isDebug()` decides once, before the argument parser |
| Not this file | How the logger is constructed, and how the menu is drawn | `requirement-python-cli-logging`, `requirement-python-tui` |

| Includes | Excludes |
|----------|----------|
| The four messages, the environment switch, and the rule that those lines stay inside `isDebug()` | Constructing ChronicleLogger, the `instantiated` line, temp / publish / discard lines, thread lines, and the about-page host checks |
| `debug mode` on the console when the text screen is not open | A `--debug` flag, a fifth identity line, and painting those lines over the text menu |

| Surface | What you open | What for |
|---------|---------------|----------|
| `html-crawler` | a non-screen command | Shows the four lines when debug mode is on |
| Daily log file | `logDir()` | Still receives the four lines when the text screen hides the console mirror |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Ask for the debug lines | Before the process starts, `DEBUG` or `debug` is already `1`, `true`, or `show`. On `version`, which does not open the text screen, the four lines below appear. The package version on the first line is the same `__version__` the `version` verb prints. | `DEBUG=1 html-crawler version` |
| Leave debug off | Those four lines are not displayed. Ordinary status lines still follow the logging requirement. | `html-crawler version` |

## 2. Core Rules (Mandatory)

**Value list.** The four messages below are the only startup identity lines. Logging calls them. This file owns the wording.

### 2.0 When this law applies

1. **MUST** print the four lines in §2.1 when `logger.isDebug()` is true, and **MUST NOT** print them when it is false.
2. **MUST NOT** use this file as the law for constructing ChronicleLogger, choosing `is_quiet`, or installing the library. Those stay on `requirement-python-cli-logging`, `requirement-python-packaging`, and `requirement-runtime-prerequisites`.
3. **MUST NOT** add a routed verb for debug mode. `requirement-python-cli-interface` still rejects `--debug`.

### 2.1 The four lines

4. `main` **MUST** run the block only inside `if logger.isDebug():`, after `logName()`, `baseDir()`, and `logDir()` have been read, and before the argument parser. The block is exactly four `log_message` calls. Each uses `component="main"`. **MUST NOT** add a fifth identity line.
5. The four messages, in this order:

| # | Message | Level | What the value is |
|---|---------|-------|-------------------|
| 1 | `"{0} v{1} ({2})".format(appname, __version__, __file__)` | omitted, so the library uses INFO | `appname` is `logger.logName()`. For this product that resolved name is `html-crawler`. `__version__` is the single package string. `__file__` is this file’s path |
| 2 | `"Using {0}".format(ChronicleLogger.class_version())` | omitted, so the library uses INFO | The library’s own version string. **MUST NOT** type that version by hand |
| 3 | `"Base {0}".format(resolved_base)` | `DEBUG` | `resolved_base` is `logger.baseDir()` |
| 4 | `debug mode` | omitted, so the library uses INFO | Those two words, exactly |

6. When `isDebug()` is false, those four lines **MUST NOT** be displayed on the console and **MUST NOT** be written as if debug mode were on.
7. A line with `level="DEBUG"` in this block **MUST** sit inside `if logger.isDebug():`. Row 3 is that line. Logging rule 15 is the same gate for any other `level="DEBUG"` line.

### 2.2 The switch

8. `DEBUG` or `debug` **MUST** already be `1`, `true`, or `show` (any letter case) **before** `ChronicleLogger(...)`. `isDebug()` remembers the first answer.
9. Product code **MUST** ask `logger.isDebug()` and **MUST NOT** read `DEBUG` again. **MUST NOT** add `--debug`. **MUST NOT** add `--verbose` in order to show these four lines. This product does not claim `--json`.
10. The human practice sample is `DEBUG=1 html-crawler version`. On this tree the live console script is still `html-downloader` until the ship-unit pass. The law command is `html-crawler`.

### 2.3 What is not a debug print

11. `CheckSystem.in_venv`, `in_pyenv`, and `in_conda` are not these four lines. They **MUST NOT** be printed on the about page and **MUST NOT** choose a location line. That rule stays on `requirement-python-cli-logging`. The proof is `TP-ABOUT-16`, primary on `requirement-python-about`.
12. The `instantiated` line, a temp / publish / discard line, and a thread line are INFO. They **MUST NOT** sit inside `if logger.isDebug():`. Those calls stay on `requirement-python-cli-logging`.
13. **MUST NOT** put secrets into these four messages. This product has none. A page path is not one of the four.

### 2.4 Where the operator sees them

14. On a run that does not open the text screen, logging leaves `is_quiet` false, so the operator sees `debug mode` and the other three lines on the console.
15. When the text screen is already known (empty argv on a terminal, or `about` on a terminal), logging passes `is_quiet=True`. Those runs **MUST NOT** mirror the four lines onto the console. The daily file still receives them.
16. `download`, `serve`, `help`, `version`, and the pip verbs do not open the text screen. They leave the mirror on, so debug mode shows on the console when `isDebug()` is true.

### 2.5 Version token on line 1

17. Line 1 and the `version` verb read the same package version: the single string `__version__` (`requirement-python-packaging`, restated on `requirement-python-cli-logging`). The current string is `1.0.0`. **MUST NOT** add `MAJOR` / `MINOR` / `PATCH` integers. **MUST NOT** keep a second version literal for display.

### 2.6 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Owner of the four messages** | This file |
| **Who calls ChronicleLogger** | `requirement-python-cli-logging`. `def main` in `src/HtmlDownloader/cli.py` writes `ChronicleLogger(...)`, then this block |
| **logname** | `HtmlCrawler`, which `logName()` resolves to `html-crawler` |
| **Line 1** | `html-crawler v1.0.1 (<this file>)` using `__version__` and `__file__` |
| **Line 2** | `Using` plus `ChronicleLogger.class_version()` |
| **Line 3** | `Base` plus `baseDir()`, `level="DEBUG"`, `component="main"` |
| **Line 4** | `debug mode` |
| **Switch** | `DEBUG` or `debug` already `1`, `true`, or `show`. No `--debug`. No `--verbose` |
| **Practice** | `DEBUG=1 html-crawler version` |
| **Live console this tree** | `html-downloader`, until the ship-unit pass |
| **Proof** | `TP-DEBUG-01` stays todo. The suite file `tests/test_logging.py` is not on disk. Do not mark the row have |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: the four messages have one owner, so a later edit cannot silently change what debug mode prints.
- **Principle 12 – Traceability**: debug mode shows the resolved name, the package version, this file, the library version, and the base folder.
- **Principle 1 – Caution**: the lines stay off unless the environment was set before the process started.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, debug mode is an environment value for this login. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to turn debug mode on or to install ChronicleLogger. Type 1 and Type 2 are unused on that class. The next step for a missing library stays the pip line on `requirement-python-cli-logging`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Four lines, and only when `isDebug()` is true.
- **Intentional:** Each message is written out. The library version comes from `class_version()`.
- **Anti-fragile:** The switch is the environment read once by the library. Product code does not read it again.
- **Over-protect:** No `--debug` flag and no fifth identity line.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

1. Add a fifth identity line, or drop one of the four messages.
2. Type `ChronicleLogger`’s version by hand in place of `class_version()`.
3. Add `--debug` or `--verbose` so these lines appear.
4. Print the four lines when `isDebug()` is false, or put them outside `if logger.isDebug():`.
5. Move the ChronicleLogger construct or the `isDebug()` / `log_message` call off `requirement-python-cli-logging`.
6. Print `in_venv`, `in_pyenv`, or `in_conda` as one of these four lines.
7. Put `instantiated`, a file operation, or a thread line inside this debug block.
8. Add `MAJOR` / `MINOR` / `PATCH` integers beside `__version__`.
9. Mark `TP-DEBUG-01` have while `tests/test_logging.py` does not assert these four messages.
10. Treat this file as a new routed verb.

**Violating this rule is a critical debug-output regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | With `DEBUG` already `1`, `true`, or `show`, a non-screen run prints the four messages in §2.1 and no fifth identity line |
| AC-2 | With `DEBUG` unset, those four lines are not displayed |
| AC-3 | Line 1 uses `logName()`, `__version__`, and `__file__`. Line 2 uses `ChronicleLogger.class_version()`. Line 3 uses `baseDir()` at level `DEBUG`. Line 4 is `debug mode` |
| AC-4 | Product code does not read `DEBUG` again and does not add `--debug` |
| AC-5 | A text-screen run does not mirror the four lines. The daily file still receives them. That mirror rule stays on `requirement-python-cli-logging` |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-logging` | Constructs ChronicleLogger and calls `isDebug()` / `log_message` for this list. Quiet mirror. INFO lines that must stay outside the gate |
| `requirement-python-cli-interface` | Rejects `--debug`. Parser runs after this block |
| `requirement-python-packaging` | `__version__` and the ChronicleLogger floor |
| `requirement-runtime-prerequisites` | Required library |
| `requirement-python-about` | `TP-ABOUT-16`. The three environment booleans are not these four lines |
| `requirement-python-tui` | Text screen that must not mirror these lines |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-DEBUG-01** | `tests/test_logging.py` | todo | Primary owner of the four messages. `DEBUG` already on shows them on a non-screen run. Unset shows none. The suite file is not on disk |
| **TP-LOG-02** | `tests/test_logging.py` | todo | Quiet mirror. Primary owner is `requirement-python-cli-logging`. A text-screen run does not mirror the four lines. The daily file still receives them |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Debug mode.** A gate inside the logger. `isDebug()` is that gate. The four identity lines, including the message `debug mode`, run only inside it. The `instantiated` line, a major file operation, and a thread line do not.

**Daily-life example:** You open the notebook’s extra page only when the kitchen light labeled DEBUG was already on before you started. That page has four lines: the appliance name with its edition and the recipe card’s place, which notebook brand you are holding, which cupboard is the base, and the words “debug mode.” When the light is off, that page stays blank. “Kettle arrived” is still written on the ordinary page.

**Chronicle logger.** The one process status logger. `def main` instantiates it by writing `ChronicleLogger(...)` before any product object. Debug mode asks that object `isDebug()` and then `log_message`. The log folder is the one `logDir()` returns. Product code does not copy that ladder and does not type the path. Not a second logger.

**Daily-life example:** You buy a kettle and write “kettle arrived” in the household book. The guests in the dining room do not hear that line. The book still has it. The shelf for the book is the one the notebook already chose. You ask where that shelf is. You do not nail a second address into the recipe.

**Project requirements.** Product law is the finished must/should rules for this product. They are not blank forms and not agent procedures.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form is not.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.0 | The four debug messages leave the logging requirement. Logging still calls ChronicleLogger for this list |
| 2026-10-28 | Active 1.0.1 | The sample identity line uses the current `__version__` string **1.0.1** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
