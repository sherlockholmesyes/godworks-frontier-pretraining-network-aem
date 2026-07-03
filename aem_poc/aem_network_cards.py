from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from typing import Any, Sequence

from .schema_validation import SchemaValidationError, validate_data


NODE_CARD_SCHEMA = "node_card.schema.json"
HOST_ADVERTISEMENT_SCHEMA = "host_advertisement.schema.json"
CARD_VERSION = "2026-07-01.v1"
RECEIPT_BY_ROLE = {
    "inference": "inference_work_receipt",
    "training": "training_work_receipt",
    "verification": "verification_receipt",
}
RATE_BY_ROLE = {
    "inference": "inference_credit_rate_micros",
    "training": "training_credit_rate_micros",
    "verification": "verification_credit_rate_micros",
}
MIN_RATE_BY_ROLE = {
    "inference": "min_inference_credit_rate_micros",
    "training": "min_training_credit_rate_micros",
    "verification": "min_verification_credit_rate_micros",
}
ALLOWED_ROLES = set(RECEIPT_BY_ROLE)


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _int_ge(value: Any, floor: int) -> bool:
    return isinstance(value, int) and value >= floor


def _object(value: Any) -> bool:
    return isinstance(value, dict)


def _validate_with_schema_or_shape(data: dict[str, Any], schema_name: str, shape_ok: bool) -> None:
    result = validate_data(data, schema_name)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {schema_name}",) and shape_ok:
        return
    raise SchemaValidationError(f"{schema_name} validation failed: {result.errors}")


def _node_card_shape_ok(card: dict[str, Any]) -> bool:
    required = (
        "card_version",
        "node_id",
        "owner_key",
        "signature",
        "locality",
        "capacity",
        "economic_policy",
        "host_policy",
        "available_roles",
        "advertised_experts",
        "receipts_required",
    )
    if not all(key in card for key in required):
        return False
    for key in ("card_version", "node_id", "owner_key", "signature"):
        if not isinstance(card.get(key), str):
            return False
    locality = card.get("locality")
    if not _object(locality):
        return False
    if not isinstance(locality.get("bucket"), str) or not isinstance(locality.get("jurisdiction_hint"), str):
        return False
    if not isinstance(locality.get("exact_location_disclosed"), bool):
        return False
    capacity = card.get("capacity")
    if not _object(capacity):
        return False
    for key, floor in (
        ("gpu_count", 0),
        ("gpu_vram_gb", 0),
        ("ram_gb", 1),
        ("bandwidth_mbps", 1),
        ("max_concurrent_jobs", 1),
        ("uptime_window_hours", 1),
    ):
        if not _int_ge(capacity.get(key), floor):
            return False
    if not isinstance(capacity.get("compute_class"), str):
        return False
    economic = card.get("economic_policy")
    if not _object(economic):
        return False
    if not isinstance(economic.get("credit_account"), str) or economic.get("settlement_currency") != "AEM_CREDIT":
        return False
    if not isinstance(economic.get("resale_allowed"), bool):
        return False
    if not _str_list(economic.get("earning_roles")) or not set(economic["earning_roles"]).issubset(ALLOWED_ROLES):
        return False
    for key in (*MIN_RATE_BY_ROLE.values(), "collateral_required_micros"):
        if not _int_ge(economic.get(key), 0):
            return False
    policy = card.get("host_policy")
    if not _object(policy):
        return False
    if not _str_list(policy.get("accepted_task_classes")) or not _str_list(policy.get("rejected_task_classes")):
        return False
    if policy.get("max_prompt_privacy_class") not in {"public", "redacted", "private_prohibited"}:
        return False
    if not _str_list(policy.get("sandbox_profiles")):
        return False
    if not _str_list(card.get("available_roles")) or not set(card["available_roles"]).issubset(ALLOWED_ROLES):
        return False
    return _str_list(card.get("advertised_experts")) and _str_list(card.get("receipts_required"))


def _host_ad_shape_ok(advertisement: dict[str, Any]) -> bool:
    required = (
        "advertisement_version",
        "advertisement_id",
        "node_id",
        "expert_id",
        "expert_card_hash",
        "locality_bucket",
        "expires_at",
        "offer",
        "availability",
        "policy",
        "receipt_requirements",
        "signature",
    )
    if not all(key in advertisement for key in required):
        return False
    for key in ("advertisement_version", "advertisement_id", "node_id", "expert_id", "expert_card_hash", "locality_bucket", "expires_at", "signature"):
        if not isinstance(advertisement.get(key), str):
            return False
    offer = advertisement.get("offer")
    if not _object(offer):
        return False
    if not _str_list(offer.get("roles")) or not set(offer["roles"]).issubset(ALLOWED_ROLES):
        return False
    if offer.get("accepted_payment") != ["AEM_CREDIT"]:
        return False
    for key in (*RATE_BY_ROLE.values(), "min_job_credits_micros"):
        if not _int_ge(offer.get(key), 0):
            return False
    availability = advertisement.get("availability")
    if not _object(availability):
        return False
    if not isinstance(availability.get("capacity_class"), str) or not isinstance(availability.get("endpoint_hint"), str):
        return False
    for key in ("max_concurrent_jobs", "uptime_window_hours"):
        if not _int_ge(availability.get(key), 1):
            return False
    policy = advertisement.get("policy")
    if not _object(policy):
        return False
    if not _str_list(policy.get("accepted_task_classes")):
        return False
    if policy.get("max_prompt_privacy_class") not in {"public", "redacted", "private_prohibited"}:
        return False
    if not isinstance(policy.get("sandbox_profile"), str):
        return False
    return _str_list(advertisement.get("receipt_requirements"))


def required_receipts_for_roles(roles: Sequence[str]) -> set[str]:
    return {RECEIPT_BY_ROLE[role] for role in roles}


def build_demo_node_card() -> dict[str, Any]:
    return {
        "card_version": CARD_VERSION,
        "node_id": "node.argentina.cordoba.7800x3d-rtx5070.demo",
        "owner_key": "owner_pubkey_demo_001",
        "signature": "node_signature_demo_001",
        "locality": {
            "bucket": "sa-east-privacy-bucket-001",
            "jurisdiction_hint": "AR",
            "exact_location_disclosed": False,
        },
        "capacity": {
            "compute_class": "consumer_gpu_12gb",
            "gpu_count": 1,
            "gpu_vram_gb": 12,
            "ram_gb": 32,
            "bandwidth_mbps": 100,
            "max_concurrent_jobs": 2,
            "uptime_window_hours": 12,
        },
        "economic_policy": {
            "credit_account": "aem_credit_account_demo_001",
            "settlement_currency": "AEM_CREDIT",
            "earning_roles": ["inference", "training", "verification"],
            "min_inference_credit_rate_micros": 100,
            "min_training_credit_rate_micros": 500,
            "min_verification_credit_rate_micros": 50,
            "collateral_required_micros": 1000,
            "resale_allowed": True,
        },
        "host_policy": {
            "accepted_task_classes": ["code_patch", "verification", "small_adapter_training"],
            "rejected_task_classes": ["private_prompt_unredacted"],
            "max_prompt_privacy_class": "redacted",
            "sandbox_profiles": ["stdlib_no_network", "workspace_limited"],
        },
        "available_roles": ["inference", "training", "verification"],
        "advertised_experts": ["expert.code_patch.local.demo"],
        "receipts_required": [
            "capacity_probe_receipt",
            "inference_work_receipt",
            "training_work_receipt",
            "verification_receipt",
        ],
    }


def build_demo_host_advertisement(node_card: dict[str, Any] | None = None) -> dict[str, Any]:
    node = node_card or build_demo_node_card()
    return {
        "advertisement_version": CARD_VERSION,
        "advertisement_id": "host_ad.demo.001",
        "node_id": node["node_id"],
        "expert_id": "expert.code_patch.local.demo",
        "expert_card_hash": "sha256:demo_expert_card_hash",
        "locality_bucket": node["locality"]["bucket"],
        "expires_at": "2026-07-01T01:00:00Z",
        "offer": {
            "roles": ["inference", "verification"],
            "accepted_payment": ["AEM_CREDIT"],
            "inference_credit_rate_micros": 150,
            "training_credit_rate_micros": 0,
            "verification_credit_rate_micros": 75,
            "min_job_credits_micros": 100,
        },
        "availability": {
            "capacity_class": node["capacity"]["compute_class"],
            "max_concurrent_jobs": 1,
            "endpoint_hint": "local-relay://demo-node/expert.code_patch.local.demo",
            "uptime_window_hours": 6,
        },
        "policy": {
            "accepted_task_classes": ["code_patch", "verification"],
            "max_prompt_privacy_class": "redacted",
            "sandbox_profile": "stdlib_no_network",
        },
        "receipt_requirements": ["inference_work_receipt", "verification_receipt", "route_trace_receipt"],
        "signature": "host_ad_signature_demo_001",
    }


def validate_node_card(card: dict[str, Any]) -> None:
    _validate_with_schema_or_shape(card, NODE_CARD_SCHEMA, _node_card_shape_ok(card))
    errors: list[str] = []
    roles = set(card["economic_policy"]["earning_roles"])
    available_roles = set(card["available_roles"])
    receipts = set(card["receipts_required"])
    if not roles:
        errors.append("economic_policy.earning_roles must not be empty")
    if not roles.issubset(available_roles):
        errors.append("earning_roles must be subset of available_roles")
    required = required_receipts_for_roles(sorted(roles))
    missing = sorted(required - receipts)
    if missing:
        errors.append(f"receipts_required missing role receipts: {missing}")
    if "capacity_probe_receipt" not in receipts:
        errors.append("receipts_required must include capacity_probe_receipt")
    if card["capacity"]["gpu_count"] > 0 and card["capacity"]["gpu_vram_gb"] <= 0:
        errors.append("gpu_vram_gb must be positive when gpu_count > 0")
    if errors:
        raise SchemaValidationError("node_card validation failed: " + "; ".join(errors))


def host_advertisement_report(advertisement: dict[str, Any], node_card: dict[str, Any]) -> dict[str, Any]:
    validate_node_card(node_card)
    _validate_with_schema_or_shape(advertisement, HOST_ADVERTISEMENT_SCHEMA, _host_ad_shape_ok(advertisement))
    errors: list[str] = []
    roles = set(advertisement["offer"]["roles"])
    node_roles = set(node_card["available_roles"])
    earning_roles = set(node_card["economic_policy"]["earning_roles"])
    if not roles:
        errors.append("offer.roles must not be empty")
    if advertisement["node_id"] != node_card["node_id"]:
        errors.append("advertisement.node_id must match node_card.node_id")
    if advertisement["locality_bucket"] != node_card["locality"]["bucket"]:
        errors.append("advertisement.locality_bucket must match node_card locality bucket")
    if advertisement["expert_id"] not in set(node_card["advertised_experts"]):
        errors.append("advertised expert_id must be listed in node_card.advertised_experts")
    if not roles.issubset(node_roles):
        errors.append("offer.roles must be subset of node_card.available_roles")
    if not roles.issubset(earning_roles):
        errors.append("offer.roles must be subset of economic_policy.earning_roles")
    receipts = set(advertisement["receipt_requirements"])
    missing_receipts = sorted(required_receipts_for_roles(sorted(roles)) - receipts)
    if missing_receipts:
        errors.append(f"receipt_requirements missing role receipts: {missing_receipts}")
    if "AEM_CREDIT" not in advertisement["offer"]["accepted_payment"]:
        errors.append("offer.accepted_payment must include AEM_CREDIT")
    for role in roles:
        offer_rate = advertisement["offer"][RATE_BY_ROLE[role]]
        min_rate = node_card["economic_policy"][MIN_RATE_BY_ROLE[role]]
        if offer_rate < min_rate:
            errors.append(f"{role} offer rate below node minimum")
    if advertisement["availability"]["max_concurrent_jobs"] > node_card["capacity"]["max_concurrent_jobs"]:
        errors.append("advertisement concurrency exceeds node capacity")
    accepted = set(advertisement["policy"]["accepted_task_classes"])
    node_accepted = set(node_card["host_policy"]["accepted_task_classes"])
    if not accepted.issubset(node_accepted):
        errors.append("advertisement task classes must be subset of node accepted task classes")
    if advertisement["policy"]["sandbox_profile"] not in set(node_card["host_policy"]["sandbox_profiles"]):
        errors.append("advertisement sandbox_profile must be offered by node")
    return {
        "ok": not errors,
        "errors": errors,
        "node_id": advertisement.get("node_id"),
        "expert_id": advertisement.get("expert_id"),
        "roles": sorted(roles),
        "credit_account": node_card["economic_policy"]["credit_account"],
        "settlement_currency": node_card["economic_policy"]["settlement_currency"],
        "receipts_required": sorted(receipts),
    }


def validate_host_advertisement(advertisement: dict[str, Any], node_card: dict[str, Any]) -> None:
    report = host_advertisement_report(advertisement, node_card)
    if not report["ok"]:
        raise SchemaValidationError("host_advertisement validation failed: " + "; ".join(report["errors"]))


def demo_report() -> dict[str, Any]:
    node = build_demo_node_card()
    advertisement = build_demo_host_advertisement(node)
    report = host_advertisement_report(advertisement, node)
    return {"node_card": node, "host_advertisement": advertisement, "eligibility_report": report}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate AEM NodeCard and HostAdvertisement economy foundation")
    parser.add_argument("--check", action="store_true", help="validate demo NodeCard and HostAdvertisement")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    report = demo_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["eligibility_report"]["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
