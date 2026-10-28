**file**: docs/requirements/requirement-class-software-dev.md
**Status**: Active (Version 1.2.7 – HtmlDownloader software-development class law + residual stack)
**Area**: class
**Key**: `requirement-class-software-dev`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare this workspace as a software-development project class and hold the residual collection of software-engineering stack facts not already owned by more specific Active peer requirements: primary language, toolchain policy, package and build tooling, and runtime OS family.

This file is class law plus the residual SSOT. It is not a second copy of the download domain, the CLI surface, the text menu, the logger construct, the class map, packaging tables, error-handling tables, or the agent-use skill. Those stay on peer requirements.

### 1.1 Human-facing

**In one sentence:** This file records that HtmlDownloader is Python, built with setuptools, and it points at the requirement that owns each other topic.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer checking which file owns a topic | The menu picture is the TUI requirement. The language row stays here |
| The other role | Peer requirements | CLI, TUI, logging, domain, packaging |
| Not this file | The page save, the frame glyphs, and the pip command strings | Their own requirements. This file only points |

| Includes | Excludes |
|----------|----------|
| Language, interpreter, package tool, and the residual pointer table | A second copy of the menu, the logger construct, or the class map |
| Shell install and root elevation marked absent | A pip lifecycle marked absent. That lifecycle is owned by the CLI and the TUI |
| A pointer to the who-list. No dest approver | A second copy of that who-list, or an Approver column |

| Surface | What you open | What for |
|---------|---------------|----------|
| This file | Residual table | Which requirement owns the topic |
| `pyproject.toml` | Package tool facts | The concrete manifest. Packaging owns the tables |
| `html-downloader` | The program | You run it as the normal user |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Find the menu law | Open the TUI requirement. Do not expect the picture in this file. | `html-downloader` |
| Find the logger law | Open the logging requirement. The floor is packaging and runtime. | `html-downloader version` |
| Install | Use pip. There is no shell installer. | `python -m pip install HtmlDownloader` |

## 2. Core Rules (Mandatory)

### 2.0 Project class membership

1. **MUST** treat this workspace as software-development (shippable software), not genesis-template and not server-maintenance.
2. **MUST** use basename `requirement-class-software-dev.md` as the sole Active class-law file for this class.
3. **MUST NOT** register an Active `requirement-class-server-maintenance.md` while the class is software-development.
4. **MUST** retain portable harness knowledge when present. Specialized product knowledge lives in this and peer `requirement-*.md` files.
5. **MUST** apply the software-development SSOT and gate posture when claimed (identity, package ship surface, and a pre-commit check when git is used — as applicable).
6. **MUST NOT** invent hollow product docs solely to look specialized.

### 2.1 Residual collection principle (SSOT hygiene)

7. **MUST** treat this file as the default home for software-stack facts not owned by another Active requirement.
8. **MUST NOT** duplicate full normative tables that already live in a more specific Active requirement. Prefer a one-line pointer to the peer requirement key.
9. When a new specialized requirement takes ownership of a topic previously only listed here, **MUST** update this file in the same change: shrink the residual entry and point to the new owner.
10. **MUST NOT** leave contradictory stack facts across this file and peer requirements.

### 2.2 Programming language(s)

11. **MUST** declare at least one primary programming language for the ship unit.
12. **SHOULD** list secondary languages only when they are real product law.
13. **MUST** state whether the product is primarily interpreted, compiled, polyglot, or package-multi-language.
14. **MUST NOT** freeze a marketing product name as if it were the language name.

### 2.3 Compilers, interpreters, and toolchains

15. **MUST** declare the target toolchain class used to build or run the product.
16. **MUST** state version policy as one of: unconstrained, minimum version, range, or pinned.
17. **SHOULD** record whether cross-compilation is in scope.
18. **MUST** fail closed in docs claims: do not claim “supports all interpreters” without tests or an explicit unconstrained policy.

### 2.4 Project / package / build tools

19. **MUST** declare the primary project or package tool used for dependencies and builds.
20. **MUST** declare how dependencies are resolved when the ecosystem supports lockfiles.
21. **SHOULD** name the test runner and linter or formatter classes when they are project law.
22. **MUST NOT** require a secret token or a private registry password in this file.

### 2.5 Runtime and platform (residual)

23. **MUST** declare the intended primary runtime and OS family when not fully owned by another architecture requirement.
24. **SHOULD** declare minimum CPU or architecture support only when it is real product law.
25. **MUST** separate developer-machine toolchain requirements from end-user runtime requirements when they differ.

### 2.6 No-hardcode / dual policy (class file)

26. **MUST NOT** hard-code a single product brand, one organization’s production hostname, or a personal owner identity as universal core law.
27. **MUST** put the live product name, the repo slug, and the concrete stack choices in Implementation Notes.
28. **MUST NOT** store secrets, PATs, or toy credentials in this file.

### 2.7 Implementation Notes (this project)

| Field | Value (HtmlDownloader) |
|-------|---------------------|
| **Project display name** | HtmlDownloader |
| **Project class** | software-development |
| **Class requirement basename** | `requirement-class-software-dev.md` |
| **Primary language(s)** | Python |
| **Language role** | primary only for the runtime package under `src/HtmlDownloader/` |
| **Execution model** | interpreted package. Optional Cython or `build.sh` tooling is not required for the CLI |
| **Toolchain / interpreter** | CPython |
| **Toolchain version policy** | range declared in `pyproject.toml` (`requires-python`). Re-verify before advertising a specific minor as tested |
| **Cross-compile in scope?** | no |
| **Primary project/package tool** | setuptools via PEP 517/621 `pyproject.toml` |
| **Lockfile policy** | not used as product law |
| **Test runner** | `python3 -m unittest discover -s tests`. Suites are on disk. Some TP rows stay todo |
| **Linter/formatter** | none as project law |
| **Primary runtime / OS family** | multi-OS where CPython runs (documented focus: Linux; macOS and Windows when Python is present) |
| **Architectures supported** | any architecture with CPython |
| **Git surface** | used — remote `https://github.com/cloudgen/HtmlDownloader` |
| **Ship surface** | installable Python package `HtmlDownloader`; console script `html-downloader`; module form `python -m HtmlDownloader` |
| **Product version SSOT** | `src/HtmlDownloader/__init__.py` → `__version__` and `pyproject.toml` `[project].version` stay equal when either is bumped (current: **1.1.1**) |
| **Install mode** | pip / local package. Not a shell online-install product |
| **Type 1 elevation** | intentionally absent. No root or sudo product surface |
| **Actor / role / subject / approver** | **Points at `requirement-actor-role-subject`.** The human operator of `html-downloader` is the only actor. No dest approval machine. The who-list has Actor, Role, and Subject. This residual does not replace that file |
| **Dest fence conditions** | **Considered — no dest fence conditions.** No dest inbound, approve, or reject queue |
| **Author contact (non-secret)** | Wilgat Wong · `wilgat.wong@gmail.com` |

**Residual ownership table:**

| Topic | Owner | Notes |
|-------|-------|--------|
| Project class membership | **this file** | Fixed |
| Primary language + toolchain policy | **this file** | Python / CPython |
| Package/build tool + lockfile | **this file** + `requirement-python-packaging` | packaging owns the PEP 621 tables and the ChronicleLogger floor |
| Project layout | `requirement-python-project-structure` | Running tree versus the class map |
| Class homes | `requirement-python-oop` | One class per file. Do not duplicate the map |
| CLI entry / typed verbs | `requirement-python-cli-interface` | Empty argv and the verb table |
| Text menu | `requirement-python-tui` | Front board and the picture |
| Menu language | `requirement-python-cli-language` | Front row 7, codes 71–83, and the language leaf |
| Status logger | `requirement-python-cli-logging` | Construct in `def main`. How to ask ChronicleLogger |
| Debug values | `requirement-python-cli-debug` | Printed catalog and the environment switch. This row points. It does not copy the list |
| Domain surface | `requirement-domain-htmldownloader` | Download, list, and serve. The about page uses the domain sentence |
| About page | `requirement-python-about` | Identity, host check, and the star box |
| No encoder | `requirement-domain-htmldownloader` and `requirement-runtime-prerequisites` | This program does not call an encoder |
| Python coding style / temps / `shutil.move` | `requirement-python-coding-style` | Publish. StateLogic stays unordered |
| Error / fail-closed user messaging | `requirement-python-error-handling` | Console sentences |
| Host runtime deps | `requirement-runtime-prerequisites` | ChronicleLogger. No encoder |
| Shell online install / shell self-update / Type O | **intentionally absent** | Not a shell channel |
| Pip lifecycle (`version-check`, `self-update`, `self-install`, `self-uninstall`) | `requirement-python-cli-interface` and `requirement-python-tui` | `python -m pip` only. Not a shell channel |
| Type 1 sudoers / root elevation | **intentionally absent** | No elevation law |
| Actor / role / subject / approver | `requirement-actor-role-subject` | No dest approver. This file points. It does not own the table |
| Dest fence conditions | **this file (residual)** | Considered — no dest fence conditions |
| Agent use skill | `requirement-agent-use-skill` | Side-product. Instructs an LLM agent to use `html-downloader`. Not a second domain file |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional**: Class and stack choices are explicit.
- **CIAO Principle 5 – SSOT**: Residual facts stay here until a peer takes the topic. The menu, the logger, and the class map have already moved.
- **CIAO Principle 1 – Caution**: This file does not invent a shell installer.
- **CIAO Principle 21 – Dual Policies**: Pointers stay short. Concrete values sit in Implementation Notes.
- **CIAO Principle 4 (O) + Principle 20**: One class file. No second stack SSOT.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: This file does not install an encoder. None is required.
- **Intentional**: The residual table points. It does not copy peer bodies.
- **Anti-fragile**: Packaging identity stays in `pyproject.toml`.
- **Over-protect**: Shell Type O stays absent while pip lifecycle is claimed on the CLI and the TUI.

## 5. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Delete this file while the workspace remains software-development with other Active product requirements.
2. Rename the specialized basename away from `requirement-class-software-dev.md` without an explicit class-model change.
3. Hard-code secrets, personal tokens, or production host names into core rules as universal law.
4. Duplicate full peer requirement bodies into this residual section.
5. Leave Implementation Notes hollow while Status is Active.
6. Introduce a shell online-install channel, a `curl|sh` installer, or shell Type O empty-argv install-ensure. Pip lifecycle owned by the CLI and TUI requirements is not that channel.
7. Introduce Type 1 sudoers or root elevation without an explicit user order and an elevation allowlist.
8. Treat this file as server-maintenance allowlist law, or register an Active server-maintenance class file in parallel.
9. Invent a second primary language that contradicts the Python requirements.
10. Skip `requirement-actor-role-subject`, add an Approver column to it, or publish `requirement-actor-role-subject-approver` while there is no dest approver.
11. Mark pip lifecycle absent, or mark shell Type O present.

**Violating any of these is a critical regression.**

## 6. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | The sole Active class file is `requirement-class-software-dev.md` |
| AC-2 | Primary language is Python with the CPython toolchain |
| AC-3 | The package tool is setuptools plus `pyproject.toml` |
| AC-4 | The residual table points at the CLI, TUI, logging, debug, OOP, and domain peers without copying their bodies |
| AC-5 | Shell Type O and Type 1 elevation are absent. Pip lifecycle is owned by the CLI and the TUI |
| AC-6 | Registered in `docs/requirements/index.md` with Area `class` |
| AC-7 | Actor residual points at Active `requirement-actor-role-subject`. Columns are Actor, Role, and Subject. No Approver column |

## 7. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-packaging` | Manifest, entry point, logger floor |
| `requirement-python-project-structure` | Layout |
| `requirement-python-oop` | Class map |
| `requirement-python-cli-interface` | Typed verbs and empty argv |
| `requirement-python-tui` | Text menu |
| `requirement-python-cli-logging` | Logger construct. How to ask ChronicleLogger |
| `requirement-python-cli-debug` | Debug catalog. This file points |
| `requirement-domain-htmldownloader` | Download, list, and serve |
| `requirement-python-coding-style` | Temps and `shutil.move` |
| `requirement-python-error-handling` | Console errors |
| `requirement-runtime-prerequisites` | Host tools and the logger floor |
| `requirement-agent-use-skill` | Side-product skill for an LLM agent |
| `requirement-actor-role-subject` | Who-list. This file points. It does not copy the table |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| n/a | packaging and structure smoke | deferred | Class residual is exercised by TP-PKG, TP-STRUCT, TP-LOG, TP-TUI, and TP-OOP when those rows leave todo |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, HtmlDownloader runs as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`. Pip lifecycle, when the operator asks for it, is `python -m pip` from the CLI and TUI requirements.

## Terminologies

**Project requirements.** Product law is the finished must/should rules for this product. They are complete for this product. They are not blank forms, not agent procedures, and not a glossary.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form in a stationery shop is not.

**Project class.** The internal name for which kind of work this folder is. Everyday talk says project nature. Every workspace is one kind. This file is the software-development class law plus the residual stack.

**Daily-life example:** Before you stock a room, you decide whether it is a bakery, a law office, or an empty spare room. The workshop word for that choice is project class.

**Coding-style requirement.** The specialize-in home for portable learned lessons about how this program is written. Without that file, those lessons arrive raw and get treated as this product’s law. This file is where a lesson is adopted, pointed at a peer requirement, or refused.

**Daily-life example:** A newsroom keeps one style sheet (“we write dates this way”). That adopted sheet is the coding-style requirement. The industry handbook on the shelf is not house law until the sheet says so.

## 8. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial software-dev class law for HtmlDownloader |
| 2026-10-04 | Active 1.1.0 | Residual pointers for the text menu, the logger, the class map, and pip lifecycle. Shell Type O stays absent |
| 2026-10-04 | Active 1.1.1 | Menu language points at `requirement-python-cli-language`. No new actor file |
| 2026-10-04 | Active 1.1.2 | Residual row for the about page. Product version **1.0.5** |
| 2026-10-16 | Active 1.2.0 | Product version **1.0.0**. No FFmpeg dependency. Menu language is front row 7 |
| 2026-10-28 | Active 1.2.1 | Residual points at the page save. The domain file owns download, list, and serve |
| 2026-10-28 | Active 1.2.2 | Product version **1.1.0** |
| 2026-10-28 | Active 1.2.3 | Terminologies for project requirements, project class, and the coding-style requirement |
| 2026-10-28 | Active 1.2.4 | Residual points at `requirement-agent-use-skill`. Product version stays **1.1.0**. No actor file |
| 2026-10-28 | Active 1.2.5 | Residual points at `requirement-actor-role-subject`. No dest approver. Product version stays **1.1.0** |
| 2026-10-28 | Active 1.2.6 | Residual points at `requirement-python-cli-debug`. The value list stays on that file. Product version stays **1.1.0** |
| 2026-10-28 | Active 1.2.7 | Product version **1.1.1** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
