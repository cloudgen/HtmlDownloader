**file**: docs/requirements/requirement-actor-role-subject.md
**Status**: Active (Version 1.0.0)
**Area**: architecture
**Key**: `requirement-actor-role-subject`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Say who runs this program, in what role, and for whom. There is no second person who approves a download, a served page, or a pip action. The who-list has three columns: Actor, Role, and Subject. It does not have an Approver column.

The class file points here. It does not keep a second copy of the table. Verb behavior stays on the CLI, the text menu, and the domain file.

### 1.1 Human-facing

**In one sentence:** The person who starts `html-downloader` is the only one on the who-list, and nobody else approves the page.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who runs the command, as yourself | `html-downloader` |
| The other role | There is no second person who stamps or approves | A download does not wait for someone else |
| Not this file | The save rules, the menu picture, and the pip command strings | Their own requirements |

| Includes | Excludes |
|----------|----------|
| Who runs the menu, the page verbs, help, and the pip actions | An Approver column, a Submitter column, or a made-up admin account |
| Subject **None** when nobody is being filed for | Using this three-column list as if a review queue existed |

| Surface | What you open | What for |
|---------|---------------|----------|
| `html-downloader` on a terminal | The front board | You are the operator. The menu does not ask an approver |
| `html-downloader help` | The verb list | You are still the same person. Help does not file a request |
| `html-downloader download --url URL --name PAGENAME` | The terminal | You save one page for yourself |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the menu | You are the operator. The program does not look up a second account. | `html-downloader` |
| Read help | Help is a normal action with no one to file it for. | `html-downloader help` |
| Install or update | You run the pip verbs yourself. There is no approver account. | `html-downloader version-check` |

## 2. Core Rules (Mandatory)

1. A program with no dest approver **MUST** keep this who-list as its own Active requirement. The class residual **points** at that file. The residual **MUST NOT** replace the file.
2. The printed table **MUST** use exactly these columns: **Actor**, **Role**, **Subject**.
3. **MUST NOT** add **Submitter**. **MUST NOT** add **Approver**. **MUST NOT** invent an admin account, a `*-adm` name, or any other approver so the list looks complete.
4. **Actor** is the login that can run a verb. It is never empty. **Role** is what that person is doing. It is never empty. **Subject** is who a dest request would be for. **Subject** is **None** when there is no dest request.
5. Every verb family people actually run **MUST** have at least one row. Help **MUST** appear. Install, update, and remove of the program **MUST** appear when the product has those actions. Those rows use **Subject** **None** when there is no dest request.
6. This file names who. It does not own verb flags, the menu picture, or the page folder. Those stay on their peer requirements.
7. If a dest review machine is later implemented, this three-column list **MUST NOT** be treated as that coverage. The five-column catalog is a different file. Do not publish that file while no dest approver exists.

### 2.1 Implementation Notes (this project)

HtmlDownloader has no dest approval machine. The only actor is the person who invokes `html-downloader` or `python -m HtmlDownloader`. The actor is that login at run time (`id -un`). This file does not name a Unix account. There is no dedicated system user and no approver.

| Actor | Role | Subject |
|-------|------|---------|
| The invoking login | Operator of the text menu and the page verbs: empty argv on a terminal, `download`, list downloaded, `serve` | None |
| The invoking login | Operator of `help`, `version`, and `about` | None |
| The invoking login | Operator of System Log, language, and Exit on the menu | None |
| The invoking login | Installer of the pip lifecycle: `self-install`, `version-check`, `self-update`, `self-uninstall` | None |

Samples the same person can type:

```text
html-downloader
html-downloader help
html-downloader version
html-downloader about
html-downloader download --url URL --name PAGENAME
html-downloader serve --page-name PAGENAME
html-downloader version-check
html-downloader self-install
html-downloader self-update
html-downloader self-uninstall --force
```

`list downloaded`, System Log, language, and Exit are menu rows. They are not extra argv verbs. `language` is not an argv verb. Pip runs only when that person asks. Empty argv does not install.

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution**: The who-list is written. A missing approver is not filled in.
- **CIAO Principle 2 – Intentional**: Actor, Role, and Subject stay visible. The class file only points.
- **CIAO Principle 9 – Least privilege**: The person runs the program as themself. No admin account is created to complete a form.
- **CIAO Principle 21 – Dual policies**: The table is finished for this product. The core rules stay free of one product’s verb names.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the person in the table runs HtmlDownloader as themself (normal user privilege). **This requirement:** do not add an approver, do not use administrator privilege, `sudo`, `apt`, or a dedicated system user, and do not pipe a downloaded script into a shell. Admin privilege and dedicated system user privilege stay unused on that class. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Subject stays **None**. No invented stamp person.
- **Intentional**: Four rows cover the menu, help, and the pip lifecycle without copying their rules.
- **Anti-fragile**: The actor is whoever invokes the command. A renamed Unix login does not require a new row.
- **Over-protect**: An Approver column is forbidden while no dest review exists. One who-list. The class residual points at it.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Delete this file while HtmlDownloader has no dest approver.
2. Add an Approver column or a Submitter column.
3. Invent an admin account or a `*-adm` name.
4. Publish `requirement-actor-role-subject-approver` while there is no dest approver.
5. Put the verb flag rules or the menu picture in this file.
6. Mark **TP-ARS-*** have before a suite asserts this table.
7. Copy this table back into the class residual.

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Status is Active and the key is `requirement-actor-role-subject` |
| AC-2 | The only columns are Actor, Role, and Subject |
| AC-3 | Every row’s Subject is None |
| AC-4 | Help and the pip lifecycle each have a row |
| AC-5 | No Approver column and no invented admin account |
| AC-6 | `requirement-class-software-dev` points here and does not repeat the table |

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-class-software-dev.md` | Points here. Does not own the table |
| `docs/requirements/requirement-python-cli-interface.md` | Typed verbs |
| `docs/requirements/requirement-python-tui.md` | Menu rows, including list downloaded and Exit |
| `docs/requirements/requirement-domain-htmldownloader.md` | Download, list, and serve behavior |
| `html-downloader` | The command the invoking login runs |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ARS-01** | not written | todo | The table has Actor, Role, and Subject only |
| **TP-ARS-02** | not written | todo | Help and the pip lifecycle have rows. Subject is None |
| **TP-ARS-03** | not written | todo | No Approver column and no invented admin account |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Actor / role / subject.** The light who-list for a program that has no dest approver: who runs a verb, in what role, and for whom, if anyone. The printed table has three columns — Actor, Role, and Subject. It must not grow an Approver column. When a dest review exists, the five-column list is a different catalog and this three-column list is not that coverage.

**Human daily-life explanation.** Actor / role / subject is the short who-is-who list for a kitchen that has no stamp person: who cooks, in what job, and whose cake it is, if anyone’s. You still write the list. You do not add a fake teacher signature.

**Daily-life example.** A home bake has a mixer (actor), the job “mix” (role), and None for whose form it is (subject) because nobody dest-submits. You do not invent a vice-principal so the sheet looks official.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-28 | Active 1.0.0 | Light who-list. No dest approver. Columns are Actor, Role, and Subject |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
