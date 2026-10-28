# =============================================================================
# Walk one host. Depth and page cap are required. robots.txt is read first.
# requirement-html-site-crawl — same host, bounds, robots, one-second wait.
# requirement-html-page-download — each HTML document and its assets.
# The site folder is output/<sitename>/ under the live app name.
# =============================================================================
from __future__ import annotations

import os
import time
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit

from . import __version__
from .page_download import PageDownload, PageDownloadError


class SiteCrawl:
    """Save HTML pages on one host, up to a depth and a page cap.

    Depth 0 is the start page. A link from depth D is depth D+1.
    robots.txt for that host is fetched before any HTML page.
    Requests to one host wait one second after the previous request.
    """

    DELAY_SECONDS = 1
    CRAWL_PRODUCT = "HtmlCrawler"

    def __init__(self, app_name, logger=None, home=None, opener=None, sleeper=None, clock=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="SiteCrawl")
        self.pages = PageDownload(app_name, logger=logger, home=home, opener=opener)
        self.pages.user_agent = "{0}/{1}".format(self.CRAWL_PRODUCT, __version__)
        self.pages.gate = self._gate
        self._sleeper = sleeper if sleeper is not None else time.sleep
        self._clock = clock if clock is not None else time.monotonic
        self._last = {}
        self._robots = {}

    def crawl(self, url, name, depth, max_pages) -> str:
        """General Purpose: Walk one site and save each HTML document.

        Returns a short report. A failed robots fetch raises and saves nothing.
        A path robots disallows is skipped. Pages already saved stay on disk.
        """
        name = self.pages.clean_name(name)
        start = self._canonical(self.pages.validate_url(url))
        if start is None:
            raise PageDownloadError("The URL path must not contain '..'.")
        depth = self._bound(depth, "--depth", 0)
        max_pages = self._bound(max_pages, "--max-pages", 1)
        if self.logger is not None:
            self.logger.log_message(
                "crawl {0} as {1} depth {2} max {3}".format(start, name, depth, max_pages),
                component="SiteCrawl",
            )
        self._load_robots(start)
        allowed = self._host_key(start)
        queue = deque([(start, 0)])
        seen = set()
        saved = []
        skipped = []
        stopped_pages = False
        stopped_depth = False
        while queue:
            current, level = queue.popleft()
            if current in seen:
                continue
            if len(saved) >= max_pages:
                stopped_pages = True
                break
            seen.add(current)
            if self._disallowed(current):
                skipped.append(current)
                continue
            try:
                relative = self._relative(name, current)
            except PageDownloadError:
                skipped.append(current)
                continue
            _index_path, html, final_url = self.pages.save_document(current, relative)
            saved.append(current)
            final = self._canonical(final_url) or current
            final_host = self._host_key(final)
            if final_host != allowed:
                self._load_robots(final)
                allowed = final_host
            links = self._links(html, final_url or current)
            if level >= depth:
                if self._deeper(links, allowed, seen):
                    stopped_depth = True
                    if len(saved) >= max_pages:
                        stopped_pages = True
                continue
            for link in links:
                canon = self._canonical(link)
                if canon is None:
                    skipped.append(link)
                    continue
                if self._host_key(canon) != allowed:
                    continue
                if canon not in seen:
                    queue.append((canon, level + 1))
        if saved and self._is_root(start):
            self.pages._remember(start, name, self.pages.INDEX_NAME)
        return self._report(name, saved, skipped, stopped_pages, stopped_depth)

    def _gate(self, url) -> None:
        """Wait out the remainder of one second since the last request to this host."""
        key = self._host_key(url)
        if key is None:
            return
        now = self._clock()
        last = self._last.get(key)
        if last is not None:
            gap = self.DELAY_SECONDS - (now - last)
            if gap > 0:
                self._sleeper(gap)
                now = self._clock()
        self._last[key] = now

    def _bound(self, value, label, minimum) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise PageDownloadError("{0} must be an integer.".format(label))
        if value < minimum:
            raise PageDownloadError(
                "{0} must be an integer >= {1}.".format(label, minimum)
            )
        return value

    def _load_robots(self, url) -> None:
        key = self._host_key(url)
        if key is None:
            raise PageDownloadError("The URL needs a host name.")
        if key in self._robots:
            return
        robots_url = self._robots_url(url)
        host = key[0]
        try:
            body, content_type, _final = self.pages._get(robots_url)
        except PageDownloadError as exc:
            raise PageDownloadError(
                "Could not read robots.txt for {0}. {1}".format(host, exc)
            )
        self._robots[key] = self._parse_robots(self.pages._decode(body, content_type))

    def _robots_url(self, url) -> str:
        parts = urlsplit(url)
        return urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))

    def _parse_robots(self, text) -> list:
        """Union of Disallow prefixes for * and for a HtmlCrawler user agent."""
        disallows = []
        agents = []
        saw_rule = False
        for raw in (text or "").splitlines():
            line = raw.split("#", 1)[0].strip()
            if line == "":
                agents = []
                saw_rule = False
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "user-agent":
                if saw_rule:
                    agents = []
                    saw_rule = False
                agents.append(value)
                continue
            if key in ("allow", "crawl-delay", "sitemap"):
                saw_rule = True
                continue
            if key != "disallow":
                continue
            saw_rule = True
            if value == "":
                continue
            if self._agents_apply(agents):
                disallows.append(value)
        return disallows

    def _agents_apply(self, agents) -> bool:
        for agent in agents:
            token = agent.strip().lower()
            if token == "*":
                return True
            if token.startswith(self.CRAWL_PRODUCT.lower()):
                return True
        return False

    def _disallowed(self, url) -> bool:
        rules = self._robots.get(self._host_key(url), [])
        path = urlsplit(url).path or "/"
        for prefix in rules:
            if path.startswith(prefix):
                return True
        return False

    def _links(self, html, base) -> list:
        found = []

        class Anchors(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag != "a":
                    return
                for key, value in attrs:
                    if key and key.lower() == "href" and value:
                        found.append(value)

        parser = Anchors(convert_charrefs=True)
        parser.feed(html or "")
        parser.close()
        resolved = []
        for raw in found:
            if self._dotdot(raw):
                resolved.append(raw)
                continue
            joined = self.pages._join(base, raw)
            if joined:
                resolved.append(joined)
        return resolved

    def _deeper(self, links, allowed, seen) -> bool:
        for link in links:
            canon = self._canonical(link)
            if canon is None:
                continue
            if self._host_key(canon) != allowed:
                continue
            if canon not in seen:
                return True
        return False

    def _dotdot(self, url) -> bool:
        text = url or ""
        if "://" in text or text.startswith("/"):
            path = urlsplit(text).path
        else:
            path = text.split("?", 1)[0].split("#", 1)[0]
        return ".." in path.split("/")

    def _canonical(self, url):
        parts = urlsplit(url or "")
        if parts.scheme not in ("http", "https") or not parts.hostname:
            return None
        if self._dotdot(url):
            return None
        host = parts.hostname.lower()
        port = parts.port
        if (parts.scheme == "http" and port == 80) or (parts.scheme == "https" and port == 443):
            port = None
        netloc = host if port is None else "{0}:{1}".format(host, port)
        path = parts.path or "/"
        if not path.startswith("/"):
            path = "/" + path
        return urlunsplit((parts.scheme.lower(), netloc, path, "", ""))

    def _host_key(self, url):
        parts = urlsplit(url or "")
        if not parts.hostname:
            return None
        port = parts.port
        if (parts.scheme == "http" and port == 80) or (parts.scheme == "https" and port == 443):
            port = None
        return (parts.hostname.lower(), port)

    def _is_root(self, url) -> bool:
        path = urlsplit(url).path or "/"
        return path == "/"

    def _relative(self, sitename, url) -> str:
        path = urlsplit(url).path or "/"
        segments = [part for part in path.split("/") if part]
        reserved = (self.pages.ASSETS_DIR, self.pages.MAP_NAME)
        for part in segments:
            if part in (".", "..") or part in reserved or "\x00" in part:
                raise PageDownloadError("The URL path is not a page folder.")
        if not segments:
            return sitename
        return "/".join([sitename] + segments)

    def _report(self, name, saved, skipped, stopped_pages, stopped_depth) -> str:
        root = os.path.join(self.pages.output_root(), name)
        lines = [
            "Crawled {0}".format(name),
            "Pages: {0}".format(len(saved)),
            "Site: {0}".format(root),
        ]
        if stopped_pages and stopped_depth:
            lines.append("Stopped by --max-pages and --depth.")
        elif stopped_pages:
            lines.append("Stopped by --max-pages.")
        elif stopped_depth:
            lines.append("Stopped by --depth.")
        else:
            lines.append("Finished.")
        if skipped:
            lines.append("Skipped:")
            lines.extend(skipped)
        return "\n".join(lines)
