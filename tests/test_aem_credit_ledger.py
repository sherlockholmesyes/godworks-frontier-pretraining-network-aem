import json
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO

from aem_poc.aem_bootstrap_growth import build_demo_contribution, build_growth_ledger
from aem_poc.aem_credit_ledger import (
    DEFAULT_PAYER_ACCOUNT,
    build_demo_settlement,
    contribution_credit_micros,
    demo_report,
    main,
    settle_credit_ledger,
    validate_credit_ledger_settlement,
)
from aem_poc.aem_inference_receipts import build_demo_inference_receipt
from aem_poc.aem_network_cards import build_demo_host_advertisement, build_demo_node_card


class AemCreditLedgerTest(unittest.TestCase):
    def test_demo_settlement_consumes_contribution_and_inference_receipts(self) -> None:
        settlement = build_demo_settlement()

        validate_credit_ledger_settlement(settlement)
        self.assertTrue(settlement["ok"])
        self.assertEqual(settlement["contribution_receipt_count"], 6)
        self.assertEqual(settlement["inference_receipt_count"], 1)
        self.assertEqual(settlement["total_minted_micros"], 6000)
        self.assertGreater(settlement["total_transferred_micros"], 0)
        self.assertEqual(settlement["net_supply_delta_micros"], 6000)
        event_types = [event["event_type"] for event in settlement["events"]]
        self.assertEqual(event_types.count("contribution_mint"), 6)
        self.assertIn("inference_debit", event_types)
        self.assertIn("inference_host_credit", event_types)

    def test_contribution_credit_uses_quality_multiplier(self) -> None:
        receipt = build_demo_contribution("operator")

        self.assertEqual(contribution_credit_micros(receipt, 1.0), 1000)
        self.assertEqual(contribution_credit_micros(receipt, 3.0), 3000)
        self.assertEqual(contribution_credit_micros(receipt, 99.0), 5000)

    def test_duplicate_inference_spend_key_is_rejected(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        settlement = settle_credit_ledger(
            contribution_receipts=[],
            inference_receipts=[receipt, deepcopy(receipt)],
            node_card=node,
            host_advertisement=ad,
        )

        self.assertFalse(settlement["ok"])
        self.assertEqual(settlement["inference_receipt_count"], 2)
        self.assertEqual(settlement["rejected_event_count"], 1)
        self.assertIn("duplicate spend key already seen", settlement["rejections"][0]["reason"])
        event_types = [event["event_type"] for event in settlement["events"]]
        self.assertEqual(event_types.count("inference_host_credit"), 1)

    def test_open_challenge_window_blocks_inference_settlement(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        settlement = settle_credit_ledger(
            contribution_receipts=[],
            inference_receipts=[receipt],
            node_card=node,
            host_advertisement=ad,
            challenge_window_closed=False,
        )

        self.assertFalse(settlement["ok"])
        self.assertEqual(settlement["total_transferred_micros"], 0)
        self.assertIn("challenge window is not closed", settlement["rejections"][0]["reason"])

    def test_invalid_contribution_is_not_minted(self) -> None:
        receipt = build_demo_contribution("knowledge")
        receipt["source_policy"]["allowed_for_training"] = False
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        settlement = settle_credit_ledger(
            contribution_receipts=[receipt],
            inference_receipts=[],
            node_card=node,
            host_advertisement=ad,
        )

        self.assertFalse(settlement["ok"])
        self.assertEqual(settlement["total_minted_micros"], 0)
        self.assertEqual(settlement["accepted_event_count"], 0)
        self.assertEqual(settlement["rejected_event_count"], 1)

    def test_inference_transfer_debits_payer_and_credits_host(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        receipt = build_demo_inference_receipt(node, ad)
        settlement = settle_credit_ledger(
            contribution_receipts=[],
            inference_receipts=[receipt],
            node_card=node,
            host_advertisement=ad,
            initial_balances={DEFAULT_PAYER_ACCOUNT: 10000},
        )
        balances = {item["account"]: item["balance_micros"] for item in settlement["accounts"]}
        charge = receipt["credit_charge_micros"]

        self.assertTrue(settlement["ok"])
        self.assertEqual(balances[DEFAULT_PAYER_ACCOUNT], 10000 - charge)
        self.assertEqual(balances[node["economic_policy"]["credit_account"]], charge)

    def test_cli_prints_valid_settlement(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertTrue(data["settlement"]["ok"])
        self.assertEqual(data["settlement"]["settlement_currency"], "AEM_CREDIT")


if __name__ == "__main__":
    unittest.main()
