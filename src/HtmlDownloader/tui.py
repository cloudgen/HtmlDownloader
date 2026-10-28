# =============================================================================
# Text menu session for HtmlDownloader.
# requirement-python-tui — menu region and the bottom input box.
# requirement-python-about — the about result page is framework_about.
# requirement-python-oop — this module defines class Tui and MenuScreenError.
# The frame is class MenuPainter. cli.py constructs Tui and calls it.
# =============================================================================
from __future__ import annotations

import curses
import os

from .menu_painter import MenuPainter
from .menu_session import MenuSession
from .page_download import PageDownload, PageDownloadError
from .page_open import PageOpen, PageOpenError
from .page_serve import PageServe, PageServeError
from .system_log import SystemLog



class MenuScreenError(Exception):
    """The terminal cannot hold the menu and the framed input box."""

    def __init__(self, message="", logger=None):
        super().__init__(message)
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuScreenError")


class Tui:
    """Text menu session. Download and the front board stay on this screen.

    MenuModel, MenuSession, and MenuPainter live in their own modules.
    The rows are download, list downloaded, serve, System Log, self-management,
    language, and Exit. List downloaded is row 2. Serve is row 3.
    System Log is row 4 and its list is 41–43. Self-management is row 6 and
    its list is 61–66. Language is row 7 and its list is 71–83.
    """

    def __init__(self, app=None, app_name="HtmlDownloader", version=None, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Tui")
        self.app = app
        self.app_name = app_name
        if version is None:
            from . import __version__
            version = __version__
        self.version = version
        self.painter = MenuPainter(logger=logger)
        self.system_log = SystemLog(logger=logger)

    def _name(self):
        if self.app is not None:
            return self.app.app_name
        return self.app_name

    def _ver(self):
        if self.app is not None:
            return self.app.version
        return self.version

    def front_lines(self):
        """General Purpose: Path line and the front board rows."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("front")
        )

    def self_lines(self):
        """General Purpose: Path line and the self-management board under 6."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("self")
        )

    def log_lines(self):
        """General Purpose: Path line and the System Log board under 4."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("log")
        )

    def language_lines(self):
        """General Purpose: Path line and the language board under 7."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("lang")
        )

    def help_on_screen(self):
        """
        General Purpose: Help text when help is typed on the open menu.
        The typed html-downloader help verb does not call this and does not draw the screen.
        """
        name = self._name()
        return (
            "help: usage for {0}.\n"
            "Verbs: help, version, about, download, serve, "
            "self-install, version-check, self-update, self-uninstall.\n"
            "version shows the installed version and does not call pip.\n"
            "about shows the about page.\n"
            "download saves one page. On the command line it needs --url.\n"
            "--name is the page folder. Omit it when the URL ends with .html, .htm,\n"
            "or a folder name such as xxx. --html names the HTML file. An empty --html\n"
            "keeps a stored name, or the name taken from the URL.\n"
            "It does not draw this menu. Menu row 1 download lists saved pages\n"
            "or accepts a URL, then a page name, then an HTML file name.\n"
            "An empty page name keeps the saved name, or the name from the URL.\n"
            "Menu row 2 list downloaded lists saved page names.\n"
            "After a page is chosen, 21 edit opens it in Visual Studio Code when\n"
            "code is installed, and 22 view opens it in the default browser when\n"
            "one is set. A tool that is not installed is left off that menu.\n"
            "serve serves one saved page on 127.0.0.1. On the command line it needs\n"
            "--page-name. --port defaults to {1}. Menu row 3 serve lists saved page\n"
            "names, then asks for a port. An empty port uses {1}.\n"
            "Each page is ~/.app/{0}/output/<name>/<html file>.\n"
            "The HTML file defaults to index.html.\n"
            "This program does not join media or list files in this folder.\n"
            "version-check runs: python -m pip index versions {0}\n"
            "self-update runs: python -m pip install --upgrade {0}\n"
            "self-install runs: python -m pip install {0}\n"
            "self-uninstall runs: python -m pip uninstall -y {0}\n"
            "On the command line, self-uninstall also needs --force.\n"
            "Empty arguments on a terminal open this menu and do not run pip."
        ).format(name, PageServe.DEFAULT_PORT)

    def about_text(self):
        """General Purpose: The about page body from AboutPage.framework_about."""
        if self.app is None:
            return ""
        return self.app.about.framework_about()

    def _visible_lines(self, lines, room, pin_last):
        """Lines that fit above the input box. A question pins its last line."""
        if room < 1:
            return []
        if len(lines) <= room:
            return list(lines)
        if not pin_last:
            return list(lines[-room:])
        if room == 1:
            return [lines[-1]]
        return list(lines[: room - 2]) + ["…", lines[-1]]

    def _paint_lines(self, screen, model, title, lines, pin_last):
        """Hand one question to MenuPainter. The session does not draw a second frame."""
        self.painter.paint_prompt(
            screen,
            model,
            title,
            lines,
            pin_last,
            self._name(),
            self._ver(),
            self._visible_lines,
        )

    def _arm_blocking(self, screen):
        """Clear the one-second clock wait. A no-key from that wait is not Esc."""
        arm = getattr(screen, "timeout", None)
        if arm is not None:
            arm(-1)

    def read_key(self, screen, model, lines, title="menu"):
        """
        General Purpose: Read one line from the bottom input box.

        Returns the text, or None when the person presses Esc. The board's
        one-second clock wait is cleared before each key.
        """
        model.buffer = ""
        model.cursor = 0
        model.focus = "input"
        while True:
            self._paint_lines(screen, model, title, lines, pin_last=True)
            self._arm_blocking(screen)
            key = screen.getch()
            if key in (-1, 27):
                model.error = ""
                model.buffer = ""
                model.cursor = 0
                model.focus = "list"
                return None
            if key in (10, 13, curses.KEY_ENTER):
                text = model.buffer
                model.buffer = ""
                model.cursor = 0
                model.error = ""
                return text
            if key in (curses.KEY_BACKSPACE, 127, 8):
                model._backspace()
                model.error = ""
                continue
            if key in (curses.KEY_LEFT, curses.KEY_RIGHT) or key in model.edge_keys():
                model._slide(key)
                continue
            if key in (curses.KEY_UP, curses.KEY_DOWN):
                continue
            if 32 <= key < 127:
                model._insert(chr(key))
                model.error = ""
                continue

    def notice(self, screen, model, lines, title="result", closing=None):
        """General Purpose: Show lines until the next key. The clock wait is cleared."""
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        if closing is None:
            closing = "Press a key to return to the main menu."
        body = list(lines) + ["", closing]
        self._paint_lines(screen, model, title, body, pin_last=True)
        self._arm_blocking(screen)
        try:
            screen.getch()
        except Exception:
            return

    def _read_yes_no(self, screen, model, lines, title="System Log"):
        """y/n from the box. Esc returns None. Empty is no."""
        while True:
            raw = self.read_key(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip().lower()
            if raw == "" or raw in ("n", "no"):
                return False
            if raw in ("y", "yes"):
                return True
            model.error = "Please enter y or n"

    def _read_index(self, screen, model, lines, count, title="System Log"):
        """1-based index from the box. Ask again on a bad value. Esc returns None."""
        while True:
            raw = self.read_key(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip()
            try:
                idx = int(raw)
            except ValueError:
                model.error = "Please type a number"
                continue
            if 1 <= idx <= count:
                return idx - 1
            model.error = "Enter 1–{0}".format(count)

    def about_on_screen(self, screen=None, model=None):
        """
        General Purpose: Show the about page.
        With no screen, open the text screen when this is the direct verb.
        """
        text = self.about_text()
        if screen is not None and model is not None:
            self.notice(screen, model, text.splitlines() or [""], title="about")
            return 0
        if self.app is not None and self.app.stdout_is_tty():
            return self.open_direct("about")
        return text

    def _screen_error(self, too_small):
        if self.app is None:
            return "missing"
        if too_small:
            self.app.report_error(
                "The text screen is too small for the menu and the input box.",
                "{0} help".format(self.app.CONSOLE_NAME),
            )
        else:
            self.app.report_error(
                "The text menu could not open on this terminal.",
                "{0} help".format(self.app.CONSOLE_NAME),
            )
        return "missing"

    def _require_terminal(self):
        if self.app is None or not self.app.stdout_is_tty():
            if self.app is not None:
                self.app.report_error(
                    "No terminal for the text menu. Use a terminal.",
                    "{0} help".format(self.app.CONSOLE_NAME),
                )
            return False
        return True

    def open_text_menu(self):
        """
        General Purpose: Draw the front board. Does not download a page
        and does not run pip. Returns "missing" when the screen cannot open.
        """
        if not self._require_terminal():
            return "missing"
        try:
            import curses
        except ImportError:
            return self._screen_error(False)

        screen_box = {}

        def on_kind(kind):
            if kind == "help":
                return self.help_on_screen()
            if kind == "download":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._download_on_screen(screen, session.model)
            if kind == "list-downloaded" or kind.startswith("saved-") or kind in ("edit-page", "view-page"):
                return self._saved_page_action(kind, session.model)
            if kind == "serve" or kind.startswith("serve-saved-"):
                return self._serve_on_screen(kind, screen_box.get("screen"), session.model)
            if kind in ("version-check", "self-update", "self-install", "self-uninstall"):
                _code, text = self.app.self_manage.run_pip(kind)
                return text
            if kind == "view-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._view_log(screen, session.model)
            if kind == "clear-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._clear_log(screen, session.model)
            if kind == "log-folder":
                return self._log_folder()
            return None

        session = MenuSession(
            self._name(),
            self._ver(),
            on_version=lambda: self.app.self_manage.local_version(),
            on_about=self.about_text,
            boards=None,
            on_kind=on_kind,
            logger=self.logger,
            painter=self.painter,
        )

        def _wrapped(screen):
            screen_box["screen"] = screen
            session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            return self._screen_error(True)
        except Exception:
            return self._screen_error(False)
        return None

    def open_direct(self, kind):
        """
        General Purpose: Open the text screen on about.
        Does not start on the front board. Returns a process status.
        """
        if not self._require_terminal():
            return 1
        try:
            import curses
        except ImportError:
            self._screen_error(False)
            return 1

        code_box = {"code": 0}
        session = MenuSession(
            self._name(),
            self._ver(),
            on_version=lambda: self.app.self_manage.local_version(),
            on_about=self.about_text,
            boards=None,
            on_kind=lambda _kind: None,
            logger=self.logger,
            painter=self.painter,
        )

        def _wrapped(screen):
            try:
                if kind != "about":
                    code_box["code"] = 1
                    return
                code_box["code"] = self.about_on_screen(screen, session.model)
            except Exception as exc:
                self.notice(
                    screen, session.model, ["ERROR: {0}".format(exc)],
                    closing="Press a key to close.",
                )
                code_box["code"] = 1
            session.leave_to_front()
            # Esc and a finished page return to the front board.
            if code_box["code"] == 0:
                session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            self._screen_error(True)
            return 1
        except Exception:
            self._screen_error(False)
            return 1
        return code_box["code"]

    def _download_on_screen(self, screen, model):
        """List saved pages, or accept a URL, a page name, and an HTML file name."""
        worker = PageDownload(self._name(), logger=self.logger)
        while True:
            raw = self.read_key(screen, model, worker.choice_lines(), title="download")
            if raw is None:
                return None
            kind, value = worker.interpret(raw)
            if kind == "error":
                model.error = value
                continue
            if kind == "page":
                url = value["url"]
                name = value["name"]
                default_html = value.get("html") or PageDownload.INDEX_NAME
            else:
                url = value
                name = self._ask_page_name(screen, model, worker, url)
                if name is None:
                    return None
                default_html = worker.suggested_html(url, name)
            html_name = self._ask_html_name(screen, model, worker, default_html)
            if html_name is None:
                return None
            self._please_wait(screen, model, name, html_name)
            try:
                return worker.download(url, name, html_name)
            except PageDownloadError as exc:
                return "ERROR: {0}".format(exc)

    def _please_wait(self, screen, model, name, html_name):
        """Clear the input box and show Please wait before the download runs."""
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        model.notice = ""
        self._paint_lines(
            screen,
            model,
            "download",
            [
                "Page name: {0}".format(name),
                "HTML file: {0}".format(html_name),
                "",
                "Please wait.",
            ],
            pin_last=True,
        )

    def _saved_page_action(self, kind, model):
        """List saved page names, then edit or view the chosen page."""
        if kind == "list-downloaded":
            return self._open_downloaded(model)
        if kind.startswith("saved-"):
            return self._open_saved_page(model, kind)
        if kind == "edit-page":
            return self._edit_saved_page()
        if kind == "view-page":
            return self._view_saved_page()
        return None

    def _open_downloaded(self, model):
        """Show the numbered page names. An empty list is a result page."""
        worker = PageDownload(self._name(), logger=self.logger)
        pages = worker.saved_pages()
        if not pages:
            return "No saved pages."
        language = self.painter.language
        rows = []
        self._saved_by_kind = {}
        for index, page in enumerate(pages, start=1):
            kind = "saved-{0}".format(index)
            self._saved_by_kind[kind] = page
            rows.append((index, self._page_label(page), page["url"], kind))
        rows.append((
            0,
            language.row_short("back", "Back"),
            language.row_long("back", "return to the main menu"),
            "back",
        ))
        if model.boards is None:
            model.boards = {}
        model.boards["pages"] = tuple(rows)
        model.layer = "pages"
        model.phase = "board"
        model.index = 0
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        model.notice = ""
        return None

    def _action_rows(self, opener):
        """21 edit and 22 view. A missing tool is left out. 0 returns to the list."""
        language = self.painter.language
        rows = []
        available = opener.actions()
        if "edit" in available:
            rows.append((21, "edit", language.text("edit_long"), "edit-page"))
        if "view" in available:
            rows.append((22, "view", language.text("view_page_long"), "view-page"))
        rows.append((
            0,
            language.row_short("back", "Back"),
            language.text("back_pages_long"),
            "back",
        ))
        return tuple(rows)

    def _open_saved_page(self, model, kind):
        """Show edit and view for one saved page. Hidden tools stay off the menu."""
        page = getattr(self, "_saved_by_kind", {}).get(kind)
        if page is None:
            return "That page is not on the list."
        if not os.path.isfile(page.get("index") or ""):
            return "That saved page is not on disk."
        self._open_page = page
        opener = getattr(self, "_page_open", None)
        if opener is None:
            opener = PageOpen(logger=self.logger)
        self._action_opener = opener
        rows = self._action_rows(opener)
        if model.boards is None:
            model.boards = {}
        model.boards["page-action"] = rows
        model.layer = "page-action"
        model.phase = "board"
        model.page_title = page["name"]
        model.index = 0
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        model.notice = ""
        if not any(item[3] in ("edit-page", "view-page") for item in rows):
            model.notice = self.painter.language.text("no_page_tools")
        return None

    def _edit_saved_page(self):
        """Open the saved HTML file in Visual Studio Code."""
        page = getattr(self, "_open_page", None)
        opener = getattr(self, "_action_opener", None)
        if page is None or opener is None:
            return "No saved page is selected."
        try:
            opener.edit(page["index"])
        except PageOpenError as exc:
            return "ERROR: {0}".format(exc)
        return "Opened {0} in Visual Studio Code.".format(page["name"])

    def _view_saved_page(self):
        """Open the saved HTML file in the default browser."""
        page = getattr(self, "_open_page", None)
        opener = getattr(self, "_action_opener", None)
        if page is None or opener is None:
            return "No saved page is selected."
        try:
            opener.view(page["index"])
        except PageOpenError as exc:
            return "ERROR: {0}".format(exc)
        return "Opened {0} in the default browser.".format(page["name"])

    def _server(self):
        """General Purpose: The static server for one saved page."""
        found = getattr(self, "_page_serve", None)
        if found is not None:
            return found
        return PageServe(self._name(), logger=self.logger)

    def _serve_on_screen(self, kind, screen, model):
        """List saved page names, ask for a port, then serve that page."""
        if kind == "serve":
            return self._open_serve_list(model)
        return self._serve_saved_page(screen, model, kind)

    def _open_serve_list(self, model):
        """Show the numbered page names. An empty list is a result page."""
        worker = PageDownload(self._name(), logger=self.logger)
        pages = worker.saved_pages()
        if not pages:
            return "No saved pages."
        language = self.painter.language
        rows = []
        self._serve_by_kind = {}
        for index, page in enumerate(pages, start=1):
            kind = "serve-saved-{0}".format(index)
            self._serve_by_kind[kind] = page
            rows.append((index, self._page_label(page), page["url"], kind))
        rows.append((
            0,
            language.row_short("back", "Back"),
            language.row_long("back", "return to the main menu"),
            "back",
        ))
        if model.boards is None:
            model.boards = {}
        model.boards["serve-pages"] = tuple(rows)
        model.layer = "serve-pages"
        model.phase = "board"
        model.index = 0
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        model.notice = ""
        return None

    def _ask_port(self, screen, model, name):
        """Port for one saved page. Esc returns None. Empty uses 5000."""
        lines = [
            "Page name: {0}".format(name),
            "",
            "Port [{0}]:".format(PageServe.DEFAULT_PORT),
        ]
        server = self._server()
        while True:
            raw = self.read_key(screen, model, lines, title="serve")
            if raw is None:
                return None
            try:
                return server.parse_port(raw)
            except PageServeError as exc:
                model.error = str(exc)

    def _suspend_screen(self, screen):
        """Leave curses so the server can print and take Ctrl+C."""
        try:
            curses.endwin()
        except Exception:
            return

    def _resume_screen(self, screen):
        """Draw the menu again after the server stops."""
        try:
            screen.refresh()
        except Exception:
            return

    def _serve_saved_page(self, screen, model, kind):
        """Ask for a port, then serve the chosen page until Ctrl+C."""
        page = getattr(self, "_serve_by_kind", {}).get(kind)
        if page is None:
            return "That page is not on the list."
        if screen is None:
            return "The text screen is not open."
        port = self._ask_port(screen, model, page["name"])
        if port is None:
            return None
        server = self._server()
        self._suspend_screen(screen)
        try:
            return server.serve(page["name"], port)
        except PageServeError as exc:
            return "ERROR: {0}".format(exc)
        finally:
            self._resume_screen(screen)

    def _page_label(self, page):
        """Page name. A non-default HTML file is shown in brackets."""
        html = page.get("html") or PageDownload.INDEX_NAME
        if html != PageDownload.INDEX_NAME:
            return "{0} [{1}]".format(page["name"], html)
        return page["name"]

    def _ask_html_name(self, screen, model, worker, default_html):
        """HTML file name. Esc returns None. Empty keeps the shown default."""
        lines = ["HTML file [{0}]:".format(default_html)]
        while True:
            raw = self.read_key(screen, model, lines, title="download")
            if raw is None:
                return None
            text = raw.strip()
            if text == "":
                return default_html
            try:
                return worker.clean_html(text)
            except PageDownloadError as exc:
                model.error = str(exc)

    def _ask_page_name(self, screen, model, worker, url):
        """Page name for a typed URL. Esc returns None.

        Empty keeps the saved name for this URL. A new URL keeps the folder
        recommended from the path. A host-only URL still needs a typed name.
        """
        known = ""
        for entry in worker.entries():
            if entry["url"] == url:
                known = entry["name"]
                break
        suggested, _html_name = worker.recommend(url)
        default = known or suggested
        lines = ["URL: {0}".format(url), ""]
        if default:
            lines.append("Page name [{0}]:".format(default))
        else:
            lines.append("Page name:")
        while True:
            raw = self.read_key(screen, model, lines, title="download")
            if raw is None:
                return None
            text = raw.strip()
            if text == "" and default:
                return default
            if text == "":
                model.error = "Type a page name."
                continue
            try:
                return worker.clean_name(text)
            except PageDownloadError as exc:
                model.error = str(exc)

    def _view_log(self, screen, model):
        """List log files and return the chosen file for the result page."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file:")
        picked = self._read_index(screen, model, lines, len(files), title="System Log")
        if picked is None:
            return None
        path = files[picked]
        body = self.system_log.read_log(path)
        if body is None:
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        if body == "":
            body = "(empty)"
        return "{0}\n\n{1}".format(path.name, body)

    def _clear_log(self, screen, model):
        """List log files, confirm, and empty the chosen file."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file to clear:")
        picked = self._read_index(screen, model, lines, len(files), title="System Log")
        if picked is None:
            return None
        path = files[picked]
        answer = self._read_yes_no(
            screen,
            model,
            ["Clear {0}? (y/n)".format(path.name)],
            title="System Log",
        )
        if answer is not True:
            return None
        if not self.system_log.clear_log(path):
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        return "Cleared {0}.".format(path.name)

    def _log_folder(self):
        """The log-folder result page. The path is logDir()."""
        return self.system_log.folder_text()
