from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from typing import Any, Sequence

from .aem_bootstrap_growth import build_growth_ledger
from .aem_credit_ledger import (
    DEFAULT_PAYER_ACCOUNT,
    DEFAULT_PAYER_START_BALANCE_MICROS,
    SETTLEMENT_CURRENCY,
    SETTLEMENT_VERSION,
    contribution_credit_micros,
    validate_credit_ledger_settlement,
)
from .aem_inference_receipts import build_demo_inference_receipt, inference_receipt_report
from .aem_network_cards import build_demo_host_advertisement, build_demo_node_card
from .aem_skill_receipts import build_demo_skill_receipt, validate_skill_receipt


def _event(event_id: str, event_type: str, source_receipt_id: str, account: str, amount_micros: int, reason: str) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "source_receipt_id": source_receipt_id,
        "account": account,
        "amount_micros": amount_micros,
        "settlement_currency": SETTLEMENT_CURRENCY,
        "reason": reason,
    }


def _reject(source_receipt_id: str, reason: str) -> dict[str, str]:
    return {"source_receipt_id": source_receipt_id, "reason": reason}


def skill_credit_micros(receipt: dict[str, Any], quality_multiplier: float = 1.0) -> int:
    credit = receipt["credit_policy"]
    multiplier = min(credit["quality_multiplier_cap"], max(credit["quality_multiplier_floor"], quality_multiplier))
    return int(credit["base_credit_micros"] * multiplier)


def settle_credit_ledger_with_skills(
    *,
    contribution_receipts: Sequence[dict[str, Any]],
    skill_receipts: Sequence[dict[str, Any]],
    inference_receipts: Sequence[dict[str, Any]],
    node_card: dict[str, Any],
    host_advertisement: dict[str, Any],
    payer_account: str = DEFAULT_PAYER_ACCOUNT,
    initial_balances: dict[str, int] | None = None,
    challenge_window_closed: bool = True,
    contribution_quality_multiplier: float = 1.0,
    skill_quality_multiplier: float = 1.0,
) -> dict[str, Any]:
    balances: defaultdict[str, int] = defaultdict(int)
    for account, balance in (initial_balances or {payer_account: DEFAULT_PAYER_START_BALANCE_MICROS}).items():
        balances[account] += balance

    events: list[dict[str, Any]] = []
    rejections: list[dict[str, str]] = []
    seen_spend_keys: set[str] = set()
    total_minted = 0
    total_transferred = 0

    for receipt in contribution_receipts:
        receipt_id = str(receipt.get("receipt_id", "unknown_contribution_receipt"))
        try:
            from .aem_bootstrap_growth import validate_contribution

            validate_contribution(receipt)
            amount = contribution_credit_micros(receipt, contribution_quality_multiplier)
        except Exception as exc:
            rejections.append(_reject(receipt_id, str(exc)))
            continue
        account = receipt["credit_policy"]["credit_account"]
        events.append(_event(f"settle.{receipt_id}.mint", "contribution_mint", receipt_id, account, amount, receipt["credit_policy"]["credit_basis"]))
        balances[account] += amount
        total_minted += amount

    for receipt in skill_receipts:
        receipt_id = str(receipt.get("skill_receipt_id", "unknown_skill_receipt"))
        try:
            validate_skill_receipt(receipt)
            amount = skill_credit_micros(receipt, skill_quality_multiplier)
        except Exception as exc:
            rejections.append(_reject(receipt_id, str(exc)))
            continue
        account = receipt["credit_policy"]["credit_account"]
        events.append(_event(f"settle.{receipt_id}.skill_mint", "skill_mint", receipt_id, account, amount, "verified_skill_use"))
        balances[account] += amount
        total_minted += amount

    for receipt in inference_receipts:
        receipt_id = str(receipt.get("receipt_id", "unknown_inference_receipt"))
        if not challenge_window_closed:
            rejections.append(_reject(receipt_id, "challenge window is not closed"))
            continue
        report = inference_receipt_report(receipt, node_card, host_advertisement, seen_spend_keys=seen_spend_keys)
        if not report["ok"]:
            rejections.append(_reject(receipt_id, "; ".join(report["errors"])))
            continue
        spend_key = report["spend_key"]
        if not isinstance(spend_key, str):
            rejections.append(_reject(receipt_id, "missing spend key"))
            continue
        charge = int(report["credit_charge_micros"])
        host_account = receipt["credit_account"]
        events.append(_event(f"settle.{receipt_id}.debit", "inference_debit", receipt_id, payer_account, -charge, "inference spend"))
        events.append(_event(f"settle.{receipt_id}.host_credit", "inference_host_credit", receipt_id, host_account, charge, "inference work credit"))
        balances[payer_account] -= charge
        balances[host_account] += charge
        total_transferred += charge
        seen_spend_keys.add(spend_key)

    report = {
        "settlement_version": SETTLEMENT_VERSION,
        "settlement_currency": SETTLEMENT_CURRENCY,
        "challenge_window_closed": challenge_window_closed,
        "contribution_receipt_count": len(contribution_receipts),
        "skill_receipt_count": len(skill_receipts),
        "inference_receipt_count": len(inference_receipts),
        "accepted_event_count": len(events),
        "rejected_event_count": len(rejections),
        "total_minted_micros": total_minted,
        "total_transferred_micros": total_transferred,
        "net_supply_delta_micros": total_minted,
        "accounts": [{"account": account, "balance_micros": balance} for account, balance in sorted(balances.items())],
        "events": events,
        "rejections": rejections,
        "seen_spend_keys": sorted(seen_spend_keys),
        "ok": not rejections,
    }
    validate_credit_ledger_settlement(report)
    return report


def demo_report() -> dict[str, Any]:
    node = build_demo_node_card()
    ad = build_demo_host_advertisement(node)
    growth = build_growth_ledger()
    skill = build_demo_skill_receipt()
    inference = build_demo_inference_receipt(node, ad)
    settlement = settle_credit_ledger_with_skills(
        contribution_receipts=growth["contributions"],
        skill_receipts=[skill],
        inference_receipts=[inference],
        node_card=node,
        host_advertisement=ad,
    )
    return {
        "node_card": node,
        "host_advertisement": ad,
        "contribution_receipts": growth["contributions"],
        "skill_receipts": [skill],
        "inference_receipts": [inference],
        "settlement": settlement,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Settle contribution, skill, and inference receipts into AEM_CREDIT balances")
    parser.add_argument("--check", action="store_true", help="validate demo skill-aware CreditLedger settlement")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    report = demo_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["settlement"]["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
