import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReadmeLocalVerificationTest(unittest.TestCase):
    def test_readme_names_evidence_local_ci_as_canonical_command(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("make evidence-local-ci", readme)
        self.assertIn("canonical local command", readme)
        self.assertIn("run: make evidence-local-ci", readme)

    def test_readme_local_verification_section_is_not_hand_written_gate_list_only(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        section_start = readme.index("## Canonical local verification")
        section_end = readme.index("## Evidence status")
        section = readme[section_start:section_end]

        self.assertIn("make evidence-local-ci", section)
        self.assertIn("Gate order:", section)
        self.assertIn("evidence-artifact-index-md-check", section)
        self.assertIn("evidence-status", section)
        self.assertIn("evidence-second-stage-seal-verify", section)

    def test_readme_documents_evidence_status_command(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        section_start = readme.index("## Evidence status")
        section_end = readme.index("## Evidence seal model")
        section = readme[section_start:section_end]

        self.assertIn("python -m aem_poc.evidence_status", section)
        self.assertIn("make evidence-status", section)
        self.assertIn("schemas/evidence_status.schema.json", section)
        self.assertIn("seal stage counts", section)
        self.assertIn("make evidence-docs-check", section)
        self.assertIn("make evidence-docs-sync", section)
        self.assertIn("stays out of `evidence-local-ci`", section)


if __name__ == "__main__":
    unittest.main()
