# TP-DBG-01 — DEBUG=1 shows the four debug values on a non-screen run.
# TP-DBG-02 — unset DEBUG and debug show none of those values.
# TP-DBG-03 — a text-screen run keeps the lines off the console; the daily file still has them.
# Primary owner: requirement-python-cli-debug.
# requirement-python-cli-logging keeps the ChronicleLogger construct. TP-LOG-02 is not a second primary.
from __future__ import print_function, unicode_literals

import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from HtmlDownloader import __version__  # noqa: E402
from HtmlDownloader.cli import Cli, main  # noqa: E402


class TestDebug(unittest.TestCase):
    def setUp(self):
        self._saved = {}
        for key in ("DEBUG", "debug"):
            self._saved[key] = os.environ.get(key)
            os.environ.pop(key, None)
        self.base = tempfile.mkdtemp(prefix="hd-dbg-base-")
        self.log = tempfile.mkdtemp(prefix="hd-dbg-log-")

    def tearDown(self):
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        shutil.rmtree(self.base, ignore_errors=True)
        shutil.rmtree(self.log, ignore_errors=True)

    def _run(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(argv, basedir=self.base, logdir=self.log)
        return code, buf.getvalue()

    def _daily(self):
        files = list(Path(self.log).glob("*.log"))
        self.assertTrue(files, "daily log was not written under the temp log dir")
        return "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in files)

    def _assert_catalog(self, text):
        from ChronicleLogger import ChronicleLogger

        self.assertIn("html-downloader v{0}".format(__version__), text)
        self.assertIn("cli.py", text)
        self.assertIn("Using {0}".format(ChronicleLogger.class_version()), text)
        self.assertIn("Base ", text)
        self.assertIn("debug mode", text)

    def _assert_catalog_absent(self, text):
        from ChronicleLogger import ChronicleLogger

        self.assertNotIn("html-downloader v", text)
        self.assertNotIn(ChronicleLogger.class_version(), text)
        self.assertNotIn("Base ", text)
        self.assertNotIn("debug mode", text)

    def test_debug_on_version_shows_four_values(self):
        """TP-DBG-01: DEBUG=1 on version shows the catalog. The version verb stays local."""
        os.environ["DEBUG"] = "1"
        code, text = self._run(["version"])
        self.assertEqual(code, 0)
        self.assertIn("HtmlDownloader {0}".format(__version__), text)
        self._assert_catalog(text)

    def test_debug_off_hides_the_catalog(self):
        """TP-DBG-02: unset DEBUG and debug hide the four values."""
        code, text = self._run(["version"])
        self.assertEqual(code, 0)
        self.assertIn("HtmlDownloader {0}".format(__version__), text)
        self._assert_catalog_absent(text)

    def test_text_screen_keeps_console_quiet_and_writes_the_file(self):
        """TP-DBG-03: empty argv on a terminal does not mirror the catalog. The file has it."""
        os.environ["DEBUG"] = "1"
        buf = io.StringIO()
        with patch.object(Cli, "stdout_is_tty", return_value=True), patch.object(
            Cli, "run", return_value=0
        ), redirect_stdout(buf):
            code = main([], basedir=self.base, logdir=self.log)
        text = buf.getvalue()
        self.assertEqual(code, 0)
        self._assert_catalog_absent(text)
        self._assert_catalog(self._daily())


if __name__ == "__main__":
    unittest.main()
