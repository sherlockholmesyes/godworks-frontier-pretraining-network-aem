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


class AemNetworkEconomyTargetTest(unittest.TestCase):
    def test_network_economy_check_runs_foundation_gates(self) -> None:
        self.assertEqual(
            _make_target_commands("aem-network-economy-check"),
            [
                "$(MAKE) aem-network-bricks-check",
                "$(MAKE) aem-network-cards-check",
                "$(MAKE) aem-bootstrap-growth-check",
                "$(MAKE) aem-skill-receipts-check",
                "$(MAKE) aem-inference-receipts-check",
                "$(MAKE) aem-credit-ledger-check",
            ],
        )

    def test_skill_receipt_targets_exist(self) -> None:
        self.assertEqual(_make_target_commands("aem-skill-receipts"), ["python -m aem_poc.aem_skill_receipts"])
        self.assertEqual(_make_target_commands("aem-skill-receipts-check"), ["python -m aem_poc.aem_skill_receipts --check"])

    def test_inference_receipt_targets_exist(self) -> None:
        self.assertEqual(_make_target_commands("aem-inference-receipts"), ["python -m aem_poc.aem_inference_receipts"])
        self.assertEqual(_make_target_commands("aem-inference-receipts-check"), ["python -m aem_poc.aem_inference_receipts --check"])

    def test_credit_ledger_targets_use_skill_aware_settlement(self) -> None:
        self.assertEqual(_make_target_commands("aem-credit-ledger"), ["python -m aem_poc.aem_credit_ledger_skill"])
        self.assertEqual(_make_target_commands("aem-credit-ledger-check"), ["python -m aem_poc.aem_credit_ledger_skill --check"])


if __name__ == "__main__":
    unittest.main()
