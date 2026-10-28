# Tests — HtmlDownloader

Executable proof for product law. **Design map:** `docs/reviews/test-plan.md`.  
**RTM:** `docs/reviews/requirement-test-matrix.md`.

## Status (2026-10-28, product 1.0.1)

| Item | State |
|------|--------|
| Design TP map | **present** under `docs/reviews/test-plan.md` |
| Automated suites | `tests/test_about.py` covers **TP-ABOUT-01** through **TP-ABOUT-14** and **TP-ABOUT-16** (have). There is no **TP-ABOUT-15**. `tests/test_tui.py` covers **TP-TUI-09** and **TP-TUI-10** (have). `tests/test_language.py` covers **TP-LANG-01** (have). `tests/test_docs.py` covers **TP-DOC-01** (have). `tests/test_download.py` covers download, resume, list, and edit/view. `tests/test_crawl.py` covers **TP-CRAWL-01** through **TP-CRAWL-04** (have). `tests/test_serve.py` covers serve. **TP-DOC-03** stays `todo`. **TP-AGENT-01** stays `todo`. **TP-LOG-***, **TP-DEBUG-01**, and **TP-OOP-*** stay `todo` |
| Runner | `PYTHONPATH=src python3 -m unittest discover -s tests -q` (also `tests/run.sh`) |
| Last run | 2026-10-28 — 49 tests, OK |

## Suites on disk

| File | What it covers |
|------|----------------|
| `test_about.py` | TP-ABOUT-01..14 and TP-ABOUT-16 (have). No TP-ABOUT-15 |
| `test_tui.py` | TP-TUI-09 and TP-TUI-10 (have). The front board is download, list downloaded, serve, System Log, self-management, language, and Exit |
| `test_language.py` | TP-LANG-01 (have). Row 7, codes 71–83, `HTMLDOWNLOADER_LANG` |
| `test_docs.py` | TP-DOC-01 (have). TP-DOC-03 stays todo |
| `test_download.py` | Save, resume, flat assets, menu row 1, edit and view |
| `test_crawl.py` | **TP-CRAWL-01** through **TP-CRAWL-04**. Hosts are `127.0.0.1` and `127.0.0.1:9` only |
| `test_serve.py` | `127.0.0.1`, default port 5000, menu port prompt |

## Rules

1. Assert messages / test names **MUST** include the **TP-ID** when the case is one of the named TP families.  
2. Run page cases only with **generated fixtures** in temp dirs — never a live site the operator did not name.  
3. Core cases **MUST NOT** require public network.  
4. Flip `todo` → `have` in `docs/reviews/test-plan.md` and requirement DTV only after green runs.  
5. Do not place executable tests under `docs/templates/`.

## Run

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -q
```
