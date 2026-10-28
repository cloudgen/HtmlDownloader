# download — save one page, its stylesheets, and its scripts.
# The typed verb does not draw the menu.
# Menu row 1 is download. The text menu lists saved page name:url pairs.
import io
import json
import os
import shutil
import stat
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from HtmlDownloader.cli import Cli
from HtmlDownloader.menu_model import MenuModel
from HtmlDownloader.menu_painter import MenuPainter
from HtmlDownloader.menu_session import MenuSession
from HtmlDownloader.page_download import PageDownload, PageDownloadError
from HtmlDownloader.page_open import PageOpen, PageOpenError
from HtmlDownloader.tui import Tui


PAGE = """<!DOCTYPE html>
<html><head>
<link rel="stylesheet" href="/static/app.css">
<link rel="stylesheet" href="extra.css">
</head>
<body>
<script src="/static/app.js"></script>
<script>inline()</script>
<script src="data:text/javascript,1"></script>
</body></html>
"""
APP_CSS = '@import url("more.css");\nbody { color: red; }\n'
MORE_CSS = "p { margin: 0; }\n"
EXTRA_CSS = "h1 { font-size: 2em; }\n"
APP_JS = "console.log(1);\n"

ABSOLUTE_PAGE = """<!DOCTYPE html>
<html><head>
<link rel="stylesheet" href="https://cdn.example/app.css">
<style>@import url("https://cdn.example/from-style.css");</style>
</head>
<body>
<script src="https://cdn.example/app.js"></script>
<script>inline()</script>
<script src="data:text/javascript,1"></script>
<script src="javascript:alert(1)"></script>
</body></html>
"""
CDN_APP = '@import "https://cdn.example/nested.css";\nbody{}\n'
CDN_NESTED = "p{}\n"
CDN_STYLE = "h1{}\n"
CDN_JS = "var a=1;\n"


class QuietHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        bodies = {
            "/page": (PAGE.encode("utf-8"), "text/html; charset=utf-8"),
            "/static/app.css": (APP_CSS.encode("utf-8"), "text/css"),
            "/static/more.css": (MORE_CSS.encode("utf-8"), "text/css"),
            "/extra.css": (EXTRA_CSS.encode("utf-8"), "text/css"),
            "/static/app.js": (APP_JS.encode("utf-8"), "application/javascript"),
        }
        found = bodies.get(path)
        if found is None:
            self.send_response(404)
            self.end_headers()
            return
        body, content_type = found
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


def start_server():
    server = HTTPServer(("127.0.0.1", 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server


class TestDownload(unittest.TestCase):
    """Typed download saves a page. Menu row 1 is download."""

    def test_cli_download_saves_page_assets_and_map(self):
        """TP-HTMLDOWNLOADER-01, TP-PAGE-01: one page, its assets, and the url map."""
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        previous_home = os.environ.get("HOME")
        previous_lang = os.environ.get("HTMLDOWNLOADER_LANG")
        os.environ["HOME"] = home
        os.environ.pop("HTMLDOWNLOADER_LANG", None)
        server = start_server()
        port = server.server_address[1]
        url = "http://127.0.0.1:{0}/page".format(port)
        try:
            app = Cli()
            self.assertIn("download", Cli.PRODUCT_VERBS)
            self.assertNotIn("hello", Cli.PRODUCT_VERBS)
            previous_tty = Cli.stdout_is_tty
            Cli.stdout_is_tty = staticmethod(lambda: True)
            try:
                self.assertFalse(Cli.opens_text_screen(["download"]))
                self.assertFalse(Cli.opens_text_screen(["download", "--url", url, "--name", "sample"]))
                self.assertTrue(Cli.opens_text_screen([]))
            finally:
                Cli.stdout_is_tty = previous_tty
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = app.run(["download", "--url", url, "--name", "sample"])
            self.assertEqual(code, 0, buf.getvalue())
            root = os.path.join(home, ".app", Cli.APP_NAME, "output")
            page_dir = os.path.join(root, "sample")
            page_path = os.path.join(page_dir, "index.html")
            self.assertTrue(os.path.isfile(page_path))
            self.assertFalse(os.path.isfile(os.path.join(root, "sample")))
            self.assertEqual(stat.S_IMODE(os.stat(page_path).st_mode), 0o600)
            css_dir = os.path.join(page_dir, "assets", "css")
            js_dir = os.path.join(page_dir, "assets", "js")
            img_dir = os.path.join(page_dir, "assets", "img")
            self.assertTrue(os.path.isdir(css_dir))
            self.assertTrue(os.path.isdir(js_dir))
            self.assertTrue(os.path.isdir(img_dir))
            self.assertFalse(os.path.isdir(os.path.join(root, "assets")))
            self.assertEqual(stat.S_IMODE(os.stat(css_dir).st_mode), 0o700)
            for folder in (css_dir, js_dir, img_dir):
                for _path, dirnames, _files in os.walk(folder):
                    self.assertEqual(dirnames, [])
            self.assertEqual(len(os.listdir(css_dir)), 3)
            self.assertEqual(len(os.listdir(js_dir)), 1)
            with open(page_path, encoding="utf-8") as handle:
                text = handle.read()
            self.assertIn("assets/css/", text)
            self.assertIn("assets/js/", text)
            self.assertIn("inline()", text)
            self.assertNotIn('href="/static/app.css"', text)
            self.assertNotIn('href="extra.css"', text)
            self.assertNotIn('src="/static/app.js"', text)
            linked = ""
            for filename in os.listdir(css_dir):
                with open(os.path.join(css_dir, filename), encoding="utf-8") as handle:
                    body = handle.read()
                if "color: red" in body:
                    linked = body
            self.assertNotEqual(linked, "")
            self.assertNotIn('url("more.css")', linked)
            self.assertIn(".css", linked)
            with open(os.path.join(root, "url-map.json"), encoding="utf-8") as handle:
                saved = json.load(handle)
            self.assertEqual(
                saved["pages"],
                [{"url": url, "name": "sample", "html": "index.html"}],
            )
            summary = buf.getvalue()
            self.assertIn("Stylesheets: 3", summary)
            self.assertIn("Scripts: 1", summary)
            self.assertIn("Images: 0", summary)
            self.assertNotIn("Not saved:", summary)

            again = io.StringIO()
            with redirect_stdout(again):
                code = app.run(["download", "--url", url, "--name", "sample"])
            self.assertEqual(code, 0)
            with open(os.path.join(root, "url-map.json"), encoding="utf-8") as handle:
                saved = json.load(handle)
            self.assertEqual(len(saved["pages"]), 1)
            self.assertEqual(len(os.listdir(css_dir)), 3)
        finally:
            server.shutdown()
            server.server_close()
            shutil.rmtree(home, ignore_errors=True)
            if previous_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = previous_home
            if previous_lang is None:
                os.environ.pop("HTMLDOWNLOADER_LANG", None)
            else:
                os.environ["HTMLDOWNLOADER_LANG"] = previous_lang

    def test_download_rejects_a_bad_url_a_bad_name_and_hello(self):
        """TP-HTMLDOWNLOADER-03, TP-PAGE-02, TP-ERR-01: a bad URL, a bad name, and hello do not save."""
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        previous_home = os.environ.get("HOME")
        os.environ["HOME"] = home
        try:
            app = Cli()
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run(["download"])
            self.assertEqual(code, 1)
            self.assertIn("--url", err.getvalue())
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run(["download", "--url", "file:///etc/passwd", "--name", "secret"])
            self.assertEqual(code, 1)
            self.assertIn("http://", err.getvalue())
            self.assertFalse(os.path.exists(os.path.join(home, ".app")))
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run([
                    "download",
                    "--url",
                    "http://127.0.0.1/page",
                    "--name",
                    "../outside",
                ])
            self.assertEqual(code, 1)
            self.assertFalse(os.path.exists(os.path.join(home, "outside")))
            self.assertIn("folder", err.getvalue())
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run(["hello"])
            self.assertEqual(code, 1)
            self.assertIn("Unknown verb 'hello'", err.getvalue())
            help_buf = io.StringIO()
            with redirect_stdout(help_buf):
                self.assertEqual(app.run(["help"]), 0)
            help_text = help_buf.getvalue()
            self.assertIn("download", help_text)
            self.assertIn("crawl", help_text)
            self.assertIn("--url", help_text)
            self.assertIn("--name", help_text)
            self.assertIn("--html", help_text)
            self.assertIn("--depth", help_text)
            self.assertNotIn("list-videos", help_text)
        finally:
            shutil.rmtree(home, ignore_errors=True)
            if previous_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = previous_home

    def test_linked_files_are_rewritten_and_the_map_lists_them(self):
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        seen = []

        def opener(url):
            seen.append(url)
            bodies = {
                "https://cdn.example/page": (ABSOLUTE_PAGE.encode("utf-8"), "text/html; charset=utf-8"),
                "https://cdn.example/app.css": (CDN_APP.encode("utf-8"), "text/css"),
                "https://cdn.example/nested.css": (CDN_NESTED.encode("utf-8"), "text/css"),
                "https://cdn.example/from-style.css": (CDN_STYLE.encode("utf-8"), "text/css"),
                "https://cdn.example/app.js": (CDN_JS.encode("utf-8"), "application/javascript"),
            }
            if url not in bodies:
                raise PageDownloadError("HTTP 404 for {0}.".format(url))
            return bodies[url]

        worker = PageDownload(Cli.APP_NAME, home=home, opener=opener)
        self.assertEqual(worker.choice_lines(), ["No saved pages.", "Type a URL:"])
        self.assertEqual(worker.interpret("1")[0], "error")
        self.assertEqual(worker.interpret("https://cdn.example/page")[0], "url")
        text = worker.download("https://cdn.example/page", "cdn")
        self.assertIn("Stylesheets: 3", text)
        self.assertIn("Scripts: 1", text)
        self.assertNotIn("Not saved:", text)
        self.assertNotIn("data:", " ".join(seen))
        self.assertNotIn("javascript:", " ".join(seen))
        page_dir = os.path.join(home, ".app", Cli.APP_NAME, "output", "cdn")
        page_path = os.path.join(page_dir, "index.html")
        with open(page_path, encoding="utf-8") as handle:
            html = handle.read()
        self.assertIn("assets/css/", html)
        self.assertIn("assets/js/", html)
        self.assertIn("inline()", html)
        self.assertNotIn("https://cdn.example/app.css", html)
        self.assertNotIn("https://cdn.example/app.js", html)
        self.assertNotIn("https://cdn.example/from-style.css", html)
        css_dir = os.path.join(page_dir, "assets", "css")
        nested_ok = False
        for filename in os.listdir(css_dir):
            with open(os.path.join(css_dir, filename), encoding="utf-8") as handle:
                body = handle.read()
            if "body{}" in body:
                self.assertNotIn("https://cdn.example/nested.css", body)
                self.assertIn(".css", body)
                nested_ok = True
        self.assertTrue(nested_ok)
        lines = worker.choice_lines()
        self.assertEqual(lines[1], "1. cdn: https://cdn.example/page")
        kind, value = worker.interpret("1")
        self.assertEqual(kind, "page")
        self.assertEqual(value["name"], "cdn")
        self.assertEqual(value["url"], "https://cdn.example/page")
        worker.download("https://cdn.example/page", "other")
        names = [item["name"] for item in worker.entries()]
        self.assertEqual(names, ["other"])
        shutil.rmtree(home, ignore_errors=True)

    def test_saved_html_drops_base_url_after_local_links(self):
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        page = """<!DOCTYPE html>
<html xml:base="https://cdn.example/root/">
<head>
<base href="https://cdn.example/static/" target="_blank">
<BASE HREF='https://cdn.example/other/'>
<link rel="canonical" href="https://cdn.example/page">
<link href="https://cdn.example/elsewhere" rel="canonical" />
<!--
<script src="https://cdn.example/hidden.js"></script>
-->
<link rel="stylesheet" href="app.css">
</head>
<body>
<script src="app.js"></script>
<p>Visible <!-- side note --> text</p>
</body></html>
"""
        seen = []

        def opener(url):
            seen.append(url)
            bodies = {
                "https://cdn.example/page": (page.encode("utf-8"), "text/html; charset=utf-8"),
                "https://cdn.example/static/app.css": (b"body{color:red}\n", "text/css"),
                "https://cdn.example/static/app.js": (b"var a=1;\n", "application/javascript"),
            }
            if url not in bodies:
                raise PageDownloadError("HTTP 404 for {0}.".format(url))
            return bodies[url]

        try:
            worker = PageDownload(Cli.APP_NAME, home=home, opener=opener)
            text = worker.download("https://cdn.example/page", "based")
            self.assertIn("Stylesheets: 1", text)
            self.assertIn("Scripts: 1", text)
            self.assertIn("https://cdn.example/static/app.css", seen)
            self.assertNotIn("https://cdn.example/other/app.css", seen)
            self.assertNotIn("https://cdn.example/root/app.css", seen)
            page_path = os.path.join(home, ".app", Cli.APP_NAME, "output", "based", "index.html")
            with open(page_path, encoding="utf-8") as handle:
                html = handle.read()
            lowered = html.lower()
            self.assertNotIn("<base", lowered)
            self.assertNotIn("xml:base", lowered)
            self.assertNotIn("canonical", lowered)
            self.assertNotIn("<!--", html)
            self.assertNotIn("-->", html)
            self.assertNotIn("hidden.js", html)
            self.assertNotIn("https://cdn.example/hidden.js", seen)
            self.assertIn("Visible", html)
            self.assertIn("text", html)
            self.assertIn("assets/css/", html)
            self.assertIn("assets/js/", html)
            self.assertNotIn("https://cdn.example/static/", html)
        finally:
            shutil.rmtree(home, ignore_errors=True)

    def test_images_are_flat_and_a_saved_page_is_not_fetched_again(self):
        """TP-HTMLDOWNLOADER-02, TP-PAGE-03: a stored page is not fetched again."""
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        seen = []
        page = """<!DOCTYPE html>
<html><head>
<link rel="icon" href="favicon.ico">
<link rel="stylesheet" href="assets/css/app.css">
</head><body>
<img src="assets/images/avatars/1.jpg">
<img srcset="assets/images/avatars/1.jpg 1x, assets/images/other/1.jpg 2x">
<div style="background-image: url('assets/images/dropdown-header/city2.jpg')"></div>
</body></html>
"""
        css = (
            'body{background:url("../images/bg/hero.png")}\n'
            '@font-face{src:url("../woff2/roboto.woff2")}\n'
            'i{background:url("../svg/flags/ai.svg#ai")}\n'
        )
        bodies = {
            "https://cdn.example/page": (page.encode("utf-8"), "text/html"),
            "https://cdn.example/assets/css/app.css": (css.encode("utf-8"), "text/css"),
            "https://cdn.example/favicon.ico": (b"ICO1", "image/x-icon"),
            "https://cdn.example/assets/images/avatars/1.jpg": (b"JPG1", "image/jpeg"),
            "https://cdn.example/assets/images/other/1.jpg": (b"JPG2", "image/jpeg"),
            "https://cdn.example/assets/images/dropdown-header/city2.jpg": (b"JPG3", "image/jpeg"),
            "https://cdn.example/assets/images/bg/hero.png": (b"PNG1", "image/png"),
            "https://cdn.example/assets/woff2/roboto.woff2": (b"WOFF", "font/woff2"),
            "https://cdn.example/assets/svg/flags/ai.svg": (b"<svg/>", "image/svg+xml"),
        }

        def opener(url):
            seen.append(url)
            if url not in bodies:
                raise PageDownloadError("HTTP 404 for {0}.".format(url))
            return bodies[url]

        try:
            worker = PageDownload(Cli.APP_NAME, home=home, opener=opener)
            text = worker.download("https://cdn.example/page", "fiori")
            self.assertIn("Saved fiori", text)
            self.assertIn("Images: 6", text)
            self.assertIn("Fonts: 1", text)
            self.assertNotIn("Not saved:", text)
            root = os.path.join(home, ".app", Cli.APP_NAME, "output")
            page_dir = os.path.join(root, "fiori")
            index = os.path.join(page_dir, "index.html")
            css_dir = os.path.join(page_dir, "assets", "css")
            js_dir = os.path.join(page_dir, "assets", "js")
            img_dir = os.path.join(page_dir, "assets", "img")
            self.assertTrue(os.path.isfile(index))
            self.assertFalse(os.path.isdir(os.path.join(root, "assets")))
            for folder in (css_dir, js_dir, img_dir):
                self.assertTrue(os.path.isdir(folder))
                for _path, dirnames, _files in os.walk(folder):
                    self.assertEqual(dirnames, [])
            self.assertEqual(len(os.listdir(img_dir)), 6)
            with open(index, encoding="utf-8") as handle:
                html = handle.read()
            self.assertNotIn("assets/images/", html)
            self.assertNotIn("dropdown-header", html)
            self.assertIn("assets/img/", html)
            self.assertIn("assets/css/", html)
            css_name = ""
            css_text = ""
            for name in os.listdir(css_dir):
                if name.endswith(".css"):
                    css_name = name
                    with open(os.path.join(css_dir, name), encoding="utf-8") as handle:
                        css_text = handle.read()
            self.assertNotEqual(css_name, "")
            self.assertNotIn("../images/", css_text)
            self.assertNotIn("../woff2/", css_text)
            self.assertNotIn("../svg/", css_text)
            self.assertIn("../img/", css_text)
            self.assertIn(".woff2", css_text)
            self.assertIn("#ai", css_text)
            self.assertTrue(any(name.endswith(".woff2") for name in os.listdir(css_dir)))
            seen.clear()
            again = worker.download("https://cdn.example/page", "fiori")
            self.assertIn("Continued fiori", again)
            self.assertEqual(seen, [])
            hero_name = ""
            for name in os.listdir(img_dir):
                with open(os.path.join(img_dir, name), "rb") as handle:
                    if handle.read() == b"PNG1":
                        hero_name = name
            self.assertNotEqual(hero_name, "")
            os.remove(os.path.join(img_dir, hero_name))
            css_text = css_text.replace("../img/" + hero_name, "../images/bg/hero.png")
            with open(os.path.join(css_dir, css_name), "w", encoding="utf-8") as handle:
                handle.write(css_text)
            seen.clear()
            worker.download("https://cdn.example/page", "fiori")
            self.assertEqual(seen, ["https://cdn.example/assets/images/bg/hero.png"])
            restored = False
            for name in os.listdir(img_dir):
                with open(os.path.join(img_dir, name), "rb") as handle:
                    if handle.read() == b"PNG1":
                        restored = True
            self.assertTrue(restored)
            for _path, dirnames, _files in os.walk(img_dir):
                self.assertEqual(dirnames, [])
        finally:
            shutil.rmtree(home, ignore_errors=True)

    def test_old_page_file_continues_from_index_html(self):
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        root = os.path.join(home, ".app", Cli.APP_NAME, "output")
        legacy_css = os.path.join(root, "assets", "css")
        os.makedirs(legacy_css)
        with open(os.path.join(legacy_css, "app.css"), "w", encoding="utf-8") as handle:
            handle.write("body{color:red}\n")
        html = (
            "<html><link rel=\"stylesheet\" href=\"assets/css/app.css\">"
            "<img src=\"assets/images/a/b.png\"></html>"
        )
        with open(os.path.join(root, "legacy"), "w", encoding="utf-8") as handle:
            handle.write(html)
        seen = []

        def opener(url):
            seen.append(url)
            if url == "https://cdn.example/dir/assets/images/a/b.png":
                return (b"PNG", "image/png")
            raise PageDownloadError("HTTP 404 for {0}.".format(url))

        try:
            worker = PageDownload(Cli.APP_NAME, home=home, opener=opener)
            text = worker.download("https://cdn.example/dir/page", "legacy")
            self.assertIn("Continued legacy", text)
            self.assertNotIn("Not saved:", text)
            self.assertEqual(seen, ["https://cdn.example/dir/assets/images/a/b.png"])
            self.assertFalse(os.path.exists(os.path.join(root, "legacy")) and os.path.isfile(os.path.join(root, "legacy")))
            index = os.path.join(root, "legacy", "index.html")
            self.assertTrue(os.path.isfile(index))
            self.assertTrue(os.path.isfile(os.path.join(root, "legacy", "assets", "css", "app.css")))
            with open(index, encoding="utf-8") as handle:
                saved = handle.read()
            self.assertNotIn("assets/images/", saved)
            self.assertIn("assets/img/", saved)
            img_dir = os.path.join(root, "legacy", "assets", "img")
            self.assertEqual(len(os.listdir(img_dir)), 1)
            for name in ("css", "js", "img"):
                for _path, dirnames, _files in os.walk(os.path.join(root, "legacy", "assets", name)):
                    self.assertEqual(dirnames, [])
        finally:
            shutil.rmtree(home, ignore_errors=True)

    def test_html_file_name_defaults_renames_and_rejects(self):
        """TP-PAGE-05: --html, a rename, and a rejected path."""
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        calls = []

        def opener(url):
            calls.append(url)
            return (b"<html><p>ok</p></html>", "text/html")

        try:
            worker = PageDownload(Cli.APP_NAME, home=home, opener=opener)
            url = "https://cdn.example/page"
            text = worker.download(url, "sample")
            root = os.path.join(home, ".app", Cli.APP_NAME, "output")
            index = os.path.join(root, "sample", "index.html")
            custom = os.path.join(root, "sample", "page.html")
            self.assertIn("Saved sample", text)
            self.assertTrue(os.path.isfile(index))
            self.assertEqual(calls, [url])
            text = worker.download(url, "sample")
            self.assertIn("Continued sample", text)
            self.assertEqual(calls, [url])
            text = worker.download(url, "sample", "page.html")
            self.assertIn("Continued sample", text)
            self.assertEqual(calls, [url])
            self.assertFalse(os.path.isfile(index))
            self.assertTrue(os.path.isfile(custom))
            with open(os.path.join(root, "url-map.json"), encoding="utf-8") as handle:
                saved = json.load(handle)
            self.assertEqual(saved["pages"][0]["html"], "page.html")
            self.assertIn("sample [page.html]", "\n".join(worker.choice_lines()))
            text = worker.download(url, "sample")
            self.assertIn("Continued sample", text)
            self.assertEqual(calls, [url])
            self.assertTrue(os.path.isfile(custom))
            for bad in ("assets", "url-map.json", "../x", "a/b", "a\\b", ".", ".."):
                with self.assertRaises(PageDownloadError):
                    worker.download(url, "sample", bad)
            self.assertTrue(os.path.isfile(custom))
            self.assertFalse(os.path.exists(os.path.join(home, "x")))
            self.assertFalse(os.path.isdir(os.path.join(root, "sample", "a")))
        finally:
            shutil.rmtree(home, ignore_errors=True)

    def test_url_recommends_the_html_file_and_the_folder(self):
        """TP-PAGE-06: guide.html and xxx recommend the folder and the file."""
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        calls = []

        def opener(url):
            calls.append(url)
            return (b"<html>ok</html>", "text/html")

        try:
            worker = PageDownload(Cli.APP_NAME, home=home, opener=opener)
            self.assertEqual(
                worker.recommend("https://example.com/docs/guide.html"),
                ("guide", "guide.html"),
            )
            self.assertEqual(
                worker.recommend("https://example.com/docs/guide.htm?x=1"),
                ("guide", "guide.htm"),
            )
            self.assertEqual(
                worker.recommend("https://example.com/docs/Guide.HTML"),
                ("Guide", "Guide.HTML"),
            )
            self.assertEqual(
                worker.recommend("https://example.com/a/xxx/"),
                ("xxx", "index.html"),
            )
            self.assertEqual(worker.recommend("https://example.com/"), ("", "index.html"))
            self.assertEqual(
                worker.recommend("https://example.com/a/b.php"),
                ("", "index.html"),
            )
            self.assertEqual(
                worker.recommend("https://example.com/assets.html"),
                ("", "assets.html"),
            )
            self.assertEqual(
                worker.recommend("https://example.com/my%2Fevil.html"),
                ("evil", "evil.html"),
            )
            root = os.path.join(home, ".app", Cli.APP_NAME, "output")
            text = worker.download("https://example.com/docs/guide.html", "")
            self.assertIn("Saved guide", text)
            self.assertTrue(os.path.isfile(os.path.join(root, "guide", "guide.html")))
            self.assertFalse(os.path.isfile(os.path.join(root, "guide", "index.html")))
            self.assertEqual(calls, ["https://example.com/docs/guide.html"])
            text = worker.download("https://example.com/docs/guide.html", "")
            self.assertIn("Continued guide", text)
            self.assertEqual(calls, ["https://example.com/docs/guide.html"])
            text = worker.download("https://example.com/a/xxx/", "")
            self.assertIn("Saved xxx", text)
            self.assertTrue(os.path.isfile(os.path.join(root, "xxx", "index.html")))
            text = worker.download("https://example.com/docs/guide.html", "docs")
            self.assertTrue(os.path.isfile(os.path.join(root, "docs", "guide.html")))
            text = worker.download("https://example.com/a/xxx", "sample")
            self.assertTrue(os.path.isfile(os.path.join(root, "sample", "index.html")))
            seen = len(calls)
            text = worker.download("https://example.com/docs/guide.html", "sample")
            self.assertIn("Continued sample", text)
            self.assertEqual(len(calls), seen)
            self.assertTrue(os.path.isfile(os.path.join(root, "sample", "index.html")))
            self.assertFalse(os.path.isfile(os.path.join(root, "sample", "guide.html")))
            with self.assertRaises(PageDownloadError):
                worker.download("https://example.com/", "")
            self.assertEqual(len(calls), seen)
        finally:
            shutil.rmtree(home, ignore_errors=True)

    def test_menu_accepts_the_name_recommended_from_the_url(self):
        home = tempfile.mkdtemp(prefix="htmlname_", dir="/tmp")
        painter = MenuPainter(home=home)
        model = MenuModel(painter=painter)
        tui = Tui()
        tui.painter = painter
        worker = PageDownload(Cli.APP_NAME, home=home)

        class EnterScreen:
            def __init__(self, keys):
                self.keys = list(keys)

            def getmaxyx(self):
                return (24, 80)

            def erase(self):
                return None

            def addstr(self, y, x, text, _attr=0):
                return None

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

        try:
            folder = tui._ask_page_name(
                EnterScreen([10]),
                model,
                worker,
                "https://example.com/a/xxx/",
            )
            self.assertEqual(folder, "xxx")
            self.assertEqual(
                worker.suggested_html("https://example.com/a/xxx/", folder),
                "index.html",
            )
            folder = tui._ask_page_name(
                EnterScreen([10]),
                model,
                worker,
                "https://example.com/docs/guide.html",
            )
            self.assertEqual(folder, "guide")
            self.assertEqual(
                worker.suggested_html("https://example.com/docs/guide.html", folder),
                "guide.html",
            )
            missing = tui._ask_page_name(
                EnterScreen([10, 27]),
                model,
                worker,
                "https://example.com/",
            )
            self.assertIsNone(missing)
        finally:
            shutil.rmtree(home, ignore_errors=True)

    def test_cli_download_uses_the_url_when_name_is_omitted(self):
        """TP-PAGE-06: an omitted --name uses the name recommended from the URL."""
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        previous_home = os.environ.get("HOME")
        os.environ["HOME"] = home

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.split("?", 1)[0]
                if path not in ("/guide.html", "/xxx"):
                    self.send_response(404)
                    self.end_headers()
                    return
                body = b"<html>ok</html>"
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, fmt, *args):
                return

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        port = server.server_address[1]
        try:
            app = Cli()
            guide = "http://127.0.0.1:{0}/guide.html".format(port)
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = app.run(["download", "--url", guide])
            self.assertEqual(code, 0, buf.getvalue())
            root = os.path.join(home, ".app", Cli.APP_NAME, "output")
            self.assertTrue(os.path.isfile(os.path.join(root, "guide", "guide.html")))
            self.assertFalse(os.path.isfile(os.path.join(root, "guide", "index.html")))
            folder = "http://127.0.0.1:{0}/xxx".format(port)
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = app.run(["download", "--url", folder])
            self.assertEqual(code, 0, buf.getvalue())
            self.assertTrue(os.path.isfile(os.path.join(root, "xxx", "index.html")))
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run(["download", "--url", "http://127.0.0.1:{0}/".format(port)])
            self.assertEqual(code, 1)
            self.assertIn("--name", err.getvalue())
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
            shutil.rmtree(home, ignore_errors=True)
            if previous_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = previous_home

    def test_cli_html_flag_is_download_only(self):
        seen = {}
        original = PageDownload.download

        def fake_download(self, url, name, html=None):
            seen["url"] = url
            seen["name"] = name
            seen["html"] = html
            return "Saved sample"

        PageDownload.download = fake_download
        try:
            app = Cli()
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = app.run([
                    "download",
                    "--url",
                    "https://example.com/",
                    "--name",
                    "sample",
                    "--html",
                    "page.html",
                ])
            self.assertEqual(code, 0)
            self.assertEqual(seen["html"], "page.html")
            self.assertIn("Saved sample", buf.getvalue())
            previous_tty = Cli.stdout_is_tty
            Cli.stdout_is_tty = staticmethod(lambda: True)
            try:
                self.assertFalse(Cli.opens_text_screen([
                    "download",
                    "--url",
                    "https://example.com/",
                    "--name",
                    "sample",
                    "--html",
                    "page.html",
                ]))
            finally:
                Cli.stdout_is_tty = previous_tty
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run(["serve", "--html", "page.html", "--page-name", "sample"])
            self.assertEqual(code, 1)
            self.assertIn("only for download", err.getvalue())
        finally:
            PageDownload.download = original

    def test_menu_row_1_is_download(self):
        home = tempfile.mkdtemp(prefix="htmldl_", dir="/tmp")
        saved = os.environ.get("HTMLDOWNLOADER_LANG")
        os.environ.pop("HTMLDOWNLOADER_LANG", None)
        painter = MenuPainter(home=home)
        try:
            rows = painter.display_rows("front")
        finally:
            if saved is None:
                os.environ.pop("HTMLDOWNLOADER_LANG", None)
            else:
                os.environ["HTMLDOWNLOADER_LANG"] = saved
        self.assertEqual(
            rows[0],
            (1, "download", "download a page and its stylesheets, scripts, and images", "download"),
        )
        tui = Tui()
        session = MenuSession(
            Cli.APP_NAME,
            Cli.VERSION,
            on_version=lambda: "",
            on_about=lambda: "",
            on_kind=lambda kind: "download" if kind == "download" else None,
            painter=painter,
        )
        session.model = MenuModel(painter=painter)
        self.assertEqual(session.take_action("download"), "stay")
        self.assertEqual(session.model.phase, "result")
        self.assertEqual(session.model.result_text, "download")
        self.assertFalse(hasattr(tui, "hello_text"))
        shutil.rmtree(home, ignore_errors=True)

    def test_page_name_clears_the_box_and_says_please_wait(self):
        """The download screen shows Please wait with an empty box before it fetches."""
        home = tempfile.mkdtemp(prefix="htmlwait_", dir="/tmp")
        saved = {
            name: os.environ.get(name)
            for name in ("HOME", "HTMLDOWNLOADER_LANG")
        }
        os.environ["HOME"] = home
        os.environ.pop("HTMLDOWNLOADER_LANG", None)
        painter = MenuPainter(home=home)
        model = MenuModel(painter=painter)
        tui = Tui()
        tui.painter = painter
        keys = [ord(char) for char in "https://example.com/"] + [10]
        keys += [ord(char) for char in "fiori"] + [10, 10]

        class WaitScreen:
            """Feeds the page-name keys and records the painted text."""

            def __init__(self):
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

        screen = WaitScreen()
        captured = {}
        original = PageDownload.download

        def fake_download(self, url, name, html=None):
            captured["url"] = url
            captured["name"] = name
            captured["html"] = html
            captured["buffer"] = model.buffer
            captured["focus"] = model.focus
            captured["text"] = [item[2] for item in screen.calls]
            return "Saved fiori"

        PageDownload.download = fake_download
        try:
            model.buffer = "leftover"
            model.cursor = 8
            model.focus = "input"
            text = tui._download_on_screen(screen, model)
        finally:
            PageDownload.download = original
            if saved["HOME"] is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = saved["HOME"]
            if saved["HTMLDOWNLOADER_LANG"] is None:
                os.environ.pop("HTMLDOWNLOADER_LANG", None)
            else:
                os.environ["HTMLDOWNLOADER_LANG"] = saved["HTMLDOWNLOADER_LANG"]
            shutil.rmtree(home, ignore_errors=True)
        self.assertEqual(text, "Saved fiori")
        self.assertEqual(captured["url"], "https://example.com/")
        self.assertEqual(captured["name"], "fiori")
        self.assertEqual(captured["html"], "index.html")
        self.assertEqual(captured["buffer"], "")
        self.assertEqual(captured["focus"], "list")
        self.assertIn("Please wait.", captured["text"])
        self.assertIn("Page name: fiori", captured["text"])
        self.assertIn("HTML file: index.html", captured["text"])
        self.assertNotIn("█", "".join(captured["text"]))

    def test_menu_html_prompt_accepts_a_typed_name(self):
        painter = MenuPainter()
        model = MenuModel(painter=painter)
        tui = Tui()
        tui.painter = painter
        worker = PageDownload(Cli.APP_NAME, home=tempfile.mkdtemp(prefix="htmlname_", dir="/tmp"))
        keys = [ord(char) for char in "assets"] + [10]
        keys += [ord(char) for char in "home.html"] + [10]

        class NameScreen:
            def __init__(self):
                self.keys = list(keys)

            def getmaxyx(self):
                return (24, 80)

            def erase(self):
                return None

            def addstr(self, y, x, text, _attr=0):
                return None

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

        try:
            chosen = tui._ask_html_name(NameScreen(), model, worker, "index.html")
        finally:
            shutil.rmtree(worker.home, ignore_errors=True)
        self.assertEqual(chosen, "home.html")


class TestListDownloaded(unittest.TestCase):
    """Menu row 2 lists saved page names, then edit and view when the tools exist."""

    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="htmllist_", dir="/tmp")
        self.saved = {
            name: os.environ.get(name)
            for name in ("HOME", "HTMLDOWNLOADER_LANG", "BROWSER")
        }
        os.environ["HOME"] = self.home
        os.environ.pop("HTMLDOWNLOADER_LANG", None)
        os.environ.pop("BROWSER", None)
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

    def _write_page(self, name, url, body="<html>ok</html>\n"):
        root = os.path.join(self.home, ".app", "HtmlDownloader", "output")
        folder = os.path.join(root, name)
        os.makedirs(folder, mode=0o700)
        index = os.path.join(folder, "index.html")
        with open(index, "w", encoding="utf-8") as handle:
            handle.write(body)
        os.chmod(index, 0o600)
        return index

    def _write_map(self, pages):
        root = os.path.join(self.home, ".app", "HtmlDownloader", "output")
        os.makedirs(root, mode=0o700, exist_ok=True)
        path = os.path.join(root, "url-map.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"pages": pages}, handle)
            handle.write("\n")
        os.chmod(path, 0o600)

    def _commit(self, token):
        self.model.buffer = token
        self.model.cursor = len(token)
        self.model.focus = "input"
        return self.model.apply_key(10)

    def test_saved_pages_skip_missing_and_empty_files(self):
        kept = self._write_page("fiori", "https://example.com/fiori")
        self._write_page("empty", "https://example.com/empty", body="")
        self._write_map([
            {"url": "https://example.com/fiori", "name": "fiori"},
            {"url": "https://example.com/gone", "name": "gone"},
            {"url": "https://example.com/empty", "name": "empty"},
        ])
        worker = PageDownload("HtmlDownloader", home=self.home)
        pages = worker.saved_pages()
        self.assertEqual([item["name"] for item in pages], ["fiori"])
        self.assertEqual(pages[0]["index"], kept)
        self.assertEqual(pages[0]["html"], "index.html")
        self.assertEqual(self._commit("2"), "list-downloaded")
        self.assertIsNone(self.tui._open_downloaded(self.model))
        self.assertEqual(self.model.layer, "pages")
        shown = self.model.rows()
        self.assertEqual([(row[0], row[1]) for row in shown], [(1, "fiori"), (0, "Back")])
        self.assertEqual(shown[0][2], "https://example.com/fiori")

    def test_list_shows_a_custom_html_name(self):
        index = self._write_page("fiori", "https://example.com/fiori")
        custom = os.path.join(os.path.dirname(index), "page.html")
        os.rename(index, custom)
        self._write_map([{
            "url": "https://example.com/fiori",
            "name": "fiori",
            "html": "page.html",
        }])
        self.assertIsNone(self.tui._open_downloaded(self.model))
        shown = self.model.rows()
        self.assertEqual(shown[0][1], "fiori [page.html]")
        self.assertEqual(self.tui._saved_by_kind["saved-1"]["index"], custom)

    def test_no_saved_pages_is_a_result(self):
        self.assertEqual(self.tui._open_downloaded(self.model), "No saved pages.")
        self.assertEqual(self.model.layer, "front")

    def test_edit_and_view_hide_when_the_tool_is_missing(self):
        index = self._write_page("fiori", "https://example.com/fiori")
        self._write_map([{"url": "https://example.com/fiori", "name": "fiori"}])
        self.tui._open_downloaded(self.model)
        seen = []

        def opener(**kwargs):
            return PageOpen(
                which=kwargs.get("which", lambda _name: ""),
                desktop_file=kwargs.get("desktop_file", lambda _name: ""),
                browser_command=kwargs["browser_command"],
                runner=lambda argv: seen.append(list(argv)),
                platform_name="linux",
            )

        self.tui._page_open = opener(browser_command=lambda: [])
        self.assertIsNone(self.tui._open_saved_page(self.model, "saved-1"))
        self.assertEqual([row[0] for row in self.model.rows()], [0])
        self.assertIn("Visual Studio Code", self.model.notice)
        self.assertIn("default browser", self.model.notice)
        self.assertIsNone(self._commit("21"))
        self.assertIn("not on this list", self.model.error)
        self.assertEqual(self.model.layer, "page-action")

        self.tui._page_open = opener(
            which=lambda name: "/usr/bin/code" if name == "code" else "",
            browser_command=lambda: [],
        )
        self.assertIsNone(self.tui._open_saved_page(self.model, "saved-1"))
        self.assertEqual([row[0] for row in self.model.rows()], [21, 0])
        self.assertEqual(self.model.rows()[0][1], "edit")
        self.assertEqual(self.model.notice, "")
        self.assertEqual(self._commit("21"), "edit-page")
        text = self.tui._edit_saved_page()
        self.assertEqual(text, "Opened fiori in Visual Studio Code.")
        self.assertEqual(seen[-1][0], "/usr/bin/code")
        self.assertEqual(seen[-1][1], index)

        self.tui._page_open = opener(browser_command=lambda: ["firefox"])
        self.assertIsNone(self.tui._open_saved_page(self.model, "saved-1"))
        self.assertEqual([row[0] for row in self.model.rows()], [22, 0])
        self.assertEqual(self.model.rows()[0][1], "view")
        self.assertIsNone(self._commit("21"))
        self.assertIn("not on this list", self.model.error)
        text = self.tui._view_saved_page()
        self.assertEqual(text, "Opened fiori in the default browser.")
        self.assertEqual(seen[-1][0], "firefox")
        self.assertTrue(seen[-1][-1].startswith("file:"))
        self.assertIsNone(self._commit("0"))
        self.assertEqual(self.model.layer, "pages")

    def test_view_uses_the_default_browser_desktop_entry(self):
        index = self._write_page("fiori", "https://example.com/fiori")
        desktop = os.path.join(self.home, "firefox.desktop")
        with open(desktop, "w", encoding="utf-8") as handle:
            handle.write("[Desktop Entry]\nExec=firefox %u\nTryExec=firefox\n")
        seen = []
        opener = PageOpen(
            which=lambda name: "/usr/bin/" + name if name in ("xdg-mime", "firefox") else "",
            run_text=lambda _argv: "firefox.desktop\n",
            desktop_file=lambda name: desktop if name == "firefox.desktop" else "",
            runner=lambda argv: seen.append(list(argv)),
            platform_name="linux",
        )
        self.assertEqual(opener.actions(), ("view",))
        opener.view(index)
        self.assertEqual(seen, [["firefox", Path(os.path.abspath(index)).as_uri()]])
        missing = PageOpen(
            which=lambda name: "/usr/bin/xdg-mime" if name == "xdg-mime" else "",
            run_text=lambda _argv: "gone.desktop\n",
            desktop_file=lambda _name: "",
            platform_name="linux",
        )
        self.assertEqual(missing.actions(), ())
        with self.assertRaises(PageOpenError):
            missing.view(index)

    def test_code_desktop_entry_opens_the_page_when_code_is_not_on_path(self):
        index = self._write_page("fiori", "https://example.com/fiori")
        desktop = os.path.join(self.home, "code.desktop")
        with open(desktop, "w", encoding="utf-8") as handle:
            handle.write("[Desktop Entry]\nExec=/usr/bin/code %F\n")
        seen = []
        opener = PageOpen(
            which=lambda _name: "",
            desktop_file=lambda name: desktop if name == "code.desktop" else "",
            browser_command=lambda: [],
            runner=lambda argv: seen.append(list(argv)),
            platform_name="linux",
        )
        self.assertEqual(opener.actions(), ("edit",))
        opener.edit(index)
        self.assertEqual(seen, [["/usr/bin/code", index]])
        with self.assertRaises(PageOpenError):
            opener.edit(os.path.join(self.home, "missing.html"))


if __name__ == "__main__":
    unittest.main()
