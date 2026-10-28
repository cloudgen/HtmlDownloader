# crawl — same-host walk with required depth and page cap.
# TP-CRAWL-01 missing bounds. TP-CRAWL-02 other host.
# TP-CRAWL-03 page cap. TP-CRAWL-04 robots.
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from HtmlDownloader.cli import Cli
from HtmlDownloader.page_download import PageDownload, PageDownloadError
from HtmlDownloader.site_crawl import SiteCrawl


ROBOTS_OPEN = "User-agent: *\nDisallow:\n"
HOME = "http://127.0.0.1"
OTHER = "http://127.0.0.1:9"


def page(links):
    body = ["<!DOCTYPE html><html><body>"]
    for href in links:
        body.append('<a href="{0}">go</a>'.format(href))
    body.append("</body></html>")
    return "".join(body).encode("utf-8")


class Clock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def clock(self):
        return self.now

    def sleeper(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class TestCrawl(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="htmlcrawl_", dir="/tmp")
        self.previous = os.environ.get("HOME")
        os.environ["HOME"] = self.home
        self.clock = Clock()

    def tearDown(self):
        if self.previous is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = self.previous

    def _run(self, argv):
        app = Cli()
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = app.run(argv)
        return code, out.getvalue(), err.getvalue()

    def _opener(self, table):
        def open_url(url):
            found = table.get(url)
            if found is None:
                raise PageDownloadError("HTTP 404 for {0}.".format(url))
            if isinstance(found, tuple):
                body, final = found
                return body, "text/html; charset=utf-8", final
            return found, "text/html; charset=utf-8"

        return open_url

    def _crawl(self, table, url, name, depth, max_pages):
        worker = SiteCrawl(
            Cli.APP_NAME,
            home=self.home,
            opener=self._opener(table),
            sleeper=self.clock.sleeper,
            clock=self.clock.clock,
        )
        text = worker.crawl(url, name, depth, max_pages)
        return worker, text

    def _index(self, *parts):
        return os.path.join(self.home, ".app", Cli.APP_NAME, "output", *parts)

    def test_missing_bounds_name_the_flag(self):
        """TP-CRAWL-01: a missing bound exits non-zero and names the flag."""
        code, _out, err = self._run(["crawl", "--url", HOME + "/", "--name", "example"])
        self.assertEqual(code, 1)
        self.assertIn("--depth", err)
        self.assertIn("--max-pages", err)
        code, _out, err = self._run(
            ["crawl", "--url", HOME + "/", "--name", "example", "--depth", "1"]
        )
        self.assertEqual(code, 1)
        self.assertIn("--max-pages", err)
        code, _out, err = self._run(
            ["crawl", "--url", HOME + "/", "--name", "example", "--max-pages", "2"]
        )
        self.assertEqual(code, 1)
        self.assertIn("--depth", err)
        code, _out, err = self._run(
            ["crawl", "--name", "example", "--depth", "0", "--max-pages", "1"]
        )
        self.assertEqual(code, 1)
        self.assertIn("--url", err)
        code, _out, err = self._run(["--depth", "0"])
        self.assertEqual(code, 1)
        self.assertIn("--depth", err)
        code, _out, err = self._run(["crawl", "--url", HOME + "/", "--name", "example", "--depth", "no", "--max-pages", "1"])
        self.assertNotEqual(code, 0)
        self.assertIn("--depth", err)
        code, _out, err = self._run(
            ["crawl", "--url", HOME + "/", "--name", "example", "--depth", "-1", "--max-pages", "1"]
        )
        self.assertNotEqual(code, 0)
        self.assertIn("--depth", err)
        code, _out, err = self._run(
            ["crawl", "--url", HOME + "/", "--name", "example", "--depth", "0", "--max-pages", "0"]
        )
        self.assertNotEqual(code, 0)
        self.assertIn("--max-pages", err)
        called = {"download": 0}
        original = PageDownload.download

        def boom(self, url, name):
            called["download"] += 1
            return original(self, url, name)

        PageDownload.download = boom
        try:
            code, _out, err = self._run(
                ["download", "--url", HOME + "/", "--name", "example", "--depth", "1", "--max-pages", "2"]
            )
        finally:
            PageDownload.download = original
        self.assertEqual(code, 1)
        self.assertIn("--depth", err)
        self.assertIn("--max-pages", err)
        self.assertEqual(called["download"], 0)
        self.assertIn("crawl", Cli.PRODUCT_VERBS)
        previous = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertFalse(Cli.opens_text_screen(["crawl"]))
            self.assertFalse(Cli.opens_text_screen(["crawl", "--url", HOME + "/"]))
            self.assertTrue(Cli.opens_text_screen([]))
        finally:
            Cli.stdout_is_tty = previous
        code, out, _err = self._run(["help"])
        self.assertEqual(code, 0)
        self.assertIn("crawl", out)
        self.assertIn("download", out)
        self.assertIn("serve", out)
        self.assertIn("--depth", out)
        self.assertIn("--max-pages", out)
        self.assertFalse(os.path.isdir(self._index("example")))

    def test_other_host_is_not_saved(self):
        """TP-CRAWL-02: a link on another host is not fetched."""
        start = HOME + "/"
        other = OTHER + "/out"
        table = {
            HOME + "/robots.txt": ROBOTS_OPEN.encode("utf-8"),
            start: page([other, HOME + "/inside"]),
            HOME + "/inside": page([]),
        }
        seen = []
        raw = self._opener(table)

        def open_url(url):
            seen.append(url)
            return raw(url)

        worker = SiteCrawl(
            Cli.APP_NAME,
            home=self.home,
            opener=open_url,
            sleeper=self.clock.sleeper,
            clock=self.clock.clock,
        )
        text = worker.crawl(start, "example", 1, 5)
        self.assertIn("Finished.", text)
        self.assertNotIn(other, seen)
        self.assertTrue(os.path.isfile(self._index("example", "index.html")))
        self.assertTrue(os.path.isfile(self._index("example", "inside", "index.html")))
        self.assertFalse(os.path.exists(self._index("example", "out", "index.html")))
        self.assertEqual(worker.pages.user_agent, "HtmlCrawler/{0}".format(Cli.VERSION))
        self.assertEqual(SiteCrawl.DELAY_SECONDS, 1)
        self.assertGreaterEqual(len(self.clock.sleeps), 2)
        self.assertTrue(all(gap == 1 for gap in self.clock.sleeps))

    def test_redirect_keeps_the_final_host(self):
        """A start-page redirect follows the final host only."""
        start = HOME + "/start"
        landed = OTHER + "/landed"
        table = {
            HOME + "/robots.txt": ROBOTS_OPEN.encode("utf-8"),
            start: (page([HOME + "/nope", OTHER + "/yes"]), landed),
            OTHER + "/robots.txt": ROBOTS_OPEN.encode("utf-8"),
            OTHER + "/yes": page([]),
        }
        seen = []
        raw = self._opener(table)

        def open_url(url):
            seen.append(url)
            return raw(url)

        worker = SiteCrawl(
            Cli.APP_NAME,
            home=self.home,
            opener=open_url,
            sleeper=self.clock.sleeper,
            clock=self.clock.clock,
        )
        worker.crawl(start, "example", 1, 5)
        self.assertNotIn(HOME + "/nope", seen)
        self.assertIn(OTHER + "/yes", seen)
        self.assertTrue(os.path.isfile(self._index("example", "start", "index.html")))
        self.assertTrue(os.path.isfile(self._index("example", "yes", "index.html")))

    def test_page_cap_and_depth_say_which_bound(self):
        """TP-CRAWL-03: the walk stops at the page cap and says so."""
        start = HOME + "/"
        table = {
            HOME + "/robots.txt": ROBOTS_OPEN.encode("utf-8"),
            start: page([HOME + "/a", HOME + "/b"]),
            HOME + "/a": page([HOME + "/c"]),
            HOME + "/b": page([]),
            HOME + "/c": page([]),
        }
        _worker, text = self._crawl(table, start, "example", 2, 2)
        self.assertIn("Stopped by --max-pages.", text)
        self.assertTrue(os.path.isfile(self._index("example", "index.html")))
        saved = 0
        root = self._index("example")
        for dirpath, _dirs, files in os.walk(root):
            if "index.html" in files:
                saved += 1
        self.assertEqual(saved, 2)
        self.clock.sleeps.clear()
        self.clock.now = 0.0
        table[HOME + "/deep"] = page([HOME + "/a"])
        _worker, text = self._crawl(table, HOME + "/deep", "deep", 0, 5)
        self.assertIn("Stopped by --depth.", text)
        self.assertTrue(os.path.isfile(self._index("deep", "deep", "index.html")))
        self.assertFalse(os.path.exists(self._index("deep", "a", "index.html")))
        _worker, text = self._crawl(table, start, "both", 0, 1)
        self.assertIn("Stopped by --max-pages and --depth.", text)

    def test_robots_disallow_and_failure(self):
        """TP-CRAWL-04: a disallowed path is skipped, and a failed robots fetch saves nothing."""
        start = HOME + "/"
        secret = HOME + "/secret"
        table = {
            HOME + "/robots.txt": (
                "User-agent: *\nDisallow: /secret\n\n"
                "User-agent: HtmlCrawler\nDisallow: /hidden\n\n"
                "User-agent: OtherBot\nDisallow: /visible\n"
            ).encode("utf-8"),
            start: page([secret, HOME + "/hidden", HOME + "/visible"]),
            HOME + "/visible": page([]),
            secret: page([]),
            HOME + "/hidden": page([]),
        }
        _worker, text = self._crawl(table, start, "example", 1, 5)
        self.assertIn("Finished.", text)
        self.assertIn(secret, text)
        self.assertIn(HOME + "/hidden", text)
        self.assertTrue(os.path.isfile(self._index("example", "index.html")))
        self.assertTrue(os.path.isfile(self._index("example", "visible", "index.html")))
        self.assertFalse(os.path.exists(self._index("example", "secret", "index.html")))
        self.assertFalse(os.path.exists(self._index("example", "hidden", "index.html")))
        for folder in (
            self._index("example"),
            self._index("example", "visible"),
        ):
            for kind in ("css", "js", "img"):
                self.assertTrue(os.path.isdir(os.path.join(folder, "assets", kind)))
        map_path = self._index("url-map.json")
        self.assertTrue(os.path.isfile(map_path))
        broken = {
            HOME + "/robots.txt": PageDownloadError("HTTP 404 for {0}/robots.txt.".format(HOME)),
        }

        def open_url(url):
            found = broken.get(url)
            if isinstance(found, Exception):
                raise found
            raise PageDownloadError("HTTP 404 for {0}.".format(url))

        worker = SiteCrawl(
            Cli.APP_NAME,
            home=self.home,
            opener=open_url,
            sleeper=self.clock.sleeper,
            clock=self.clock.clock,
        )
        with self.assertRaises(PageDownloadError) as caught:
            worker.crawl(start, "blocked", 1, 5)
        self.assertIn("robots.txt", str(caught.exception))
        self.assertIn("127.0.0.1", str(caught.exception))
        self.assertFalse(os.path.exists(self._index("blocked", "index.html")))

    def test_dotdot_and_nested_folder(self):
        """A parent segment fails that URL. A path is its own index.html."""
        start = HOME + "/guide.html"
        table = {
            HOME + "/robots.txt": ROBOTS_OPEN.encode("utf-8"),
            start: page([HOME + "/a/../b", HOME + "/docs/intro"]),
            HOME + "/docs/intro": page([]),
        }
        _worker, text = self._crawl(table, start, "example", 1, 5)
        self.assertIn("Finished.", text)
        self.assertTrue(os.path.isfile(self._index("example", "guide.html", "index.html")))
        self.assertTrue(os.path.isfile(self._index("example", "docs", "intro", "index.html")))
        self.assertFalse(os.path.exists(self._index("example", "b", "index.html")))
        self.assertIn("..", text)
        with self.assertRaises(PageDownloadError):
            self._crawl(table, HOME + "/a/../b", "bad", 0, 1)
        self.assertFalse(os.path.exists(self._index("bad")))
