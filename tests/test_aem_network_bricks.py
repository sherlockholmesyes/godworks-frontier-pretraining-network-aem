import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from aem_poc.aem_network_bricks import (
    build_network_brick_ledger,
    ledger_sync_report,
    load_network_brick_ledger,
    main,
    validate_network_brick_ledger,
    write_network_brick_ledger,
)

EXPECTED_BRICK_COUNT = 12


class AemNetworkBrickLedgerTest(unittest.TestCase):
    def test_build_network_brick_ledger_maps_required_bricks(self) -> None:
        ledger = build_network_brick_ledger()

        validate_network_brick_ledger(ledger)
        self.assertEqual(ledger["brick_count"], EXPECTED_BRICK_COUNT)
        self.assertEqual(ledger["status_counts"]["closed_poc"], 1)
        self.assertGreaterEqual(ledger["status_counts"]["proto_brick"], 4)
        self.assertGreaterEqual(ledger["status_counts"]["research_packet"], 5)
        self.assertIn("Off-chain expert training/inference produces signed receipts", ledger["network_third"])
        self.assertIn("inference_challenge_protocol", ledger["missing_primitives"])
        self.assertIn("settlement_finality_rule", ledger["missing_primitives"])

    def test_every_brick_has_design_and_primitive_closure(self) -> None:
        ledger = build_network_brick_ledger()

        for brick in ledger["bricks"]:
            for key in ("wrong1", "death1", "wrong2", "death2", "third"):
                self.assertTrue(brick[key], brick["id"])
            self.assertTrue(brick["nodes"], brick["id"])
            self.assertTrue(brick["minimal_tests"], brick["id"])
            self.assertTrue(brick["kill_criteria"], brick["id"])
            self.assertIn(brick["primitive_closure"]["closure_status"], {"closed", "partially_closed", "open"})

    def test_blockchain_inference_collapse_is_rejected(self) -> None:
        ledger = build_network_brick_ledger()
        joined = json.dumps(ledger, sort_keys=True)

        self.assertIn("blockchain executes inference", joined)
        self.assertIn("too expensive", joined)
        self.assertIn("signed receipts", joined)
        self.assertIn("verifier challenges", joined)

    def test_write_and_load_network_brick_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            written = write_network_brick_ledger(path)
            loaded = load_network_brick_ledger(path)

        self.assertEqual(loaded, written)
        validate_network_brick_ledger(loaded)

    def test_sync_report_detects_matching_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            write_network_brick_ledger(path)
            report = ledger_sync_report(path)

        self.assertTrue(report["ok"])
        self.assertTrue(report["matches_generated"])
        self.assertEqual(report["brick_count"], EXPECTED_BRICK_COUNT)

    def test_cli_prints_ledger(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertEqual(data["brick_count"], EXPECTED_BRICK_COUNT)
        self.assertIn("credit_ledger_settlement", [brick["id"] for brick in data["bricks"]])

    def test_cli_syncs_ledger_to_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            out = StringIO()
            with redirect_stdout(out):
                code = main(["--output", str(path), "--sync"])
            saved = load_network_brick_ledger(path)

        self.assertEqual(code, 0)
        self.assertEqual(saved, build_network_brick_ledger())
        self.assertTrue(json.loads(out.getvalue())["ok"])


if __name__ == "__main__":
    unittest.main()
