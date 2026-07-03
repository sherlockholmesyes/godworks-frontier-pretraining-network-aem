import json
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO

from aem_poc.aem_bootstrap_growth import (
    build_demo_contribution,
    build_growth_ledger,
    contribution_report,
    main,
    validate_contribution,
)
from aem_poc.schema_validation import SchemaValidationError


class AemBootstrapGrowthTest(unittest.TestCase):
    def test_growth_ledger_covers_all_contribution_types(self) -> None:
        ledger = build_growth_ledger()

        self.assertEqual(ledger["contribution_count"], 6)
        self.assertEqual(set(ledger["contribution_type_counts"]), {"curriculum", "data_shard", "eval", "knowledge", "operator", "skill"})
        self.assertEqual(ledger["credit_settlement_currency"], "AEM_CREDIT")
        self.assertIn("unauthorized competitor distillation", ledger["forbidden_reductions"])
        self.assertIn("verified capability deltas", ledger["growth_third"])

    def test_demo_contributions_validate(self) -> None:
        for kind in ("knowledge", "skill", "data_shard", "eval", "curriculum", "operator"):
            receipt = build_demo_contribution(kind)
            validate_contribution(receipt)
            report = contribution_report(receipt)
            self.assertTrue(report["ok"])
            self.assertEqual(report["settlement_currency"], "AEM_CREDIT")

    def test_rejects_terms_unverified_third_party_outputs(self) -> None:
        receipt = build_demo_contribution("knowledge")
        receipt["source_policy"]["contains_third_party_model_outputs"] = True
        receipt["source_policy"]["third_party_terms_verified"] = False

        with self.assertRaisesRegex(SchemaValidationError, "third-party model outputs require verified terms"):
            validate_contribution(receipt)

    def test_rejects_unauthorized_competitor_distillation_policy(self) -> None:
        receipt = build_demo_contribution("skill")
        receipt["anti_distillation"]["no_unauthorized_competitor_distillation"] = False

        with self.assertRaisesRegex(SchemaValidationError, "unauthorized competitor distillation"):
            validate_contribution(receipt)

    def test_rejects_credit_without_required_receipts(self) -> None:
        receipt = build_demo_contribution("skill")
        receipt["receipts_required"] = ["provenance_receipt"]

        with self.assertRaisesRegex(SchemaValidationError, "receipts_required missing"):
            validate_contribution(receipt)

    def test_rejects_raw_unowned_upload(self) -> None:
        receipt = build_demo_contribution("data_shard")
        receipt["source_policy"]["human_authored_or_owned"] = False

        with self.assertRaisesRegex(SchemaValidationError, "human-authored"):
            validate_contribution(receipt)

    def test_contribution_report_returns_errors_without_throwing(self) -> None:
        receipt = build_demo_contribution("operator")
        broken = deepcopy(receipt)
        broken["source_policy"]["allowed_for_training"] = False

        report = contribution_report(broken)

        self.assertFalse(report["ok"])
        self.assertTrue(report["errors"])

    def test_cli_prints_growth_ledger(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertIn("ledger", data)
        self.assertEqual(data["ledger"]["contribution_count"], 6)
        self.assertTrue(all(report["ok"] for report in data["reports"]))


if __name__ == "__main__":
    unittest.main()
