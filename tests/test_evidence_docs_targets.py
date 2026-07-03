import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _make_target_commands(target: str) -> list[str]:
    lines = (REPO_ROOT / "Makefile").read_text(encoding="utf-8").splitlines()
    start = lines.index(f"{target}:") + 1
    commands: list[str] = []
    for line in lines[start:]:
        if line and not line.startswith("\t") and line.endswith(":"):
            break
        if line.startswith("\t"):
            commands.append(line[1:])
    return commands


class EvidenceDocsTargetsTest(unittest.TestCase):
    def test_evidence_docs_check_groups_docs_drift_checks(self) -> None:
        self.assertEqual(
            _make_target_commands("evidence-docs-check"),
            [
                "$(MAKE) evidence-artifact-index",
                "$(MAKE) evidence-artifact-index-md-check",
                "$(MAKE) evidence-status-example-check",
            ],
        )

    def test_evidence_docs_sync_groups_docs_generation(self) -> None:
        self.assertEqual(
            _make_target_commands("evidence-docs-sync"),
            [
                "$(MAKE) evidence-artifact-index-sync",
                "$(MAKE) evidence-artifact-index-md-sync",
                "$(MAKE) evidence-status-example-sync",
            ],
        )

    def test_status_example_check_stays_out_of_evidence_local_ci(self) -> None:
        local_ci = _make_target_commands("evidence-local-ci")

        self.assertIn("$(MAKE) evidence-status", local_ci)
        self.assertNotIn("$(MAKE) evidence-status-example-check", local_ci)
        self.assertNotIn("$(MAKE) evidence-docs-check", local_ci)


if __name__ == "__main__":
    unittest.main()
