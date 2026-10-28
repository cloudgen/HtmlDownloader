# =============================================================================
# Download one HTML page and the stylesheets, scripts, and images it links to.
# requirement-python-oop — class PageDownload.
# requirement-python-coding-style — publish with shutil.move.
# requirement-python-error-handling — a failed fetch names the URL and stops.
# Each page is ~/.app/<app name>/output/<page name>/<html file>.
# The HTML file name defaults to index.html.
# A URL that ends in .html or .htm recommends that file name.
# A URL that ends in a folder name such as xxx recommends xxx/index.html.
# Flat asset folders are assets/css, assets/js, and assets/img under that page.
# The url map stays at ~/.app/<app name>/output/url-map.json.
# =============================================================================
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit, urlunsplit, urljoin


class PageDownloadError(Exception):
    """A download cannot continue. The message is safe to show to the operator."""

    def __init__(self, message="", logger=None):
        super().__init__(message)
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="PageDownloadError")


class PageDownload:
    """Save one page, its stylesheets, its scripts, and its images.

    output/<page name>/<html file> is the page. The HTML file name defaults
    to index.html. output/<page name>/assets/css/, assets/js/, and assets/img/
    are flat. Those three folders have no subfolders. Font files sit in
    assets/css/. output/url-map.json remembers the url, the page name, and
    the HTML file name. When that HTML file is already there, the page URL
    is not fetched again. A different HTML file name moves the file already
    stored for this page. Links in that file are checked, missing files are
    fetched, and saved files are kept.
    """

    APP_PARENT = ".app"
    OUTPUT_DIR = "output"
    ASSETS_DIR = "assets"
    CSS_DIR = "css"
    JS_DIR = "js"
    IMG_DIR = "img"
    INDEX_NAME = "index.html"
    MAP_NAME = "url-map.json"
    MAX_BYTES = 15 * 1024 * 1024
    TIMEOUT_SECONDS = 30
    MAX_CSS = 40
    MAX_JS = 40
    MAX_IMG = 400
    MAX_FONT = 80
    MAX_CSS_DEPTH = 4
    IMAGE_EXTS = (
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".bmp", ".avif", ".apng",
    )
    FONT_EXTS = (".woff", ".woff2", ".ttf", ".otf", ".eot")
    IMPORT_RE = re.compile(
        r"""@import\s+(?:url\(\s*(['"]?)([^'")\s]+)\1\s*\)|(['"])([^'"]+)\3)""",
        re.IGNORECASE,
    )
    URL_RE = re.compile(
        r"""url\(\s*(['"]?)([^'")\s]+)\1\s*\)""",
        re.IGNORECASE,
    )
    LOCAL_HTML_RE = re.compile(r"^assets/(css|js|img)/([^/]+)$")
    COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
    BASE_TAG_RE = re.compile(r"<\s*/?\s*base\b[^>]*>", re.IGNORECASE)
    XML_BASE_RE = re.compile(
        r"""\s+xml:base\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'=<>`]+)""",
        re.IGNORECASE,
    )
    CANONICAL_LINK_RE = re.compile(
        r"""<\s*link\b[^>]*\brel\s*=\s*(?:"\s*canonical\s*"|'\s*canonical\s*'|canonical(?=[\s/>]))[^>]*>""",
        re.IGNORECASE,
    )
    HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

    def __init__(self, app_name, logger=None, home=None, opener=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="PageDownload")
        self.app_name = app_name
        if home is None:
            home = os.environ.get("HOME", "")
        self.home = home
        self.opener = opener
        self.user_agent = None
        self.gate = None

    def output_root(self) -> str:
        """General Purpose: The folder that holds pages, assets, and the url map."""
        self._require_home()
        return os.path.join(self.home, self.APP_PARENT, self.app_name, self.OUTPUT_DIR)

    def entries(self) -> list:
        """General Purpose: Saved url and page name pairs, in list order."""
        path = self._map_path()
        if not path or not os.path.isfile(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            return []
        pages = data.get("pages") if isinstance(data, dict) else None
        if not isinstance(pages, list):
            return []
        kept = []
        for item in pages:
            if not isinstance(item, dict):
                continue
            url = item.get("url")
            name = item.get("name")
            if isinstance(url, str) and isinstance(name, str) and url and name:
                kept.append({
                    "url": url,
                    "name": name,
                    "html": self._stored_html(item.get("html")),
                })
        return kept

    def saved_pages(self) -> list:
        """General Purpose: Downloaded pages that already have an HTML file.

        Each item has name, url, html, and index. The url-map order is kept.
        A map row with no page file is left out. A row with no html name
        means index.html.
        """
        found = []
        for entry in self.entries():
            try:
                path = self._html_path(entry["name"], entry["html"])
            except PageDownloadError:
                continue
            if not os.path.isfile(path):
                continue
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size <= 0:
                continue
            found.append({
                "name": entry["name"],
                "url": entry["url"],
                "html": entry["html"],
                "index": path,
            })
        return found

    def choice_lines(self) -> list:
        """General Purpose: Numbered page name and url lines for the download prompt."""
        entries = self.entries()
        if not entries:
            return ["No saved pages.", "Type a URL:"]
        lines = ["Saved pages:"]
        for index, entry in enumerate(entries, start=1):
            label = entry["name"]
            if entry["html"] != self.INDEX_NAME:
                label = "{0} [{1}]".format(entry["name"], entry["html"])
            lines.append("{0}. {1}: {2}".format(index, label, entry["url"]))
        lines.append("")
        lines.append("Type a number, or type a URL:")
        return lines

    def interpret(self, raw):
        """General Purpose: A list number, a URL, or an error sentence.

        Returns ('page', entry), ('url', url), or ('error', message).
        """
        text = (raw or "").strip()
        rows = self.entries()
        if text.isdigit():
            number = int(text)
            if 1 <= number <= len(rows):
                return ("page", rows[number - 1])
            if rows:
                return ("error", "Enter 1–{0}, or type a URL.".format(len(rows)))
            return ("error", "Type a URL that starts with http:// or https://.")
        if self._looks_like_url(text):
            try:
                return ("url", self.validate_url(text))
            except PageDownloadError as exc:
                return ("error", str(exc))
        if rows:
            return ("error", "Enter 1–{0}, or type a URL.".format(len(rows)))
        return ("error", "Type a URL that starts with http:// or https://.")

    def clean_name(self, name) -> str:
        """General Purpose: One file name under output/. Reject a path."""
        text = (name or "").strip()
        if text == "" or text in (".", ".."):
            raise PageDownloadError("Type a page name.")
        if "/" in text or "\\" in text or "\x00" in text:
            raise PageDownloadError("The page name must be one file name, without a folder.")
        if len(text) > 200:
            raise PageDownloadError("The page name is too long.")
        if text == self.MAP_NAME or text == self.ASSETS_DIR:
            raise PageDownloadError("That page name is reserved.")
        return text

    def clean_html(self, html) -> str:
        """General Purpose: One HTML file name inside the page folder.

        An empty value is index.html. A path, assets, and url-map.json are rejected.
        """
        text = (html or "").strip()
        if text == "":
            return self.INDEX_NAME
        if text in (".", ".."):
            raise PageDownloadError("Type an HTML file name.")
        if "/" in text or "\\" in text or "\x00" in text:
            raise PageDownloadError("The HTML file name must be one file name, without a folder.")
        if len(text) > 200:
            raise PageDownloadError("The HTML file name is too long.")
        if text == self.MAP_NAME or text == self.ASSETS_DIR:
            raise PageDownloadError("That HTML file name is reserved.")
        return text

    def html_name_for(self, name) -> str:
        """General Purpose: The stored HTML file name for one page. Default index.html."""
        clean = self.clean_name(name)
        for entry in self.entries():
            if entry["name"] == clean:
                return entry["html"]
        return self.INDEX_NAME

    def recommend(self, url):
        """General Purpose: Page folder and HTML file suggested by the URL path.

        A path that ends with .html or .htm suggests that file name. The folder
        is that name without the extension. A last segment with no extension,
        such as xxx, suggests the folder xxx and index.html. A host-only URL
        suggests no folder. Returns (page name or "", html file name).
        """
        leaf = self._url_leaf(url)
        if not leaf:
            return "", self.INDEX_NAME
        lower = leaf.lower()
        if lower.endswith(".html") or lower.endswith(".htm"):
            try:
                html_name = self.clean_html(leaf)
            except PageDownloadError:
                html_name = self.INDEX_NAME
            if lower.endswith(".html"):
                stem = leaf[:-5]
            else:
                stem = leaf[:-4]
            page_name = ""
            if stem:
                try:
                    page_name = self.clean_name(stem)
                except PageDownloadError:
                    page_name = ""
            return page_name, html_name
        if "." not in leaf:
            try:
                return self.clean_name(leaf), self.INDEX_NAME
            except PageDownloadError:
                return "", self.INDEX_NAME
        return "", self.INDEX_NAME

    def suggested_html(self, url, name) -> str:
        """General Purpose: HTML file to offer for this page and URL.

        A page already in the url map keeps its stored file name. A new page
        takes the file name recommended from the URL.
        """
        try:
            clean = self.clean_name(name)
        except PageDownloadError:
            return self.INDEX_NAME
        for entry in self.entries():
            if entry["name"] == clean:
                return entry["html"]
        _page_name, html_name = self.recommend(url)
        return html_name

    def validate_url(self, url) -> str:
        """General Purpose: An http or https URL with a host and no password."""
        text = (url or "").strip()
        if text == "":
            raise PageDownloadError("download needs a URL.")
        if len(text) > 2000:
            raise PageDownloadError("The URL is too long.")
        if any(char.isspace() for char in text):
            raise PageDownloadError("The URL must not contain spaces.")
        parts = urlsplit(text)
        if parts.scheme not in ("http", "https"):
            raise PageDownloadError("The URL must start with http:// or https://.")
        if not parts.hostname:
            raise PageDownloadError("The URL needs a host name.")
        if parts.username or parts.password:
            raise PageDownloadError("The URL must not contain a username or password.")
        return text

    def download(self, url, name, html=None) -> str:
        """General Purpose: Fetch the page and its linked stylesheets, scripts, and images.

        Creates the page folder, writes the HTML file, then updates the url map.
        An empty page name uses the folder recommended from the URL. An empty
        HTML file name keeps the stored name, or the name recommended from the
        URL. A path that ends with .html or .htm recommends that file. A last
        segment with no extension, such as xxx, recommends xxx/index.html.
        When that file already exists, the page URL is not fetched again.
        A different name moves the file already stored for this page.
        Stylesheets, scripts, and images are fetched only when missing.
        A failed page fetch raises. A failed asset is listed.
        """
        url = self.validate_url(url)
        suggested_name, suggested_html = self.recommend(url)
        explicit_name = (name or "").strip()
        if explicit_name:
            name = self.clean_name(explicit_name)
        else:
            known = self._entry_for_url(url)
            if known is not None:
                name = known["name"]
            elif suggested_name:
                name = suggested_name
            else:
                raise PageDownloadError(
                    "download needs --name. The URL did not end with an "
                    ".html file or a folder name."
                )
        if html is None or str(html).strip() == "":
            known_page = self._entry_for_name(name)
            if known_page is not None:
                html_name = known_page["html"]
            else:
                html_name = suggested_html
        else:
            html_name = self.clean_html(html)
        if self.logger is not None:
            self.logger.log_message(
                "download {0} as {1}/{2}".format(url, name, html_name),
                component="PageDownload",
            )
        index_path, resumed = self._prepare_index(name, html_name)
        if resumed:
            html = self._read_text(index_path)
            base_url = url
        else:
            body, content_type, final_url = self._get(url)
            html = self._decode(body, content_type)
            base_url = final_url
        css_dir, js_dir, img_dir = self._ensure_page_dirs(name)
        if not resumed:
            self._publish(html.encode("utf-8"), index_path)
        failures = []
        try:
            styles, scripts, images, fonts = self._collect(
                html, base_url, self._page_dir(name)
            )
        except Exception as exc:
            styles, scripts, images, fonts = [], [], [], []
            failures.append("The page links could not be read. {0}".format(exc))
        names = {}
        used = {"css": set(), "js": set(), "img": set()}
        documents, order, css_raws, binaries, css_failures = self._gather_css(
            styles, css_dir, base_url, names, used
        )
        binaries.extend(self._html_binary_jobs(images, "img"))
        binaries.extend(self._html_binary_jobs(fonts, "font"))
        bin_pairs, img_files, font_files, bin_failures = self._store_binaries(
            binaries, css_dir, img_dir, names, used
        )
        self._rewrite_css(documents, order, css_raws, bin_pairs, css_dir)
        js_count, js_pairs, js_failures = self._save_scripts(scripts, js_dir, names, used)
        css_pairs = self._html_css_pairs(css_raws, documents, names)
        failures.extend(css_failures)
        failures.extend(js_failures)
        failures.extend(bin_failures)
        rewritten = self._clean_saved_html(
            self._replace_urls(html, css_pairs + js_pairs + bin_pairs.get("html", []))
        )
        self._publish(rewritten.encode("utf-8"), index_path)
        try:
            self._remember(url, name, html_name)
        except PageDownloadError as exc:
            failures.append(str(exc))
        head = "Continued {0}".format(name) if resumed else "Saved {0}".format(name)
        lines = [
            head,
            "Page: {0}".format(index_path),
            "Stylesheets: {0}".format(len(order)),
            "Scripts: {0}".format(js_count),
            "Images: {0}".format(len(img_files)),
            "Fonts: {0}".format(len(font_files)),
        ]
        if failures:
            lines.append("Not saved:")
            lines.extend(failures)
        return "\n".join(lines)

    def save_document(self, url, relative):
        """General Purpose: Save one HTML document under output/<relative>/index.html.

        relative may contain folders. It may not leave output/.
        This method does not write url-map.json.
        Returns the index path, the HTML before local rewriting, and the final URL.
        """
        url = self.validate_url(url)
        page_dir = self._document_dir(relative)
        index_path = os.path.join(page_dir, self.INDEX_NAME)
        if self.logger is not None:
            self.logger.log_message(
                "download {0} as {1}".format(url, relative),
                component="PageDownload",
            )
        body, content_type, final_url = self._get(url)
        html = self._decode(body, content_type)
        css_dir, js_dir, img_dir = self._ensure_dirs(page_dir)
        self._publish(html.encode("utf-8"), index_path)
        failures = []
        try:
            styles, scripts, images, fonts = self._collect(html, final_url or url, page_dir)
        except Exception as exc:
            styles, scripts, images, fonts = [], [], [], []
            failures.append("The page links could not be read. {0}".format(exc))
        names = {}
        used = {"css": set(), "js": set(), "img": set()}
        documents, order, css_raws, binaries, css_failures = self._gather_css(
            styles, css_dir, final_url or url, names, used
        )
        binaries.extend(self._html_binary_jobs(images, "img"))
        binaries.extend(self._html_binary_jobs(fonts, "font"))
        bin_pairs, _img_files, _font_files, bin_failures = self._store_binaries(
            binaries, css_dir, img_dir, names, used
        )
        self._rewrite_css(documents, order, css_raws, bin_pairs, css_dir)
        _js_count, js_pairs, js_failures = self._save_scripts(scripts, js_dir, names, used)
        css_pairs = self._html_css_pairs(css_raws, documents, names)
        failures.extend(css_failures)
        failures.extend(js_failures)
        failures.extend(bin_failures)
        rewritten = self._clean_saved_html(
            self._replace_urls(html, css_pairs + js_pairs + bin_pairs.get("html", []))
        )
        self._publish(rewritten.encode("utf-8"), index_path)
        if failures and self.logger is not None:
            self.logger.log_message(
                "Not saved: {0}".format("; ".join(failures)),
                component="PageDownload",
            )
        return index_path, html, final_url or url

    def _looks_like_url(self, text) -> bool:
        if not text or any(char.isspace() for char in text):
            return False
        parts = urlsplit(text)
        return parts.scheme in ("http", "https") and bool(parts.hostname)

    def _require_home(self) -> None:
        if not self.home:
            raise PageDownloadError("HOME is not set, so the page folder cannot be created.")
        if not self.app_name or "/" in self.app_name or "\\" in self.app_name:
            raise PageDownloadError("The app name cannot be used as a folder name.")

    def _map_path(self) -> str:
        try:
            return os.path.join(self.output_root(), self.MAP_NAME)
        except PageDownloadError:
            return ""

    def _page_dir(self, name) -> str:
        root = self.output_root()
        dest = os.path.join(root, name)
        if not self._inside(root, dest) or os.path.dirname(os.path.normpath(dest)) != os.path.normpath(root):
            raise PageDownloadError("The page name must be one file name, without a folder.")
        return dest

    def _document_dir(self, relative) -> str:
        """A folder under output/. Slashes stay inside that root. .. does not."""
        root = self.output_root()
        text = (relative or "").strip().replace("\\", "/").strip("/")
        if text == "" or "\x00" in text:
            raise PageDownloadError("The page folder is not valid.")
        parts = text.split("/")
        if any(part in ("", ".", "..") for part in parts):
            raise PageDownloadError("The page folder must stay under output.")
        dest = root
        for part in parts:
            dest = os.path.join(dest, part)
        if not self._inside(root, dest):
            raise PageDownloadError("The page folder must stay under output.")
        return dest

    def _ensure_dirs(self, page_dir):
        """Create page_dir/assets/{css,js,img}. Return the three flat folders."""
        self._require_home()
        cursor = self.home
        for part in (self.APP_PARENT, self.app_name, self.OUTPUT_DIR):
            cursor = os.path.join(cursor, part)
            self._mkdir(cursor)
        assets = os.path.join(page_dir, self.ASSETS_DIR)
        css_dir = os.path.join(assets, self.CSS_DIR)
        js_dir = os.path.join(assets, self.JS_DIR)
        img_dir = os.path.join(assets, self.IMG_DIR)
        self._mkdir(page_dir)
        self._mkdir(assets)
        self._mkdir(css_dir)
        self._mkdir(js_dir)
        self._mkdir(img_dir)
        return css_dir, js_dir, img_dir

    def _url_leaf(self, url) -> str:
        """The last path segment, without a query or a trailing slash."""
        text = (url or "").strip()
        try:
            path = unquote(urlsplit(text).path or "")
        except ValueError:
            return ""
        path = path.replace("\\", "/").rstrip("/")
        if not path:
            return ""
        leaf = path.split("/")[-1]
        if leaf in ("", ".", "..") or "\x00" in leaf:
            return ""
        return leaf

    def _entry_for_url(self, url):
        for entry in self.entries():
            if entry["url"] == url:
                return entry
        return None

    def _entry_for_name(self, name):
        for entry in self.entries():
            if entry["name"] == name:
                return entry
        return None

    def _stored_html(self, html) -> str:
        """A missing or unusable map value means index.html."""
        try:
            return self.clean_html(html)
        except PageDownloadError:
            return self.INDEX_NAME

    def _html_path(self, name, html_name) -> str:
        return os.path.join(self._page_dir(name), html_name)

    def _index_path(self, name) -> str:
        return self._html_path(name, self.INDEX_NAME)

    def _inside(self, root, dest) -> bool:
        root_norm = os.path.normpath(root)
        dest_norm = os.path.normpath(dest)
        prefix = root_norm + os.sep
        return dest_norm.startswith(prefix)

    def _mkdir(self, path) -> None:
        try:
            os.makedirs(path, mode=0o700, exist_ok=True)
            os.chmod(path, 0o700)
        except OSError as exc:
            raise PageDownloadError(
                "Could not create {0}. {1}".format(path, exc.strerror or exc)
            )

    def _ensure_page_dirs(self, name):
        """Create output/<page>/assets/{css,js,img}. Return the three flat folders."""
        self._require_home()
        cursor = self.home
        for part in (self.APP_PARENT, self.app_name, self.OUTPUT_DIR):
            cursor = os.path.join(cursor, part)
            self._mkdir(cursor)
        page_dir = self._page_dir(name)
        assets = os.path.join(page_dir, self.ASSETS_DIR)
        css_dir = os.path.join(assets, self.CSS_DIR)
        js_dir = os.path.join(assets, self.JS_DIR)
        img_dir = os.path.join(assets, self.IMG_DIR)
        self._mkdir(page_dir)
        self._mkdir(assets)
        self._mkdir(css_dir)
        self._mkdir(js_dir)
        self._mkdir(img_dir)
        return css_dir, js_dir, img_dir

    def _prepare_index(self, name, html_name):
        """Return (html path, already saved).

        An empty HTML name is index.html. A ready file at the requested name is
        not downloaded again. A ready file stored under the previous name is
        moved to the requested name and is not downloaded again. A previous save
        that wrote output/<name> as a file is moved to the requested name.
        """
        root = self.output_root()
        index_path = self._html_path(name, html_name)
        if self._file_ready(index_path):
            return index_path, True
        previous = self._stored_html_path(name, html_name)
        if previous and self._file_ready(previous):
            self._rename_html(previous, index_path)
            return index_path, True
        legacy = os.path.join(root, name)
        if not os.path.isfile(legacy):
            return index_path, False
        if not self._file_ready(legacy):
            raise PageDownloadError(
                "{0} is a file, so the page folder cannot be created.".format(name)
            )
        self._mkdir(root)
        descriptor, tmp = tempfile.mkstemp(prefix=".page-", dir=root)
        os.close(descriptor)
        try:
            os.unlink(tmp)
        except OSError:
            pass
        shutil.move(legacy, tmp)
        try:
            self._mkdir(self._page_dir(name))
            if self.logger is not None:
                self.logger.log_message(
                    "publish {0}".format(index_path),
                    component="PageDownload",
                )
            shutil.move(tmp, index_path)
            os.chmod(index_path, 0o600)
        except Exception as exc:
            if os.path.exists(tmp) and not os.path.exists(legacy):
                try:
                    shutil.move(tmp, legacy)
                except OSError:
                    pass
            if isinstance(exc, PageDownloadError):
                raise
            raise PageDownloadError(
                "Could not move {0} to {1}. {2}".format(name, index_path, exc)
            )
        return index_path, True

    def _file_ready(self, path) -> bool:
        try:
            return os.path.isfile(path) and os.path.getsize(path) > 0
        except OSError:
            return False

    def _read_bytes(self, path) -> bytes:
        try:
            with open(path, "rb") as handle:
                return handle.read()
        except OSError as exc:
            raise PageDownloadError(
                "Could not read {0}. {1}".format(path, exc.strerror or exc)
            )

    def _read_text(self, path) -> str:
        return self._decode(self._read_bytes(path), "")

    def _legacy_path(self, kind, filename) -> str:
        if kind not in (self.CSS_DIR, self.JS_DIR) or not filename:
            return ""
        return os.path.join(self.output_root(), self.ASSETS_DIR, kind, filename)

    def _load_asset(self, folder, filename, absolute, legacy_kind):
        """Return (payload, final url, from disk). Do not publish.

        A file already in the page folder is kept. A file left in the old
        shared output/assets folder is reused. Otherwise the URL is fetched.
        """
        if not self._safe_leaf(filename):
            raise PageDownloadError("Refusing to save outside the page folder.")
        dest = os.path.join(folder, filename)
        if self._file_ready(dest):
            return self._read_bytes(dest), "", True
        if legacy_kind:
            legacy = self._legacy_path(legacy_kind, filename)
            if (
                legacy
                and self._file_ready(legacy)
                and os.path.normpath(legacy) != os.path.normpath(dest)
            ):
                return self._read_bytes(legacy), "", True
        if not absolute:
            raise PageDownloadError(
                "Missing {0}. The page names that file but not its URL.".format(filename)
            )
        payload, _content_type, final_url = self._get(absolute)
        return payload, final_url or absolute, False

    def _store_bytes(self, folder, filename, payload) -> None:
        dest = os.path.join(folder, filename)
        if self._file_ready(dest):
            return
        self._publish(payload, dest)

    def _store_text(self, folder, filename, text) -> None:
        dest = os.path.join(folder, filename)
        data = text.encode("utf-8")
        if self._file_ready(dest) and self._read_bytes(dest) == data:
            return
        self._publish(data, dest)

    def _get(self, url):
        self.validate_url(url)
        if self.gate is not None:
            self.gate(url)
        if self.opener is not None:
            loaded = self.opener(url)
            hinted = url
            if isinstance(loaded, (tuple, list)) and len(loaded) >= 3:
                body, content_type, hinted = loaded[0], loaded[1], loaded[2] or url
            elif isinstance(loaded, (tuple, list)) and len(loaded) >= 2:
                body, content_type = loaded[0], loaded[1]
            else:
                body, content_type = None, ""
            if not isinstance(body, (bytes, bytearray)):
                raise PageDownloadError("The response for {0} was empty.".format(url))
            payload = bytes(body)
            self.validate_url(hinted)
        else:
            payload, content_type, final_url = self._fetch(url)
            self.validate_url(final_url)
            if len(payload) > self.MAX_BYTES:
                raise PageDownloadError(
                    "The response for {0} is larger than {1} bytes.".format(url, self.MAX_BYTES)
                )
            return payload, content_type, final_url
        if len(payload) > self.MAX_BYTES:
            raise PageDownloadError(
                "The response for {0} is larger than {1} bytes.".format(url, self.MAX_BYTES)
            )
        return payload, content_type or "", hinted

    def _fetch(self, url):
        import socket
        import urllib.error
        import urllib.request

        request = urllib.request.Request(
            url,
            headers={"User-Agent": self._user_agent()},
        )
        try:
            response = urllib.request.urlopen(request, timeout=self.TIMEOUT_SECONDS)
        except urllib.error.HTTPError as exc:
            try:
                exc.close()
            except Exception:
                pass
            raise PageDownloadError("HTTP {0} for {1}.".format(exc.code, url))
        except urllib.error.URLError as exc:
            raise PageDownloadError("Could not fetch {0}. {1}".format(url, exc.reason))
        except socket.timeout:
            raise PageDownloadError("The request for {0} timed out.".format(url))
        try:
            length = response.headers.get("Content-Length", "")
            if length.isdigit() and int(length) > self.MAX_BYTES:
                raise PageDownloadError(
                    "The response for {0} is larger than {1} bytes.".format(url, self.MAX_BYTES)
                )
            chunks = []
            total = 0
            while True:
                block = response.read(64 * 1024)
                if not block:
                    break
                total += len(block)
                if total > self.MAX_BYTES:
                    raise PageDownloadError(
                        "The response for {0} is larger than {1} bytes.".format(
                            url, self.MAX_BYTES
                        )
                    )
                chunks.append(block)
            content_type = response.headers.get("Content-Type", "")
            final_url = response.geturl() or url
            return b"".join(chunks), content_type, final_url
        finally:
            response.close()

    def _user_agent(self) -> str:
        if self.user_agent:
            return self.user_agent
        from . import __version__

        return "{0}/{1}".format(self.app_name, __version__)

    def _decode(self, body, content_type) -> str:
        charset = ""
        match = re.search(r"charset=([^\s;]+)", content_type or "", re.IGNORECASE)
        if match:
            charset = match.group(1).strip("\"'")
        for encoding in (charset, "utf-8", "latin-1"):
            if not encoding:
                continue
            try:
                return body.decode(encoding)
            except (LookupError, UnicodeDecodeError):
                continue
        return body.decode("latin-1")

    def _join(self, base, raw):
        text = (raw or "").strip()
        if text == "" or text.startswith("#"):
            return None
        lowered = text.lower()
        if lowered.startswith(("#", "%23", "data:", "javascript:", "mailto:", "blob:")):
            return None
        joined = urljoin(base, text)
        parts = urlsplit(joined)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            return None
        if parts.username or parts.password:
            return None
        return urlunsplit(parts._replace(fragment=""))

    def _collect(self, html, base_url, page_dir):
        found = {
            "styles": [],
            "scripts": [],
            "images": [],
            "fonts": [],
            "styled": [],
            "base": "",
            "xml_base": "",
            "in_style": False,
            "style_parts": [],
        }

        def attrs_of(attrs):
            mapped = {}
            for key, value in attrs:
                if key:
                    mapped[key.lower()] = value or ""
            return mapped

        def take_style(value):
            if not value:
                return
            for raw in self._url_refs(value):
                found["styled"].append(raw)

        def on_start(tag, attrs):
            attr = attrs_of(attrs)
            for key, value in attrs:
                if key and key.lower() == "xml:base" and value and not found["xml_base"]:
                    found["xml_base"] = value
            take_style(attr.get("style", ""))
            if tag == "base" and attr.get("href") and not found["base"]:
                found["base"] = attr.get("href")
            elif tag == "link":
                rel = attr.get("rel", "").lower().split()
                href = attr.get("href", "")
                kind = attr.get("as", "").lower()
                if not href:
                    return
                if "stylesheet" in rel or ("preload" in rel and kind == "style"):
                    found["styles"].append(href)
                elif ("preload" in rel and kind == "script") or "modulepreload" in rel:
                    found["scripts"].append(href)
                elif "preload" in rel and kind == "image":
                    found["images"].append(href)
                elif "preload" in rel and kind == "font":
                    found["fonts"].append(href)
                elif any(part in ("icon", "apple-touch-icon", "apple-touch-icon-precomposed", "mask-icon") for part in rel):
                    found["images"].append(href)
            elif tag == "script":
                src = attr.get("src", "")
                if src:
                    found["scripts"].append(src)
            elif tag in ("img", "image", "source"):
                src = attr.get("src", "") or attr.get("href", "")
                if src:
                    found["images"].append(src)
                for piece in self._srcset_urls(attr.get("srcset", "")):
                    found["images"].append(piece)
            elif tag == "video":
                poster = attr.get("poster", "")
                if poster:
                    found["images"].append(poster)
            elif tag == "input" and attr.get("type", "").lower() == "image":
                src = attr.get("src", "")
                if src:
                    found["images"].append(src)
            elif tag == "style":
                found["in_style"] = True
                found["style_parts"] = []

        def on_end(tag):
            if tag == "style" and found["in_style"]:
                found["in_style"] = False
                text = "".join(found["style_parts"])
                for raw in self._import_refs(text):
                    found["styles"].append(raw)
                for raw in self._url_refs(text):
                    found["styled"].append(raw)
                found["style_parts"] = []

        def on_data(data):
            if found["in_style"] and data:
                found["style_parts"].append(data)

        class Markup(HTMLParser):
            def handle_starttag(self, tag, attrs):
                on_start(tag, attrs)

            def handle_endtag(self, tag):
                on_end(tag)

            def handle_data(self, data):
                on_data(data)

        parser = Markup(convert_charrefs=True)
        parser.feed(html or "")
        parser.close()
        declared = found["base"] or found["xml_base"]
        page_base = self._join(base_url, declared) if declared else None
        page_base = page_base or base_url
        styles = self._resolve_many(found["styles"], page_base, "css", page_dir)
        scripts = self._resolve_many(found["scripts"], page_base, "js", page_dir)
        images = self._resolve_many(found["images"], page_base, "img", page_dir)
        fonts = self._resolve_many(found["fonts"], page_base, "font", page_dir)
        for raw in found["styled"]:
            item = self._resolve_html_ref(raw, page_base, "", page_dir)
            if not item:
                continue
            if item[0] == "local":
                kind = item[2]
            else:
                kind = self._kind_of_url(item[2])
            if kind == "css":
                styles.append(item if item[0] == "local" else ("remote", raw, item[2]))
            elif kind == "img":
                images.append(("remote", raw, item[2]) if item[0] == "remote" else item)
            elif kind == "font":
                fonts.append(("remote", raw, item[2]) if item[0] == "remote" else item)
        return styles, scripts, images, fonts

    def _resolve_many(self, raws, page_base, force_kind, page_dir) -> list:
        items = []
        for raw in raws:
            item = self._resolve_html_ref(raw, page_base, force_kind, page_dir)
            if item:
                items.append(item)
        return items

    def _resolve_html_ref(self, raw, page_base, force_kind, page_dir):
        """A local flat asset, a remote URL, or None.

        force_kind is css, js, img, font, or "" when the extension decides.
        assets/css, assets/js, and assets/img count as local only when the file is on disk.
        The same shape on the site is still fetched.
        """
        if self._ignore_ref(raw):
            return None
        local = self._local_html_asset(raw, page_dir)
        if local:
            kind, filename = local
            ext = os.path.splitext(filename)[1].lower()
            if force_kind == "img" and kind != "img":
                return None
            if force_kind == "js" and kind != "js":
                return None
            if force_kind == "css" and kind != "css":
                return None
            if force_kind == "font":
                if kind == "css" and ext in self.FONT_EXTS:
                    return ("local", raw, "font", filename)
                return None
            if force_kind in ("css", "js", "img"):
                return ("local", raw, force_kind, filename)
            if kind == "img" or ext in self.IMAGE_EXTS:
                return ("local", raw, "img", filename)
            if ext in self.FONT_EXTS:
                return ("local", raw, "font", filename)
            if ext == ".js" or kind == "js":
                return ("local", raw, "js", filename)
            if ext == ".css" or kind == "css":
                return ("local", raw, "css", filename)
            return None
        absolute = self._join(page_base, raw)
        if not absolute:
            return None
        if force_kind == "font" and self._kind_of_url(absolute) not in ("font", ""):
            if self._kind_of_url(absolute) != "font":
                return None
        if force_kind == "":
            if self._kind_of_url(absolute) == "":
                return None
        return ("remote", raw, absolute)

    def _ignore_ref(self, raw) -> bool:
        text = (raw or "").strip()
        if text == "" or text.startswith("#"):
            return True
        lowered = text.lower()
        if lowered.startswith(("%23", "data:", "javascript:", "mailto:", "blob:")):
            return True
        return False

    def _local_html_asset(self, raw, page_dir):
        """Return (kind, filename) when that flat file is already saved."""
        text = (raw or "").strip().split("?", 1)[0].split("#", 1)[0]
        match = self.LOCAL_HTML_RE.fullmatch(text)
        if not match:
            return None
        kind = match.group(1)
        filename = match.group(2)
        if not self._safe_leaf(filename):
            return None
        dest = os.path.join(page_dir, self.ASSETS_DIR, kind, filename)
        if self._file_ready(dest):
            return kind, filename
        if kind in (self.CSS_DIR, self.JS_DIR):
            legacy = self._legacy_path(kind, filename)
            if legacy and self._file_ready(legacy):
                return kind, filename
        return None

    def _safe_leaf(self, filename) -> bool:
        if not filename or filename in (".", ".."):
            return False
        if "/" in filename or "\\" in filename or "\x00" in filename:
            return False
        return self._sanitize_leaf(filename) == filename

    def _kind_of_url(self, absolute) -> str:
        ext = os.path.splitext(urlsplit(absolute).path)[1].lower()
        if ext == ".css":
            return "css"
        if ext == ".js":
            return "js"
        if ext in self.IMAGE_EXTS:
            return "img"
        if ext in self.FONT_EXTS:
            return "font"
        return ""

    def _srcset_urls(self, value) -> list:
        found = []
        for part in (value or "").split(","):
            piece = part.strip()
            if not piece:
                continue
            url = piece.split()[0]
            if url:
                found.append(url)
        return found

    def _html_binary_jobs(self, items, kind) -> list:
        jobs = []
        for item in items:
            if item[0] == "local":
                _mode, raw, local_kind, filename = item
                jobs.append({
                    "parent": "html",
                    "raw": raw,
                    "mode": "local",
                    "kind": kind if kind == "font" else local_kind,
                    "key": filename,
                })
                continue
            _mode, raw, absolute = item
            jobs.append({
                "parent": "html",
                "raw": raw,
                "mode": "remote",
                "kind": kind,
                "key": absolute,
            })
        return jobs

    def _drop_document_base(self, html: str) -> str:
        """Remove base-url markup so rewritten relative links stay on this page.

        Collection already used the remote base. The saved file must not keep it.
        """
        text = self.BASE_TAG_RE.sub("", html or "")
        return self.XML_BASE_RE.sub("", text)

    def _clean_saved_html(self, html: str) -> str:
        """Drop base, canonical, and HTML comments after assets are saved.

        Asset collection already read the original page. The saved file does not keep them.
        """
        text = self._drop_document_base(html)
        text = self.CANONICAL_LINK_RE.sub("", text)
        return self.HTML_COMMENT_RE.sub("", text)

    def _import_refs(self, text) -> list:
        cleaned = self.COMMENT_RE.sub("", text or "")
        refs = []
        for match in self.IMPORT_RE.finditer(cleaned):
            raw = match.group(2) or match.group(4) or ""
            raw = raw.strip()
            if raw:
                refs.append(raw)
        return refs

    def _url_refs(self, text) -> list:
        cleaned = self.COMMENT_RE.sub("", text or "")
        refs = []
        for match in self.URL_RE.finditer(cleaned):
            raw = (match.group(2) or "").strip()
            if raw and raw not in refs:
                refs.append(raw)
        return refs

    def _gather_css(self, styles, css_dir, page_base, names, used):
        """Load stylesheets. Return documents, order, import raws, binary jobs, failures.

        A local assets/css file is kept. A remote stylesheet is fetched only when missing.
        """
        failures = []
        raws = {}
        documents = {}
        order = []
        queue = []
        seen = set()
        binaries = []
        for item in styles:
            if item[0] == "local":
                _mode, raw, _kind, filename = item
                queue.append(("local", filename, raw, 0))
            else:
                _mode, raw, absolute = item
                queue.append(("remote", absolute, raw, 0))
        while queue and len(order) < self.MAX_CSS:
            mode, key, html_raw, depth = queue.pop(0)
            token = (mode, key)
            if token in seen:
                if html_raw is not None:
                    raws.setdefault(("html", token), set()).add(html_raw)
                continue
            seen.add(token)
            if html_raw is not None:
                raws.setdefault(("html", token), set()).add(html_raw)
            if mode == "local":
                filename = key
                try:
                    payload, _final, _disk = self._load_asset(css_dir, filename, "", "css")
                except PageDownloadError as exc:
                    failures.append(str(exc))
                    continue
                text = self._decode(payload, "")
                css_base = self._join(
                    page_base,
                    "{0}/{1}/{2}".format(self.ASSETS_DIR, self.CSS_DIR, filename),
                ) or page_base
                used["css"].add(filename)
            else:
                absolute = key
                filename = self._filename_for(absolute, "css", "style", names, used)
                try:
                    payload, final_url, _disk = self._load_asset(
                        css_dir, filename, absolute, "css"
                    )
                except PageDownloadError as exc:
                    failures.append(str(exc))
                    continue
                text = self._decode(payload, "")
                css_base = final_url or absolute
            documents[token] = {"text": text, "filename": filename}
            order.append(token)
            if depth + 1 < self.MAX_CSS_DEPTH:
                for raw in self._import_refs(text):
                    classified = self._classify_css_ref(raw, css_dir, css_base)
                    if not classified or classified[2] not in ("", "css"):
                        continue
                    child_mode, child_key, _kind = classified
                    child = (child_mode, child_key)
                    raws.setdefault((token, child), set()).add(raw)
                    if child not in seen:
                        queue.append((child_mode, child_key, None, depth + 1))
            for raw in self._url_refs(text):
                if self._ignore_ref(raw):
                    continue
                classified = self._classify_css_ref(raw, css_dir, css_base)
                if not classified:
                    continue
                child_mode, child_key, kind = classified
                if kind not in ("img", "font"):
                    continue
                binaries.append({
                    "parent": token,
                    "raw": raw,
                    "mode": child_mode,
                    "kind": kind,
                    "key": child_key,
                })
        if queue and len(order) >= self.MAX_CSS:
            failures.append("Stopped after {0} stylesheets.".format(self.MAX_CSS))
        return documents, order, raws, binaries, failures

    def _classify_css_ref(self, raw, css_dir, css_base):
        """Return (mode, key, kind) for a url inside a stylesheet, or None."""
        local = self._local_css_ref(raw, css_dir)
        if local:
            kind, filename = local
            return ("local", filename, kind)
        absolute = self._join(css_base, raw)
        if not absolute:
            return None
        return ("remote", absolute, self._kind_of_url(absolute))

    def _local_css_ref(self, raw, css_dir):
        """A flat file this saver owns, or None when the url still belongs to the site."""
        text = (raw or "").strip()
        path = text.split("?", 1)[0].split("#", 1)[0]
        match = re.fullmatch(r"\.\./(img|css|js)/([^/]+)", path)
        if match:
            filename = match.group(2)
            if not self._safe_leaf(filename):
                return None
            kind = match.group(1)
            folder = os.path.join(os.path.dirname(css_dir), kind)
            if self._file_ready(os.path.join(folder, filename)):
                if kind == "img":
                    return ("img", filename)
                if kind == "js":
                    return ("js", filename)
                return ("css", filename)
            if kind in (self.CSS_DIR, self.JS_DIR):
                legacy = self._legacy_path(kind, filename)
                if legacy and self._file_ready(legacy):
                    return (kind, filename)
            return None
        match = re.fullmatch(r"([^/]+)", path)
        if not match:
            return None
        filename = match.group(1)
        if not self._safe_leaf(filename):
            return None
        dest = os.path.join(css_dir, filename)
        legacy = self._legacy_path(self.CSS_DIR, filename)
        if not self._file_ready(dest) and not (legacy and self._file_ready(legacy)):
            return None
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".css":
            return ("css", filename)
        if ext in self.FONT_EXTS:
            return ("font", filename)
        if ext in self.IMAGE_EXTS:
            return ("font", filename)
        return ("css", filename)

    def _store_binaries(self, jobs, css_dir, img_dir, names, used):
        """Fetch missing images and fonts. Return pairs, image names, font names, failures."""
        failures = []
        pairs = {}
        img_files = set()
        font_files = set()
        seen = set()
        stopped_img = False
        stopped_font = False
        for job in jobs:
            kind = job["kind"]
            if kind not in ("img", "font"):
                continue
            folder = img_dir if kind == "img" else css_dir
            legacy_kind = None if kind == "img" else "css"
            fallback = "image" if kind == "img" else "font"
            if job["mode"] == "local":
                filename = job["key"]
                if not self._safe_leaf(filename):
                    failures.append(
                        "Missing {0}. The page names that file but not its URL.".format(job["raw"])
                    )
                    continue
                dest = os.path.join(folder, filename)
                if not self._file_ready(dest):
                    try:
                        payload, _final, _disk = self._load_asset(folder, filename, "", legacy_kind)
                    except PageDownloadError as exc:
                        failures.append(str(exc))
                        continue
                    self._store_bytes(folder, filename, payload)
                if not self._file_ready(dest):
                    failures.append(
                        "Missing {0}. The page names that file but not its URL.".format(filename)
                    )
                    continue
                bucket_name = "img" if kind == "img" else "css"
                used[bucket_name].add(filename)
            else:
                absolute = job["key"]
                marker = (kind, absolute)
                if marker in seen:
                    filename = names.get(absolute, (None, ""))[1]
                    if not filename:
                        continue
                else:
                    bucket = img_files if kind == "img" else font_files
                    limit = self.MAX_IMG if kind == "img" else self.MAX_FONT
                    label = "images" if kind == "img" else "fonts"
                    stopped = stopped_img if kind == "img" else stopped_font
                    if len(bucket) >= limit:
                        if not stopped:
                            failures.append("Stopped after {0} {1}.".format(limit, label))
                            if kind == "img":
                                stopped_img = True
                            else:
                                stopped_font = True
                        continue
                    seen.add(marker)
                    filename = self._filename_for(absolute, kind, fallback, names, used)
                    try:
                        payload, _final, _disk = self._load_asset(
                            folder, filename, absolute, legacy_kind
                        )
                    except PageDownloadError as exc:
                        failures.append(str(exc))
                        continue
                    self._store_bytes(folder, filename, payload)
            if not self._file_ready(os.path.join(folder, filename)):
                continue
            if kind == "img":
                img_files.add(filename)
            else:
                font_files.add(filename)
            relative = self._relative_for(job["parent"], kind, filename)
            pairs.setdefault(job["parent"], []).append(
                (job["raw"], self._with_fragment(job["raw"], relative))
            )
        return pairs, img_files, font_files, failures

    def _rewrite_css(self, documents, order, raws, bin_pairs, css_dir) -> None:
        for token in order:
            doc = documents.get(token)
            if not doc:
                continue
            pairs = list(bin_pairs.get(token, []))
            for (parent, child), forms in raws.items():
                if parent != token:
                    continue
                child_doc = documents.get(child)
                if not child_doc:
                    continue
                for raw in forms:
                    pairs.append((raw, self._with_fragment(raw, child_doc["filename"])))
            rewritten = self._replace_urls(doc["text"], pairs)
            self._store_text(css_dir, doc["filename"], rewritten)

    def _html_css_pairs(self, raws, documents, names) -> list:
        pairs = []
        for (parent, child), forms in raws.items():
            if parent != "html":
                continue
            doc = documents.get(child)
            if not doc:
                continue
            relative = self._html_relative("css", doc["filename"])
            for raw in forms:
                pairs.append((raw, self._with_fragment(raw, relative)))
        return pairs

    def _relative_for(self, parent, kind, filename) -> str:
        if parent == "html":
            return self._html_relative("img" if kind == "img" else "css", filename)
        if kind == "img":
            return "../{0}/{1}".format(self.IMG_DIR, filename)
        return filename

    def _html_relative(self, kind, filename) -> str:
        folder = {"css": self.CSS_DIR, "js": self.JS_DIR, "img": self.IMG_DIR}.get(kind, kind)
        return "{0}/{1}/{2}".format(self.ASSETS_DIR, folder, filename)

    def _with_fragment(self, raw, relative) -> str:
        if "#" in (raw or ""):
            return relative + "#" + raw.split("#", 1)[1]
        return relative

    def _filename_for(self, absolute, kind, fallback, names, used) -> str:
        known = names.get(absolute)
        if known:
            return known[1]
        bucket = "img" if kind == "img" else "js" if kind == "js" else "css"
        filename = self._asset_filename(absolute, kind, fallback, used[bucket])
        names[absolute] = (kind, filename)
        return filename

    def _save_scripts(self, scripts, js_dir, names, used):
        failures = []
        pairs = []
        seen = set()
        written = 0
        attempted = 0
        stopped = False
        for item in scripts:
            if item[0] == "local":
                _mode, raw, _kind, filename = item
                if attempted >= self.MAX_JS:
                    if not stopped:
                        failures.append("Stopped after {0} scripts.".format(self.MAX_JS))
                        stopped = True
                    break
                attempted += 1
                try:
                    payload, _final, _disk = self._load_asset(js_dir, filename, "", "js")
                except PageDownloadError as exc:
                    failures.append(str(exc))
                    continue
                self._store_bytes(js_dir, filename, payload)
                used["js"].add(filename)
                written += 1
                pairs.append((raw, self._with_fragment(raw, self._html_relative("js", filename))))
                continue
            _mode, raw, absolute = item
            if absolute in seen:
                known = names.get(absolute)
                if known:
                    pairs.append((raw, self._with_fragment(raw, self._html_relative("js", known[1]))))
                continue
            if attempted >= self.MAX_JS:
                if not stopped:
                    failures.append("Stopped after {0} scripts.".format(self.MAX_JS))
                    stopped = True
                break
            attempted += 1
            seen.add(absolute)
            filename = self._filename_for(absolute, "js", "script", names, used)
            try:
                payload, _final, _disk = self._load_asset(js_dir, filename, absolute, "js")
            except PageDownloadError as exc:
                failures.append(str(exc))
                continue
            self._store_bytes(js_dir, filename, payload)
            written += 1
            pairs.append((raw, self._with_fragment(raw, self._html_relative("js", filename))))
        return written, pairs, failures

    def _asset_filename(self, url, kind, fallback, used) -> str:
        path = urlsplit(url).path
        base = self._sanitize_leaf(os.path.basename(path))
        root, ext = os.path.splitext(base)
        if kind == "css" and ext.lower() != ".css":
            if ext == "":
                ext = ".css"
        elif kind == "js" and ext == "":
            ext = ".js"
        elif kind == "img" and ext == "":
            ext = ".img"
        elif kind == "font" and ext == "":
            ext = ".font"
        if root == "":
            root = fallback
        root = root[:60]
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
        name = self._sanitize_leaf("{0}-{1}{2}".format(root, digest, ext))
        if name == "":
            name = "{0}-{1}{2}".format(fallback, digest, ext or "")
        candidate = name
        serial = 2
        while candidate in used:
            candidate = "{0}-{1}".format(serial, name)
            serial += 1
        used.add(candidate)
        return candidate

    def _sanitize_leaf(self, text) -> str:
        cleaned = []
        for char in text or "":
            if char in ("/", "\\", "\x00") or ord(char) < 32:
                cleaned.append("_")
            else:
                cleaned.append(char)
        leaf = "".join(cleaned).strip().strip(".")
        if leaf in ("", ".", ".."):
            return ""
        return leaf[:120]

    def _raw_forms(self, raw) -> list:
        forms = [raw]
        escaped = raw.replace("&", "&amp;").replace('"', "&quot;")
        if escaped != raw:
            forms.append(escaped)
        return forms

    def _replace_urls(self, text, pairs) -> str:
        expanded = []
        seen = set()
        for raw, new in pairs:
            if not raw or raw == new:
                continue
            for form in self._raw_forms(raw):
                key = (form, new)
                if key in seen:
                    continue
                seen.add(key)
                expanded.append(key)
        expanded.sort(key=lambda item: len(item[0]), reverse=True)
        for raw, new in expanded:
            escaped = re.escape(raw)
            patterns = (
                re.compile(r'(href\s*=\s*")' + escaped + r'(")', re.IGNORECASE),
                re.compile(r"(href\s*=\s*')" + escaped + r"(')", re.IGNORECASE),
                re.compile(r'(src\s*=\s*")' + escaped + r'(")', re.IGNORECASE),
                re.compile(r"(src\s*=\s*')" + escaped + r"(')", re.IGNORECASE),
                re.compile(r'(poster\s*=\s*")' + escaped + r'(")', re.IGNORECASE),
                re.compile(r"(poster\s*=\s*')" + escaped + r"(')", re.IGNORECASE),
                re.compile(r'(srcset\s*=\s*"[^"]*?)' + escaped + r'([^"]*")', re.IGNORECASE),
                re.compile(r"(srcset\s*=\s*'[^']*?)" + escaped + r"([^']*')", re.IGNORECASE),
                re.compile(r'(url\(\s*")' + escaped + r'("\s*\))', re.IGNORECASE),
                re.compile(r"(url\(\s*')" + escaped + r"('\s*\))", re.IGNORECASE),
                re.compile(r"(url\(\s*)" + escaped + r"(\s*\))", re.IGNORECASE),
                re.compile(r'(@import\s+")' + escaped + r'(")', re.IGNORECASE),
                re.compile(r"(@import\s+')" + escaped + r"(')", re.IGNORECASE),
            )
            for pattern in patterns:
                text = pattern.sub(lambda match, replacement=new: match.group(1) + replacement + match.group(2), text)
            text = re.sub(
                r"(?i)(\b(?:href|src)\s*=\s*)" + escaped + r"(?=\s|>)",
                lambda match, replacement=new: match.group(1) + replacement,
                text,
            )
        return text

    def _publish(self, data, dest) -> None:
        folder = os.path.dirname(dest)
        self._mkdir(folder)
        if not self._inside(folder, dest):
            raise PageDownloadError("Refusing to save outside the page folder.")
        descriptor, tmp = tempfile.mkstemp(prefix=".part-", dir=folder)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            if self.logger is not None:
                self.logger.log_message("publish {0}".format(dest), component="PageDownload")
            shutil.move(tmp, dest)
            os.chmod(dest, 0o600)
        except PageDownloadError:
            if os.path.exists(tmp):
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
            raise
        except Exception as exc:
            if os.path.exists(tmp):
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
            raise PageDownloadError("Could not save {0}. {1}".format(dest, exc))

    def _stored_html_path(self, name, html_name) -> str:
        """The previous HTML file for this page when the requested name differs."""
        previous_name = ""
        for entry in self.entries():
            if entry["name"] == name:
                previous_name = entry["html"]
                break
        if not previous_name:
            previous_name = self.INDEX_NAME
        if previous_name == html_name:
            return ""
        try:
            return self._html_path(name, previous_name)
        except PageDownloadError:
            return ""

    def _rename_html(self, source, dest) -> None:
        """Move one saved HTML file onto its new name inside the page folder."""
        self._mkdir(os.path.dirname(dest))
        if self.logger is not None:
            self.logger.log_message(
                "publish {0}".format(dest),
                component="PageDownload",
            )
        try:
            shutil.move(source, dest)
            os.chmod(dest, 0o600)
        except OSError as exc:
            raise PageDownloadError(
                "Could not rename the HTML file to {0}. {1}".format(
                    os.path.basename(dest), exc.strerror or exc
                )
            )

    def _remember(self, url, name, html_name) -> None:
        pages = self.entries()
        kept = []
        placed = False
        record = {"url": url, "name": name, "html": html_name}
        for item in pages:
            if item["name"] == name or item["url"] == url:
                if not placed:
                    kept.append(record)
                    placed = True
                continue
            kept.append({
                "url": item["url"],
                "name": item["name"],
                "html": item["html"],
            })
        if not placed:
            kept.append(record)
        self._write_map(kept)

    def _write_map(self, pages) -> None:
        path = os.path.join(self.output_root(), self.MAP_NAME)
        payload = json.dumps({"pages": pages}, ensure_ascii=False, indent=2) + "\n"
        self._publish(payload.encode("utf-8"), path)
