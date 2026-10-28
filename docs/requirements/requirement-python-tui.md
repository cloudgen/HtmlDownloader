**file**: docs/requirements/requirement-python-tui.md
**Status**: Active (Version 1.3.5)
**Area**: python
**Key**: `requirement-python-tui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the picture of HtmlDownloader’s text menu. The screen has two parts on one board: the menu, and a bottom input box. The first row of the menu region keeps the current path on the left and, when that row has room, a clock of the local time on the right. That clock is drawn again each second. It does not show the product name or the package version. That picture is the default TUI style.

The session is class `Tui` in `src/HtmlDownloader/tui.py`. The frame is class `MenuPainter` in `src/HtmlDownloader/menu_painter.py`. Those homes are `requirement-python-oop`. `def main` stays in `src/HtmlDownloader/cli.py`. Class `Cli` constructs `Tui` and passes this product’s name, version, and front board into that session. `cli.py` does not keep a second frame painter. The product does not import another menu package.

Which verb runs stays on `requirement-python-cli-interface`. Download, list, and serve stay on `requirement-domain-htmldownloader`. This program does not call an encoder. Status lines stay on `requirement-python-cli-logging`.

Class `Tui` and class `MenuPainter` are on disk. The default path label is English `Path`. `MenuPainter` stores `路徑`. `requirement-python-cli-language` selects the word. This file does not detect a language. A menu column is a display column. East Asian Wide and Fullwidth count as two. Ambiguous stays one. `TP-TUI-09` and `TP-TUI-10` have. `TP-TUI-01` through `TP-TUI-08` stay todo.

### 1.1 Human-facing

**In one sentence:** On a terminal, `html-downloader` with no arguments shows a numbered menu and, along the bottom, a rounded box as wide as the screen, and you type on the only line inside that box.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person at the keyboard | `html-downloader` |
| The other role | The session and the painter | class `Tui` in `tui.py`; class `MenuPainter` in `menu_painter.py` |
| Not this file | The page folder and the serve bind | The domain file |

| Includes | Excludes |
|----------|----------|
| The menu region above the box, and the rounded three-row frame | A `Choice:` line, `print` / `read`, or `input()` for that menu |
| The first row: Path and the folder on the left; a local clock on the right when the row has room, drawn again each second | The product name and the version on that first row. They stay on the status line |
| UTF-8 arc corners and bars, full screen width, typing on the only inner line | Frame glyphs copied into `cli.py`, and a menu pip wheel |
| The status line under the frame, and this product’s front rows (download, list downloaded, serve, System Log, self-management, language, Exit) | Putting the numbered rows inside the frame. Rows 5 and 8 are omitted |

| Surface | What you open | What for |
|---------|---------------|----------|
| `html-downloader` on a terminal | Text screen | Menu above, input box on the bottom, status line on the last row |
| `src/HtmlDownloader/cli.py` | `def main` and class `Cli` | Builds the session. Does not paint the frame |
| `src/HtmlDownloader/tui.py` | class `Tui` | Session loop |
| `src/HtmlDownloader/menu_painter.py` | class `MenuPainter` | Frame and columns |
| `html-downloader` with no terminal | Help text | No screen and no wait. Exit 0 |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal with no words | You see download, list downloaded, serve, System Log, self-management, language, and Exit. The program does not download a page yet and does not run pip. The bottom of the screen is one rounded box, then a status line. | `html-downloader` |
| Read the first row | The left side names the folder this process is in. The word before that colon is Path until a saved language selects another word. When the row has room, the right side is a clock of the local time, hours, minutes, and seconds. It moves once a second while this board is showing. The name and the version stay on the status line under the box. | `html-downloader` |
| Choose download | The screen stays up. The menu lists saved pages or accepts a URL and a page name, then asks for an HTML file name. An empty page name keeps the saved name, or the folder recommended from the URL. An empty HTML file name keeps the stored name, or the file recommended from the URL. Each answer is typed in the same bottom box. Esc returns to the menu. | `1` then Enter |
| Choose view-log | The screen lists the log files and waits in the bottom box. It stays until you type a file number and Enter, or press Esc. A pause does not send you back to the System Log board. | `4`, then `41` |
| Start with no terminal | Help text and exit 0. The program does not draw the box and does not wait. | `html-downloader` with no terminal |

## 2. Core Rules (Mandatory)

1. **Package writer.** The text-menu session **MUST** be class `Tui` in `src/HtmlDownloader/tui.py`. The frame **MUST** be drawn by class `MenuPainter` in `src/HtmlDownloader/menu_painter.py` (`requirement-python-oop`). HtmlDownloader **MUST** pass its product name, package version, and front board into that session. `cli.py` **MUST NOT** contain the frame glyphs (`FRAME_TOP_LEFT` belongs to `MenuPainter`). The product **MUST NOT** import `py_tui` and **MUST NOT** declare `py-tui`. The menu **MUST NOT** be drawn with `print` / `read` / `input()` or a `Choice:` line. After **download**, **list downloaded**, or **serve** is chosen, those questions stay on this same screen: the question text is in the menu region, and the answer is typed in the same bottom box. Those questions **MUST NOT** close the screen or use `input()`.
2. **Two regions.** On the front board the writer **MUST** draw a menu region and a bottom input box on the same screen. The menu region is every row above the box. Its first row **MUST** be the path line in rule 13. That row **MUST NOT** show the product name or the package version. The numbered rows for that board **MUST** follow the path line. Those rows **MUST NOT** be drawn inside the box. Each numbered row is a number, a verb, and an explain. On that board the number field is as wide as the longest number, and a shorter number is padded with spaces on the left. The verb field is as wide as the longest verb on that same board, and a shorter verb is padded with spaces immediately before the colon. The explain **MUST** be drawn after exactly one space. Those widths are display columns. East Asian Wide and Fullwidth count as two columns. Ambiguous stays one column. The next write on that row starts at the display column after the text already placed. A wide character that does not fit is dropped whole. This board uses its own widths. HtmlDownloader’s front board is the one in Implementation Notes: **1** download, **2** list downloaded, **3** serve, **4** System Log, **6** self-management, **7** language, **9** Exit. Rows **5** and **8** are omitted. **MUST NOT** renumber the printed rows to close those gaps. Row **4** **MUST** open the System Log board. That board **MUST** list **41** view-log, **42** clear-log, **43** log-folder, and **0** Back. Numbers **44**–**49** are not printed. Row **7** **MUST** open the language board. The codes and the words stay on `requirement-python-cli-language`. `language` is not an argv verb. Row **6** **MUST** open the self-management board. That board **MUST** list **61** version, **62** about, **63** version-check, **64** self-update, **65** self-uninstall, **66** self-install, and **0** Back. Numbers **67**–**70** are not printed. `help` **MUST** stay off every numbered row. The front board **MUST NOT** list version, about, the pip verbs, view-log, clear-log, or log-folder.
3. **Three-row frame plus status line.** The bottom input box **MUST** be exactly three terminal rows high: a top border, one inner row, and a bottom border. The status line **MUST** be the next row, and that row **MUST** be the last row of the screen. The frame **MUST** span the full width of the screen. The left border is the first column. The right border is the last column the screen writer can place. There **MUST** be no blank column before the left border or after the right border.
4. **UTF-8 frame.** Those three rows **MUST** be drawn with these UTF-8 box-drawing characters. Each one occupies one column. ASCII `+`, `-`, and `|` **MUST NOT** stand in for them. Sharp corners `┌` `┐` `└` `┘` **MUST NOT** stand in for the arcs.

| Row of the box | Characters, left to right |
|----------------|---------------------------|
| Top | `╭` (U+256D), then `─` (U+2500) repeated, then `╮` (U+256E) |
| Inner | `│` (U+2502), then the input field, then `│` (U+2502) |
| Bottom | `╰` (U+2570), then `─` (U+2500) repeated, then `╯` (U+256F) |

5. **Input inside the frame.** One space, the mark `> `, the typed characters, and the caret **MUST** sit on the only inner line, strictly between the two `│` characters. The mark, the typed characters, and the caret **MUST NOT** sit on the top border, the bottom border, or a menu row. When the box is focused, the caret **MUST** be the block `█` (U+2588) at the caret index on that inner line. When the list is focused, that block **MUST NOT** be drawn. Up and Down **MUST** walk the numbered rows and the box: Down on the last row enters the box, Up on the first row enters the box, Up from the box returns to the last row, and Down from the box returns to the first row. Enter **MUST** run the typed token, or the highlighted row when the box is empty. The box **MUST NOT** be a `Choice:` line.
6. **This board’s actions.** **download** (**1**) **MUST** list saved pages or accept a URL and a page name. An empty page name **MUST** keep the saved name for that URL, or the folder recommended from the URL. It **MUST** then ask for an HTML file name. An empty answer keeps the stored HTML file name, or the file recommended from the URL. The typed verb `html-downloader download` saves the page and **MUST NOT** draw this screen. **list downloaded** (**2**) **MUST** list saved page names, then **21** edit and **22** view when those tools are installed. **serve** (**3**) **MUST** list saved page names, then ask for a port. An empty port uses **5000** and the server listens on `127.0.0.1`. **self-management** (**6**) **MUST** open that board and **MUST NOT** leave the program. On that board, **version** (**61**) **MUST** show the installed `__version__` and **MUST NOT** call pip. **about** (**62**) **MUST** show the result page. The page body is `requirement-python-about`: identity, the host check, and the star box. The domain sentence stays on `requirement-domain-htmldownloader`. That page **MUST NOT** name `py-tui`. When the page is longer than the screen, Up and Down scroll it. The footer says `Up/Down scrolls this page.` and `Press a key to return to the main menu.` **version-check** (**63**) **MUST** run `python -m pip index versions HtmlDownloader`. **self-update** (**64**) **MUST** run `python -m pip install --upgrade HtmlDownloader`. **self-uninstall** (**65**) **MUST** run `python -m pip uninstall -y HtmlDownloader`. Choosing that row is the confirmation. **self-install** (**66**) **MUST** run `python -m pip install HtmlDownloader`. Those pip commands **MUST NOT** use `sudo` and **MUST NOT** use `curl`. **0** **MUST** return to the front board. **System Log** (**4**) **MUST** open that board and **MUST NOT** leave the program. **view-log** (**41**) **MUST** list the `.log` file names in the log folder and **MUST** show the chosen file on a result page. The person picks the number in the bottom box. That list **MUST** stay until the person chooses a number or presses Esc. The one-second clock wait from rule 13 **MUST NOT** close it. A pause longer than one second **MUST** keep the characters already typed. The result page **MUST** be the file name, a blank line, then the file text. An empty file **MUST** show `(empty)` in place of that text. Esc **MUST** return to the system-log board and **MUST NOT** show the file. When the folder has no `.log` file, the result page **MUST** be `No log file in <folder>.` **clear-log** (**42**) **MUST** list those same names, then ask `Clear <name>? (y/n)` in the bottom box. That list and that question **MUST** stay until the person answers or presses Esc. The one-second clock wait **MUST NOT** close them. Yes **MUST** empty that file and **MUST NOT** delete it. The result page **MUST** be `Cleared <name>.` No, Esc, or Enter **MUST** leave the file unchanged and **MUST NOT** show a result page. **log-folder** (**43**) **MUST** show `Log folder: <path>`, where `<path>` is the absolute path `logDir()` returns. When no logger is present, that page **MUST** be `No log folder.` This row **MUST NOT** type a folder ladder and **MUST NOT** create a directory. Rows 41, 42, and 43 are menu actions. They are not product verbs. Typing the short name on an open screen **MUST** run that row. Before the read and before the empty, the program **MUST** call `log_message` with the operation and the path, component `menu`, level INFO (`requirement-python-cli-logging`). The read line **MUST** be `read log path=<path>`. The empty line **MUST** be `clear log path=<path>`. The call **MUST NOT** sit inside `isDebug()`. A chosen path **MUST** be a regular `.log` file whose parent, after resolve, is that log folder. **Exit** (**9**) **MUST** leave the program and return 0. It **MUST NOT** ask `Exit? (y/n)`. An unknown token **MUST** stay on this board and show an error line in the menu region above the box. It **MUST NOT** exit the process. A typed product verb (`requirement-python-cli-interface`) **MUST** enter that action without a front-board pick. Choosing row 1 **MUST** start download. `about` **MUST** open its result page. `html-downloader download` **MUST NOT** draw this screen. `version` **MUST** print the installed version and **MUST NOT** call pip and **MUST NOT** draw this screen. `version-check`, `self-update`, and `self-install` **MUST** run the pip command above and **MUST NOT** open this screen. `self-uninstall` on the command line **MUST** require `--force` and **MUST NOT** open this screen. The command `help` **MUST NOT** draw this screen. Typing `help` on an open screen **MUST** show a result page and **MUST NOT** add a numbered help row. Empty argv on a terminal **MUST** show the front board and **MUST NOT** run self-install or self-update and **MUST NOT** download a page by itself.
7. **Status line and errors.** The status line under the frame **MUST** show the product name, the version from `__version__`, the board title, and the key hint `Up/Down  •  Enter`, separated by `│`. It **MUST NOT** replace one of the three frame rows. An error line, when shown, **MUST** sit in the menu region above the box.
8. **Result page.** After about, after a download result, after a log action, or after another result page, the result page may omit the menu rows, the box, and the status line until the next key returns to the previous board. When the body is longer than the room under the title, Up and Down scroll that body and the footer says `Up/Down scrolls this page.` A one-line result still closes on Down.
9. **Too small or no terminal.** If the screen cannot hold the path line from rule 13 (a path shortened to fit still counts), at least one numbered menu row, the three-row box, and the status line, or cannot hold both corners plus the mark and one cell between them, the program **MUST NOT** collapse the box into one unframed row and **MUST NOT** fall back to a `Choice:` line. It **MUST** fail closed: non-zero, an operator-readable line, and the next step `html-downloader help`. If stdout is not a terminal and argv is empty, the program **MUST** print help and return 0 (`requirement-python-cli-interface`). It **MUST NOT** draw this screen and **MUST NOT** wait. `hello`, `join`, and `list-videos` are not verbs. An unknown verb **MUST** exit non-zero.
10. **One writer.** The screen writer **MUST NOT** become a second logger. A run that is not a text-screen verb **MUST NOT** open this screen. While **download** or **serve** is on this screen, its questions and job lines **MUST** be drawn by class `Tui` calling class `MenuPainter`. They **MUST NOT** be `print` / `input()` lines that close the screen.
11. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`. This file does **not** add an actor requirement.
12. Dest fence conditions: **considered — none**. Do not invent one.
13. **Path line.** The first row of the menu region, on the front board, on the self-management board, on the system-log board, and on the language board, **MUST** be the path line. The shape **MUST** be `<label>: <current path>`, with one space after the colon. `<current path>` **MUST** be the absolute current working directory at the moment that board is painted. The path **MUST NOT** be translated. The product name and the package version **MUST NOT** appear on this row. They stay on the status line (rule 7). The label is one translatable message. `requirement-python-cli-language` selects the language and owns the word. English, the default, is `Path`. Traditional Chinese is `路徑`. This file does not detect the language, and it does not invent a second line shape. The path line is also the first row of the language board. When the path text is wider than the screen, the writer **MUST** keep the path label, the colon, and the space, and **MUST** shorten the path from the left so that field fits on one row. A wide character that does not fit is dropped whole. The screen **MUST** still open.

The same row **MUST** carry a clock on the right when the row has room. The clock **MUST** be the local time of this machine at the moment that row is drawn. The shape **MUST** be `HH:MM:SS`: hours, minutes, and seconds, each two digits, 24-hour, zero-padded, separated by colons. Eight characters. No date. No timezone name. No label before the clock. The clock **MUST NOT** be translated. At least two spaces **MUST** separate the path text from the clock. When both fields fit with those two spaces, the path field **MUST** stay at the left and the clock **MUST** end on the last column the writer can place. That fit, that width, and that last column are display columns. East Asian Wide and Fullwidth count as two. Ambiguous stays one. When both do not fit, the writer **MUST** keep the path field, including the shorten-from-the-left rule above, and **MUST NOT** draw the clock. When no width is known, the row **MUST** be the path field, then two spaces, then the clock. The writer **MUST NOT** read `USER`, `USERNAME`, or `getpass` for this row, and **MUST NOT** run `id`.

While the front board, the self-management board, the system-log board, or the language board is showing, the session **MUST** wait at most one second for the next key. When that wait ends and no key arrived, the session **MUST** draw this row again with the local time at that moment and **MUST** wait again. That wait **MUST NOT** leave the program, **MUST NOT** change the highlighted row, the typed buffer, or the board, and **MUST NOT** drop a key that arrived during the wait. The session **MUST NOT** start a thread to move the clock. A screen that cannot arm this wait keeps the key read it already had. A result page, a download question, a page list, a port question, a notice that waits for a key, the view-log file list, the clear-log file list, and the clear confirm keep the product title on row 0. They do not draw this clock, and they do not use this one-second wait. Before each key read on those questions, the session **MUST** clear that wait. A no-key from the one-second wait **MUST NOT** be read as Esc there. The question **MUST** stay until the person answers or presses Esc. A pause longer than one second **MUST** keep the characters already typed. The clock redraw **MUST NOT** be a log line. The clock wait is not Esc and is not row 9 Exit.

14. **Control-C is not row 9.** This file does not own Control-C. Row **9** Exit leaves with no confirm question and returns 0. A clock redraw **MUST NOT** leave the program.

Picture of this board. The box in the picture is 16 columns wide so the corners stay visible. On a real screen those 16 columns become the full width, and the menu stays above the frame. The block in the picture is the focused caret. `14:05:09` is a sample local time. `1.1.1` is the current package version and moves with `__version__`.

```text
Path: /tmp/clips                                              14:05:09

1. download       : download a page and its stylesheets, scripts, and images
2. list downloaded: show saved page names
3. serve          : serve a saved page on this computer
4. System Log     : view, clear, and the log folder
6. self-management: version, about, and pip lifecycle
7. language       : display language for this menu
9. Exit           : leave
╭──────────────╮
│ > █          │
╰──────────────╯
  HtmlDownloader 1.1.1  │  main menu  │  Up/Down  •  Enter
```

The same first row when `requirement-python-cli-language` has selected Traditional Chinese:

```text
路徑: /tmp/clips                                              14:05:09
```

The spaces in those pictures stand for the gap that grows on a wider screen. The clock ends on the last column the writer can place. When the row cannot hold both fields, the picture of that row is the path field alone.

### Screen parts

This screen has seven parts. The three artifacts below name them. Caption cells and the image address stay on `requirement-python-readme`. This product does not download an AI model and does not convert images.

#### Components list

| Part | What it is |
|------|------------|
| Navigation | The numbered rows on the current board. The front board prints **1** download, **2** list downloaded, **3** serve, **4** System Log, **6** self-management, **7** language, and **9** Exit. System Log prints **41**–**43** and **0** Back. Self-management prints **61**–**66** and **0** Back. Language prints **71**–**83** and **0** Back. Rows **5** and **8** are omitted |
| Status | The line under the frame: product name, the version from `__version__`, the board title, and the hint `Up/Down  •  Enter` |
| Major input | The only inner line of the three-row box, where the person types |
| Major output | The menu region above the box: the path row, the numbered rows, an error line, and a result page when a result replaces those rows |
| Path display | The first row of the menu region: the path label, a colon, and the absolute current working directory |
| System-time display | The local clock on the right of that same path row when the row has room |
| Time-consuming process messages | The job lines drawn while row **1** download or serve stays on this screen. They are not a waiting sentence for an AI-model download or an image conversion |

#### Style guide

| Part | Where it sits | Display style |
|------|---------------|---------------|
| Navigation | Menu region, under the path row, never inside the box | Number, verb, and explain. The number is padded on the left to the longest number on that board. The verb is padded with spaces before the colon. One space, then the explain. Widths are display columns. East Asian Wide and Fullwidth count as two. Ambiguous stays one |
| Status | The row after the three-row box. That row is the last row of the screen | Plain text separated by `│`. It does not replace one of the three frame rows. Sample shape: `HtmlDownloader <version> │ main menu │ Up/Down  •  Enter` |
| Major input | The only inner row, between the two `│` characters | A space, then `> `, then the typed characters. When the box is focused, the caret is the block `█`. The frame is `╭` `─` `╮` / `│` / `╰` `─` `╯`. It is not a `Choice:` line |
| Major output | Menu region above the box. A result page may omit the rows, the box, and the status line until the next key | Drawn by class `Tui` calling class `MenuPainter`. Not `print` and not `input()` |
| Path display | First row of the menu region on the front board, self-management, System Log, and the language board | `<label>: <path>` with one space after the colon. The default label is `Path`. Traditional Chinese is `路徑`. The path is not translated. A path wider than the screen is shortened from the left. The product name and the version stay off this row |
| System-time display | Right end of that same path row | `HH:MM:SS`, 24-hour, zero-padded, eight characters, no date and no timezone name. At least two spaces separate it from the path. It is omitted when both fields do not fit. On those four boards it is drawn again each second. A result page, a download question, a page list, a port question, and a notice that waits for a key do not draw it |
| Time-consuming process messages | Menu region, while row **1** download or serve is working on this screen | Job lines from rule 10, drawn by class `Tui` through class `MenuPainter`. The screen stays open. A finished download then uses the result page in rule 8. This product does not show a waiting sentence for an AI-model download or an image conversion |

#### Storyboard

Each row names the action that opens a capture already in `screenshots/`. Download in progress, the saved-page list, and serve have no capture on disk, so they are not rows.

| Order | Action that opens the capture | Capture |
|------:|--------------------------------|---------|
| 1 | Empty argv on a terminal opens the English main menu | `main-menu-en.png` |
| 2 | Row **7** opens the language list | `language-menu.png` |
| 3 | Choosing **72** opens the Simplified Chinese main menu | `main-menu-zh-hans.png` |
| 4 | Choosing **73** opens the Traditional Chinese main menu | `main-menu-zh-hant.png` |
| 5 | Choosing **74** opens the Spanish main menu | `main-menu-es.png` |
| 6 | Choosing **75** opens the Arabic main menu | `main-menu-ar.png` |
| 7 | Choosing **76** opens the French main menu | `main-menu-fr.png` |
| 8 | Choosing **77** opens the Portuguese main menu | `main-menu-pt.png` |
| 9 | Choosing **78** opens the Russian main menu | `main-menu-ru.png` |
| 10 | Choosing **79** opens the German main menu | `main-menu-de.png` |
| 11 | Choosing **80** opens the Japanese main menu | `main-menu-ja.png` |
| 12 | Choosing **81** opens the Korean main menu | `main-menu-ko.png` |
| 13 | Choosing **82** opens the Dutch main menu | `main-menu-nl.png` |
| 14 | Choosing **83** opens the Greek main menu | `main-menu-el.png` |
| 15 | Row **6** opens self-management | `self-management.png` |
| 16 | Row **62** about opens the about page | `tui-about.png` |
| 17 | Row **4** opens System Log | `system-log.png` |

### Sample code

The front board, the self-management board, the system-log board, and the language board arm a one-second wait in `MenuSession.wait_key`. A question and a notice clear that wait before the key read. A no-key from the clock is not Esc. `TP-TUI-09` does not prove this wait. `TP-TUI-01` through `TP-TUI-08` stay todo.

```python
# Boards that draw the clock. A no-key redraws the clock. It is not Esc.
screen.timeout(1000)
key = screen.getch()

# Download questions, notices, and file lists. Clear the one-second wait first.
screen.timeout(-1)
key = screen.getch()
```

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Command** | `html-downloader` |
| **Open the screen** | `html-downloader` or `python -m HtmlDownloader` on a terminal, with no verb |
| **Direct verb** | `html-downloader download` saves a page and does not draw this screen. `html-downloader serve` serves a page and does not draw this screen. `html-downloader about` opens the result page. `help`, `version`, and the pip verbs do not draw this screen |
| **Session** | Class `Tui` in `src/HtmlDownloader/tui.py` |
| **Painter** | Class `MenuPainter` in `src/HtmlDownloader/menu_painter.py`. Stores `Path` and `路徑`. `path_label` returns the word `requirement-python-cli-language` selected. English is the default |
| **Caller** | Class `Cli` in `src/HtmlDownloader/cli.py`. `def main` stays in that file. Empty argv on a terminal opens class `Tui` |
| **Front rows** | **1** download; **2** list downloaded; **3** serve; **4** System Log; **6** self-management; **7** language; **9** Exit. Rows 5 and 8 are omitted |
| **System Log rows** | **41** `view-log`; **42** `clear-log`; **43** `log-folder`; **0** `Back`. Numbers 44–49 are not printed. These rows are not product verbs |
| **Language rows** | **71**–**83** and **0** Back. Numbers 84–98 are not printed. Codes, the leaf, and the words are `requirement-python-cli-language` |
| **Self-management rows** | **61** `version`; **62** `about`; **63** `version-check` (`python -m pip index versions HtmlDownloader`); **64** `self-update` (`python -m pip install --upgrade HtmlDownloader`); **65** `self-uninstall` (`python -m pip uninstall -y HtmlDownloader`); **66** `self-install` (`python -m pip install HtmlDownloader`); **0** `Back`. Numbers 67–70 are not printed. `help` is typed, not numbered |
| **download / list / serve** | Stay on the screen. Download lists saved pages or accepts a URL. List downloaded opens edit or view when the tool is installed. Serve asks for a port and uses 5000 when the answer is empty. Esc returns to the previous board |
| **about** | Row **62**. Result page from `requirement-python-about`, composed by class `AboutPage`. The domain sentence stays on the domain file. Omits the frame. Does not name `py-tui`. Up and Down scroll when the page is longer than the screen |
| **Box height** | 3 terminal rows, then one status row |
| **Box width** | Full width the writer can place. Left border at column 0 |
| **Mark inside the frame** | one space, then `> ` |
| **Caret when the box is focused** | `█` U+2588 on the inner row |
| **Top line** | Left: `<label>: <absolute current working directory>`. Right, when the row has room: local time `HH:MM:SS`. Same first row on the front board, the self-management board, the system-log board, and the language board. Product name and version stay on the status line |
| **Path label** | English `Path` by default. Traditional Chinese `路徑` when the language requirement selects `zh-Hant`. The path value is not translated. This file does not detect the language |
| **Worked Traditional Chinese top line** | `路徑: /tmp/clips` then a gap, then `14:05:09` flush right |
| **Clock wait** | One second on those four boards. No thread. Questions and file lists do not use this wait. A no-key is not Esc and is not Exit |
| **Status line** | `  HtmlDownloader <version>  │  main menu  │  Up/Down  •  Enter` |
| **External menu package** | Not imported and not declared |
| **No terminal, empty argv** | Help text, return 0 |
| **No terminal, download or serve** | Those verbs still run. They do not draw this screen |
| **Too small** | Non-zero. Next step `html-downloader help` |
| **Privilege** | normal user. Pip rows do not use sudo |
| **Proof** | `TP-TUI-09` and `TP-TUI-10` have. `TP-TUI-01` through `TP-TUI-08` stay todo |

16-column inner line, focused and empty: `│ > █          │`

Invocation samples for the rows this file owns:

```text
html-downloader
7
73
```

```text
html-downloader
6
61
```

```text
html-downloader version
html-downloader version-check
html-downloader self-update
html-downloader self-install
html-downloader self-uninstall --force
```

`html-downloader` on a terminal is the front board. `7` then `73` saves Traditional Chinese. `4` then `41` is view-log. `6` then `61` is version and does not call pip. The typed pip lines do not open this screen.

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional**: The menu and the box are two named regions. The session is `Tui`. The frame is `MenuPainter`. The first row keeps the folder on the left and the local clock on the right.
- **CIAO Principle 16 – Interactive**: A process with no terminal never draws the screen, so it cannot wait inside the box. Empty argv in that case prints help and returns 0.
- **CIAO Principle 1 – Caution**: A screen too small to hold the frame fails closed. A number that is not on the list does not download.
- **CIAO Principle 5 – SSOT**: This file owns the picture. Verb names also live on `requirement-python-cli-interface`. Download, list, and serve live on `requirement-domain-htmldownloader`.
- **CIAO Principle 10 – Least privilege**: Pip rows use `python -m pip` as the normal user.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The frame is three rows plus the status line, or the screen does not open.
- **Intentional:** Typing happens on the only inner line. The front rows are download, list downloaded, serve, System Log, self-management, language, and Exit.
- **Anti-fragile:** The right border uses the last column the writer can place, and the left border stays on column 0.
- **Over-protect:** Do not replace the frame with a single underlined row, and do not fork the painter into `cli.py`.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Collapse the bottom input box to one row.
- Draw the frame with ASCII `+`, `-`, or `|`, or with sharp corners `┌` `┐` `└` `┘`.
- Put the typed text, the caret, or `> ` on a border line or on a menu row.
- Inset the box so a blank column remains on the left or the right.
- Draw the numbered menu rows inside the three-row frame.
- Draw this menu with `print` / `read` / `input()` or a `Choice:` line.
- Close the screen when **download** or **serve** is chosen and continue those questions with `input()`.
- Ask for a working-directory folder in order to download a page.
- Copy the frame glyphs into `cli.py`.
- Declare `py-tui`, or import `py_tui`.
- Renumber the front board to fill omitted rows 5 and 8.
- Hide row 6 while rows 61–66 are claimed.
- Run pip from empty argv, or run pip with `sudo` or `curl`.
- Treat the one-second clock wait as Esc or as row 9 Exit.
- Translate the folder path or the clock. The path word belongs to `requirement-python-cli-language`. English is `Path`. Traditional Chinese is `路徑`.
- Count a menu column with `len()` when the text can contain an East Asian Wide or Fullwidth character. The next write starts at the display column after the cells already drawn. Wide and Fullwidth count as two. Ambiguous stays one. A wide character that does not fit is dropped whole.
- Detect a language in this file. `requirement-python-cli-language` selects the language.
- Add `Exit? (y/n)` to row 9, or invent a Control-C protocol in this file.
- Mark `TP-TUI-*` have while `src/` still uses `input()`.

**Violating this rule is a critical menu regression.**

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the person runs `html-downloader` as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to open the menu or to run rows 63–66. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`. Pip rows call `python -m pip` only.

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Empty argv on a terminal opens the front board and does not download a page and does not run pip |
| AC-2 | Front rows are 1 download, 2 list downloaded, 3 serve, 4 System Log, 6 self-management, 7 language, 9 Exit. Rows 5 and 8 stay omitted |
| AC-3 | Self-management lists 61–66 and 0 Back. version does not call pip. Pip rows do not use sudo or curl |
| AC-4 | System Log lists 41, 42, 43, and 0 Back. Those rows are not product verbs |
| AC-5 | Download, list, and serve questions stay in the bottom box. Esc returns to the previous board |
| AC-6 | Empty argv with no terminal prints help and returns 0. `download` and `serve` do not draw this screen |
| AC-7 | The frame uses the arc glyphs. `cli.py` does not contain them. `py_tui` is not imported |
| AC-8 | The default path label is `Path`. The painter stores `路徑`. `requirement-python-cli-language` selects the word. The path and the clock are not translated |
| AC-9 | A wide short stays whole. The colon starts at the display column after that short. A wide path label keeps the clock on that row when both fields fit |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-cli-interface` | Typed verbs and empty-argv contract |
| `requirement-domain-htmldownloader` | Download, list, serve, and the about domain sentence |
| `requirement-python-cli-language` | Menu language, front row 7, and the path word |
| `requirement-python-oop` | Class homes for `Tui`, `MenuPainter`, `MenuSession`, `MenuLanguage` |
| `requirement-python-cli-logging` | Quiet mirror. view-log and clear-log lines |
| `requirement-python-error-handling` | Fail-closed sentences |
| `requirement-python-packaging` | Package name `HtmlDownloader` on the pip rows |
| `requirement-class-software-dev` | Actor residual. No new actor file |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-TUI-01** | `tests/test_tui.py` | todo | Empty argv on a tty opens the front board. It does not download and does not run pip |
| **TP-TUI-02** | `tests/test_tui.py` | todo | Empty argv off a tty prints help and returns 0 |
| **TP-TUI-03** | `tests/test_download.py` | have | Row 1 is download. The questions stay on the screen |
| **TP-TUI-04** | `tests/test_language.py` | have | Self-management is row 6 and lists 61–66 and 0 Back |
| **TP-TUI-05** | `tests/test_language.py` | have | System Log is row 4 and lists 41, 42, 43, and 0 Back |
| **TP-TUI-06** | `tests/test_tui.py` | todo | No `print` / `input()` / `Choice:` menu. No `py_tui`. Frame glyphs are absent from `cli.py` |
| **TP-TUI-07** | `tests/test_download.py` | have | `download` does not draw this screen |
| **TP-TUI-08** | `tests/test_tui.py` | todo | Path line and clock on the four boards. No thread. A no-key is not Esc and is not Exit |
| **TP-TUI-09** | `tests/test_tui.py` | have | With no language file, the label is `Path`. `路徑` is stored. `LANG` does not switch the label. The path and the clock are not translated |
| **TP-TUI-10** | `tests/test_tui.py` | have | Wide and Fullwidth count as two columns. The colon starts after that width. The four wide path labels keep the clock on the row |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## Terminologies

**Project requirements.** Product law is the finished must/should rules for this product. They are complete for this product. They are not blank forms, not agent procedures, and not a glossary.

**Daily-life example:** “This household must lock the door by 10” is law for this house. A blank curfew form in a stationery shop is not.

**Major TUI entry point.** The major entry of a claimed text screen is interactive mode with no positional command word. A flag that is not a command stays on that entry. A verb opens the screen only when this requirement names that verb for the screen.

**Daily-life example:** You walk in and name no dish. That board is the major entry. You name a dish. That order stays at the board only when the card already names that dish for the board.

**Default TUI style.** The full-screen look of this text menu. One writer draws a menu region and a bottom input box. The first menu row is the path line, with a local clock on the right when the row has room. The box is a rounded frame exactly three terminal rows high. The product name and the version sit on the status line under the box.

**Daily-life example:** On the lunch board the top line names the folder you are standing in, and the clock `14:05:09` ends at the right edge. A second later the clock shows the new local time and the dishes have not moved.

**Well-known menu.** The shared numbered membership of a text menu: reserved row numbers, a front Exit, and a self-management board. Which rows this product prints are the rows in this file. Rows 5 and 8 are omitted and are not renumbered.

**Daily-life example:** Similar kitchens agree on room numbers. Help is a word you say, not a numbered dish. This shop prints the rooms named in this file.

**Python CLI verb default route.** For a Python command, each routed verb’s default route is the terminal: standard output, standard error, and a scriptable run, with no text screen. A verb uses the text screen only when this requirement names that verb for the screen. The major entry with no command word stays the text screen.

**Daily-life example:** You write one dish name on a slip. The default route is the plain counter, so a checker can read the slip without the board. A dish stays at the board only when the card already says that dish is served there.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | Text menu for HtmlDownloader. Front board is join, system-log, self-management, Exit. Ship unit still uses `input()` |
| 2026-10-04 | Active 1.1.0 | Path label words are English `Path` and Traditional Chinese `路徑`. English stays in force until a multi-language environment requirement is Active. `TP-TUI-09` has |
| 2026-10-04 | Active 1.1.1 | Purpose, sample, and implementation notes match the session on disk. `TP-TUI-01` through `TP-TUI-08` stay todo |
| 2026-10-04 | Active 1.2.0 | Front row 4 is language. System-log moves to row 3 and children 31–33. The language requirement selects the path word. `TP-TUI-01` through `TP-TUI-08` stay todo |
| 2026-10-04 | Active 1.2.1 | Menu columns are display columns. Wide and Fullwidth count as two. Ambiguous stays one. `TP-TUI-10` has. `./tests/run.sh`: 6 tests, OK |
| 2026-10-04 | Active 1.2.2 | Row 83 shows `requirement-python-about`. A long result page scrolls. Product version in the sample is **1.0.5** |
| 2026-10-16 | Active 1.3.0 | Front board is download, list downloaded, serve, System Log, self-management, language, and Exit. Sample version is **1.0.0** |
| 2026-10-28 | Active 1.3.1 | Menu row 1 asks for an HTML file name after the page name. An empty answer keeps the stored name, or `index.html` |
| 2026-10-28 | Active 1.3.2 | An empty page name keeps the folder recommended from the URL. The HTML file question uses that recommendation too |
| 2026-10-28 | Active 1.3.3 | The sample status line is package **1.1.0** |
| 2026-10-28 | Active 1.3.4 | Components list, style guide, and storyboard of the captures already on disk. Terminologies added |
| 2026-10-28 | Active 1.3.5 | The sample status line is package **1.1.1** |

---

**Last Updated**: 2026-10-28
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
