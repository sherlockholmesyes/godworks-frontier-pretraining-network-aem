from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from .aem_network_cards import build_demo_host_advertisement, build_demo_node_card, host_advertisement_report
from .schema_validation import SchemaValidationError, validate_data


RECEIPT_SCHEMA = "inference_work_receipt.schema.json"
RECEIPT_VERSION = "2026-07-01.v1"
SETTLEMENT_CURRENCY = "AEM_CREDIT"
REQUIRED_CHALLENGE_METHODS = {"output_commitment_open", "route_trace_replay", "metered_cost_audit", "expert_hash_check"}
REQUIRED_POLICY_RECEIPTS = {"inference_work_receipt", "route_trace_receipt"}


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _object(value: Any) -> bool:
    return isinstance(value, dict)


def _non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 1


def _shape_ok(receipt: dict[str, Any]) -> bool:
    required = (
        "receipt_version",
        "receipt_id",
        "task_hash",
        "task_class",
        "expert_id",
        "expert_card_hash",
        "node_id",
        "host_advertisement_id",
        "credit_account",
        "settlement_currency",
        "credit_charge_micros",
        "work",
        "commitments",
        "challenge_surface",
        "duplicate_spend",
        "policy",
        "signature",
    )
    if not all(key in receipt for key in required):
        return False
    for key in ("receipt_version", "receipt_id", "task_hash", "task_class", "expert_id", "expert_card_hash", "node_id", "host_advertisement_id", "credit_account", "settlement_currency", "signature"):
        if not isinstance(receipt.get(key), str):
            return False
    if not _non_negative_int(receipt.get("credit_charge_micros")):
        return False
    work = receipt.get("work")
    if not _object(work):
        return False
    for key in ("input_tokens", "output_tokens", "metered_cost_micros"):
        if not _non_negative_int(work.get(key)):
            return False
    if not _positive_int(work.get("wall_time_ms")):
        return False
    if not isinstance(work.get("started_at"), str) or not isinstance(work.get("completed_at"), str):
        return False
    commitments = receipt.get("commitments")
    if not _object(commitments):
        return False
    for key in ("prompt_commitment", "output_commitment", "route_trace_id", "nonce"):
        if not isinstance(commitments.get(key), str):
            return False
    challenge = receipt.get("challenge_surface")
    if not _object(challenge):
        return False
    if not _positive_int(challenge.get("challenge_window_seconds")):
        return False
    if not _str_list(challenge.get("challenge_methods")) or not set(challenge["challenge_methods"]).issubset(REQUIRED_CHALLENGE_METHODS):
        return False
    if not isinstance(challenge.get("replay_material_commitment"), str) or not isinstance(challenge.get("sample_seed_commitment"), str):
        return False
    if not _str_list(challenge.get("verifier_set")):
        return False
    duplicate = receipt.get("duplicate_spend")
    if not _object(duplicate):
        return False
    if not isinstance(duplicate.get("spend_key"), str) or not isinstance(duplicate.get("idempotency_key"), str):
        return False
    if duplicate.get("spend_scope") not in {"task_expert_node_nonce", "route_trace_nonce"}:
        return False
    if duplicate.get("previous_receipt") is not None and not isinstance(duplicate.get("previous_receipt"), str):
        return False
    policy = receipt.get("policy")
    if not _object(policy):
        return False
    if policy.get("privacy_class") not in {"public", "redacted", "private_prohibited"}:
        return False
    if not isinstance(policy.get("sandbox_profile"), str) or not isinstance(policy.get("allowed_for_credit"), bool):
        return False
    return _str_list(policy.get("receipt_requirements"))


def _validate_with_schema_or_shape(receipt: dict[str, Any]) -> None:
    result = validate_data(receipt, RECEIPT_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {RECEIPT_SCHEMA}",) and _shape_ok(receipt):
        return
    raise SchemaValidationError(f"{RECEIPT_SCHEMA} validation failed: {result.errors}")


def build_spend_key(task_hash: str, expert_id: str, node_id: str, nonce: str) -> str:
    return f"{task_hash}|{expert_id}|{node_id}|{nonce}"


def expected_credit_charge_micros(receipt: dict[str, Any], host_advertisement: dict[str, Any]) -> int:
    tokens = receipt["work"]["input_tokens"] + receipt["work"]["output_tokens"]
    rate = host_advertisement["offer"]["inference_credit_rate_micros"]
    min_job = host_advertisement["offer"]["min_job_credits_micros"]
    return max(min_job, tokens * rate)


def build_demo_inference_receipt(
    node_card: dict[str, Any] | None = None,
    host_advertisement: dict[str, Any] | None = None,
) -> dict[str, Any]:
    node = node_card or build_demo_node_card()
    ad = host_advertisement or build_demo_host_advertisement(node)
    nonce = "nonce.demo.001"
    task_hash = "sha256:demo_task_hash"
    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "receipt_id": "inference.receipt.demo.001",
        "task_hash": task_hash,
        "task_class": "code_patch",
        "expert_id": ad["expert_id"],
        "expert_card_hash": ad["expert_card_hash"],
        "node_id": node["node_id"],
        "host_advertisement_id": ad["advertisement_id"],
        "credit_account": node["economic_policy"]["credit_account"],
        "settlement_currency": SETTLEMENT_CURRENCY,
        "credit_charge_micros": 3000,
        "work": {
            "input_tokens": 12,
            "output_tokens": 8,
            "wall_time_ms": 1200,
            "metered_cost_micros": 2800,
            "started_at": "2026-07-01T00:00:00Z",
            "completed_at": "2026-07-01T00:00:01Z",
        },
        "commitments": {
            "prompt_commitment": "sha256:demo_prompt_commitment",
            "output_commitment": "sha256:demo_output_commitment",
            "route_trace_id": "route_trace.demo.001",
            "nonce": nonce,
        },
        "challenge_surface": {
            "challenge_window_seconds": 3600,
            "challenge_methods": sorted(REQUIRED_CHALLENGE_METHODS),
            "replay_material_commitment": "sha256:demo_replay_material",
            "sample_seed_commitment": "sha256:demo_sample_seed",
            "verifier_set": ["verifier.local.demo"],
        },
        "duplicate_spend": {
            "spend_key": build_spend_key(task_hash, ad["expert_id"], node["node_id"], nonce),
            "spend_scope": "task_expert_node_nonce",
            "previous_receipt": None,
            "idempotency_key": "idem.demo.001",
        },
        "policy": {
            "privacy_class": "redacted",
            "sandbox_profile": "stdlib_no_network",
            "allowed_for_credit": True,
            "receipt_requirements": ["inference_work_receipt", "route_trace_receipt"],
        },
        "signature": "inference_receipt_signature_demo_001",
    }
    receipt["credit_charge_micros"] = expected_credit_charge_micros(receipt, ad)
    return receipt


def inference_receipt_report(
    receipt: dict[str, Any],
    node_card: dict[str, Any],
    host_advertisement: dict[str, Any],
    *,
    seen_spend_keys: set[str] | None = None,
) -> dict[str, Any]:
    seen = seen_spend_keys or set()
    host_report = host_advertisement_report(host_advertisement, node_card)
    errors: list[str] = []
    if not host_report["ok"]:
        errors.extend(f"host_advertisement: {error}" for error in host_report["errors"])
    try:
        _validate_with_schema_or_shape(receipt)
    except SchemaValidationError as exc:
        errors.append(str(exc))
        return {"ok": False, "errors": errors, "receipt_id": receipt.get("receipt_id"), "spend_key": None, "credit_charge_micros": receipt.get("credit_charge_micros")}
    if receipt["settlement_currency"] != SETTLEMENT_CURRENCY:
        errors.append("settlement_currency must be AEM_CREDIT")
    if receipt["credit_account"] != node_card["economic_policy"]["credit_account"]:
        errors.append("credit_account must match NodeCard economic account")
    if receipt["node_id"] != node_card["node_id"]:
        errors.append("node_id must match NodeCard")
    if receipt["host_advertisement_id"] != host_advertisement["advertisement_id"]:
        errors.append("host_advertisement_id must match HostAdvertisement")
    if receipt["expert_id"] != host_advertisement["expert_id"]:
        errors.append("expert_id must match HostAdvertisement")
    if receipt["task_class"] not in set(host_advertisement["policy"]["accepted_task_classes"]):
        errors.append("task_class must be accepted by HostAdvertisement policy")
    if receipt["policy"]["sandbox_profile"] != host_advertisement["policy"]["sandbox_profile"]:
        errors.append("sandbox_profile must match HostAdvertisement")
    if not receipt["policy"]["allowed_for_credit"]:
        errors.append("policy.allowed_for_credit must be true")
    missing_policy_receipts = sorted(REQUIRED_POLICY_RECEIPTS - set(receipt["policy"]["receipt_requirements"]))
    if missing_policy_receipts:
        errors.append(f"policy receipt requirements missing: {missing_policy_receipts}")
    missing_challenges = sorted(REQUIRED_CHALLENGE_METHODS - set(receipt["challenge_surface"]["challenge_methods"]))
    if missing_challenges:
        errors.append(f"challenge methods missing: {missing_challenges}")
    if not receipt["challenge_surface"]["verifier_set"]:
        errors.append("challenge_surface.verifier_set must not be empty")
    expected_spend_key = build_spend_key(
        receipt["task_hash"],
        receipt["expert_id"],
        receipt["node_id"],
        receipt["commitments"]["nonce"],
    )
    if receipt["duplicate_spend"]["spend_key"] != expected_spend_key:
        errors.append("duplicate_spend.spend_key does not match task/expert/node/nonce binding")
    if receipt["duplicate_spend"]["spend_key"] in seen:
        errors.append("duplicate spend key already seen")
    expected_charge = expected_credit_charge_micros(receipt, host_advertisement)
    if receipt["credit_charge_micros"] != expected_charge:
        errors.append("credit_charge_micros must match host advertisement rate")
    if receipt["work"]["metered_cost_micros"] > receipt["credit_charge_micros"]:
        errors.append("metered_cost_micros cannot exceed charged credits")
    return {
        "ok": not errors,
        "errors": errors,
        "receipt_id": receipt["receipt_id"],
        "spend_key": receipt["duplicate_spend"]["spend_key"],
        "credit_charge_micros": receipt["credit_charge_micros"],
        "expected_credit_charge_micros": expected_charge,
        "challenge_methods": receipt["challenge_surface"]["challenge_methods"],
    }


def validate_inference_receipt(
    receipt: dict[str, Any],
    node_card: dict[str, Any],
    host_advertisement: dict[str, Any],
    *,
    seen_spend_keys: set[str] | None = None,
) -> None:
    report = inference_receipt_report(receipt, node_card, host_advertisement, seen_spend_keys=seen_spend_keys)
    if not report["ok"]:
        raise SchemaValidationError("inference_work_receipt validation failed: " + "; ".join(report["errors"]))


def demo_report() -> dict[str, Any]:
    node = build_demo_node_card()
    ad = build_demo_host_advertisement(node)
    receipt = build_demo_inference_receipt(node, ad)
    report = inference_receipt_report(receipt, node, ad)
    return {"node_card": node, "host_advertisement": ad, "inference_work_receipt": receipt, "eligibility_report": report}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate AEM InferenceWorkReceipt duplicate-spend and challenge surface")
    parser.add_argument("--check", action="store_true", help="validate demo inference work receipt")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    report = demo_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["eligibility_report"]["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
