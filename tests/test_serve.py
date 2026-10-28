# serve — static server for one saved page.
# The typed verb needs --page-name. The default port is 5000.
# Menu row 3 lists saved page names, then asks for a port.
import io
import json
import os
import shutil
import socket
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

from HtmlDownloader.cli import Cli
from HtmlDownloader.menu_model import MenuModel
from HtmlDownloader.menu_painter import MenuPainter
from HtmlDownloader.page_serve import PageServe, PageServeError
from HtmlDownloader.tui import Tui


class TestServe(unittest.TestCase):
    """Typed serve and menu row 3 serve one saved page on 127.0.0.1."""

    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="htmlserve_", dir="/tmp")
        self.saved = {
            name: os.environ.get(name)
            for name in ("HOME", "HTMLDOWNLOADER_LANG")
        }
        os.environ["HOME"] = self.home
        os.environ.pop("HTMLDOWNLOADER_LANG", None)
        self.painter = MenuPainter(home=self.home)
        self.model = MenuModel(painter=self.painter)
        self.tui = Tui()
        self.tui.painter = self.painter

    def tearDown(self):
        for name, value in self.saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        shutil.rmtree(self.home, ignore_errors=True)

    def _root(self):
        return os.path.join(self.home, ".app", "HtmlDownloader", "output")

    def _write_page(self, name, url, body="<html>hello</html>\n", css="body{}\n", html_name="index.html"):
        folder = os.path.join(self._root(), name)
        css_dir = os.path.join(folder, "assets", "css")
        os.makedirs(css_dir, mode=0o700)
        index = os.path.join(folder, html_name)
        with open(index, "w", encoding="utf-8") as handle:
            handle.write(body)
        with open(os.path.join(css_dir, "app.css"), "w", encoding="utf-8") as handle:
            handle.write(css)
        secret = os.path.join(self._root(), "secret.txt")
        with open(secret, "w", encoding="utf-8") as handle:
            handle.write("SECRET-TOKEN\n")
        return index

    def _write_map(self, pages):
        root = self._root()
        os.makedirs(root, mode=0o700, exist_ok=True)
        path = os.path.join(root, "url-map.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"pages": pages}, handle)
            handle.write("\n")

    def _commit(self, token):
        self.model.buffer = token
        self.model.cursor = len(token)
        self.model.focus = "input"
        return self.model.apply_key(10)

    def _free_port(self):
        sock = socket.socket()
        sock.bind((PageServe.BIND, 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    def test_parse_port_defaults_and_rejects(self):
        worker = PageServe("HtmlDownloader", home=self.home)
        self.assertEqual(worker.parse_port(None), 5000)
        self.assertEqual(worker.parse_port(""), 5000)
        self.assertEqual(worker.parse_port(" 8080 "), 8080)
        for bad in ("0", "65536", "nope", "-1"):
            with self.assertRaises(PageServeError):
                worker.parse_port(bad)

    def test_missing_page_and_flags(self):
        """TP-CLI-03, TP-ERR-02: a missing page does not start the server."""
        app = Cli()
        err = io.StringIO()
        with redirect_stderr(err):
            code = app.run(["serve"])
        self.assertEqual(code, 1)
        self.assertIn("--page-name", err.getvalue())
        err = io.StringIO()
        with redirect_stderr(err):
            code = app.run(["serve", "--page-name", "missing"])
        self.assertEqual(code, 1)
        self.assertIn("not a saved page", err.getvalue())
        self._write_page("sample", "https://example.com/sample", body="")
        self._write_map([{"url": "https://example.com/sample", "name": "sample"}])
        err = io.StringIO()
        with redirect_stderr(err):
            code = app.run(["serve", "--page-name", "sample"])
        self.assertEqual(code, 1)
        self.assertIn("not a saved page", err.getvalue())
        err = io.StringIO()
        with redirect_stderr(err):
            code = app.run(["download", "--page-name", "sample"])
        self.assertEqual(code, 1)
        self.assertIn("only for serve", err.getvalue())
        err = io.StringIO()
        with redirect_stderr(err):
            code = app.run(["serve", "--url", "https://example.com/", "--page-name", "sample"])
        self.assertEqual(code, 1)
        self.assertIn("only for download", err.getvalue())
        self.assertFalse(Cli.opens_text_screen(["serve"]))
        self.assertFalse(Cli.opens_text_screen(["serve", "--page-name", "sample"]))
        self.assertIn("serve", Cli.PRODUCT_VERBS)

    def test_cli_passes_the_page_and_port(self):
        seen = {}
        original = PageServe.serve

        def fake_serve(self, name, port=None):
            seen["name"] = name
            seen["port"] = port
            return "Stopped {0}.".format(name)

        PageServe.serve = fake_serve
        try:
            app = Cli()
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = app.run(["serve", "--page-name", "sample"])
            self.assertEqual(code, 0)
            self.assertEqual(seen, {"name": "sample", "port": None})
            self.assertIn("Stopped sample.", buf.getvalue())
            with redirect_stdout(io.StringIO()):
                code = app.run(["serve", "--page-name", "sample", "--port", "8080"])
            self.assertEqual(code, 0)
            self.assertEqual(seen["port"], "8080")
        finally:
            PageServe.serve = original

    def test_server_serves_the_page_folder_only(self):
        self._write_page("sample", "https://example.com/sample")
        worker = PageServe("HtmlDownloader", home=self.home)
        port = self._free_port()
        httpd, url, clean, directory = worker.listen("sample", port)
        self.assertEqual(clean, "sample")
        self.assertEqual(httpd.server_address[0], "127.0.0.1")
        self.assertTrue(directory.endswith(os.path.join("output", "sample")))
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            conn = HTTPConnection("127.0.0.1", httpd.server_address[1], timeout=5)
            conn.request("GET", "/")
            response = conn.getresponse()
            body = response.read()
            self.assertEqual(response.status, 200)
            self.assertIn(b"hello", body)
            conn.request("GET", "/assets/css/app.css")
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertIn(b"body{}", response.read())
            for path in ("/../secret.txt", "/assets/../../secret.txt"):
                conn.request("GET", path)
                response = conn.getresponse()
                payload = response.read()
                self.assertNotIn(b"SECRET-TOKEN", payload)
                self.assertNotEqual(response.status, 200)
            self.assertTrue(url.startswith("http://127.0.0.1:"))
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=5)

    def test_renamed_html_is_the_site_root(self):
        """TP-HTMLDOWNLOADER-01: the stored HTML file is /."""
        self._write_page(
            "sample",
            "https://example.com/sample",
            body="<html>renamed</html>\n",
            html_name="page.html",
        )
        self._write_map([{
            "url": "https://example.com/sample",
            "name": "sample",
            "html": "page.html",
        }])
        worker = PageServe("HtmlDownloader", home=self.home)
        port = self._free_port()
        httpd, _url, clean, directory = worker.listen("sample", port)
        self.assertEqual(clean, "sample")
        self.assertTrue(os.path.isfile(os.path.join(directory, "page.html")))
        self.assertFalse(os.path.isfile(os.path.join(directory, "index.html")))
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            conn = HTTPConnection("127.0.0.1", httpd.server_address[1], timeout=5)
            conn.request("GET", "/")
            response = conn.getresponse()
            body = response.read()
            self.assertEqual(response.status, 200)
            self.assertIn(b"renamed", body)
            conn.request("GET", "/page.html")
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertIn(b"renamed", response.read())
            conn.request("HEAD", "/")
            response = conn.getresponse()
            response.read()
            self.assertEqual(response.status, 200)
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=5)

    def test_taken_port_is_an_error(self):
        self._write_page("sample", "https://example.com/sample")

        class Quiet(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()

            def log_message(self, fmt, *args):
                return

        holder = HTTPServer(("127.0.0.1", 0), Quiet)
        thread = threading.Thread(target=holder.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            worker = PageServe("HtmlDownloader", home=self.home)
            with self.assertRaises(PageServeError) as caught:
                worker.listen("sample", holder.server_address[1])
            self.assertIn("not available", str(caught.exception))
        finally:
            holder.shutdown()
            holder.server_close()
            thread.join(timeout=5)

    def test_menu_lists_pages_then_asks_for_a_port(self):
        self._write_page("fiori", "https://example.com/fiori")
        self._write_map([{"url": "https://example.com/fiori", "name": "fiori"}])
        rows = self.painter.display_rows("front")
        self.assertEqual(rows[2][0], 3)
        self.assertEqual(rows[2][3], "serve")
        self.assertEqual(rows[3][0], 4)
        self.assertEqual(rows[3][1], "System Log")
        self.assertEqual(self._commit("3"), "serve")
        self.assertIsNone(self.tui._open_serve_list(self.model))
        self.assertEqual(self.model.layer, "serve-pages")
        shown = self.model.rows()
        self.assertEqual([(row[0], row[1]) for row in shown], [(1, "fiori"), (0, "Back")])
        self.assertEqual(self.painter.board_title(self.model), "serve")
        self.assertIsNone(self._commit("0"))
        self.assertEqual(self.model.layer, "front")
        self.tui._open_serve_list(self.model)
        self.assertEqual(self._commit("1"), "serve-saved-1")

        class PortScreen:
            """Feeds port keys and records the painted question."""

            def __init__(self, keys):
                self.keys = list(keys)
                self.calls = []

            def getmaxyx(self):
                return (24, 80)

            def erase(self):
                self.calls = []

            def addstr(self, y, x, text, _attr=0):
                self.calls.append((y, x, text))

            def refresh(self):
                return None

            def curs_set(self, _visibility):
                return None

            def timeout(self, _milliseconds):
                return None

            def getch(self):
                if self.keys:
                    return self.keys.pop(0)
                return 27

        seen = []
        real = PageServe("HtmlDownloader", home=self.home)

        class FakeServe:
            def parse_port(self, port):
                return real.parse_port(port)

            def serve(self, name, port=None):
                seen.append((name, port))
                return "Stopped {0}.".format(name)

        self.tui._page_serve = FakeServe()
        screen = PortScreen([10])
        text = self.tui._serve_saved_page(screen, self.model, "serve-saved-1")
        painted = [item[2] for item in screen.calls]
        self.assertEqual(text, "Stopped fiori.")
        self.assertEqual(seen, [("fiori", 5000)])
        self.assertIn("Page name: fiori", painted)
        self.assertIn("Port [5000]:", painted)

        screen = PortScreen([ord(char) for char in "nope"] + [10, 27])
        text = self.tui._serve_saved_page(screen, self.model, "serve-saved-1")
        painted = [item[2] for item in screen.calls]
        self.assertIsNone(text)
        self.assertEqual(seen, [("fiori", 5000)])
        self.assertIn("Port must be a number from 1 to 65535.", painted)

        screen = PortScreen([ord(char) for char in "8080"] + [10])
        text = self.tui._serve_saved_page(screen, self.model, "serve-saved-1")
        self.assertEqual(text, "Stopped fiori.")
        self.assertEqual(seen[-1], ("fiori", 8080))

    def test_no_saved_pages_is_a_result(self):
        self.assertEqual(self.tui._open_serve_list(self.model), "No saved pages.")
        self.assertEqual(self.model.layer, "front")


if __name__ == "__main__":
    unittest.main()
