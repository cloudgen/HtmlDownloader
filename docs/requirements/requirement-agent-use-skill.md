**file**: docs/requirements/requirement-agent-use-skill.md
**Status**: Active (Version 1.0.1)
**Area**: agent
**Key**: `requirement-agent-use-skill`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement defines the side-product for HtmlCrawler. The side-product is one skill. That skill instructs an LLM agent how to use this application. It is not a second program, not a second domain file, and not a second save or walk procedure.

The human menu, the typed verbs, the page folder, and the site walk stay on their owners. This file says what the agent skill must teach, and where that skill file sits. On this tree the skill must also say which command the copied program accepts.

### 1.1 Human-facing

**In one sentence:** An LLM agent reads `agent/SKILL.md`, then runs `html-downloader` on this tree to save one page, crawl one site, or serve one saved page.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who asks an agent to save, crawl, or serve | “Save this URL.” |
| The other role | The LLM agent that reads the skill and types the command | `html-downloader download --url URL --name PAGENAME` |
| Not this file | The page folder, the site walk, the menu picture, and the pip manifest | Page, crawl, text-menu, and packaging requirements |

| Includes | Excludes |
|----------|----------|
| One skill file that tells an agent the live console script, the intended `crawl` command, and the flags that fail closed | A second console script, a second domain file, or an encoder step |
| Typed `download` and typed `serve` as the agent’s path on this tree | Telling the agent to open the text menu when nobody is at the terminal |
| `crawl` on `html-downloader` with the four required flags | An unlimited crawl, or `--depth` and `--max-pages` on `download` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `agent/SKILL.md` | The side-product skill | Instructions for the agent |
| `html-downloader download --url URL --name PAGENAME` | The terminal on this tree | Save one page. No menu |
| `html-downloader serve --page-name PAGENAME` | This computer | Serve that saved page on `127.0.0.1` |
| `html-downloader crawl --url URL --name SITENAME --depth N --max-pages N` | The terminal on this tree | The walk. No menu |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Ask an agent to save a page | The agent follows the skill. It passes `--url` and `--name`. It does not draw the menu. | `html-downloader download --url https://example.com/ --name example` |
| Ask an agent to crawl a site | The agent names depth and the page cap on `html-downloader`. | `html-downloader crawl --url https://example.com/ --name example --depth 1 --max-pages 20` |
| Ask an agent to serve a page | The agent serves the saved folder on this computer. The default port is **5000**. | `html-downloader serve --page-name example` |

## 2. Core Rules / Requirements (Mandatory)

1. A specialized product **MAY** ship one side-product. That side-product **MUST** be a skill whose only job is to instruct an LLM agent to use this application.
2. The skill **MUST** name the console script this tree actually installs, and the console script the law intends. On this tree the installed script is `html-downloader`. The intended script is `html-crawler`. The intended module is `python -m HtmlCrawler`. The module that runs today is `python -m HtmlDownloader`.
3. The skill **MUST** name `download` and `serve` as typed verbs the copied dispatcher accepts. `download` **MUST** require `--url` and `--name`. The skill **MUST NOT** tell the agent to omit `--name`. There is no `--html` flag. `serve` **MUST** require `--page-name`. The bind address **MUST** be `127.0.0.1`. The default port **MUST** be **5000**.
4. The skill **MUST** give the intended `crawl` command with `--url`, `--name`, `--depth`, and `--max-pages`, all required. It **MUST** say `--depth` is an integer ≥ 0 and `--max-pages` is an integer ≥ 1. It **MUST NOT** default either bound to unlimited. It **MUST NOT** put those two flags on `download`.
5. On this tree the skill **MUST** give the live `crawl` command on `html-downloader` with `--url`, `--name`, `--depth`, and `--max-pages`. It **MUST** say help lists `crawl`, `download`, and `serve`. It **MUST NOT** label `crawl` as an unknown verb. It **MUST NOT** tell the agent to edit the dispatcher to add `crawl`. It **MUST NOT** say this product has no `crawl` verb.
6. The skill **MUST** tell the agent to use typed verbs. Empty argv opens the text menu for a person at a terminal. An agent **MUST NOT** be told to drive that menu when no person is there. With no terminal, empty argv prints help and returns 0.
7. The skill **MUST** say that list-downloaded is menu row **2** and not a typed verb. `language` is menu row **7** and not a typed verb. `crawl` is not a menu row.
8. The skill **MUST** forbid `hello`, `join`, `list-videos`, an encoder, a working-directory file listing, a shell installer, and root elevation. It **MUST NOT** give those as steps the agent should run.
9. The skill **MUST NOT** restate the save procedure or the walk procedure. Folder shape, resume, and caps stay on `requirement-html-page-download`. Depth, page cap, same host, robots, and the wait stay on `requirement-html-site-crawl`.
10. The skill **MUST NOT** become a second domain file. Exactly one Active domain file remains `requirement-domain-htmlcrawler`.
11. The skill **MUST** be one file at the path in Implementation Notes. A second skill that teaches the same use is forbidden.
12. The skill **MUST NOT** contain a session login or a home directory path. The page-folder family in Implementation Notes is the product path and is allowed.
13. Product source that checks this skill **MUST** cite this requirement. The skill text itself **MUST** stay instructions for the agent. It **MUST NOT** become the product law file.
14. Pip verbs on this tree target the distribution name `HtmlDownloader`. The skill **MUST NOT** tell the agent that `python -m pip install HtmlCrawler` already matches this tree. `self-uninstall` **MUST** be shown with `--force`.

### 2.1 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Application** | HtmlCrawler |
| **Intended console script** | `html-crawler` |
| **Intended module** | `python -m HtmlCrawler` |
| **This tree console script** | `html-downloader` |
| **This tree module** | `python -m HtmlDownloader` |
| **This tree package directory** | `src/HtmlDownloader` |
| **This tree distribution** | `HtmlDownloader` |
| **Side-product path** | `agent/SKILL.md` |
| **Download sample** | `html-downloader download --url https://example.com/ --name example` |
| **Serve sample** | `html-downloader serve --page-name example` |
| **Port override** | `html-downloader serve --page-name example --port 8080` |
| **Bind** | `127.0.0.1`. Default port **5000** |
| **Crawl sample on this tree** | `html-downloader crawl --url https://example.com/ --name example --depth 1 --max-pages 20` |
| **Crawl on this tree** | Accepted. Not a menu row. Output root `~/.app/HtmlDownloader/output/<sitename>/` |
| **Page folder on this tree** | `~/.app/HtmlDownloader/output/<pagename>/index.html` |
| **Page folder in law** | `~/.app/HtmlCrawler/output/<pagename>/index.html` |
| **Menu-only** | Row **2** list downloaded. Row **7** language. The agent does not invent an argv verb for either |
| **Front rows** | 1 download, 2 list downloaded, 3 serve, 4 System Log, 6 self-management, 7 language, 9 Exit. Rows 5 and 8 stay omitted |
| **Install the agent may name** | `python -m pip install -e .` from a checkout of this tree |
| **Pip verbs on this tree** | `python -m pip` with distribution `HtmlDownloader`. `self-uninstall` needs `--force` |
| **Product version** | The skill does not freeze a version literal. `html-downloader version` prints `__version__` |
| **Origin** | Stays the sentence on `requirement-domain-htmlcrawler` until you confirm a new remote |

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **Principle 2 – Intentional**: The agent is told the real verbs, including `crawl` on `html-downloader`.
- **Principle 5 – SSOT**: One skill file. The domain file still owns crawl, list, and serve. The walk stays on the crawl requirement.
- **Principle 1 – Caution**: A missing `--url` or `--name` stays an error. A crawl without depth or a page cap stays an error.
- **Principle 10 – Least privilege**: The skill must not tell the agent to use root.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the agent runs the console script as the normal user. **This requirement:** the skill must not tell the agent to use administrator privilege, `sudo`, `apt`, or a dedicated system user. Do not pipe a downloaded script into a shell. Type 1 (administrator privilege) and Type 2 (dedicated system user privilege) are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The skill names the flags that fail closed, and it names the console script this tree installs.
- **Intentional:** The side-product is a skill for agents. The menu stays for a person.
- **Anti-fragile:** The skill still works when the agent has no other instruction files, because the commands are in the skill itself.
- **Over-protect:** One skill. No second domain file. No encoder steps. No unlimited crawl.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Add `join`, `list-videos`, `hello`, or an encoder as work the agent should run.
2. Tell the agent this product has no `crawl` verb, or tell the agent to run `crawl` on this tree before the dispatcher accepts it.
3. Drop `--depth` or `--max-pages` from the crawl sample, or add them to `download`.
4. Split this side-product into a second skill that teaches the same use.
5. Copy the save steps or the walk steps into the skill or into this file.
6. Open a second Active domain file from this skill.
7. Tell the agent to serve on an address other than `127.0.0.1`.
8. Put a session login or a home directory path in the skill.
9. Turn `agent/SKILL.md` into product law. This file stays the law.
10. Cite templates or skills as product-source authority.
11. Specialize this file onto HtmlDownloader.

**Violating this rule is a critical side-product regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `agent/SKILL.md` exists and names `html-downloader download --url` with `--name`, and `html-downloader serve --page-name` |
| AC-2 | The skill says both `--url` and `--name` are required for `download` |
| AC-3 | The skill says the server binds to `127.0.0.1` and defaults to port **5000** |
| AC-4 | The skill gives `html-downloader crawl` with `--depth` and `--max-pages`, and does not label `crawl` as an unknown verb |
| AC-5 | The skill does not invent a typed verb for list downloaded |
| AC-6 | The skill names distribution `HtmlDownloader` for pip on this tree |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-domain-htmlcrawler` | Owns the verb catalog, help, about, and the ship-unit gap |
| `requirement-html-site-crawl` | Owns the walk. This skill does not restate it |
| `requirement-html-page-download` | Owns the page folder. This skill does not restate it |
| `requirement-python-cli-interface` | Owns the typed verbs and the flags |
| `requirement-python-tui` | Owns the text menu. The agent does not drive it unattended |
| `requirement-python-project-structure` | Repository layout. This file owns `agent/SKILL.md` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-AGENT-01** | `tests/test_agent_skill.py` | todo | The skill names download with `--name`, serve, and `html-downloader crawl`. The suite file is not in the tree |
| **TP-AGENT-02** | `tests/test_agent_skill.py` | todo | The crawl sample includes `--depth` and `--max-pages`. The download sample does not |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Side-product.** One extra artifact this application ships for a reader who is not the person at the menu. For this product that artifact is the skill at `agent/SKILL.md`. Its only job is to instruct an LLM agent to use this application. It is not a second program and not the product law. The shop sells the tool. A one-page card tells a helper which buttons to press.

**Daily-life example:** The helper card says “press download, then the address.” It does not say “build a second downloader.”

**Skill.** In this requirement, the instruction sheet an LLM agent reads before it runs this application. It names the commands and the bans. It is not the law file and not the program. The card is in the helper’s pocket. The sign on the wall is the law. The sign wins if they disagree.

**Daily-life example:** The card says which button to press. The helper does not treat the card as permission to add a new button.

**Project requirements.** The finished must and should rules for this product. They are not blank forms and not agent procedures. This household’s rules are for this house.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form is not.

**CLI gap name.** A command word the law names and the running program still rejects. The live command fails closed. Help does not list it until the program accepts it.

**Daily-life example:** A chalkboard says “add pie next month,” and the kitchen will not take a pie order today. Pie is a gap name until the waiter routes it.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.0 | The side-product is `agent/SKILL.md`. It instructs an LLM agent to use HtmlCrawler. On this tree the console script is `html-downloader`, and `crawl` is a gap. |
| 2026-10-28 | Active 1.0.1 | `html-downloader crawl` is the live command. The skill does not freeze a version literal. |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
