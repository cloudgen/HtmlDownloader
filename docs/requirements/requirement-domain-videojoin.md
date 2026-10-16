**file**: docs/requirements/requirement-domain-videojoin.md
**Status**: Active (Version 1.2.0)
**Area**: domain
**Key**: `requirement-domain-videojoin`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the domain surface Single Source of Truth for VideoJoin: the welcome message, and the two ways a person sees it.

Typed verbs and empty argv are owned by `requirement-python-cli-interface`. The screen that shows menu row 1 is owned by `requirement-python-tui`. Class `Tui` owns the welcome sentence (`requirement-python-oop`). The about page is `requirement-python-about`.

This file remains the sole Active `requirement-domain-*`. Headings and pictures in the root user document are `requirement-python-readme`.

### 1.1 Human-facing

**In one sentence:** VideoJoin shows one welcome line, either printed by `hello` or shown from menu row 1.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who wants the welcome line | `video-join hello` |
| The other role | The text menu, row 1 | `requirement-python-tui` |
| Not this file | The rounded menu frame, pip install, and the log folder | TUI, packaging, and logging requirements |

| Includes | Excludes |
|----------|----------|
| One welcome line, `Welcome to VideoJoin <version>.` | Joining media, an encoder, a scan of the working directory |
| Typed `hello`, which prints that line and does not draw the menu | A front-board row that lists files |
| Menu row 1 **hello**, which shows that same line on the menu | `join` and `list-videos` as verbs |
| Help and about as real pages | A downloaded-script installer advertised on the about page |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-join hello` | The terminal | The welcome line. No menu |
| Menu row 1 | The text menu result page | The same welcome line |
| `video-join about` | About page | Name, version, what the product does, how to start it |
| `video-join help` | Help page | The same capabilities, including what this product does not do |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Print the welcome | One line on the terminal. The menu does not open. The process returns 0. | `video-join hello` |
| Show the welcome | On a terminal, open the menu and choose **1**. The result page shows the same line. | `video-join`, then `1` |
| Read about | You see VideoJoin, the package version, the welcome summary, and the two ways to start the program. | `video-join about` |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — The welcome line

The welcome sentence is `Welcome to VideoJoin <version>.` `<version>` is `__version__`, the same string as `pyproject.toml`. `Tui.hello_text` is the only place that builds it.

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| D-01 | Print the welcome | typed verb `hello` | The sentence on standard output. Return 0. The menu does not open | this file + CLI |
| D-02 | Show the welcome | menu row 1, kind `hello` | The same sentence on the result page | this file + TUI |

**Routing:** `video-join hello` **MUST** run D-01 and **MUST NOT** run D-02. Front-board row 1 **MUST** run D-02. Bare `video-join` on a terminal opens the front board and **MUST NOT** run D-01 or D-02.

**Non-goals:** joining media, calling FFmpeg or any other encoder, listing files in the working directory, `join`, `list-videos`, a folder prompt, a shell installer, file-operand flags.

Complete invocation sample this pillar owns:

```text
video-join hello
```

`video-join hello` prints the welcome line and returns 0, with or without a terminal. It does not draw the menu.

### 2.2 Pillar B — What this product does not do

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Welcome line | One sentence, shared by the verb and row 1 | this file |
| No media join | **MUST NOT** concatenate, re-encode, or publish a media file | this file |
| No file list | **MUST NOT** scan the working directory to list files for the person | this file |
| No encoder | **MUST NOT** require or invoke `ffmpeg` | `requirement-video-ffmpeg-pipeline` is Retired |

### 2.3 Pillar C — Help

`video-join help` and `python -m VideoJoin --help` **MUST** list the welcome line and **MUST NOT** list `join`, `list-videos`, or an encoder. Help is a typed verb. It is not a numbered menu row.

The help page **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Welcome | `hello` prints one line and does not draw the menu |
| Menu | On a terminal, `video-join` with no words shows the front board. Row 1 shows the welcome line |
| Absence | This program does not join media or list files in the folder |

### 2.4 Pillar D — About

The domain sentence on the about page is `Show a welcome message`. The page, the host check, and the star box are `requirement-python-about`.

| Field | Content |
|-------|---------|
| Product name | VideoJoin |
| Version | `__version__`, the same string as `pyproject.toml` (current `1.0.5`) |
| Domain summary | Show a welcome message |

The page **MUST** use that domain sentence. The runtime-tools line **MUST** be `none`. It **MUST NOT** name FFmpeg.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `VideoJoin` |
| **Console script** | `video-join` |
| **Welcome sentence** | `Tui.hello_text` in `src/VideoJoin/tui.py` |
| **Menu row** | Front row 1, kind `hello`, short `hello` |
| **VERSION** | `1.0.5` (`__init__.py` and `pyproject.toml`) |
| **Absent** | `src/VideoJoin/join.py`, verbs `join` and `list-videos`, FFmpeg |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **Screen** | `requirement-python-tui` |
| **User docs** | Root `README.md` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: The welcome line is explicit, and empty argv does not print it.
- **Principle 5 – SSOT**: One Active domain file. The sentence is built in one method.
- **Principle 1 – Caution**: Join, file listing, and an encoder stay non-goals.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, `hello` and the menu run as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to print the welcome line. Do not pipe a downloaded script into a shell.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not scan the folder in order to say hello.
- **Intentional:** One sentence, two surfaces.
- **Anti-fragile:** README, help, about, the terminal, and row 1 name the same line.
- **Over-protect:** Keep the sole Active domain file.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Add `join`, `list-videos`, FFmpeg, or a working-directory file listing back without an explicit user order and a new revision of this file.
2. Add a shell installer or root elevation as silent domain behavior.
3. Create a second Active `requirement-domain-*` without superseding this one.
4. Give the terminal and menu row 1 two different welcome sentences.
5. Make empty argv print the welcome line or start a media job.

**Violating this rule is a critical domain regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `video-join hello` prints `Welcome to VideoJoin <version>.` and returns 0 |
| AC-2 | That verb does not draw the menu |
| AC-3 | Menu row 1 is `hello` and shows the same line |
| AC-4 | `join` and `list-videos` are unknown verbs |
| AC-5 | Help and about do not describe a join or an encoder |
| AC-6 | This file stays the sole Active domain SSOT |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-video-ffmpeg-pipeline` | Retired. Do not restore |
| `requirement-python-cli-interface` | Typed `hello` |
| `requirement-python-about` | About page. This file keeps the domain sentence |
| `requirement-python-tui` | Row 1 shows the welcome line |
| `requirement-python-oop` | `Tui.hello_text` |
| `requirement-runtime-prerequisites` | ChronicleLogger. No encoder |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-readme` | Headings and pictures in the user document |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-HELLO-01** | `tests/test_hello.py` | have | Typed `hello` prints the welcome line and does not open the menu |
| **TP-HELLO-02** | `tests/test_hello.py` | have | `join` and `list-videos` are unknown. Help does not name an encoder |
| **TP-HELLO-03** | `tests/test_hello.py` | have | Row 1 shows the same welcome line on the result page |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for VideoJoin interactive two-file join |
| 2026-10-04 | Active 1.1.2 | Pillar D kept the join domain sentence. Product version **1.0.5** |
| 2026-10-05 | Active 1.2.0 | The domain is the welcome line. Join, file listing, and FFmpeg are non-goals |

---

**Last Updated**: 2026-10-05
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
