# =============================================================================
# Serve one saved page as static files.
# The page folder is the site root. Listening stays on 127.0.0.1.
# An empty port uses 5000. Ctrl+C stops the server.
# =============================================================================
from __future__ import annotations

import http.server
import mimetypes
import os

from .page_download import PageDownload, PageDownloadError


class PageServeError(Exception):
    """The saved page cannot be served."""

    def __init__(self, message="", logger=None):
        super().__init__(message)
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="PageServeError")


class PageServe:
    """Serve one saved page on this computer. One class in this file.

    The page folder is the site root. The stored HTML file is /. That file
    defaults to index.html. Assets stay under that folder. The server listens
    on 127.0.0.1. An empty port uses 5000.
    """

    DEFAULT_PORT = 5000
    BIND = "127.0.0.1"

    class _Server(http.server.ThreadingHTTPServer):
        allow_reuse_address = True
        daemon_threads = True

    def __init__(self, app_name, logger=None, home=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="PageServe")
        self.pages = PageDownload(app_name, logger=logger, home=home)
        self._register_types()

    def _register_types(self) -> None:
        pairs = (
            (".woff2", "font/woff2"),
            (".woff", "font/woff"),
            (".ttf", "font/ttf"),
            (".otf", "font/otf"),
            (".eot", "application/vnd.ms-fontobject"),
        )
        for ext, kind in pairs:
            mimetypes.add_type(kind, ext)

    def parse_port(self, port) -> int:
        """General Purpose: A TCP port from 1 to 65535. Empty uses 5000."""
        if port is None:
            return self.DEFAULT_PORT
        text = str(port).strip()
        if text == "":
            return self.DEFAULT_PORT
        if not text.isdigit():
            raise PageServeError("Port must be a number from 1 to 65535.")
        number = int(text)
        if number < 1 or number > 65535:
            raise PageServeError("Port must be a number from 1 to 65535.")
        return number

    def listen(self, name, port=None):
        """General Purpose: Bind one saved page. The caller accepts connections.

        Returns the server, the URL, the page name, and the page folder.
        """
        clean, directory, number, html_name = self._ready(name, port)
        handler = self._handler_class(directory, html_name)
        try:
            httpd = self._Server((self.BIND, number), handler)
        except OSError as exc:
            reason = exc.strerror or "the port could not be opened"
            raise PageServeError(
                "Port {0} is not available. {1}.".format(number, reason)
            )
        url = "http://{0}:{1}/".format(self.BIND, httpd.server_address[1])
        return httpd, url, clean, directory

    def serve(self, name, port=None) -> str:
        """General Purpose: Serve one saved page until Ctrl+C.

        Prints the page and the URL, then blocks. Returns a stopped line.
        """
        httpd, url, clean, directory = self.listen(name, port)
        print("Serving {0}".format(clean))
        print("Page: {0}".format(os.path.join(directory, self.pages.html_name_for(clean))))
        print("URL: {0}".format(url))
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()
        return "Stopped {0}.".format(clean)

    def _ready(self, name, port):
        try:
            clean = self.pages.clean_name(name)
            directory = self.pages._page_dir(clean)
        except PageDownloadError as exc:
            raise PageServeError(str(exc))
        html_name = self.pages.html_name_for(clean)
        index = os.path.join(directory, html_name)
        if not os.path.isfile(index):
            raise PageServeError("{0} is not a saved page.".format(clean))
        try:
            size = os.path.getsize(index)
        except OSError:
            raise PageServeError("{0} is not a saved page.".format(clean))
        if size <= 0:
            raise PageServeError("{0} is not a saved page.".format(clean))
        return clean, directory, self.parse_port(port), html_name

    def _handler_class(self, directory, html_name):
        index_name = html_name

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)

            def _point_at_page(self):
                """/ is the stored HTML file. The file name itself stays reachable."""
                raw = self.path
                query = ""
                if "?" in raw:
                    raw, query = raw.split("?", 1)
                    query = "?" + query
                if raw in ("", "/"):
                    self.path = "/" + index_name + query

            def do_GET(self):
                self._point_at_page()
                return super().do_GET()

            def do_HEAD(self):
                self._point_at_page()
                return super().do_HEAD()

            def log_message(self, fmt, *args):
                return

        return Handler
