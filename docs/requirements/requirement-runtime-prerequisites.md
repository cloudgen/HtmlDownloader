**file**: docs/requirements/requirement-runtime-prerequisites.md
**Status**: Active (Version 1.2.4)
**Area**: runtime
**Key**: `requirement-runtime-prerequisites`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare the host and Python runtime prerequisites required to run HtmlCrawler. This product does not implement a privileged installer. This file is the documentation and validation SSOT for what must already be present, together with the ChronicleLogger floor also owned by `requirement-python-packaging`.

### 1.1 Human-facing

**In one sentence:** You need Python and the ChronicleLogger package.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person about to download or serve a page | Python is already installed by you |
| The other role | pip | Installs HtmlCrawler and ChronicleLogger |
| Not this file | The menu picture and the page folder | TUI and domain requirements |

| Includes | Excludes |
|----------|----------|
| ChronicleLogger `>=1.3.1`, required | Calling that library optional |
| CPython on PATH | A claim that this product installs system packages |
| A console next step when the logger is missing | Root auto-install of the logger |

| Surface | What you open | What for |
|---------|---------------|----------|
| PATH | `python3` | The interpreter |
| pip | ChronicleLogger | Status file |
| About page | Runtime-tools line | `none`. Does not probe PATH (`requirement-python-about`) |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install the Python package | You get HtmlCrawler and the status library. | `python -m pip install HtmlCrawler` |
| Download a page | The machine needs a network only while that download runs. | `html-crawler download --url URL --name PAGENAME` |
| Start with the library missing | The console prints the pip next step and returns non-zero. | `html-crawler` |

## 2. Core Rules (Mandatory)

### 2.1 Scope

1. **MUST** document every external tool required at runtime.
2. **MUST NOT** claim the product auto-installs system packages via root or sudo.
3. **MUST** separate pip-installable Python dependencies from system binaries.

### 2.2 Required runtime components

| Component | Kind | Required for | Install surface |
|-----------|------|--------------|-----------------|
| CPython | interpreter | package import and the CLI | OS, pyenv, or the system Python. This product does not require you to install pyenv |
| ChronicleLogger `>=1.3.1` | pip package | the one status logger | `pyproject.toml` / `python -m pip`. Required, not optional |

### 2.3 Validation

4. Network access is required only while a download fetches a page. Serve and the menu do not need it.
5. If `ChronicleLogger` cannot be imported, `def main` **MUST** print the pip next step and return non-zero (`requirement-python-cli-logging`). That line is console text. The library is required.

### 2.4 Privilege

6. **MUST NOT** require root to satisfy runtime prerequisites for normal use.
7. Type 1 elevation is out of scope.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Python package install** | `python -m pip install HtmlCrawler`, or `python -m pip install -e .` from a checkout |
| **Declared pip dependency (law)** | `ChronicleLogger>=1.3.1`, required |
| **Live manifest** | `pyproject.toml` lists `ChronicleLogger>=1.3.1`. Matches the law floor |
| **System binary** | none |
| **Auto install command** | none. The product does not run a root install |
| **Platform notes** | Linux primary. macOS and Windows when CPython is available |
| **Product version** | 1.1.2 |
| **Startup check** | ChronicleLogger import |
| **User docs** | Root `README.md` Quick Installation |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: The logger may be missing. The console says so.
- **Principle 10 – Least privilege**: No root installer.
- **Principle 2 – Intentional**: The pip library is required.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the normal user installs the pip package. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to install ChronicleLogger from inside HtmlCrawler. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Document the missing logger before the program continues.
- **Intentional:** ChronicleLogger is required.
- **Anti-fragile:** The menu opens on a machine that has Python and the logger.
- **Over-protect:** No silent root install.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Add a root package-manager install from this product.
2. Store secrets in this file.
3. Add an unused library as a requirement.
4. Call ChronicleLogger optional, or hide the manifest lag.

**Violating this rule is a critical honesty regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | No system binary is listed as required |
| AC-2 | ChronicleLogger is a required pip dependency at `>=1.3.1` |
| AC-3 | No root auto-install claim |
| AC-4 | Missing ChronicleLogger produces the pip next step and a non-zero return |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-packaging` | Floor owner for the pip dependency |
| `requirement-python-cli-logging` | Construct. Missing-import sentence |
| `requirement-python-error-handling` | Missing-tool messages |
| `requirement-domain-htmlcrawler` | About runtime tools are `none` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PRE-01** | `tests/test_prerequisites.py` | todo | The about page says `Runtime tools: none`. No extra system binary is required |
| **TP-PRE-02** | `tests/test_prerequisites.py` | todo | ChronicleLogger imports. Law floor is `>=1.3.1` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial runtime prerequisites law for HtmlCrawler |
| 2026-10-04 | Active 1.1.0 | ChronicleLogger `>=1.3.1` is required. Live manifest still `>=1.2.3` |
| 2026-10-04 | Active 1.1.1 | Product version **1.0.4**. Manifest floor is `ChronicleLogger>=1.3.1` |
| 2026-10-04 | Active 1.1.2 | The about page does not probe PATH. Product version **1.0.5** |
| 2026-10-16 | Active 1.2.0 | Product version **1.0.0**. The about page says `Runtime tools: none` |
| 2026-10-28 | Active 1.2.1 | External-binary rules removed from this file |
| 2026-10-28 | Active 1.2.2 | Product version **1.0.1** |
| 2026-10-28 | Active 1.2.3 | Product version **1.1.1** |
| 2026-10-28 | Active 1.2.4 | Product version **1.1.2**. |

---
**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
