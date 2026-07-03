import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReadmeDocsStatusLineTest(unittest.TestCase):
    def test_readme_evidence_status_section_names_docs_gate_fields(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        section = readme[readme.index("## Evidence status") : readme.index("## Evidence seal model")]

        self.assertIn("Docs gate status line", section)
        self.assertIn("docs_check_command", section)
        self.assertIn("docs_check_gates", section)
        self.assertIn("docs_sync_command", section)
        self.assertIn("docs_sync_gates", section)
        self.assertIn("make evidence-docs-check", section)
        self.assertIn("make evidence-docs-sync", section)


if __name__ == "__main__":
    unittest.main()
