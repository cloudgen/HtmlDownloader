# Requirements

Authoritative specialized product law for **HtmlDownloader** lives here.

**Current state (2026-10-16):** Specialized **software-development** product. Left genesis. Registry is populated — see `index.md`. Product version is **1.0.0**.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `HtmlDownloader` |
| Version SSOT | **`1.0.0`** (`pyproject.toml` + `src/HtmlDownloader/__init__.py`) |
| Product README SSOT | Root `README.md`. Sections and pictures: `requirement-python-readme` |
| Ship surface | Python package; console script **`html-downloader`**; module `python -m HtmlDownloader` |
| Install mode | **pip / local package** (`pip install HtmlDownloader`; this tree **1.0.0**; checkout `pip install -e .`) — not shell Type O |
| Public source | `https://github.com/cloudgen/HtmlDownloader` |
| Domain surface | `requirement-domain-videojoin` — download one page, list saved pages, serve a saved page |
| Text menu | `requirement-python-tui` — front rows **1** download, **2** list downloaded, **3** serve, **4** System Log, **6** self-management, **7** language, **9** Exit. Default path word is `Path` |
| Menu language | `requirement-python-cli-language` — row **7**, codes **71**–**83**, leaf `~/.local/HtmlDownloader/language`. `HTMLDOWNLOADER_LANG` overrides that file for one process. `language` is not an argv verb |
| Status logger | `requirement-python-cli-logging` — `ChronicleLogger(...)` inside `def main`. Required |
| Class map | `requirement-python-oop` — the classes under `src/HtmlDownloader/` |
| Encode ops | `requirement-video-ffmpeg-pipeline` — **Retired**. This program does not call an encoder |
| Coding style | `requirement-python-coding-style` — temps + `shutil.move`; gate **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** |
| Runtime tools | **ChronicleLogger>=1.3.1** required. No external media tool |

## Class requirement gate

| Class | Required class file |
|-------|---------------------|
| software-development | `requirement-class-software-dev.md` (**Active**) |
| genesis-template | N/A — this workspace is no longer genesis for product law |

## Purpose

- **Plan** designs work by reading and updating these docs.  
- **Implement** delivers code that **traces** to these requirements.  
- **Review** verifies delivery against requirements and CIAO checklists.  
- Product **README** must stay honest with this law (install, features, version).

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry of all requirements — keep in sync |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Rules

1. Never invent paths — verify on disk.  
2. Class files only via class process; non-class via create-specific process.  
3. Never dump harness inventories into this versioned surface.  
4. Online shell install and Type 1 elevation stay **absent** unless product mode is explicitly changed.  
5. Sole domain SSOT: `requirement-domain-videojoin.md`.  
6. When changing download, list, or serve behavior: update the domain requirement **and** root `README.md` in the same change.  
7. Version dual SSOT + README Version badge must match when a release is claimed.
