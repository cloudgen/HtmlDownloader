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
        for banned in ("hello", "join", "list-videos", "crawl"):
            self.assertIn(banned, text)
        self.assertIn("Do not call an encoder", text)
        self.assertIn("Do not pipe a downloaded script into a shell", text)
        self.assertNotIn("html-downloader join", text)
        self.assertNotIn("html-downloader crawl", text)
        self.assertNotIn("curl -fsSL", text)
