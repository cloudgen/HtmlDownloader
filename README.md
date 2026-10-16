# HtmlDownloader - Download a page from the command line and from the text menu

![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/cloudgen/HtmlDownloader?style=flat-square)](https://github.com/cloudgen/HtmlDownloader)
[![Python](https://img.shields.io/badge/Python-2.7%2B%20(3.x%20recommended)-blue?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/v/HtmlDownloader?style=flat-square)](https://pypi.org/project/HtmlDownloader/)

HtmlDownloader downloads one HTML page and the stylesheets, scripts, and images that page links to. The typed verb `download` saves that page. Menu row **1 download** lists pages saved earlier, or accepts a URL. Menu row **2 list downloaded** lists saved page names, then opens the chosen page in Visual Studio Code or the default browser.

On a terminal, starting it with no arguments opens a text menu. The menu does not download a page by itself, and it does not call pip. It does not join media, call an external encoder, or list files in the folder.

## Features

- Text menu on a terminal: **download**, **list downloaded**, **serve**, **System Log**, **self-management**, **language**, and **Exit**
- The first row shows the current folder and a local clock (`HH:MM:SS`) when the row has room
- Numbered rows line up. A rounded input box sits along the bottom, as wide as the terminal, with the name and version on the status line under the box
- **download** (1) lists saved `page name: URL` pairs, or accepts a URL and a page name. The typed verb `download --url URL --name PAGENAME` saves the page and does not draw the menu. A later run keeps `index.html` and fills in files that are still missing
- **list downloaded** (2) lists saved page names by number. After a page is chosen, **21 edit** opens `index.html` in Visual Studio Code when the `code` command or the Visual Studio Code desktop entry is installed, and **22 view** opens it in the default browser when one is set. A missing tool is left off that menu. **0** returns to the page list, then to the main menu
- **serve** (3) lists saved page names by number, then asks for a port. An empty port uses **5000**. The page folder is served at `http://127.0.0.1:<port>/` until Ctrl+C. The typed verb `serve --page-name PAGENAME` does the same without the menu. `--port` changes the port
- The page is `~/.app/HtmlDownloader/output/<pagename>/index.html`. Linked stylesheets go in `output/<pagename>/assets/css/`. Linked scripts go in `output/<pagename>/assets/js/`. Linked images go in `output/<pagename>/assets/img/`. Those three folders stay flat, with no subfolders. Font files sit in `assets/css/`. When `index.html` is already there, the page is not downloaded again. Missing stylesheets, scripts, and images are fetched. Files already saved are kept.
- **System Log** (4) opens view-log, clear-log, and log-folder. **self-management** (6) opens version, about, and the pip lifecycle rows. **language** (7) picks the menu language
- Console script `html-downloader` and module entry `python -m HtmlDownloader`
- Typed verbs: `help`, `version`, `about`, `download`, `serve`, `self-install`, `version-check`, `self-update`, `self-uninstall`

## Advantages

1. **Two ways to download.** `html-downloader download --url URL --name PAGENAME` saves the page in the terminal and does not draw the menu. On the menu, row **1 download** lists saved pages by number, or accepts a URL. With no arguments on a terminal, the text menu opens and waits. With no terminal and no verb, the program prints help and returns 0. There is no `--json`.
2. **Built-in languages.** Row **7** lists thirteen languages: English, Simplified Chinese, Traditional Chinese, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Dutch, and Greek. The choice is saved in `~/.local/HtmlDownloader/language` for the next run. `HTMLDOWNLOADER_LANG` overrides that file for one process and does not write it. The download verb stays English. The note on row 1 follows the menu language.
3. **Lifecycle and diagnostics.** `version-check`, `self-update`, `self-install`, and `self-uninstall` are menu rows **63**–**66** and typed verbs. `self-uninstall` on the command line needs `--force`. They call pip and do not use root. **System Log** (**4**) views a log, clears a log, and shows the log folder. **about** (**62**) stays in English.

## Quick Installation

**Python dependency:** `ChronicleLogger>=1.3.1` (required). Pip installs it with HtmlDownloader. No external media tool is required.

### PyPI (registry)

```bash
pip install HtmlDownloader
```

This installs the console entry **`html-downloader`** and the package **`HtmlDownloader`**. Packaging name SSOT is `pyproject.toml` `[project].name` = `HtmlDownloader`. This tree is **1.0.0**. The PyPI badge above shows the live index.

### Local install (checkout)

From a checkout (editable / unreleased work):

```bash
git clone https://github.com/cloudgen/HtmlDownloader.git
cd HtmlDownloader
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e .
```

### Main menu

After install, on a terminal, `html-downloader` with no arguments prints this screen. The verb is bold and the note after the colon is italic. `9` leaves. `0` on a submenu goes back. After a command finishes, the main menu is shown again. A number that is not on the list prints an error and lets you choose again.

Picture of the English menu. Current directory `/tmp/clips`. The rows are the text the menu paints. The frame is the 80-column box.

```text
$ html-downloader
Path: /tmp/clips                                                       12:06:45

1. **download**       : *download a page and its stylesheets, scripts, and images*
2. **list downloaded**: *show saved page names*
3. **serve**          : *serve a saved page on this computer*
4. **System Log**     : *view, clear, and the log folder*
6. **self-management**: *version, about, and pip lifecycle*
7. **language**       : *display language for this menu*
9. **Exit**           : *leave*




╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  HtmlDownloader 1.0.0  │  main menu  │  Up/Down  •  Enter
```

**System Log** (4). Numbers 44–49 are not printed.

```text
Path: /tmp/clips                                                       12:06:45

41. **view-log**  : *list a log file and show it*
42. **clear-log** : *empty one log file*
43. **log-folder**: *show the log folder*
 0. **Back**      : *return to the main menu*




╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  HtmlDownloader 1.0.0  │  System Log  │  Up/Down  •  Enter
```

**language** (7). The short on each language row is that language’s own name. Numbers 84–98 are not printed. `0` goes back and does not save.

```text
Path: /tmp/clips                                                       12:06:46

71. **English**   : *use English for this menu*
72. **简体中文**      : *use 简体中文 for this menu*
73. **繁體中文**      : *use 繁體中文 for this menu*
74. **Español**   : *use Español for this menu*
75. **العربية**   : *use العربية for this menu*
76. **Français**  : *use Français for this menu*
77. **Português** : *use Português for this menu*
78. **Русский**   : *use Русский for this menu*
79. **Deutsch**   : *use Deutsch for this menu*
80. **日本語**       : *use 日本語 for this menu*
81. **한국어**       : *use 한국어 for this menu*
82. **Nederlands**: *use Nederlands for this menu*
83. **Ελληνικά**  : *use Ελληνικά for this menu*
 0. **Back**      : *return to the main menu*

╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  HtmlDownloader 1.0.0  │  language  │  Up/Down  •  Enter
```

**self-management** (6). Numbers 67–70 are not printed.

```text
Path: /tmp/clips                                                       14:05:09

61. **version**       : *show the installed version*
62. **about**         : *version and this computer*
63. **version-check** : *compare this install with pip*
64. **self-update**   : *upgrade this package with pip*
65. **self-uninstall**: *remove this package with pip*
66. **self-install**  : *install this package with pip*
 0. **Back**          : *return to the main menu*

╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  HtmlDownloader 1.0.0  │  self-management  │  Up/Down  •  Enter
```

Choose a number, or type the command name in the box. The block caret appears in that box while it is focused.

## Usage

```bash
html-downloader
# or
python -m HtmlDownloader
```

On a terminal, that opens the main menu above. It does not download a page yet, and it does not call pip. With no terminal, the same command prints help and returns 0.

**download** (1) stays on the menu. It lists saved `page name: URL` rows. Type a number to download that pair again, or type an `http://` or `https://` URL and then a page name. The typed verb does not draw the menu:

```bash
html-downloader download --url https://example.com/ --name example
```

That writes `~/.app/HtmlDownloader/output/example/index.html`, puts linked stylesheets in `output/example/assets/css/`, linked scripts in `output/example/assets/js/`, and linked images in `output/example/assets/img/`. Each of those folders is a single layer. The saved page points at those local files. A `<base>` tag or an `xml:base` attribute is removed so local links stay on the saved page. A canonical link and HTML comments are removed too. The pair is remembered in `~/.app/HtmlDownloader/output/url-map.json`. Running the same command again leaves `index.html` in place and downloads only the stylesheets, scripts, and images that are not already in the page folder.

**list downloaded** (2) lists those page names by number. Choose one, then **21 edit** opens `index.html` in Visual Studio Code when `code` is installed, and **22 view** opens it in the default browser when a default browser is set. If either tool is missing, that row is not shown. **0** goes back.

**serve** (3) lists those page names by number. Choose one, then type a port. Press Enter with an empty box to use **5000**. The server listens on `127.0.0.1` and stops on Ctrl+C. The menu then shows `Stopped <name>.` The typed verb does not draw the menu:

```bash
html-downloader serve --page-name example
html-downloader serve --page-name example --port 8080
```

That serves `~/.app/HtmlDownloader/output/example/` so `http://127.0.0.1:5000/` is `index.html` and `assets/` stays beside it.

```bash
html-downloader help
html-downloader version
html-downloader about
html-downloader download --url https://example.com/ --name example
html-downloader serve --page-name example
html-downloader version-check
html-downloader self-update
html-downloader self-install
html-downloader self-uninstall --force
```

`version` prints `HtmlDownloader 1.0.0` and does not call pip. `about` shows one English page: the product identity, a host check of this computer, and a star box. It does not call pip. `download` saves the page and does not draw the menu. `help` prints usage.

`version-check` runs `python -m pip index versions HtmlDownloader`. `self-update` runs `python -m pip install --upgrade HtmlDownloader`. `self-install` runs `python -m pip install HtmlDownloader`. `self-uninstall` runs `python -m pip uninstall -y HtmlDownloader` and needs `--force` on the command line. Those pip verbs do not use sudo. Empty arguments do not install or update.

Exit codes: non-zero for an unknown verb, a failed download, a failed serve, a pip failure, or a menu that cannot open. Menu **Exit** (9) returns 0. A saved page returns 0. Ctrl+C on `serve` returns 0.

Import for scripts (thin entry):

```python
from HtmlDownloader import main
# interactive session; a terminal opens the text menu
```

## Screenshots

Each heading is the file name. The paragraph is what that picture shows: the words on the screen and the characters in the input box. Package **1.0.0**. These pictures were captured from the running text menu in `/tmp/clips`. On each menu picture the input box shows `>` and no typed text, and **1 download** or the first row of that board is highlighted. The package index can fetch a picture only after that file is on the public `main` branch.

### `language-menu.png`

Row **7** has opened the language list. **71 English** is highlighted, with the note "use English for this menu." The other rows are **72 简体中文**, **73 繁體中文**, **74 Español**, **75 العربية**, **76 Français**, **77 Português**, **78 Русский**, **79 Deutsch**, **80 日本語**, **81 한국어**, **82 Nederlands**, and **83 Ελληνικά**. Each note says to use that language for this menu. **0 Back** says "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:09` on the right of that row. The status line says `HtmlDownloader 1.0.0` and `language`.

![Language list, 71 English highlighted](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/language-menu.png)

### `main-menu-en.png`

English main menu. There is no saved-language line above the box. The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:12` on the right of that row. **1 download** is highlighted: "download a page and its stylesheets, scripts, and images." Then **2 list downloaded** "show saved page names," **3 serve** "serve a saved page on this computer," **4 System Log** "view, clear, and the log folder," **6 self-management** "version, about, and pip lifecycle," **7 language** "display language for this menu," and **9 Exit** "leave." The status line says `HtmlDownloader 1.0.0` and `main menu`.

![English main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-en.png)

### `main-menu-zh-hans.png`

Simplified Chinese main menu. The line above the box says `菜单语言是简体中文`. The path label is `路径`. The path is `/tmp/clips`. The clock is `19:48:14` on the right of that row. **1 download** is highlighted and stays `download`: "下载页面、样式表和脚本." **2** stays `list downloaded`. **3** stays `serve`. **4** is `系统日志`. **6** is `自我管理`. **7** is `语言`. **9** is `离开`. The status line says `HtmlDownloader 1.0.0` and `主菜单`.

![Simplified Chinese main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-zh-hans.png)

### `main-menu-zh-hant.png`

Traditional Chinese main menu. The line above the box says `選單語言是繁體中文`. The path label is `路徑`. The path is `/tmp/clips`. The clock is `19:48:17` on the right of that row. **1 download** is highlighted and stays `download`: "下載頁面、樣式表和指令碼." **2** stays `list downloaded`. **3** stays `serve`. **4** is `系統日誌`. **6** is `自我管理`. **7** is `語言`. **9** is `離開`. The status line says `HtmlDownloader 1.0.0` and `主選單`.

![Traditional Chinese main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-zh-hant.png)

### `main-menu-es.png`

Spanish main menu. The line above the box says `El idioma del menú es español`. The path label is `Ruta`. The path is `/tmp/clips`. The clock is `19:48:19` on the right of that row. **1 download** is highlighted and stays `download`: "descarga una página, sus hojas de estilo y sus scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `registro`. **6** is `autogestión`. **7** is `idioma`. **9** is `Salir`. The status line says `HtmlDownloader 1.0.0` and `menú principal`.

![Spanish main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-es.png)

### `main-menu-ar.png`

Arabic main menu. The line above the box says `لغة القائمة هي العربية`. The path label is `المسار`. The path is `/tmp/clips`. The clock is `19:48:22` on the right of that row. The numbers stay on the left. Arabic words on each row are shaped and read right to left. **1 download** is highlighted and stays `download`. **2** stays `list downloaded`. **3** stays `serve`. **4** is `سجل النظام`. **6** is `إدارة ذاتية`. **7** is `لغة`. **9** is `خروج`. The status line says `HtmlDownloader 1.0.0` and `القائمة الرئيسية`.

![Arabic main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-ar.png)

### `main-menu-fr.png`

French main menu. The line above the box says `La langue du menu est le français`. The path label is `Chemin`. The path is `/tmp/clips`. The clock is `19:48:24` on the right of that row. **1 download** is highlighted and stays `download`: "télécharger une page, ses feuilles de style et ses scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `journal`. **6** is `autogestion`. **7** is `langue`. **9** is `Quitter`. The status line says `HtmlDownloader 1.0.0` and `menu principal`.

![French main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-fr.png)

### `main-menu-pt.png`

Portuguese main menu. The line above the box says `O idioma do menu é português`. The path label is `Caminho`. The path is `/tmp/clips`. The clock is `19:48:27` on the right of that row. **1 download** is highlighted and stays `download`: "transferir uma página, as folhas de estilo e os scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `registo`. **6** is `autogestão`. **7** is `idioma`. **9** is `Sair`. The status line says `HtmlDownloader 1.0.0` and `menu principal`.

![Portuguese main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-pt.png)

### `main-menu-ru.png`

Russian main menu. The line above the box says `Язык меню — русский`. The path label is `Путь`. The path is `/tmp/clips`. The clock is `19:48:29` on the right of that row. **1 download** is highlighted and stays `download`: "скачать страницу, таблицы стилей и скрипты." **2** stays `list downloaded`. **3** stays `serve`. **4** is `системный журнал`. **6** is `самоуправление`. **7** is `язык`. **9** is `Выход`. The status line says `HtmlDownloader 1.0.0` and `главное меню`.

![Russian main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-ru.png)

### `main-menu-de.png`

German main menu. The line above the box says `Die Menüsprache ist Deutsch`. The path label is `Pfad`. The path is `/tmp/clips`. The clock is `19:48:32` on the right of that row. **1 download** is highlighted and stays `download`: "eine Seite, ihre Stylesheets und ihre Skripte herunterladen." **2** stays `list downloaded`. **3** stays `serve`. **4** is `Systemprotokoll`. **6** is `Selbstverwaltung`. **7** is `Sprache`. **9** is `Beenden`. The status line says `HtmlDownloader 1.0.0` and `Hauptmenü`.

![German main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-de.png)

### `main-menu-ja.png`

Japanese main menu. The line above the box says `メニューの言語は日本語`. The path label is `パス`. The path is `/tmp/clips`. The clock is `19:48:34` on the right of that row. **1 download** is highlighted and stays `download`: "ページとスタイルシートとスクリプトを取得する." **2** stays `list downloaded`. **3** stays `serve`. **4** is `システムログ`. **6** is `自己管理`. **7** is `言語`. **9** is `終了`. The status line says `HtmlDownloader 1.0.0` and `メインメニュー`.

![Japanese main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-ja.png)

### `main-menu-ko.png`

Korean main menu. The line above the box says `메뉴 언어는 한국어`. The path label is `경로`. The path is `/tmp/clips`. The clock is `19:48:37` on the right of that row. **1 download** is highlighted and stays `download`: "페이지와 스타일시트와 스크립트를 받습니다." **2** stays `list downloaded`. **3** stays `serve`. **4** is `시스템 로그`. **6** is `자기관리`. **7** is `언어`. **9** is `종료`. The status line says `HtmlDownloader 1.0.0` and `주 메뉴`.

![Korean main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-ko.png)

### `main-menu-nl.png`

Dutch main menu. The line above the box says `De menutaal is Nederlands`. The path label is `Pad`. The path is `/tmp/clips`. The clock is `19:48:39` on the right of that row. **1 download** is highlighted and stays `download`: "download een pagina, de stylesheets en de scripts." **2** stays `list downloaded`. **3** stays `serve`. **4** is `systeemlog`. **6** is `zelfbeheer`. **7** is `taal`. **9** is `Afsluiten`. The status line says `HtmlDownloader 1.0.0` and `hoofdmenu`.

![Dutch main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-nl.png)

### `main-menu-el.png`

Greek main menu. The line above the box says `Η γλώσσα του μενού είναι ελληνικά`. The path label is `Διαδρομή`. The path is `/tmp/clips`. The clock is `19:48:42` on the right of that row. **1 download** is highlighted and stays `download`: "κατέβασε μια σελίδα, τα φύλλα στυλ και τα σκριπτ." **2** stays `list downloaded`. **3** stays `serve`. **4** is `αρχείο καταγραφής`. **6** is `αυτοδιαχείριση`. **7** is `γλώσσα`. **9** is `Έξοδος`. The status line says `HtmlDownloader 1.0.0` and `κύριο μενού`.

![Greek main menu](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/main-menu-el.png)

### `self-management.png`

Row **6** has opened self-management. **61 version** is highlighted: "show the installed version." Then **62 about** "version and this computer", **63 version-check** "compare this install with pip", **64 self-update** "upgrade this package with pip", **65 self-uninstall** "remove this package with pip", **66 self-install** "install this package with pip", and **0 Back** "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:44` on the right of that row. The status line says `HtmlDownloader 1.0.0` and `self-management`.

![Self-management, 61 version highlighted](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/self-management.png)

### `tui-about.png`

**about** (62) on the result page. The title is `HtmlDownloader (1.0.0) — result`. The page prints `HtmlDownloader 1.0.0`, `Domain: Download a page and its stylesheets, scripts, and images`, `Runtime tools: none`, and `Entry points: html-downloader, python -m HtmlDownloader`. The host check is stamped `2026-10-16 19:48:50.012150` and headed `[CHECK SYSTEM]:`. Visible lines include Python 3.12.11, C Library GCC 13.3.0, Ubuntu 24.04.5 LTS, amd64, the current user, the shell `/bin/bash`, Python Executable `python3`, python2 location, python3 location, a blank conda location, pyenv location, `Inside docker container: False`, and `Cython String: cpython-312-x86_64-linux-gnu`. The footer says `Up/Down scrolls this page.` and `Press a key to return to the main menu.` There is no input box and no clock. The page stays in English.

![About host check, English](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/tui-about.png)

### `system-log.png`

Row **4** has opened System Log. **41 view-log** is highlighted: "list a log file and show it." Then **42 clear-log** "empty one log file", **43 log-folder** "show the log folder", and **0 Back** "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `19:48:47` on the right of that row. The status line says `HtmlDownloader 1.0.0` and `System Log`.

![System Log, 41 view-log highlighted](https://raw.githubusercontent.com/cloudgen/HtmlDownloader/main/screenshots/system-log.png)

## Examples

```bash
html-downloader
```

```bash
html-downloader version
```

`version` prints `HtmlDownloader 1.0.0` and does not call pip. A run that is not the text menu can also print ChronicleLogger status lines above that. The text menu keeps those lines off the screen.

```bash
html-downloader download --url https://example.com/ --name example
```

That saves the page and does not draw the menu. On a terminal, row **1** lists saved pages or accepts a URL.

## Platform Compatibility

| Platform | Status |
|----------|--------|
| Linux | Primary; tested development path |
| macOS | Supported when CPython is on PATH |
| Windows | Supported when CPython is on PATH (venv activate differs) |
| Architectures | Any with CPython |

The text menu needs a terminal. With no terminal and no verb, the program prints help and returns 0. It does not wait.

## Related Projects

- [HtmlDownloader on GitHub](https://github.com/cloudgen/HtmlDownloader) — this program’s source
- [HtmlDownloader on PyPI](https://pypi.org/project/HtmlDownloader/) — this program on PyPI
- [AnimeDlp](https://github.com/Wilgat/AnimeDlp) — command-line downloader for anime video sites
- [ChronicleLogger](https://github.com/Wilgat/ChronicleLogger) — status logger this program depends on (`ChronicleLogger>=1.3.1`)
- [VideoSpeed](https://github.com/Wilgat/VideoSpeed) — cuts, changes speed, and boomerangs a clip. That program is not this one
- [CIAO](https://github.com/cloudgen/ciao) — Caution, Intentional, Anti-fragile, Over-engineered
- [CIAO-Lite](https://github.com/cloudgen/ciao-lite) — short agent contract
- [safe-rm](https://github.com/cloudgen/safe-rm) — guarded `rm`

## Contributing

1. Keep product law under `docs/requirements/` in sync when behavior changes.
2. Prefer small, CIAO-safe changes. Do not put media joining, an external encoder, or a file listing back without an explicit design.
3. Version dual SSOT: bump **`pyproject.toml`** and **`src/HtmlDownloader/__init__.__version__`** together.
4. Open issues and pull requests on GitHub.

## License

MIT — see [`LICENSE.md`](./LICENSE.md). Also declared in `pyproject.toml`.

## Last Update

2026-10-16 — **1.0.0**. Public source is https://github.com/cloudgen/HtmlDownloader. The console script is `html-downloader`. `download --url URL --name PAGENAME` saves the page under `~/.app/HtmlDownloader/output/`. Menu row 1 **download** lists saved pages or accepts a URL. Menu pictures show this board: language **71**–**83**, one main menu for each language, self-management **61**–**66**, about, and System Log **41**–**43**. Product law under `docs/requirements/` names this version and this menu. Version badge matches `pyproject.toml` and `__version__`. `ChronicleLogger>=1.3.1` is required.
