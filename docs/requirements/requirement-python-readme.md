**file**: docs/requirements/requirement-python-readme.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-readme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the product user document at the repository root: which sections it has, which pictures it embeds, and the rule that a sentence in that document matches the requirement that owns the behavior. Project nature is a program a person builds and runs from a terminal. The menu picture stays on `requirement-python-tui`. The thirteen languages stay on `requirement-python-cli-language`. The verbs stay on `requirement-python-cli-interface`. The join stays on `requirement-domain-videojoin` and `requirement-video-ffmpeg-pipeline`. The prerequisite sentences stay on `requirement-runtime-prerequisites`. The package name and the console script stay on `requirement-python-packaging`. The version string is `__version__`. This file does not restate those bodies.

### 1.1 Human-facing

**In one sentence:** You open the root user document to install the program, read how the menu joins two videos, and see pictures of the language list, a two-file join, self-management, about, and system-log.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person reading how to run the program | Open `README.md` at the checkout root |
| The other role | The requirements that own the menu, the join, and the package | A sentence here matches those files |
| Not this file | The concat itself, the language file, and the host check | Pipeline, language, and domain |

| Includes | Excludes |
|----------|----------|
| Section order, badges, the Advantages contrast, install sentences, and the picture catalog | A second menu, a second verb list, or a second encode order |
| Absolute `https` image destinations for captures of the running text menu | A generated drawing that invents row text. A relative `screenshots/` image destination in this package description |
| The eight related-project lines | A shell online install, root as the documented path, or a setup script that is not on disk |

| Surface | What you open | What for |
|---------|---------------|----------|
| `README.md` | Root user document | Install, usage, pictures |
| `screenshots/` | Picture folder beside that document | The links in the Screenshots section |
| `video-join` | The program on a terminal | What those pictures show |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Read the install | The public path is pip. The document does not ask for root. | `pip install VideoJoin` |
| Check the pictures | Row 4 is the language list. The pictured job joins two files in the current directory. About stays in English. | `video-join`, then `4`, or `1` |
| Check the version line | The badge matches the package string. | `video-join version` |

## 2. Core Rules / Requirements (Mandatory)

The user document is how a person learns the program. It is not a second copy of product law. A claim in the document matches the requirement that owns that claim.

### 2.1 Where it lives

1. **MUST** keep the user document at the repository-root `README.md`. Product law stays under `docs/requirements/`. The layout rule that the file exists is `requirement-python-project-structure`. This file owns the sections and the pictures.
2. Pictures **MUST** live in a `screenshots/` folder at that same root. The user document **MUST** link every PNG in that folder. This document is the package description. Each image destination **MUST** be an absolute `https` URL that names that PNG on the public source host. A relative `screenshots/<file>` destination fails on the package index: the index fetches that path on its own host, and the picture folder is not in the published archive. The same relative destination still opens on the source forge. A link to a sibling document, such as `LICENSE.md`, **MAY** stay relative. A PNG on disk and absent from `README.md` fails this file. The URL base for this product is in Implementation Notes. That URL does not render on the package index until the file is on the public branch named in the URL.
3. **MUST NOT** freeze a session login or a `/home/<login>/` path in this requirement or in a sentence that is law. A picture may show the directory where that capture was started. The sentence in the document names “the current directory.”

### 2.2 What the document contains

The document **MUST** keep the sections in §2.5, in that order. A new heading, a dropped heading, or a reordered heading is a revision of this file.

Each behavioral sentence **MUST** match its owner and **MUST NOT** restate that owner’s procedure:

| Claim in the document | Owner |
|-----------------------|--------|
| Two-file join, formats, output name, no folder prompt | `requirement-domain-videojoin` |
| Stream copy, then re-encode, publish with `shutil.move` | `requirement-video-ffmpeg-pipeline` and `requirement-python-coding-style` |
| Menu picture, path row, clock, row numbers | `requirement-python-tui` |
| Thirteen languages and what stays English | `requirement-python-cli-language` |
| Product verbs and pip lifecycle commands | `requirement-python-cli-interface` |
| Empty argv on a terminal opens the menu. Empty argv with no terminal prints help and returns 0. Direct `join` with no terminal exits non-zero | `requirement-python-cli-interface` |
| Package name, console script, pip install | `requirement-python-packaging` |
| Package string on the badge | `__version__` in `src/VideoJoin/__init__.py`, copied by `pyproject.toml` |
| `ChronicleLogger>=1.3.1` | `requirement-python-packaging` and `requirement-runtime-prerequisites` |
| FFmpeg on `PATH`, no root auto-install | `requirement-runtime-prerequisites` |

This product does not claim `--json`. `hello` is a product verb. The user document does not name `./setup.sh` or `./build.sh`.

The first-row sentence in the user document **MUST** name the current directory on the left and a local clock (`HH:MM:SS`) on the right when the row has room. It **MUST NOT** name `Current`, a login, `USER`, `USERNAME`, or `getpass` as that right-hand field. The picture of the row stays on `requirement-python-tui`.

### 2.3 Pictures

1. A menu picture **MUST** be a capture of the running text menu. **MUST NOT** satisfy a menu row with a drawing that invents row text. Every PNG in `screenshots/` **MUST** be linked from the user document. A PNG that is not a menu capture **MUST** be labeled as that file and **MUST NOT** be described as a text-menu capture.
2. The Screenshots section **MUST** show the language list, then one main menu for each supported language in list order, then self-management, then about, then System Log.
3. Each menu picture **MUST** be a capture of the board this program paints. **MUST NOT** keep a picture of a removed verb.
4. The about picture **MUST** stay in English. Leaf shorts in every menu picture **MUST** stay the English verb. That split is `requirement-python-cli-language`.
5. A live-menu capture satisfies this file when it shows the menu the program paints, including a double-width label that stays whole and a clock that stays on the path row.
6. The heading of each picture **MUST** be that file’s basename. The paragraph and the image alt **MUST** be the catalog cells for that file. Those words come from the basename and from what the picture shows: the words on the screen, the characters in the input box, or the scene. A language name alone, or a sentence that only says the file is a picture, fails this file. The paragraph **MUST NOT** freeze a session login or a `/home/<login>/` path. The path row is “the current directory.”

### 2.4 Install honesty

1. The public install path **MUST** be pip. **MUST NOT** document a shell online install, `sudo pip`, or `sudo curl | sh`.
2. **MUST NOT** name a checkout setup script that is not on disk. This tree has no `setup.sh`. The document **MUST NOT** name `setup.sh`.
3. The document does not show a wheel or sdist example. **MUST NOT** add one unless the basename is the file the build writes and the version token matches the package version.
4. The prerequisite sentences **MUST** stay aligned with `requirement-runtime-prerequisites`. This file **MUST NOT** copy that table as a second owner.
5. **MUST NOT** add `./build.sh` verbs to the user document. Those verbs are not `video-join` verbs.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Document** | `README.md` |
| **Pictures** | `screenshots/` |
| **Package** | `HtmlDownloader` |
| **Console script** | `html-downloader` |
| **Version** | `1.0.0` from `src/HtmlDownloader/__init__.py` (`__version__`). `pyproject.toml` copies that string |
| **Python** | `>=2.7`, excluding 3.0 through 3.4. The badge says 2.7+ (3.x recommended) |
| **License file** | `LICENSE.md` (MIT). The file is present. The document link stays relative |
| **Homes** | `https://github.com/cloudgen/HtmlDownloader` and `https://pypi.org/project/HtmlDownloader/` |
| **Capture directory** | `/tmp/clips`. The clock on each menu picture is the local time when that frame was painted |
| **Every PNG** | `README.md` links each PNG under `screenshots/`. Every PNG in that folder is a text-menu capture |
| **Image URL** | `https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/<basename>`. The package index can fetch that file only after it is on that public branch |

**Title:** `HtmlDownloader - Download a page from the command line and from the text menu`.

**Badges:** a Version badge whose token is the package string; License MIT; CIAO linked to `https://github.com/cloudgen/ciao`; stars for `cloudgen/HtmlDownloader`; Python 2.7+ (3.x recommended); PyPI `HtmlDownloader` linked to `https://pypi.org/project/HtmlDownloader/`.

**Opening:** concatenate two videos in the current directory. Prefer stream copy. Re-encode when copy fails. Publish with `shutil.move`. On a terminal with no arguments, the text menu opens. The menu does not start the join by itself and does not call pip.

**Sections, in order.** Advantages is inserted after Features. Screenshots is inserted after Usage. The other headings keep the existing kit order.

| Heading | What this document must keep | Owner of the behavior |
|---------|------------------------------|------------------------|
| Features | Text menu: join, system-log, language, self-management, Exit. Path and a local clock on the first row. system-log is **3**. language is **4**. self-management is **8**. Two files in the current directory. Stream copy, then re-encode. `shutil.move`. FFmpeg on `PATH`. Verbs `help`, `version`, `about`, `hello`, `join`, `list-videos`, `self-install`, `version-check`, `self-update`, `self-uninstall` | Peers in §2.2. The path-row sentence is the clock rule in §2.2 |
| Advantages | The four parts and the comparison table below | This file for the contrast. Peers in §2.2 for the behavior |
| Quick Installation | FFmpeg on `PATH`. `ChronicleLogger>=1.3.1`. `pip install VideoJoin`. Checkout uses a venv and `pip install -e .`. The fenced text menu (front, system-log, language, self-management) stays in this section | `requirement-runtime-prerequisites`, `requirement-python-packaging`, `requirement-python-tui` |
| Usage | Menu versus typed verbs. Join asks for two indexes and an output name. No folder prompt. Esc returns. No terminal: empty argv prints help and returns 0. Direct `join` with no terminal exits non-zero. `self-uninstall` needs `--force`. No sudo | `requirement-python-cli-interface`, `requirement-domain-videojoin`, `requirement-python-tui` |
| Screenshots | Lead: each heading is the file name, and the paragraph is what that picture shows. Package **1.0.0**. The paragraph and the image alt are the catalog below | This file |
| Examples | `cd` to a folder of clips, then `video-join`, then `video-join version`, then `video-join join` | `requirement-domain-videojoin` |
| Platform Compatibility | Linux primary. macOS and Windows when Python and FFmpeg are present. The text menu needs a terminal | `requirement-runtime-prerequisites` |
| Related Projects | The eight lines below, in that order, each with one sentence | This file |
| Contributing | Keep product law in sync. Do not strip `shutil.move`. Version strings stay together | `requirement-python-coding-style`, `requirement-python-packaging` |
| License | MIT, link `LICENSE.md`, and that file exists | `requirement-python-packaging` |
| Last Update | Names package **1.0.0**, the public source, and the picture catalog. A version bump is not required for pictures that did not change | This file for the line. `__version__` for the string |

**Related projects, in this order.** The first two are this program. Each line is one sentence. Do not add an install recipe.

| Order | Link | Sentence |
|------:|------|----------|
| 1 | `https://github.com/cloudgen/HtmlDownloader` | This program’s source |
| 2 | `https://pypi.org/project/HtmlDownloader/` | This program on PyPI |
| 3 | `https://github.com/Wilgat/AnimeDlp` | Command-line downloader for anime video sites |
| 4 | `https://github.com/Wilgat/ChronicleLogger` | Status logger this program depends on (`ChronicleLogger>=1.3.1`) |
| 5 | `https://github.com/Wilgat/VideoSpeed` | Cuts, changes speed, and boomerangs a clip. That program is not this one |
| 6 | `https://github.com/cloudgen/ciao` | Caution, Intentional, Anti-fragile, Over-engineered |
| 7 | `https://github.com/cloudgen/ciao-lite` | Short agent contract |
| 8 | `https://github.com/cloudgen/safe-rm` | Guarded `rm` |

**Advantages, after Features and before Quick Installation.** Four parts, then the comparison. The path row in this section names the local clock.

1. **Dual-mode interface.** The menu asks for two indexes and an output name. A typed `join` asks the same questions. The person does not write an FFmpeg concat graph. The program tries stream copy, then re-encodes if copy fails. There is no length percent, no boomerang, and no `--json`. With no arguments on a terminal, the text menu opens. With no terminal and no verb, the program prints help and returns 0. Direct `join` with no terminal exits non-zero.
2. **Built-in languages.** Row **4** lists thirteen languages: English, Simplified Chinese, Traditional Chinese, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Dutch, and Greek. The choice is saved for the next run.
3. **USB-safe staging.** Intermediate files are written beside the output when that folder can be written, including on a removable drive. The finished file is published with `shutil.move`. When that folder cannot be written, the stage uses the system temporary directory. The section **MUST NOT** say the stage never uses that directory.
4. **Lifecycle and diagnostics.** `version-check`, `self-update`, `self-install`, and `self-uninstall` are menu rows **84**–**87** and typed verbs. `self-uninstall` on the command line needs `--force`. They call pip and do not use root. **system-log** (**3**) views a log, clears a log, and shows the log folder. **about** (**83**) stays in English.

**Comparison table.** Columns: Feature, Raw FFmpeg CLI, Typical Python wrappers (moviepy), VideoJoin.

| Feature | Raw FFmpeg CLI | Typical Python wrappers (moviepy) | VideoJoin |
|---------|----------------|-----------------------------------|-----------|
| Learning curve | A concat graph the person writes | A Python script | Text menu, or two file numbers and an output name |
| Non-interactive | Native command line | A custom script | Typed verbs. No terminal and no verb: help, return 0. Direct `join` with no terminal: non-zero. No `--json` |
| Menu languages | None | None | Thirteen, kept for the next run |
| Temporary files | You choose the paths | Often the system temporary directory | Beside the output when that folder can be written. Otherwise the system temporary directory. Publish with `shutil.move` |
| Self-management | The system package manager | pip from outside the tool | Built-in version-check, self-update, self-install, and self-uninstall |
| Diagnostics and logs | The encode stream | A logging setup in the script | system-log (row 3) and about (83), in English |

**Screenshot catalog, in this order.** Each image destination is the absolute `https` URL in Implementation Notes, with that file’s basename. The paragraph and the alt are the words `README.md` prints for that file.

| Order | File | Paragraph | Alt |
|------:|------|-----------|-----|
| 1 | `language-menu.png` | Row **7** has opened the language list. **71 English** is highlighted, with the note "use English for this menu." The other rows are **72 简体中文**, **73 繁體中文**, **74 Español**, **75 العربية**, **76 Français**, **77 Português**, **78 Русский**, **79 Deutsch**, **80 日本語**, **81 한국어**, **82 Nederlands**, and **83 Ελληνικά**. Each note says to use that language for this menu. **0 Back** says "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:09` on the right of that row. The status line says `HtmlDownloader 1.0.0` and `language`. | Language list, 71 English highlighted |
| 2 | `main-menu-en.png` | English main menu. There is no saved-language line above the box. The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:12` on the right of that row. **1 download** is highlighted: "download a page and its stylesheets, scripts, and images." Then **2 list downloaded** "show saved page names," **3 serve** "serve a saved page on this computer," **4 System Log** "view, clear, and the log folder," **6 self-management** "version, about, and pip lifecycle," **7 language** "display language for this menu," and **9 Exit** "leave." The status line says `HtmlDownloader 1.0.0` and `main menu`. | English main menu |
| 3 | `main-menu-zh-hans.png` | Simplified Chinese main menu. The line above the box says `菜单语言是简体中文`. The path label is `路径`. The path is `/tmp/clips`. The clock is `19:48:14` on the right of that row. **1 download** is highlighted and stays `download`: "下载页面、样式表和脚本." **2** stays `list downloaded`. **3** stays `serve`. **4** is `系统日志`. **6** is `自我管理`. **7** is `语言`. **9** is `离开`. The status line says `HtmlDownloader 1.0.0` and `主菜单`. | Simplified Chinese main menu |
| 4 | `main-menu-zh-hant.png` | Traditional Chinese main menu. The line above the box says `選單語言是繁體中文`. The path label is `路徑`. The path is `/tmp/clips`. The clock is `19:48:17` on the right of that row. **1 download** is highlighted and stays `download`: "下載頁面、樣式表和指令碼." **2** stays `list downloaded`. **3** stays `serve`. **4** is `系統日誌`. **6** is `自我管理`. **7** is `語言`. **9** is `離開`. The status line says `HtmlDownloader 1.0.0` and `主選單`. | Traditional Chinese main menu |
| 5 | `main-menu-es.png` | Spanish main menu. The line above the box says `El idioma del menú es español`. The path label is `Ruta`. The path is `/tmp/clips`. The clock is `19:48:19` on the right of that row. **1 download** is highlighted and stays `download`: "descarga una página, sus hojas de estilo y sus scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `registro`. **6** is `autogestión`. **7** is `idioma`. **9** is `Salir`. The status line says `HtmlDownloader 1.0.0` and `menú principal`. | Spanish main menu |
| 6 | `main-menu-ar.png` | Arabic main menu. The line above the box says `لغة القائمة هي العربية`. The path label is `المسار`. The path is `/tmp/clips`. The clock is `19:48:22` on the right of that row. The numbers stay on the left. Arabic words on each row are shaped and read right to left. **1 download** is highlighted and stays `download`. **2** stays `list downloaded`. **3** stays `serve`. **4** is `سجل النظام`. **6** is `إدارة ذاتية`. **7** is `لغة`. **9** is `خروج`. The status line says `HtmlDownloader 1.0.0` and `القائمة الرئيسية`. | Arabic main menu |
| 7 | `main-menu-fr.png` | French main menu. The line above the box says `La langue du menu est le français`. The path label is `Chemin`. The path is `/tmp/clips`. The clock is `19:48:24` on the right of that row. **1 download** is highlighted and stays `download`: "télécharger une page, ses feuilles de style et ses scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `journal`. **6** is `autogestion`. **7** is `langue`. **9** is `Quitter`. The status line says `HtmlDownloader 1.0.0` and `menu principal`. | French main menu |
| 8 | `main-menu-pt.png` | Portuguese main menu. The line above the box says `O idioma do menu é português`. The path label is `Caminho`. The path is `/tmp/clips`. The clock is `19:48:27` on the right of that row. **1 download** is highlighted and stays `download`: "transferir uma página, as folhas de estilo e os scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `registo`. **6** is `autogestão`. **7** is `idioma`. **9** is `Sair`. The status line says `HtmlDownloader 1.0.0` and `menu principal`. | Portuguese main menu |
| 9 | `main-menu-ru.png` | Russian main menu. The line above the box says `Язык меню — русский`. The path label is `Путь`. The path is `/tmp/clips`. The clock is `19:48:29` on the right of that row. **1 download** is highlighted and stays `download`: "скачать страницу, таблицы стилей и скрипты." **2** stays `list downloaded`. **3** stays `serve`. **4** is `системный журнал`. **6** is `самоуправление`. **7** is `язык`. **9** is `Выход`. The status line says `HtmlDownloader 1.0.0` and `главное меню`. | Russian main menu |
| 10 | `main-menu-de.png` | German main menu. The line above the box says `Die Menüsprache ist Deutsch`. The path label is `Pfad`. The path is `/tmp/clips`. The clock is `19:48:32` on the right of that row. **1 download** is highlighted and stays `download`: "eine Seite, ihre Stylesheets und ihre Skripte herunterladen." **2** stays `list downloaded`. **3** stays `serve`. **4** is `Systemprotokoll`. **6** is `Selbstverwaltung`. **7** is `Sprache`. **9** is `Beenden`. The status line says `HtmlDownloader 1.0.0` and `Hauptmenü`. | German main menu |
| 11 | `main-menu-ja.png` | Japanese main menu. The line above the box says `メニューの言語は日本語`. The path label is `パス`. The path is `/tmp/clips`. The clock is `19:48:34` on the right of that row. **1 download** is highlighted and stays `download`: "ページとスタイルシートとスクリプトを取得する." **2** stays `list downloaded`. **3** stays `serve`. **4** is `システムログ`. **6** is `自己管理`. **7** is `言語`. **9** is `終了`. The status line says `HtmlDownloader 1.0.0` and `メインメニュー`. | Japanese main menu |
| 12 | `main-menu-ko.png` | Korean main menu. The line above the box says `메뉴 언어는 한국어`. The path label is `경로`. The path is `/tmp/clips`. The clock is `19:48:37` on the right of that row. **1 download** is highlighted and stays `download`: "페이지와 스타일시트와 스크립트를 받습니다." **2** stays `list downloaded`. **3** stays `serve`. **4** is `시스템 로그`. **6** is `자기관리`. **7** is `언어`. **9** is `종료`. The status line says `HtmlDownloader 1.0.0` and `주 메뉴`. | Korean main menu |
| 13 | `main-menu-nl.png` | Dutch main menu. The line above the box says `De menutaal is Nederlands`. The path label is `Pad`. The path is `/tmp/clips`. The clock is `19:48:39` on the right of that row. **1 download** is highlighted and stays `download`: "download een pagina, de stylesheets en de scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `systeemlog`. **6** is `zelfbeheer`. **7** is `taal`. **9** is `Afsluiten`. The status line says `HtmlDownloader 1.0.0` and `hoofdmenu`. | Dutch main menu |
| 14 | `main-menu-el.png` | Greek main menu. The line above the box says `Η γλώσσα του μενού είναι ελληνικά`. The path label is `Διαδρομή`. The path is `/tmp/clips`. The clock is `19:48:42` on the right of that row. **1 download** is highlighted and stays `download`: "κατέβασε μια σελίδα, τα φύλλα στυλ και τα σκριπτ." **2** stays `list downloaded`. **3** stays `serve`. **4** is `αρχείο καταγραφής`. **6** is `αυτοδιαχείριση`. **7** is `γλώσσα`. **9** is `Έξοδος`. The status line says `HtmlDownloader 1.0.0` and `κύριο μενού`. | Greek main menu |
| 15 | `self-management.png` | Row **6** has opened self-management. **61 version** is highlighted: "show the installed version." Then **62 about** "version and this computer", **63 version-check** "compare this install with pip", **64 self-update** "upgrade this package with pip", **65 self-uninstall** "remove this package with pip", **66 self-install** "install this package with pip", and **0 Back** "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:44` on the right of that row. The status line says `HtmlDownloader 1.0.0` and `self-management`. | Self-management, 61 version highlighted |
| 16 | `tui-about.png` | **about** (62) on the result page. The title is `HtmlDownloader (1.0.0) — result`. The page prints `HtmlDownloader 1.0.0`, `Domain: Download a page and its stylesheets, scripts, and images`, `Runtime tools: none`, and `Entry points: html-downloader, python -m HtmlDownloader`. The host check is stamped `2026-10-16 19:48:50.012150` and headed `[CHECK SYSTEM]:`. Visible lines include Python 3.12.11, C Library GCC 13.3.0, Ubuntu 24.04.5 LTS, amd64, the current user, the shell `/bin/bash`, Python Executable `python3`, python2 location, python3 location, a blank conda location, pyenv location, `Inside docker container: False`, and `Cython String: cpython-312-x86_64-linux-gnu`. The footer says `Up/Down scrolls this page.` and `Press a key to return to the main menu.` There is no input box and no clock. The page stays in English. | About host check, English |
| 17 | `system-log.png` | Row **4** has opened System Log. **41 view-log** is highlighted: "list a log file and show it." Then **42 clear-log** "empty one log file", **43 log-folder** "show the log folder", and **0 Back** "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:47` on the right of that row. The status line says `HtmlDownloader 1.0.0` and `System Log`. | System Log, 41 view-log highlighted |
`TP-DOC-01` asserts the Version badge token, that every PNG is linked with the absolute `https` URL above, that no markdown image uses a relative `screenshots/` destination, that the section headings are present, that the document does not name `setup.sh`, that the eight related-project URLs are in order, that the path row names the local clock, and that the user document does not name `Wilgat/VideoJoin` or `video.png`. `TP-DOC-03` asserts that each screenshot paragraph and alt equals the catalog cell, and it does not claim a pixel-by-pixel proof. `TP-DOC-03` stays **todo**. Map: `docs/reviews/test-plan.md`.

### 2.6 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The sections and every PNG in `screenshots/` are a named catalog. A later edit cannot drop the language list, leave a PNG unlinked, or swap in a drawing for a menu row.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the document. Behavior stays on the peer that already owns it.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): The pictures show the text menu a person actually drives, including row **4**, the two-file join, self-management, about, and system-log.
- **CIAO Principle 21 – Dual policies** (https://github.com/cloudgen/ciao): The portable rule is “the document matches its owner.” The VideoJoin headings and file names live in §2.5.
- **CIAO Principle 4 – Over-protect** (https://github.com/cloudgen/ciao): Do not publish a setup script that is not on disk, or a success line the program did not print.

## Under command line for normal user only

The documented install is for this login. **This requirement:** the user document **MUST NOT** tell the reader to use `sudo`, `sudo pip`, `sudo curl | sh`, or a dedicated system account. Git Bash and Windows cmd **MUST NOT** be told to invoke Termux `pkg`. The public install path is pip. A picture does not change who may run a verb.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** An install sentence that names a missing script is a defect.
- **Intentional:** An Advantages section, twenty-two pictures, one pictured join, one section order. Each picture paragraph is the catalog cell for that file.
- **Anti-fragile:** A new PNG in `screenshots/` becomes a required link in the same change. A non-menu file stays labeled as itself.
- **Over-protect (Principle 20):** Do not let the user document become a second menu, a second verb list, or a second encode procedure.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Restate encode order, verb lists, menu numbers, language codes, or the prerequisite table in this file as a second procedure.
- Turn the Advantages section into an FFmpeg filter recipe. The concat graph may be named only as something the person does not write.
- Claim that intermediate files never use the system temporary directory.
- Replace a capture with a drawing that invents row text.
- Leave any PNG in `screenshots/` out of `README.md`.
- Use a relative `screenshots/` destination for a picture in this package description. The package index cannot fetch that path. A sibling-document link such as `LICENSE.md` may stay relative.
- Put a picture of a removed verb into `screenshots/` and describe it as this program.
- Caption a picture with only a language name, or with a sentence that does not say what the picture shows.
- Describe the path row’s right side as `Current` or a login.
- Name `./setup.sh` while that file is absent.
- Add `./build.sh` verbs, a shell online install, `sudo pip`, or `sudo curl | sh` to the user document.
- Add `--json`, a length percent, a boomerang, or a folder prompt.
- Freeze a session login or a `/home/<login>/` path in this file.
- Mark `TP-DOC-03` have before the suite asserts that each catalog paragraph and alt equals the cell in §2.5.
- Treat `./build.sh` verbs as `video-join` verbs.

## 5. Definition of done

1. `README.md` has the sections in §2.5, in that order, including Advantages after Features and Screenshots after Usage.
2. The Version badge token matches the package string.
3. The Screenshots section links every PNG in `screenshots/`, in catalog order. Each image destination is an absolute `https` URL. Each heading is the basename. Each paragraph and each image alt are the catalog cells for that file.
4. The path-row sentence names the local clock.
5. The document does not name `setup.sh`, `sudo pip`, or a shell online install.
6. Related Projects lists the eight URLs in §2.5, in that order.
7. `TP-DOC-01` is **have** in `tests/test_docs.py` (`./tests/run.sh`, 7 tests, OK). `TP-DOC-03` stays **todo** until the suite asserts that each paragraph and alt equals the catalog cell.

### Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-DOC-01** Version badge matches the package string. Every PNG uses the absolute `https` URL. No relative `screenshots/` image. Section headings. No `setup.sh`. Eight related-project URLs in order. The path row names the local clock. The user document does not name `Wilgat/VideoJoin` or `video.png` | `tests/test_docs.py` | have |
| **TP-DOC-03** Each screenshot paragraph and alt equals the catalog cell in §2.5 | `tests/test_docs.py` | todo |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `docs/requirements/index.md` | Registry |
| `requirement-python-project-structure` | Root `README.md` exists. Sections and pictures are this file |
| `requirement-domain-videojoin` | Domain rows inside the user document |
| `requirement-video-ffmpeg-pipeline` | Stream copy, then re-encode. This file does not restate that procedure |
| `requirement-runtime-prerequisites` | FFmpeg on `PATH`. No root auto-install |
| `requirement-python-packaging` | Package name, console script, pip install, `ChronicleLogger>=1.3.1` |
| `requirement-python-tui` | Menu picture and the clock |
| `requirement-python-about` | The about picture. This file does not own the page |
| `requirement-python-cli-language` | Row **4** and the thirteen codes. About stays English |
| `requirement-python-cli-interface` | Product verbs the document lists. `hello` is one of them |
| `requirement-python-coding-style` | `shutil.move` for the published file |
| `requirement-class-software-dev` | Class residual |
| `README.md` | The user document |
| `screenshots/` | The captures |
| `docs/reviews/test-plan.md` | `TP-DOC-01` and `TP-DOC-03` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | User-document sections, Advantages, eight related projects, and twenty-two pictures. Image destinations are absolute `https`. `TP-DOC-01` have. `TP-DOC-03` todo |
| 2026-10-04 | Active 1.0.1 | About and self-management pictures match the new page. Other menu pictures still show **1.0.4**. Package string is **1.0.5** |

---

**Last Updated**: 2026-10-04
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
