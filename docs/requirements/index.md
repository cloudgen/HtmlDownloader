# Requirements index

**Product:** HtmlCrawler (Python CLI — text menu on a terminal; intended verb `crawl` saves a same-site set of pages)
**Ship unit this pass:** the copied tree still uses `src/HtmlDownloader`, and packaging still exposes `html-downloader`, until the ship-unit pass. Requirements name `html-crawler`. Origin stays `https://github.com/cloudgen/HtmlDownloader` until you confirm a new remote. The dispatcher accepts `crawl`.
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type O).
**Product version:** **1.0.1** (align `pyproject.toml`, `__init__.__version__`, root `README.md` Version badge)
**Updated:** 2026-10-28

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-28 |
| requirement-domain-htmlcrawler | Domain surface SSOT (crawl a site, list saved sites, serve one saved site). One-page save stays available | domain | Active | `requirement-domain-htmlcrawler.md` | 2026-10-28 |
| requirement-html-page-download | One HTML page plus stylesheets, scripts, images, and fonts. Not a domain file | download | Active | `requirement-html-page-download.md` | 2026-10-28 |
| requirement-html-site-crawl | Same-site walk. Required `--depth` and `--max-pages`. Robots fail closed | crawl | Active | `requirement-html-site-crawl.md` | 2026-10-28 |
| requirement-python-about | About page: identity, host check, star box. No `--json` | python | Active | `requirement-python-about.md` | 2026-10-28 |
| requirement-python-cli-interface | CLI entry and typed verbs, including `crawl`. `--depth` and `--max-pages` belong to `crawl` only | python | Active | `requirement-python-cli-interface.md` | 2026-10-28 |
| requirement-python-cli-logging | ChronicleLogger construct in `def main`; required floor points at packaging. Debug messages point at `requirement-python-cli-debug` | python | Active | `requirement-python-cli-logging.md` | 2026-10-28 |
| requirement-python-tui | Text menu: download, list downloaded, serve, System Log, self-management, language, Exit. Path word is selected by the language requirement. Default is `Path`. Menu columns are display columns | python | Active | `requirement-python-tui.md` | 2026-10-28 |
| requirement-python-cli-language | Menu language: front row 7, codes 71–83, leaf `~/.local/HtmlCrawler/language`. `language` is not an argv verb | python | Active | `requirement-python-cli-language.md` | 2026-10-16 |
| requirement-python-oop | L2 class map. The classes under `src/HtmlDownloader/` are on disk | python | Active | `requirement-python-oop.md` | 2026-10-28 |
| requirement-python-coding-style | Python style; temps; **shutil.move** publish; end state is the class map | python | Active | `requirement-python-coding-style.md` | 2026-10-28 |
| requirement-python-packaging | `pyproject.toml` / version / console script; ChronicleLogger floor | python | Active | `requirement-python-packaging.md` | 2026-10-28 |
| requirement-python-project-structure | Repository and `src/HtmlDownloader` layout | python | Active | `requirement-python-project-structure.md` | 2026-10-28 |
| requirement-python-readme | Root user document: sections, badges, picture catalog, related projects | python | Active | `requirement-python-readme.md` | 2026-10-28 |
| requirement-python-error-handling | Fail-closed errors; saved pages stay; console sentences stay | python | Active | `requirement-python-error-handling.md` | 2026-10-28 |
| requirement-runtime-prerequisites | Required ChronicleLogger; no root auto-install | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-28 |
| requirement-agent-use-skill | Side-product: one skill at `agent/SKILL.md` that instructs an LLM to use HtmlCrawler. On this tree the console script is `html-downloader`, and `crawl` is a typed verb | agent | Active | `requirement-agent-use-skill.md` | 2026-10-28 |
| requirement-python-cli-debug | Four debug messages (`isDebug()` identity lines). Logging still calls ChronicleLogger | python | Active | `requirement-python-cli-debug.md` | 2026-10-28 |

## Intentionally absent (by design)

| Surface | Status on HtmlCrawler |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure / `curl\|sh` | **Absent** |
| Shell local `install` / `uninstall` / shell self-update | **Absent** (pip package) |
| Type 1 sudoers / root elevation allowlist | **Absent** |
| Automatic companion `.sha256` channel integrity law | **Absent** |
| OpenCV / duration probe dependency | **Absent** |
| Second Active `requirement-domain-*` | **Forbidden** while `requirement-domain-htmlcrawler` is Active |
| Open-web crawl with no depth and no page cap | **Absent**. `crawl` requires `--depth` and `--max-pages` |
| Video join, `list-videos`, an FFmpeg pipeline, `requirement-domain-videojoin`, and `requirement-video-ffmpeg-pipeline` | **Removed** 2026-10-28. Do not recreate those files. Front row 1 is `download`. Front row 2 is `list downloaded`. Front row 3 is `serve` |
| `requirement-python-dependency-management` | **Absent**. ChronicleLogger floor is packaging + runtime. Law and the live manifest are `ChronicleLogger>=1.3.1` |
| `requirement-python-version` | **Absent**. Version SSOT is the `__version__` string |
| `requirement-python-json-output` | **Absent**. This product does not claim `--json`. The about page does not grow a JSON stream |
| `requirement-python-graceful-exit` | **Absent**. Control-C on `serve` returns 0 and prints `Stopped <name>.` Row 9 Exit returns 0 with no confirm |
| `requirement-python-interactive-vs-noninteractive` | **Absent**. Empty argv on a terminal versus help off a terminal is the CLI interface |
| `requirement-python-pyenv`, `requirement-python-conda`, build-script, `requirement-python-oop-architecture` | **Absent**. Host-check path reads for pyenv and conda stay on `requirement-python-about`. Class homes are `requirement-python-oop` |
| Actor-role requirement file | **Absent**. Class residual is no dest approver |

**Install mode:** **pip / local package** (`html-crawler` console script). Not a shell installer.

**Pip lifecycle:** claimed. Rows **63**–**66** and the typed verbs `version-check`, `self-update`, `self-install`, and `self-uninstall` are `requirement-python-cli-interface` and `requirement-python-tui`. They use `python -m pip`. They are not a shell channel. Empty argv does not run them.

**Logger:** required (`ChronicleLogger>=1.3.1` in law and in `pyproject.toml`). `def main` in `src/HtmlDownloader/cli.py` writes `ChronicleLogger(...)`. The four debug messages are `requirement-python-cli-debug`. Logging still shows the `isDebug()` / `log_message` call.

**Rules for agents:**

1. Treat rows above as the **live product-law inventory** for HtmlCrawler.
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.
3. Product source comments cite **only** these live requirement files.
4. This versioned surface lists **requirement rows only**.
5. Keep Status and Path in sync with each file’s header when status changes.
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).
7. **Domain SSOT:** exactly one Active domain file (`requirement-domain-htmlcrawler`).
8. **Do not introduce** a shell installer or Type 1 elevation without an explicit user order and a registry update.
9. **Do not** treat pip rows 63–66 as a reason to add a shell installer. **Do not** mark those pip rows absent.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
