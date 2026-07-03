import json
import unittest
from contextlib import redirect_stdout
from io import StringIO

from aem_poc.aem_network_cards import (
    build_demo_host_advertisement,
    build_demo_node_card,
    demo_report,
    host_advertisement_report,
    main,
    validate_host_advertisement,
    validate_node_card,
)
from aem_poc.schema_validation import SchemaValidationError


class AemNetworkCardsTest(unittest.TestCase):
    def test_demo_cards_validate_and_bind_economy(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)

        validate_node_card(node)
        validate_host_advertisement(ad, node)
        report = host_advertisement_report(ad, node)

        self.assertTrue(report["ok"])
        self.assertEqual(report["settlement_currency"], "AEM_CREDIT")
        self.assertEqual(report["credit_account"], node["economic_policy"]["credit_account"])
        self.assertIn("inference_work_receipt", report["receipts_required"])

    def test_node_card_requires_capacity_and_economic_policy(self) -> None:
        incomplete = {
            "card_version": "2026-07-01.v1",
            "node_id": "node.incomplete",
            "owner_key": "owner_pubkey",
            "signature": "sig",
        }

        with self.assertRaises(SchemaValidationError):
            validate_node_card(incomplete)

    def test_node_card_requires_receipts_for_earning_roles(self) -> None:
        node = build_demo_node_card()
        node["receipts_required"] = ["capacity_probe_receipt"]

        with self.assertRaisesRegex(SchemaValidationError, "receipts_required missing"):
            validate_node_card(node)

    def test_host_advertisement_cannot_go_below_node_minimum_price(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        ad["offer"]["inference_credit_rate_micros"] = 0

        report = host_advertisement_report(ad, node)

        self.assertFalse(report["ok"])
        self.assertIn("inference offer rate below node minimum", report["errors"])

    def test_host_advertisement_requires_role_receipts(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        ad["receipt_requirements"] = ["route_trace_receipt"]

        report = host_advertisement_report(ad, node)

        self.assertFalse(report["ok"])
        self.assertTrue(any("receipt_requirements missing" in error for error in report["errors"]))

    def test_host_advertisement_must_use_node_expert(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        ad["expert_id"] = "expert.not.on.node"

        report = host_advertisement_report(ad, node)

        self.assertFalse(report["ok"])
        self.assertIn("advertised expert_id must be listed in node_card.advertised_experts", report["errors"])

    def test_demo_report_and_cli(self) -> None:
        report = demo_report()
        self.assertTrue(report["eligibility_report"]["ok"])

        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertTrue(data["eligibility_report"]["ok"])
        self.assertEqual(data["node_card"]["economic_policy"]["settlement_currency"], "AEM_CREDIT")


if __name__ == "__main__":
    unittest.main()
