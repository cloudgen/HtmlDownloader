#!/usr/bin/env python
# =============================================================================
# HtmlDownloader CLI — text menu and typed verbs.
# Law keys: requirement-python-cli-interface, requirement-python-cli-logging,
#           requirement-python-tui, requirement-python-oop,
#           requirement-python-about, requirement-domain-htmlcrawler,
#           requirement-python-error-handling, requirement-python-coding-style,
#           requirement-runtime-prerequisites, requirement-html-site-crawl,
#           requirement-html-page-download
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# def main writes ChronicleLogger(...). This module does not construct it
# at import time and does not re-export it.
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import sys

from .about_page import AboutPage
from .check_system import CheckSystem
from .page_download import PageDownload, PageDownloadError
from .page_serve import PageServe, PageServeError
from .site_crawl import SiteCrawl
from .self_management import SelfManage
from .tui import Tui


class Cli:
    """Parser, dispatch, verbs, and the tty gate. One class in this file.

    Identity, verb lists, and suffix sets are attributes of this class.
    Collaborators arrive through the constructor. def main stays beside this class.
    """

    from . import __version__ as VERSION

    APP_NAME = "HtmlDownloader"
    CONSOLE_NAME = "html-downloader"
    PRODUCT_VERBS = (
        "help",
        "version",
        "about",
        "download",
        "crawl",
        "serve",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    LIFECYCLE_VERBS = (
        "version",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    AUTHOR_NAME = "Wilgat Wong"
    AUTHOR_EMAIL = "wilgat.wong@gmail.com"
    HOMEPAGE = "https://github.com/cloudgen/HtmlDownloader"
    LAST_UPDATE = "2026-10-04"
    DOWNLOAD_URL = ""
    BASIC_USAGE = "html-downloader download --url URL --name PAGENAME"

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.app_name = Cli.APP_NAME
        self.version = Cli.VERSION
        self.about = AboutPage(
            CheckSystem(
                logger=logger,
                app_name=Cli.APP_NAME,
                version=Cli.VERSION,
                console_name=Cli.CONSOLE_NAME,
            ),
            Cli.APP_NAME,
            Cli.VERSION,
            Cli.AUTHOR_NAME,
            Cli.LAST_UPDATE,
            Cli.HOMEPAGE,
            Cli.DOWNLOAD_URL,
            Cli.BASIC_USAGE,
            Cli.CONSOLE_NAME,
            logger=logger,
        )
        self.self_manage = SelfManage(Cli.APP_NAME, Cli.VERSION, logger=logger)
        self.tui = Tui(self, logger=logger)

    @staticmethod
    def stdout_is_tty():
        """General Purpose: Whether the text screen can be drawn on this stdout."""
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    @staticmethod
    def opens_text_screen(argv):
        """
        General Purpose: Whether this argv draws the text screen.

        The real parser has not run yet. This walk only decides is_quiet.
        Help, version, download, crawl, serve, and the pip verbs do not draw the screen.
        Empty argv and about do, when stdout is a terminal.
        download saves a page and does not draw the screen.
        crawl walks one site and does not draw the screen.
        serve serves a saved page and does not draw the screen.
        """
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if "--help" in argv or "-h" in argv or "--version" in argv:
            return False
        if not Cli.stdout_is_tty():
            return False
        verb = None
        saw_force = False
        for token in argv:
            if token == "--force":
                saw_force = True
                continue
            if token.startswith("-"):
                return False
            if verb is None:
                verb = token
                continue
            return False
        if saw_force and verb != "self-uninstall":
            return False
        if verb == "about":
            return True
        return verb is None

    @staticmethod
    def _depth_value(text):
        return Cli._bounded_flag("--depth", text, 0)

    @staticmethod
    def _max_pages_value(text):
        return Cli._bounded_flag("--max-pages", text, 1)

    @staticmethod
    def _bounded_flag(label, text, minimum):
        try:
            value = int(text, 10)
        except (TypeError, ValueError):
            raise argparse.ArgumentTypeError(
                "{0} must be an integer >= {1}.".format(label, minimum)
            )
        if value < minimum:
            raise argparse.ArgumentTypeError(
                "{0} must be an integer >= {1}.".format(label, minimum)
            )
        return value

    def report_error(self, message, nxt):
        """User-visible failure plus the same fact on the logger when one exists."""
        if self.logger is not None:
            self.logger.log_message(
                "{0} Next: {1}".format(message, nxt),
                level="ERROR",
                component="main",
            )
        print("ERROR: {0}".format(message), file=sys.stderr)
        print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def build_parser(self):
        """
        General Purpose: One optional product verb.
        help is also --help. --force belongs only to self-uninstall.
        --url and --name belong to download and crawl.
        --depth and --max-pages belong only to crawl.
        --page-name and --port belong only to serve.
        """
        parser = argparse.ArgumentParser(
            prog=Cli.CONSOLE_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=(
                "{0} — download one HTML page and its stylesheets, scripts, and images.\n"
                "With no arguments on a terminal, opens the text menu.\n"
                "With no arguments and no terminal, prints this help and stops.\n"
                "Product verbs: help, version, about, download, crawl, serve, self-install,\n"
                "version-check, self-update, self-uninstall.\n"
                "help prints this usage. version prints the installed version.\n"
                "about prints a page. download saves the page and does not\n"
                "draw the menu. It needs --url and --name.\n"
                "crawl saves pages on one host and does not draw the menu.\n"
                "It needs --url, --name, --depth, and --max-pages.\n"
                "serve serves one saved page on 127.0.0.1 and does not draw the\n"
                "menu. It needs --page-name. --port defaults to {1}.\n"
                "Menu row 1 download lists saved pages or accepts a URL.\n"
                "Menu row 2 list downloaded lists saved page names. After a page\n"
                "is chosen, 21 edit opens it in Visual Studio Code when code is\n"
                "installed, and 22 view opens it in the default browser when one\n"
                "is set. A tool that is not installed is left off that menu.\n"
                "Menu row 3 serve lists saved page names, then asks for a port.\n"
                "An empty port uses {1}. Menu row 4 System Log opens the log list.\n"
                "Each page is ~/.app/{0}/output/<name>/index.html.\n"
                "This program does not join media or list files in this folder.\n"
                "version-check runs: python -m pip index versions {0}\n"
                "self-update runs: python -m pip install --upgrade {0}\n"
                "self-install runs: python -m pip install {0}\n"
                "self-uninstall runs: python -m pip uninstall -y {0}\n"
                "and needs --force. Empty arguments do not install or update."
                .format(Cli.APP_NAME, PageServe.DEFAULT_PORT)
            ),
        )
        parser.add_argument(
            "verb",
            nargs="?",
            default=None,
            metavar="verb",
            help=(
                "Product verb: help, version, about, download, crawl, serve, "
                "self-install, version-check, self-update, or self-uninstall"
            ),
        )
        parser.add_argument(
            "--version",
            action="version",
            version="{0} {1}".format(Cli.APP_NAME, Cli.VERSION),
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Confirm self-uninstall. Required on the command line.",
        )
        parser.add_argument(
            "--url",
            default="",
            help="Page URL for download, or start URL for crawl.",
        )
        parser.add_argument(
            "--name",
            default="",
            help="Page name for download, or site name for crawl.",
        )
        parser.add_argument(
            "--depth",
            type=Cli._depth_value,
            default=None,
            help="Crawl depth. 0 is the start page. Used only with crawl.",
        )
        parser.add_argument(
            "--max-pages",
            type=Cli._max_pages_value,
            default=None,
            help="Maximum HTML pages. Used only with crawl.",
        )
        parser.add_argument(
            "--page-name",
            default="",
            help="Saved page name for serve. Used only with the serve verb.",
        )
        parser.add_argument(
            "--port",
            default=None,
            help="Port for serve. Default {0}. Used only with the serve verb.".format(
                PageServe.DEFAULT_PORT
            ),
        )
        return parser

    def _page(self, text):
        print(text)
        return 0

    def _verb_download(self, url, name):
        """Save one page. Does not draw the menu. Needs --url and --name."""
        if not (url or "").strip() or not (name or "").strip():
            return self.report_error(
                "download needs --url and --name.",
                "{0} download --url URL --name PAGENAME".format(Cli.CONSOLE_NAME),
            )
        worker = PageDownload(Cli.APP_NAME, logger=self.logger)
        try:
            text = worker.download(url, name)
        except PageDownloadError as exc:
            return self.report_error(
                str(exc),
                "{0} download --url URL --name PAGENAME".format(Cli.CONSOLE_NAME),
            )
        print(text)
        return 0

    def _verb_crawl(self, url, name, depth, max_pages):
        """Walk one site. Does not draw the menu. Needs all four flags."""
        missing = []
        if not (url or "").strip():
            missing.append("--url")
        if not (name or "").strip():
            missing.append("--name")
        if depth is None:
            missing.append("--depth")
        if max_pages is None:
            missing.append("--max-pages")
        usage = "{0} crawl --url URL --name SITENAME --depth N --max-pages N".format(
            Cli.CONSOLE_NAME
        )
        if missing:
            return self.report_error("crawl needs {0}.".format(", ".join(missing)), usage)
        worker = SiteCrawl(Cli.APP_NAME, logger=self.logger)
        try:
            text = worker.crawl(url, name, depth, max_pages)
        except PageDownloadError as exc:
            return self.report_error(str(exc), usage)
        print(text)
        return 0

    def _verb_serve(self, name, port):
        """Serve one saved page. Does not draw the menu. Needs --page-name."""
        if not (name or "").strip():
            return self.report_error(
                "serve needs --page-name.",
                "{0} serve --page-name PAGENAME".format(Cli.CONSOLE_NAME),
            )
        worker = PageServe(Cli.APP_NAME, logger=self.logger)
        try:
            text = worker.serve(name, port)
        except PageServeError as exc:
            return self.report_error(
                str(exc),
                "{0} serve --page-name PAGENAME".format(Cli.CONSOLE_NAME),
            )
        print(text)
        return 0

    def _unknown_verb(self, token):
        names = ", ".join(Cli.PRODUCT_VERBS)
        return self.report_error(
            "Unknown verb '{0}'.".format(token),
            "{0} help — verbs: {1}".format(Cli.CONSOLE_NAME, names),
        )

    def _dispatch(self, args):
        """One product verb, the front board, or a fail-closed stop."""
        verb = args.verb
        if args.force and verb != "self-uninstall":
            return self.report_error(
                "--force is only for self-uninstall.",
                "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
            )
        if (args.depth is not None or args.max_pages is not None) and verb != "crawl":
            return self.report_error(
                "--depth and --max-pages are only for crawl.",
                "{0} crawl --url URL --name SITENAME --depth N --max-pages N".format(
                    Cli.CONSOLE_NAME
                ),
            )
        if (args.url or args.name) and verb not in ("download", "crawl"):
            return self.report_error(
                "--url and --name are only for download and crawl.",
                "{0} download --url URL --name PAGENAME".format(Cli.CONSOLE_NAME),
            )
        if (args.page_name or args.port is not None) and verb != "serve":
            return self.report_error(
                "--page-name and --port are only for serve.",
                "{0} serve --page-name PAGENAME".format(Cli.CONSOLE_NAME),
            )
        if verb == "about":
            result = self.tui.about_on_screen()
            if isinstance(result, int):
                return result
            return self._page(result)
        if verb == "download":
            return self._verb_download(args.url, args.name)
        if verb == "crawl":
            return self._verb_crawl(args.url, args.name, args.depth, args.max_pages)
        if verb == "serve":
            return self._verb_serve(args.page_name, args.port)
        if verb == "version":
            return self._page(self.self_manage.local_version())
        if verb == "self-uninstall":
            if not args.force:
                return self.report_error(
                    "self-uninstall removes this package with pip.",
                    "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
                )
            return self.self_manage.emit(verb)
        if verb in ("version-check", "self-update", "self-install"):
            return self.self_manage.emit(verb)
        if verb is not None:
            return self._unknown_verb(verb)
        if not self.stdout_is_tty():
            self.build_parser().print_help()
            return 0
        action = self.tui.open_text_menu()
        if action == "missing":
            return 1
        return 0

    def run(self, argv=None):
        """One job. def main already wrote ChronicleLogger(...) and passed it in."""
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        parser = self.build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            code = exc.code
            if code is None or code == 0:
                return 0
            return int(code)
        if args.verb == "help":
            parser.print_help()
            return 0
        return self._dispatch(args)


def main(argv=None, basedir="", logdir=""):
    """This function instantiates ChronicleLogger. The statement below is the construct."""
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        sys.stderr.write(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.3.1"\n'
        )
        return 1

    from HtmlDownloader import __version__

    screen = Cli.opens_text_screen(argv)
    logger = ChronicleLogger(
        logname=Cli.APP_NAME,
        is_quiet=screen,
        basedir=basedir,
        logdir=logdir,
    )
    appname = logger.logName()
    resolved_base = logger.baseDir()
    logger.logDir()

    if logger.isDebug():
        logger.log_message(
            "{0} v{1} ({2})".format(appname, __version__, __file__),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(resolved_base),
            level="DEBUG",
            component="main",
        )
        logger.log_message("debug mode", component="main")

    app = Cli(logger)
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())
