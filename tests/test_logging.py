# TP-LOG-01 — one ChronicleLogger construct in main; logName, baseDir, logDir; html-downloader.
# TP-LOG-03 — version does not start a thread.
# TP-LOG-04 — each class __init__ logs instantiated at INFO, outside isDebug().
# TP-LOG-05 — temp write, publish, and discard are logged before the operation.
# Primary owner: requirement-python-cli-logging.
# TP-LOG-02 stays on tests/test_debug.py. It is not a second primary.
from __future__ import print_function, unicode_literals

import inspect
import io
import os
import shutil
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from HtmlDownloader.about_page import AboutPage  # noqa: E402
from HtmlDownloader.check_system import CheckSystem  # noqa: E402
from HtmlDownloader.cli import Cli, main  # noqa: E402
from HtmlDownloader.menu_language import MenuLanguage  # noqa: E402
from HtmlDownloader.menu_model import MenuModel  # noqa: E402
from HtmlDownloader.menu_painter import MenuPainter  # noqa: E402
from HtmlDownloader.menu_session import MenuSession  # noqa: E402
from HtmlDownloader.page_download import PageDownload, PageDownloadError  # noqa: E402
from HtmlDownloader.page_open import PageOpen, PageOpenError  # noqa: E402
from HtmlDownloader.page_serve import PageServe, PageServeError  # noqa: E402
from HtmlDownloader.self_management import SelfManage  # noqa: E402
from HtmlDownloader.system_log import SystemLog  # noqa: E402
from HtmlDownloader.tui import MenuScreenError, Tui  # noqa: E402


CLASS_NAMES = (
    "Cli",
    "CheckSystem",
    "AboutPage",
    "SelfManage",
    "Tui",
    "MenuPainter",
    "MenuLanguage",
    "SystemLog",
    "MenuModel",
    "MenuSession",
    "MenuScreenError",
    "PageDownload",
    "PageDownloadError",
    "PageServe",
    "PageServeError",
    "PageOpen",
    "PageOpenError",
)


class RecordingLogger(object):
    """Records log_message. isDebug stays false so instantiated lines are outside that gate."""

    def __init__(self):
        self.lines = []
        self.debug_calls = 0

    def log_message(self, message, level="INFO", component="main"):
        self.lines.append((message, level, component))

    def isDebug(self):
        self.debug_calls += 1
        return False

    def logName(self):
        return "html-downloader"

    def baseDir(self):
        return ""

    def logDir(self):
        return ""


class TestLogging(unittest.TestCase):
    def setUp(self):
        self._saved = {}
        for key in ("DEBUG", "debug"):
            self._saved[key] = os.environ.get(key)
            os.environ.pop(key, None)
        self.base = tempfile.mkdtemp(prefix="hd-log-base-")
        self.log = tempfile.mkdtemp(prefix="hd-log-dir-")
        self.home = tempfile.mkdtemp(prefix="hd-log-home-")

    def tearDown(self):
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        shutil.rmtree(self.base, ignore_errors=True)
        shutil.rmtree(self.log, ignore_errors=True)
        shutil.rmtree(self.home, ignore_errors=True)

    def _run(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(argv, basedir=self.base, logdir=self.log)
        return code, buf.getvalue()

    def test_one_construct_and_resolved_name(self):
        """TP-LOG-01: one construct. The three reads precede debug. The daily file is html-downloader."""
        from ChronicleLogger import ChronicleLogger

        source = inspect.getsource(main)
        self.assertEqual(source.count("ChronicleLogger("), 1)
        debug_at = source.index("logger.isDebug()")
        self.assertLess(source.index("logger.logName()"), debug_at)
        self.assertLess(source.index("logger.baseDir()"), debug_at)
        self.assertLess(source.index("logger.logDir()"), debug_at)
        seen = []

        def watch(label, original):
            def inner(this, *args, **kwargs):
                value = original(this, *args, **kwargs)
                seen.append((label, value))
                return value
            return inner

        with patch.object(ChronicleLogger, "logName", watch("logName", ChronicleLogger.logName)), patch.object(
            ChronicleLogger, "baseDir", watch("baseDir", ChronicleLogger.baseDir)
        ), patch.object(ChronicleLogger, "logDir", watch("logDir", ChronicleLogger.logDir)):
            code, _text = self._run(["version"])
        self.assertEqual(code, 0)
        self.assertIn(("logName", "html-downloader"), seen)
        self.assertIn(("baseDir", self.base), seen)
        self.assertIn(("logDir", self.log), seen)
        files = list(Path(self.log).glob("html-downloader*.log"))
        self.assertTrue(files, "resolved log name was not html-downloader")

    def test_version_starts_no_thread(self):
        """TP-LOG-03: the version verb does not create a thread."""
        before = {thread.ident for thread in threading.enumerate()}
        code, _text = self._run(["version"])
        after = {thread.ident for thread in threading.enumerate()}
        self.assertEqual(code, 0)
        self.assertEqual(before, after)

    def test_each_class_logs_instantiated(self):
        """TP-LOG-04: instantiated is INFO, the component is the class name, and isDebug is not asked."""
        logger = RecordingLogger()
        home = self.home
        Cli(logger)
        MenuPainter(logger=logger, home=home)
        MenuLanguage(logger=logger, home=home)
        MenuModel(logger=logger, painter=object())
        MenuSession(
            "HtmlDownloader",
            "0",
            lambda: "",
            lambda: "",
            logger=logger,
            painter=object(),
        )
        MenuScreenError("", logger=logger)
        SystemLog(logger=logger)
        SelfManage("HtmlDownloader", "0", runner=lambda _argv: None, logger=logger)
        CheckSystem(logger=logger, app_name="HtmlDownloader", version="0", console_name="html-downloader")
        AboutPage(
            CheckSystem(logger=logger),
            "HtmlDownloader",
            "0",
            "Author",
            "2026-10-04",
            "",
            "",
            "html-downloader download --url URL --name PAGENAME",
            "html-downloader",
            logger=logger,
        )
        Tui(app=None, app_name="HtmlDownloader", version="0", logger=logger)
        PageDownload("HtmlDownloader", logger=logger, home=home)
        PageDownloadError("", logger=logger)
        PageServe("HtmlDownloader", logger=logger, home=home)
        PageServeError("", logger=logger)
        PageOpen(
            logger=logger,
            which=lambda _name: "",
            run_text=lambda _argv: "",
            desktop_file=lambda _name: "",
            browser_command=lambda: "",
            runner=lambda _argv: None,
            platform_name="linux",
        )
        PageOpenError("", logger=logger)
        self.assertEqual(logger.debug_calls, 0)
        seen = {}
        for message, level, component in logger.lines:
            if message == "instantiated":
                seen.setdefault(component, level)
        missing = [name for name in CLASS_NAMES if name not in seen]
        self.assertEqual(missing, [])
        for name in CLASS_NAMES:
            self.assertEqual(seen[name], "INFO", name)

    def test_publish_logs_temp_then_move(self):
        """TP-LOG-05: write temp, then publish, both before the bytes land and before shutil.move."""
        logger = RecordingLogger()
        pages = PageDownload("HtmlDownloader", logger=logger, home=self.home)
        dest = os.path.join(self.home, "saved", "index.html")
        pages._publish(b"<html>ok</html>", dest)
        self.assertEqual(Path(dest).read_bytes(), b"<html>ok</html>")
        messages = [line[0] for line in logger.lines]
        write_at = next(i for i, text in enumerate(messages) if text.startswith("write temp path="))
        publish_at = next(i for i, text in enumerate(messages) if text.startswith("publish "))
        self.assertLess(write_at, publish_at)
        self.assertTrue(messages[publish_at].endswith(dest))
        for message, level, component in logger.lines:
            if message.startswith("write temp path=") or message.startswith("publish "):
                self.assertEqual(level, "INFO")
                self.assertEqual(component, "PageDownload")
        self.assertFalse(any(text.startswith("discard path=") for text in messages))

    def test_failed_publish_logs_discard_before_unlink(self):
        """TP-LOG-05: a failed move logs discard before the unfinished temp is removed."""
        logger = RecordingLogger()
        pages = PageDownload("HtmlDownloader", logger=logger, home=self.home)
        dest = os.path.join(self.home, "saved", "index.html")

        def fail_move(_src, _dest):
            raise OSError("move failed")

        with patch("HtmlDownloader.page_download.shutil.move", side_effect=fail_move):
            with self.assertRaises(PageDownloadError):
                pages._publish(b"<html>no</html>", dest)
        self.assertFalse(os.path.exists(dest))
        messages = [line[0] for line in logger.lines]
        write_at = next(i for i, text in enumerate(messages) if text.startswith("write temp path="))
        publish_at = next(i for i, text in enumerate(messages) if text.startswith("publish "))
        discard_at = next(i for i, text in enumerate(messages) if text.startswith("discard path="))
        self.assertLess(write_at, publish_at)
        self.assertLess(publish_at, discard_at)
        self.assertEqual(logger.lines[discard_at][1], "INFO")
        self.assertEqual(logger.lines[discard_at][2], "PageDownload")
        self.assertEqual(logger.debug_calls, 0)


if __name__ == "__main__":
    unittest.main()
