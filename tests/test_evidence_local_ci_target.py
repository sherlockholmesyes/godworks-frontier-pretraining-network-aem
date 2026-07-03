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


class EvidenceLocalCiTargetTest(unittest.TestCase):
    def test_evidence_local_ci_runs_workflow_gate_order(self) -> None:
        expected = [
            "$(MAKE) test",
            "$(MAKE) evidence-artifact-index",
            "$(MAKE) evidence-artifact-index-md-check",
            "$(MAKE) evidence-status",
            "$(MAKE) evidence-metadata-check",
            "$(MAKE) evidence-upload-policy",
            "$(MAKE) evidence-upload-drift",
            "$(MAKE) evidence-seal-verify-demo",
            "$(MAKE) evidence-second-stage-seal",
            "$(MAKE) evidence-second-stage-seal-verify",
        ]
        self.assertEqual(_make_target_commands("evidence-local-ci"), expected)

    def test_ci_workflow_delegates_to_evidence_local_ci(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

        self.assertIn("run: make evidence-local-ci", workflow)
        self.assertNotIn("run: make evidence-metadata-check", workflow)
        self.assertNotIn("run: make evidence-seal-verify-demo", workflow)


if __name__ == "__main__":
    unittest.main()
