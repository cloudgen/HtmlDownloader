**file**: docs/requirements/requirement-agent-use-skill.md
**Status**: Active (Version 1.0.0)
**Area**: agent
**Key**: `requirement-agent-use-skill`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement defines the side-product for HtmlDownloader. The side-product is one skill. That skill instructs an LLM agent how to use this application. It is not a second program, not a second domain file, and not a second save procedure.

The human menu, the typed verbs, and the page folder stay on their owners. This file says what the agent skill must teach, and where that skill file sits.

### 1.1 Human-facing

**In one sentence:** An LLM agent reads `agent/SKILL.md` and then runs `html-downloader` to save one page or serve one saved page.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who asks an agent to save or serve a page | “Save this URL.” |
| The other role | The LLM agent that reads the skill and types the command | `html-downloader download --url URL` |
| Not this file | The page folder, the menu picture, and the pip manifest | Download, text-menu, and packaging requirements |

| Includes | Excludes |
|----------|----------|
| One skill file that tells an agent the real verbs, flags, and bans | A second console script, a `crawl` verb, or an encoder step |
| Typed `download` and typed `serve` as the agent’s path | Telling the agent to open the text menu when nobody is at the terminal |
| The rule that a URL can recommend the folder and the HTML file name | A second copy of the save steps |

| Surface | What you open | What for |
|---------|---------------|----------|
| `agent/SKILL.md` | The side-product skill | Instructions for the agent |
| `html-downloader download --url URL` | The terminal | Save one page. No menu |
| `html-downloader serve --page-name PAGENAME` | This computer | Serve that saved page on `127.0.0.1` |
| `html-downloader help` | Help text | The same verbs, including what this program does not do |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Ask an agent to save a page | The agent follows the skill. It passes `--url`. It omits `--name` only when the URL recommends the folder. It does not draw the menu. | `html-downloader download --url https://example.com/guide.html` |
| Ask an agent to serve a page | The agent serves the saved folder on this computer. `/` is the stored HTML file. The default port is **5000**. | `html-downloader serve --page-name guide` |

## 2. Core Rules / Requirements (Mandatory)

1. A specialized product **MAY** ship one side-product. That side-product **MUST** be a skill whose only job is to instruct an LLM agent to use this application.
2. The skill **MUST** name the console script, the `download` verb, and the `serve` verb. `download` **MUST** require `--url`. `--name` **MAY** be omitted when the URL recommends the page folder, as the save law states. `--html` **MAY** be omitted. `serve` **MUST** require `--page-name`. The bind address **MUST** be `127.0.0.1`. The default port **MUST** be **5000**.
3. The skill **MUST** tell the agent to use typed verbs. Empty argv opens the text menu for a person at a terminal. An agent **MUST NOT** be told to drive that menu when no person is there.
4. The skill **MUST** say that list-downloaded is a menu row and not a typed verb.
5. The skill **MUST** forbid `hello`, `join`, `list-videos`, `crawl`, an encoder, a working-directory file listing, a shell installer, and root elevation. It **MUST NOT** give those as steps the agent should run.
6. The skill **MUST NOT** restate the save procedure. It points the agent at the console script. Folder shape, resume, and caps stay on `requirement-html-page-download`.
7. The skill **MUST NOT** become a second domain file. Exactly one Active domain file remains `requirement-domain-htmldownloader`.
8. The skill **MUST** be one file at the path in Implementation Notes. A second skill that teaches the same use is forbidden.
9. The skill **MUST NOT** contain a session login or a home directory path. The page folder family `~/.app/HtmlDownloader/output/` is the product path and is allowed.
10. Product source that checks this skill **MUST** cite this requirement. The skill text itself **MUST** stay instructions for the agent. It **MUST NOT** become the product law file.

### 2.1 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Application** | HtmlDownloader |
| **Console script** | `html-downloader` |
| **Side-product path** | `agent/SKILL.md` |
| **Download sample** | `html-downloader download --url https://example.com/guide.html` |
| **Explicit names** | `html-downloader download --url https://example.com/ --name example --html page.html` |
| **Serve sample** | `html-downloader serve --page-name example` |
| **Port override** | `html-downloader serve --page-name example --port 8080` |
| **Bind** | `127.0.0.1`. Default port **5000** |
| **Page folder** | `~/.app/HtmlDownloader/output/<pagename>/<html file>`. Default HTML file `index.html` |
| **URL recommendation** | `guide.html` saves `guide/guide.html`. A final segment such as `xxx` saves `xxx/index.html`. A host-only URL still needs `--name` |
| **Not verbs** | `hello`, `join`, `list-videos`, `crawl`, `language` |
| **Menu-only** | Row **2** list downloaded. The agent does not invent an argv verb for it |
| **Install the agent may name** | `pip install HtmlDownloader`, or `pip install -e .` from a checkout |
| **Product version** | The skill does not freeze a version literal. `html-downloader version` prints `__version__` |

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **Principle 2 – Intentional**: The agent is told the real verbs. It is not left to invent a join or a crawl.
- **Principle 5 – SSOT**: One skill file. The domain file still owns download, list, and serve.
- **Principle 1 – Caution**: A missing `--url` and a host-only URL without `--name` stay errors. The skill must say so.
- **Principle 10 – Least privilege**: The skill must not tell the agent to use root.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the agent runs `html-downloader` as the normal user. **This requirement:** the skill must not tell the agent to use administrator privilege, `sudo`, `apt`, or a dedicated system user. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The skill names the flags that fail closed.
- **Intentional:** The side-product is a skill for agents. The menu stays for a person.
- **Anti-fragile:** The skill still works when the agent has no workshop files, because the commands are in the skill itself.
- **Over-protect:** One skill. No second domain file. No encoder steps.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Add `join`, `list-videos`, `hello`, `crawl`, or an encoder as work the agent should run.
2. Split this side-product into a second skill that teaches the same use.
3. Copy the save steps into the skill or into this file.
4. Recreate `requirement-domain-videojoin` from this skill.
5. Tell the agent to serve on an address other than `127.0.0.1`.
6. Put a session login or a home directory path in the skill.
7. Turn `agent/SKILL.md` into product law. This file stays the law.

**Violating this rule is a critical side-product regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `agent/SKILL.md` exists and names `html-downloader download --url` and `html-downloader serve --page-name` |
| AC-2 | The skill says `--name` may be omitted when the URL recommends the folder, and that a host-only URL still needs `--name` |
| AC-3 | The skill says the server binds to `127.0.0.1` and defaults to port **5000** |
| AC-4 | The skill forbids `hello`, `join`, `list-videos`, `crawl`, an encoder, and a shell installer |
| AC-5 | The skill does not invent a typed verb for list downloaded |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-domain-htmldownloader` | Owns download, list, and serve |
| `requirement-html-page-download` | Owns the page folder. This skill does not restate it |
| `requirement-python-cli-interface` | Owns the typed verbs and the flags |
| `requirement-python-tui` | Owns the text menu. The agent does not drive it unattended |
| `requirement-class-software-dev` | Class residual points here |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-AGENT-01** | `tests/test_agent_skill.py` | have | The skill file names download, serve, the URL rule, and the bans |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

### Side-product

**Definition:** A side-product is one extra artifact this application ships for a reader who is not the person at the menu. For this product, that artifact is a skill. The skill’s only job is to instruct an LLM agent to use this application. The side-product is not a second program and not the product law.

**Human daily-life explanation:** The shop sells the tool. A one-page card tells a helper which buttons to press. The card is not a second tool, and it is not the house rulebook.

**Daily-life example:** The helper card says “press download, then the address.” It does not say “build a second downloader.”

### Skill

**Definition:** A skill, in this requirement, is the instruction sheet an LLM agent reads before it runs this application. It names the commands and the bans. It is not the law file and not the program.

**Human daily-life explanation:** A skill is the card in the helper’s pocket. The law is the sign on the wall. The helper follows the card. The sign still wins if they disagree.

**Daily-life example:** The card says “do not climb on the counter.” The helper does not treat the card as permission to add a new counter.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.0 | The side-product is `agent/SKILL.md`. It instructs an LLM agent to use `html-downloader`. It is not a second domain file |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
