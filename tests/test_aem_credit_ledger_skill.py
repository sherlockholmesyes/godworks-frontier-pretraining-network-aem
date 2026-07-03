import json
import unittest
from contextlib import redirect_stdout
from io import StringIO

from aem_poc.aem_bootstrap_growth import build_growth_ledger
from aem_poc.aem_credit_ledger_skill import demo_report, main, settle_credit_ledger_with_skills, skill_credit_micros
from aem_poc.aem_inference_receipts import build_demo_inference_receipt
from aem_poc.aem_network_cards import build_demo_host_advertisement, build_demo_node_card
from aem_poc.aem_skill_receipts import build_demo_skill_receipt


class AemCreditLedgerSkillTest(unittest.TestCase):
    def test_demo_settlement_emits_skill_mint(self) -> None:
        report = demo_report()
        settlement = report["settlement"]
        event_types = [event["event_type"] for event in settlement["events"]]

        self.assertTrue(settlement["ok"])
        self.assertEqual(settlement["skill_receipt_count"], 1)
        self.assertIn("skill_mint", event_types)
        self.assertEqual(event_types.count("skill_mint"), 1)

    def test_skill_credit_uses_quality_multiplier_and_cap(self) -> None:
        receipt = build_demo_skill_receipt()

        self.assertEqual(skill_credit_micros(receipt, 1.0), 1500)
        self.assertEqual(skill_credit_micros(receipt, 2.0), 3000)
        self.assertEqual(skill_credit_micros(receipt, 99.0), 7500)

    def test_invalid_skill_receipt_does_not_mint(self) -> None:
        node = build_demo_node_card()
        ad = build_demo_host_advertisement(node)
        growth = build_growth_ledger()
        skill = build_demo_skill_receipt()
        skill["execution_evidence"]["delta_score"] = 0
        inference = build_demo_inference_receipt(node, ad)

        settlement = settle_credit_ledger_with_skills(
            contribution_receipts=growth["contributions"],
            skill_receipts=[skill],
            inference_receipts=[inference],
            node_card=node,
            host_advertisement=ad,
        )
        event_types = [event["event_type"] for event in settlement["events"]]

        self.assertFalse(settlement["ok"])
        self.assertNotIn("skill_mint", event_types)
        self.assertEqual(settlement["skill_receipt_count"], 1)
        self.assertTrue(settlement["rejections"])

    def test_cli_uses_skill_aware_settlement(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertTrue(data["settlement"]["ok"])
        self.assertEqual(data["settlement"]["skill_receipt_count"], 1)
        self.assertIn("skill_mint", [event["event_type"] for event in data["settlement"]["events"]])


if __name__ == "__main__":
    unittest.main()
