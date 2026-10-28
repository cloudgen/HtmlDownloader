**file**: docs/requirements/requirement-python-coding-style.md
**Status**: Active (Version 1.2.4)
**Area**: python
**Key**: `requirement-python-coding-style`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define Python coding style and defensive file I/O conventions for HtmlDownloader: how agents and maintainers write Python so path, temp, and publish behavior stays safe across mounts, including USB, without duplicating the domain tables. This program does not call an encoder.

Publish with `shutil.move` stays here. This program does not call an encoder. The class map is owned by `requirement-python-oop`. The logger construct is owned by `requirement-python-cli-logging`.

Without this requirement, portable learned lessons arrive raw.

### 1.1 Human-facing

**In one sentence:** A finished file is moved into place with `shutil.move`, and the classes that do the work live in the files the class map names.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer changing a download or the menu | Keep the publish call as `shutil.move`. Put new behavior on the class that owns that job |
| The other role | The class map and the status logger | `requirement-python-oop`, `requirement-python-cli-logging` |
| Not this file | The menu picture and the page folder | TUI and `requirement-html-page-download` |

| Includes | Excludes |
|----------|----------|
| `shutil.move` as the publish call. Temps beside the destination when that folder is writable | Bare `os.rename` as the only publish when the mounts differ |
| The class map as the allowed end state | Treating the procedural pile in `cli.py` as the allowed end state |
| Package import that does not construct ChronicleLogger | Re-exporting ChronicleLogger, or a factory whose job is to build a mapped class |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/HtmlDownloader/cli.py` | Running session today. `Cli` and `def main` in the end state | Entry |
| Class files named by `requirement-python-oop` | One class each, when an implement order lands them | The jobs that `cli.py` still holds |
| Publish helper | `shutil.move` | Move the finished temp to the output name |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Publish the finished file | Call `shutil.move`. Log that publish before the call, once the logger exists. | The saved page name |
| Add a behavior | Put it on the class in the map. Do not add a module-level function beside that class. | Edit that class file |
| Import HtmlDownloader | The import succeeds even when you only need `__version__`. It does not construct the logger. | `python -c "import HtmlDownloader"` |

## 2. Core Rules (Mandatory)

### 2.1 General style (this product)

1. **MUST** keep the installable package under `src/HtmlDownloader/` with the module entry (`__main__` / console script → `cli.main`).
2. **MUST** cite only live `docs/requirements/requirement-*.md` keys in product-source law comments.
3. **SHOULD** use a clear General Purpose docstring on each public method.
4. **MUST** fail closed with a user-visible message on expected errors (a bad URL, a missing saved page, a failed download).
5. Importing the HtmlDownloader package **MUST NOT** construct ChronicleLogger. The construct stays inside `def main` (`requirement-python-cli-logging`). **MUST NOT** re-export `ChronicleLogger`.
6. The class map in `requirement-python-oop` is the layout on disk. **MUST NOT** collapse those classes back into one procedural module. **MUST NOT** order a StateLogic + `Attr` rewrite. This file does not move the code.
6a. The site that needs an object **MUST** write `ClassName(...)`. A function or a method whose job is to instantiate a class in that map is forbidden.

### 2.2 Temporary files

7. When the final destination path is known, **MUST** prefer creating intermediate files on the same filesystem or mount as that destination (a writable parent of the final path).
8. **MUST NOT** assume system `TMPDIR` or `/tmp` is the same mount as the saved page folder (USB, network, secondary disks).
9. **MUST** clean intermediate temps on success and on failure (best-effort).
10. **MUST NOT** use a fixed predictable cwd name as the sole temp path when a unique temp can be created.

### 2.3 Publishing / moving completed files (sacred)

11. To move or publish a completed intermediate file from a temporary path to its final path, **MUST** use `shutil.move` (or a thin wrapper whose only move implementation is `shutil.move`).
12. **MUST NOT** use bare `os.replace`, `os.rename`, `pathlib.Path.replace`, or `pathlib.Path.rename` alone as the sole publish mechanism when source and destination may be on different mounts.
13. **MAY** still use same-filesystem rename semantics inside what `shutil.move` performs. Do not reimplement a fragile bare rename as product publish.
14. `shutil.copy2`, `copy`, and `copyfile` copy only. If one is used, **MUST** define whether the source is kept or deleted. A copy is not a complete move by itself.
15. When an intermediate file is used, publish **MUST** go through `shutil.move` (or the thin wrapper).

Log the temp write, the publish, and the discard of an unfinished temp before the operation (`requirement-python-cli-logging`). Those lines do not replace rules 7–15.

### 2.4 Corresponding commands / APIs (reference)

| Intent | Prefer | Avoid as sole cross-mount publish |
|--------|--------|-----------------------------------|
| Move or publish a file | `shutil.move(src, dst)` | bare `os.replace`, `os.rename` |
| pathlib-oriented move | `Path` args + `shutil.move` | bare `Path.replace`, `Path.rename` across mounts |
| Copy and keep the source | `shutil.copy2` | treating a copy as a move without an unlink policy |
| Same-filesystem atomic finish | OK via the `shutil.move` rename path | assuming all mounts are identical |

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Package** | `HtmlDownloader` |
| **Running modules** | The modules named by `requirement-python-project-structure` |
| **Class modules** | Named by `requirement-python-oop`. They are on disk |
| **Page classes** | `PageDownload`, `PageServe`, and `PageOpen` |
| **Publish helper** | `shutil.move` |
| **Encoder file** | Retired. This file still owns `shutil.move` |
| **Gate checklist (cite ID)** | `CL-PYTHON-SHUTIL-MOVE-PUBLISH` — run when auditing promote and staging publish paths |
| **Architecture** | One class per file. StateLogic + `Attr` stays unordered |
| **Logger** | Package import does not construct ChronicleLogger |
| **Version** | `1.1.1` |
| **User docs** | Root `README.md` Features must not claim a Cython-required runtime or an encoder |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Mount mismatches are designed for.
- **Principle 3 – Anti-fragile**: A USB destination and a system disk both publish through `shutil.move`.
- **Principle 5 – SSOT**: This file owns move and temp rules. The class map lives in its own requirement.
- **Principle 11 – Temps**: Staging and cleanup are explicit.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, temps and the published file stay in the normal user’s folders. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to publish a file or to construct a class. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not assume one filesystem.
- **Intentional:** `shutil.move` is the named publish API. The class map is the named end state.
- **Anti-fragile:** Temps on the destination mount avoid a full-file copy when the mount allows it.
- **Over-protect:** Do not bring back a bare cross-device rename as the only publish.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Replace `shutil.move` publish with bare `os.replace` or `os.rename` for simplicity.
2. Stage every large intermediate only under the system temp when the final destination is known on another mount.
3. Cite a template or a skill from product source as behavioral authority.
4. Treat the procedural session in `cli.py` as the allowed end state. Do not start the class split inside a style-only edit. Do not order a StateLogic rewrite.
5. Store secrets in style docs or in code.
6. Add an encoder, or treat a fixed cwd name as the page publish path. The page folder stays on `requirement-html-page-download`.
7. Construct ChronicleLogger at import time, or add a factory whose job is to instantiate a mapped class.

**Violating this rule is a critical regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Publish of intermediates uses `shutil.move` (or a thin wrapper) |
| AC-2 | A bare cross-mount rename is forbidden as the sole publish |
| AC-3 | Same-filesystem staging is preferred when the destination is known |
| AC-4 | The page folder stays on `requirement-html-page-download`. This file owns `shutil.move` |
| AC-5 | Registered in the index |
| AC-6 | Package import does not construct ChronicleLogger and does not re-export it |
| AC-7 | A promote-path audit uses `CL-PYTHON-SHUTIL-MOVE-PUBLISH` when ship publish code changes |
| AC-8 | The allowed end state points at `requirement-python-oop`. StateLogic stays unordered |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-oop` | Allowed class map |
| `requirement-python-cli-logging` | Log temp, publish, and discard. Construct stays in `main` |
| `requirement-python-project-structure` | Running layout versus the map |
| `requirement-python-error-handling` | Failure messages |
| `requirement-python-cli-interface` | Entry |
| `requirement-python-packaging` | Export honesty |
| `requirement-html-page-download` | Page folder. This file does not own it |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-FS-01** | `tests/test_fs_publish.py` | todo | Publish uses `shutil.move` |
| **TP-FS-02** | `tests/test_fs_publish.py` | todo | Staging prefers the destination parent when it is writable |
| **TP-PKG-01** | `tests/test_packaging.py` | todo | `import HtmlDownloader` succeeds and does not construct ChronicleLogger |
| **TP-OOP-01** | `tests/test_oop.py` | todo | Peer: class map. Not landed |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Project requirements.** Product law is the finished must/should rules for this product. They are complete for this product. They are not blank forms, not agent procedures, and not a glossary.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form in a stationery shop is not.

**Coding-style requirement.** The specialize-in home for portable learned lessons about how this program is written. Without that file, those lessons arrive raw and get treated as this product’s law. This file is where a lesson is adopted, pointed at a peer requirement, or refused.

**Daily-life example:** A newsroom keeps one style sheet (“we write dates this way”). That adopted sheet is the coding-style requirement. The industry handbook on the shelf is not house law until the sheet says so.

**Avoid-factory-create-class.** An object is created by writing `ClassName(...)` at the site that needs that object. A factory is a function or a method whose only job is to instantiate a class and hand it back. The class can be created without that factory.

**Daily-life example:** You want a kettle. You take a kettle off the shelf. You do not fill out a slip that a back-room clerk uses to fetch the same kettle and pass it through a window. That slip is a factory.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Coding style, `shutil.move`, and multi-mount file I/O for HtmlDownloader |
| 2026-10-04 | Active 1.1.0 | Procedural `cli.py` is the running tree, not the allowed end state. The end state is `requirement-python-oop`. StateLogic stays unordered. Rules 7–15 are unchanged |
| 2026-10-04 | Active 1.1.1 | Current version string is **1.0.5** |
| 2026-10-16 | Active 1.2.0 | Version **1.0.0**. No encoder in the style rules. The class map is on disk |
| 2026-10-28 | Active 1.2.1 | The page folder is the publish subject. No concat pipeline owner |
| 2026-10-28 | Active 1.2.2 | Product version **1.1.0** |
| 2026-10-28 | Active 1.2.3 | Purpose states that without this requirement, portable learned lessons arrive raw. Terminologies added |
| 2026-10-28 | Active 1.2.4 | Product version **1.1.1**. Publish still uses `shutil.move`. The temp, publish, and discard lines are on `requirement-python-cli-logging` |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
