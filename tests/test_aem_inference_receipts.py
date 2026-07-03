import json
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO

from aem_poc.aem_inference_receipts import (
    REQUIRED_CHALLENGE_METHODS,
    build_demo_inference_receipt,
    build_spend_key,
    demo_report,
    inference_receipt_report,
    main,
    validate_inference_receipt,
)
from aem_poc.aem_network_cards import build_demo_host_advertisement, build_demo_node_card
from aem_poc.schema_validation import SchemaValidationError


class AemInferenceReceiptsTest(unittest.TestCase):
    def test_demo_inference_receipt_validates(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)

        validate_inference_receipt(receipt, node, ad)
        report = inference_receipt_report(receipt, node, ad)

        self.assertTrue(report["ok"])
        self.assertEqual(report["credit_charge_micros"], report["expected_credit_charge_micros"])
        self.assertEqual(set(report["challenge_methods"]), REQUIRED_CHALLENGE_METHODS)

    def test_duplicate_spend_key_is_rejected(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        seen = {receipt["duplicate_spend"]["spend_key"]}

        report = inference_receipt_report(receipt, node, ad, seen_spend_keys=seen)

        self.assertFalse(report["ok"])
        self.assertIn("duplicate spend key already seen", report["errors"])

    def test_spend_key_must_bind_task_expert_node_nonce(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        receipt["duplicate_spend"]["spend_key"] = build_spend_key("wrong", receipt["expert_id"], receipt["node_id"], receipt["commitments"]["nonce"])

        report = inference_receipt_report(receipt, node, ad)

        self.assertFalse(report["ok"])
        self.assertIn("duplicate_spend.spend_key does not match task/expert/node/nonce binding", report["errors"])

    def test_missing_challenge_method_is_rejected(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        receipt["challenge_surface"]["challenge_methods"] = ["output_commitment_open"]

        report = inference_receipt_report(receipt, node, ad)

        self.assertFalse(report["ok"])
        self.assertTrue(any("challenge methods missing" in error for error in report["errors"]))

    def test_credit_charge_must_match_host_rate(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        receipt["credit_charge_micros"] -= 1

        report = inference_receipt_report(receipt, node, ad)

        self.assertFalse(report["ok"])
        self.assertIn("credit_charge_micros must match host advertisement rate", report["errors"])

    def test_receipt_must_match_host_advertisement(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        receipt["host_advertisement_id"] = "host_ad.other"

        report = inference_receipt_report(receipt, node, ad)

        self.assertFalse(report["ok"])
        self.assertIn("host_advertisement_id must match HostAdvertisement", report["errors"])

    def test_policy_receipts_required_for_credit(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        receipt["policy"]["receipt_requirements"] = ["inference_work_receipt"]

        report = inference_receipt_report(receipt, node, ad)

        self.assertFalse(report["ok"])
        self.assertTrue(any("policy receipt requirements missing" in error for error in report["errors"]))

    def test_validation_raises_on_invalid_receipt(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        broken = deepcopy(receipt)
        broken["policy"]["allowed_for_credit"] = False

        with self.assertRaisesRegex(SchemaValidationError, "allowed_for_credit"):
            validate_inference_receipt(broken, node, ad)

    def test_demo_report_and_cli(self) -> None:
        report = demo_report()
        self.assertTrue(report["eligibility_report"]["ok"])

        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertTrue(data["eligibility_report"]["ok"])
        self.assertEqual(data["inference_work_receipt"]["settlement_currency"], "AEM_CREDIT")


if __name__ == "__main__":
    unittest.main()
