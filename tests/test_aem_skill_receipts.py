import json
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO

from aem_poc.aem_skill_receipts import (
    build_demo_skill_receipt,
    demo_report,
    main,
    skill_receipt_report,
    validate_skill_receipt,
)
from aem_poc.schema_validation import SchemaValidationError


class AemSkillReceiptTest(unittest.TestCase):
    def test_demo_skill_receipt_validates(self) -> None:
        receipt = build_demo_skill_receipt()

        validate_skill_receipt(receipt)
        report = skill_receipt_report(receipt)

        self.assertTrue(report["ok"])
        self.assertEqual(report["settlement_currency"], "AEM_CREDIT")
        self.assertEqual(report["credit_basis"], "verified_skill_use")
        self.assertGreater(report["delta_score"], 0)
        self.assertIn("skill_execution_receipt", report["receipt_requirements"])
        self.assertIn("skill_delta_eval_receipt", report["receipt_requirements"])

    def test_rejects_missing_execution_receipt(self) -> None:
        receipt = build_demo_skill_receipt()
        receipt["receipt_requirements"] = ["provenance_receipt", "skill_delta_eval_receipt", "operator_reality_gate_receipt"]

        with self.assertRaisesRegex(SchemaValidationError, "receipt_requirements missing"):
            validate_skill_receipt(receipt)

    def test_rejects_non_positive_delta(self) -> None:
        receipt = build_demo_skill_receipt()
        receipt["execution_evidence"]["delta_score"] = 0
        receipt["execution_evidence"]["after_score"] = receipt["execution_evidence"]["before_score"]

        with self.assertRaisesRegex(SchemaValidationError, "delta_score must be positive"):
            validate_skill_receipt(receipt)

    def test_rejects_after_score_below_before_score(self) -> None:
        receipt = build_demo_skill_receipt()
        receipt["execution_evidence"]["before_score"] = 0.8
        receipt["execution_evidence"]["after_score"] = 0.6
        receipt["execution_evidence"]["delta_score"] = 0.1

        with self.assertRaisesRegex(SchemaValidationError, "after_score must be >= before_score"):
            validate_skill_receipt(receipt)

    def test_rejects_unauthorized_competitor_distillation(self) -> None:
        receipt = build_demo_skill_receipt()
        receipt["anti_distillation"]["no_unauthorized_competitor_distillation"] = False

        with self.assertRaisesRegex(SchemaValidationError, "unauthorized competitor distillation"):
            validate_skill_receipt(receipt)

    def test_rejects_unverified_third_party_outputs(self) -> None:
        receipt = build_demo_skill_receipt()
        receipt["source_policy"]["contains_third_party_model_outputs"] = True
        receipt["source_policy"]["third_party_terms_verified"] = False

        with self.assertRaisesRegex(SchemaValidationError, "third-party model outputs require verified terms"):
            validate_skill_receipt(receipt)

    def test_rejects_wrong_credit_basis(self) -> None:
        receipt = build_demo_skill_receipt()
        receipt["credit_policy"]["credit_basis"] = "accepted_delta"

        with self.assertRaisesRegex(SchemaValidationError, "skill credit_basis must be verified_skill_use"):
            validate_skill_receipt(receipt)

    def test_rejects_missing_verifier_report(self) -> None:
        receipt = build_demo_skill_receipt()
        receipt["verifier_report_refs"] = []

        with self.assertRaisesRegex(SchemaValidationError, "verifier_report_refs must not be empty"):
            validate_skill_receipt(receipt)

    def test_report_returns_errors_without_throwing(self) -> None:
        receipt = build_demo_skill_receipt()
        broken = deepcopy(receipt)
        broken["source_policy"]["allowed_for_training"] = False

        report = skill_receipt_report(broken)

        self.assertFalse(report["ok"])
        self.assertTrue(report["errors"])

    def test_demo_report_and_cli(self) -> None:
        report = demo_report()
        self.assertTrue(report["eligibility_report"]["ok"])

        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertTrue(data["eligibility_report"]["ok"])
        self.assertEqual(data["skill_receipt"]["credit_policy"]["credit_basis"], "verified_skill_use")


if __name__ == "__main__":
    unittest.main()
