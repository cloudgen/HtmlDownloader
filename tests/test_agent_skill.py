# TP-AGENT-01 — side-product skill. Primary law: requirement-agent-use-skill.
"""The agent skill names the real verbs and the bans."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "agent" / "SKILL.md"


class TestAgentUseSkill(unittest.TestCase):
    """TP-AGENT-01."""

    def test_tp_agent_01_skill_instructs_download_and_serve(self):
        """TP-AGENT-01: the skill names download, serve, the URL rule, and the bans."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("html-downloader download --url", text)
        self.assertIn("html-downloader serve --page-name", text)
        self.assertIn("127.0.0.1", text)
        self.assertIn("5000", text)
        self.assertIn("--html", text)
        self.assertIn("Omit `--name` only when the URL recommends the folder", text)
        self.assertIn("A host-only URL does not recommend a folder", text)
        self.assertIn("menu row **2**", text)
        self.assertIn("`language` is menu row 7, not a typed verb", text)
        self.assertIn("html-downloader crawl --url", text)
        self.assertIn("--depth", text)
        self.assertIn("--max-pages", text)
        for banned in ("hello", "join", "list-videos"):
            self.assertIn(banned, text)
        self.assertIn("Do not call an encoder", text)
        self.assertIn("Do not pipe a downloaded script into a shell", text)
        self.assertNotIn("html-downloader join", text)
        self.assertNotIn("curl -fsSL", text)
        self.assertNotIn("There is no `crawl` verb", text)

    def test_tp_agent_02_crawl_sample_keeps_bounds_off_download(self):
        """TP-AGENT-02: the crawl sample has both bounds. The download samples do not."""
        text = SKILL.read_text(encoding="utf-8")
        head, tail = text.split("## Crawl one site", 1)
        crawl, _serve = tail.split("## Serve one saved page", 1)

        def fences(section):
            parts = section.split("```")
            blocks = []
            for part in parts[1::2]:
                blocks.append(part.split("\n", 1)[-1])
            return "\n".join(blocks)

        download_samples = fences(head.split("## Save one page", 1)[1])
        crawl_samples = fences(crawl)
        self.assertIn("--depth", crawl_samples)
        self.assertIn("--max-pages", crawl_samples)
        self.assertNotIn("--depth", download_samples)
        self.assertNotIn("--max-pages", download_samples)
