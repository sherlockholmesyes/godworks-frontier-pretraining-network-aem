from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from typing import Any, Iterable, Sequence

from .aem_bootstrap_growth import build_growth_ledger, validate_contribution
from .aem_inference_receipts import build_demo_inference_receipt, inference_receipt_report
from .aem_network_cards import build_demo_host_advertisement, build_demo_node_card
from .schema_validation import SchemaValidationError, validate_data


SETTLEMENT_SCHEMA = "credit_ledger_settlement.schema.json"
SETTLEMENT_VERSION = "2026-07-01.v1"
SETTLEMENT_CURRENCY = "AEM_CREDIT"
DEFAULT_PAYER_ACCOUNT = "aem_user_spend_account_demo_001"
DEFAULT_PAYER_START_BALANCE_MICROS = 50_000


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _event_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    required = ("event_id", "event_type", "source_receipt_id", "account", "amount_micros", "settlement_currency", "reason")
    for item in value:
        if not isinstance(item, dict) or not all(key in item for key in required):
            return False
        for key in ("event_id", "event_type", "source_receipt_id", "account", "settlement_currency", "reason"):
            if not isinstance(item.get(key), str):
                return False
        if item["event_type"] not in {"contribution_mint", "inference_debit", "inference_host_credit"}:
            return False
        if item["settlement_currency"] != SETTLEMENT_CURRENCY:
            return False
        if not isinstance(item.get("amount_micros"), int):
            return False
    return True


def _account_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("account"), str):
            return False
        if not isinstance(item.get("balance_micros"), int):
            return False
    return True


def _rejection_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("source_receipt_id"), str) or not isinstance(item.get("reason"), str):
            return False
    return True


def _shape_ok(report: dict[str, Any]) -> bool:
    required = (
        "settlement_version",
        "settlement_currency",
        "challenge_window_closed",
        "contribution_receipt_count",
        "inference_receipt_count",
        "accepted_event_count",
        "rejected_event_count",
        "total_minted_micros",
        "total_transferred_micros",
        "net_supply_delta_micros",
        "accounts",
        "events",
        "rejections",
        "seen_spend_keys",
        "ok",
    )
    if not all(key in report for key in required):
        return False
    if not isinstance(report["settlement_version"], str) or report["settlement_currency"] != SETTLEMENT_CURRENCY:
        return False
    if not isinstance(report["challenge_window_closed"], bool) or not isinstance(report["ok"], bool):
        return False
    for key in (
        "contribution_receipt_count",
        "inference_receipt_count",
        "accepted_event_count",
        "rejected_event_count",
        "total_minted_micros",
        "total_transferred_micros",
    ):
        if not isinstance(report[key], int) or report[key] < 0:
            return False
    if not isinstance(report["net_supply_delta_micros"], int):
        return False
    return _account_list(report["accounts"]) and _event_list(report["events"]) and _rejection_list(report["rejections"]) and _str_list(report["seen_spend_keys"])


def validate_credit_ledger_settlement(report: dict[str, Any]) -> None:
    result = validate_data(report, SETTLEMENT_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {SETTLEMENT_SCHEMA}",) and _shape_ok(report):
        return
    raise SchemaValidationError(f"{SETTLEMENT_SCHEMA} validation failed: {result.errors}")


def contribution_credit_micros(receipt: dict[str, Any], quality_multiplier: float = 1.0) -> int:
    credit = receipt["credit_policy"]
    floor = credit["quality_multiplier_floor"]
    cap = credit["quality_multiplier_cap"]
    multiplier = min(cap, max(floor, quality_multiplier))
    return int(credit["base_credit_micros"] * multiplier)


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


def _rejection(source_receipt_id: str, reason: str) -> dict[str, str]:
    return {"source_receipt_id": source_receipt_id, "reason": reason}


def settle_credit_ledger(
    *,
    contribution_receipts: Sequence[dict[str, Any]],
    inference_receipts: Sequence[dict[str, Any]],
    node_card: dict[str, Any],
    host_advertisement: dict[str, Any],
    payer_account: str = DEFAULT_PAYER_ACCOUNT,
    initial_balances: dict[str, int] | None = None,
    challenge_window_closed: bool = True,
    contribution_quality_multiplier: float = 1.0,
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
            validate_contribution(receipt)
            amount = contribution_credit_micros(receipt, contribution_quality_multiplier)
        except Exception as exc:
            rejections.append(_rejection(receipt_id, str(exc)))
            continue
        account = receipt["credit_policy"]["credit_account"]
        event = _event(
            f"settle.{receipt_id}.mint",
            "contribution_mint",
            receipt_id,
            account,
            amount,
            receipt["credit_policy"]["credit_basis"],
        )
        events.append(event)
        balances[account] += amount
        total_minted += amount

    for receipt in inference_receipts:
        receipt_id = str(receipt.get("receipt_id", "unknown_inference_receipt"))
        if not challenge_window_closed:
            rejections.append(_rejection(receipt_id, "challenge window is not closed"))
            continue
        report = inference_receipt_report(receipt, node_card, host_advertisement, seen_spend_keys=seen_spend_keys)
        if not report["ok"]:
            rejections.append(_rejection(receipt_id, "; ".join(report["errors"])))
            continue
        spend_key = report["spend_key"]
        if not isinstance(spend_key, str):
            rejections.append(_rejection(receipt_id, "missing spend key"))
            continue
        charge = int(report["credit_charge_micros"])
        host_account = receipt["credit_account"]
        events.append(_event(f"settle.{receipt_id}.debit", "inference_debit", receipt_id, payer_account, -charge, "inference spend"))
        events.append(_event(f"settle.{receipt_id}.host_credit", "inference_host_credit", receipt_id, host_account, charge, "inference work credit"))
        balances[payer_account] -= charge
        balances[host_account] += charge
        total_transferred += charge
        seen_spend_keys.add(spend_key)

    accounts = [
        {"account": account, "balance_micros": balance}
        for account, balance in sorted(balances.items())
    ]
    report = {
        "settlement_version": SETTLEMENT_VERSION,
        "settlement_currency": SETTLEMENT_CURRENCY,
        "challenge_window_closed": challenge_window_closed,
        "contribution_receipt_count": len(contribution_receipts),
        "inference_receipt_count": len(inference_receipts),
        "accepted_event_count": len(events),
        "rejected_event_count": len(rejections),
        "total_minted_micros": total_minted,
        "total_transferred_micros": total_transferred,
        "net_supply_delta_micros": total_minted,
        "accounts": accounts,
        "events": events,
        "rejections": rejections,
        "seen_spend_keys": sorted(seen_spend_keys),
        "ok": not rejections,
    }
    validate_credit_ledger_settlement(report)
    return report


def build_demo_settlement() -> dict[str, Any]:
    node = build_demo_node_card()
    ad = build_demo_host_advertisement(node)
    inference = build_demo_inference_receipt(node, ad)
    growth = build_growth_ledger()
    return settle_credit_ledger(
        contribution_receipts=growth["contributions"],
        inference_receipts=[inference],
        node_card=node,
        host_advertisement=ad,
    )


def demo_report() -> dict[str, Any]:
    node = build_demo_node_card()
    ad = build_demo_host_advertisement(node)
    inference = build_demo_inference_receipt(node, ad)
    growth = build_growth_ledger()
    settlement = settle_credit_ledger(
        contribution_receipts=growth["contributions"],
        inference_receipts=[inference],
        node_card=node,
        host_advertisement=ad,
    )
    return {
        "node_card": node,
        "host_advertisement": ad,
        "contribution_receipts": growth["contributions"],
        "inference_receipts": [inference],
        "settlement": settlement,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Settle AEM contribution and inference receipts into AEM_CREDIT balances")
    parser.add_argument("--check", action="store_true", help="validate demo credit ledger settlement")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    report = demo_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["settlement"]["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
