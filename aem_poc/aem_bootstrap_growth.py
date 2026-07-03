from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from copy import deepcopy
from typing import Any, Sequence

from .schema_validation import SchemaValidationError, validate_data


CONTRIBUTION_SCHEMA = "aem_knowledge_contribution.schema.json"
RECEIPT_VERSION = "2026-07-01.v1"
SETTLEMENT_CURRENCY = "AEM_CREDIT"
REQUIRED_RECEIPTS = {
    "knowledge": {"provenance_receipt", "knowledge_delta_eval_receipt"},
    "skill": {"provenance_receipt", "skill_execution_receipt", "skill_delta_eval_receipt"},
    "data_shard": {"provenance_receipt", "data_quality_receipt"},
    "eval": {"provenance_receipt", "eval_adversarial_receipt"},
    "curriculum": {"provenance_receipt", "curriculum_delta_receipt"},
    "operator": {"provenance_receipt", "operator_reality_gate_receipt"},
}
ALLOWED_CREDIT_BASIS = {
    "accepted_delta",
    "verified_skill_use",
    "eval_improvement",
    "curation_quality",
    "operator_adoption",
}
GROWTH_THIRD = (
    "AEM should not chase frontier models by unauthorized competitor distillation; it should bootstrap from licensed/open/human-owned "
    "knowledge, skills, data shards, evals, curricula, and operators, then pay credits only for verified capability deltas."
)


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _object(value: Any) -> bool:
    return isinstance(value, dict)


def _non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0


def _number_ge(value: Any, floor: float) -> bool:
    return isinstance(value, (int, float)) and value >= floor


def _shape_ok(receipt: dict[str, Any]) -> bool:
    required = (
        "receipt_version",
        "receipt_id",
        "contributor_id",
        "contributor_node_id",
        "contribution_type",
        "title",
        "content_commitment",
        "source_policy",
        "training_use",
        "credit_policy",
        "evaluation",
        "anti_distillation",
        "receipts_required",
        "signature",
    )
    if not all(key in receipt for key in required):
        return False
    for key in ("receipt_version", "receipt_id", "contributor_id", "contributor_node_id", "contribution_type", "title", "signature"):
        if not isinstance(receipt.get(key), str):
            return False
    if receipt["contribution_type"] not in REQUIRED_RECEIPTS:
        return False
    content = receipt.get("content_commitment")
    if not _object(content):
        return False
    if not isinstance(content.get("content_hash"), str) or not isinstance(content.get("format"), str):
        return False
    if not _non_negative_int(content.get("size_bytes")) or content["size_bytes"] < 1:
        return False
    if content.get("redaction_level") not in {"public", "redacted", "private_commitment"}:
        return False
    source = receipt.get("source_policy")
    if not _object(source):
        return False
    for key in ("origin", "license"):
        if not isinstance(source.get(key), str):
            return False
    for key in ("allowed_for_training", "allowed_for_commercial_use", "human_authored_or_owned", "contains_third_party_model_outputs", "third_party_terms_verified"):
        if not isinstance(source.get(key), bool):
            return False
    training = receipt.get("training_use")
    if not _object(training):
        return False
    if not _str_list(training.get("target_domains")) or not _str_list(training.get("allowed_uses")) or not _str_list(training.get("forbidden_uses")):
        return False
    if training.get("bootstrap_stage") not in {"seed", "expert_refinement", "router_training", "eval_hardening", "distillation_memory"}:
        return False
    credit = receipt.get("credit_policy")
    if not _object(credit):
        return False
    if credit.get("settlement_currency") != SETTLEMENT_CURRENCY:
        return False
    if not isinstance(credit.get("credit_account"), str):
        return False
    if credit.get("credit_basis") not in ALLOWED_CREDIT_BASIS:
        return False
    if not _non_negative_int(credit.get("base_credit_micros")):
        return False
    if not _number_ge(credit.get("quality_multiplier_floor"), 0) or not _number_ge(credit.get("quality_multiplier_cap"), 0):
        return False
    if not isinstance(credit.get("resale_allowed"), bool):
        return False
    evaluation = receipt.get("evaluation")
    if not _object(evaluation):
        return False
    if not _str_list(evaluation.get("required_tests")) or not isinstance(evaluation.get("measurable_delta"), str):
        return False
    if not _str_list(evaluation.get("adoption_criteria")) or not _str_list(evaluation.get("kill_criteria")):
        return False
    anti = receipt.get("anti_distillation")
    if not _object(anti):
        return False
    if not isinstance(anti.get("no_unauthorized_competitor_distillation"), bool):
        return False
    if not isinstance(anti.get("allowed_teacher_policy_required"), bool):
        return False
    if anti.get("export_policy") not in {"open_receipt", "licensed_receipt", "private_commitment"}:
        return False
    return _str_list(receipt.get("receipts_required"))


def _validate_with_schema_or_shape(receipt: dict[str, Any]) -> None:
    result = validate_data(receipt, CONTRIBUTION_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {CONTRIBUTION_SCHEMA}",) and _shape_ok(receipt):
        return
    raise SchemaValidationError(f"{CONTRIBUTION_SCHEMA} validation failed: {result.errors}")


def build_demo_contribution(contribution_type: str = "skill") -> dict[str, Any]:
    if contribution_type not in REQUIRED_RECEIPTS:
        raise ValueError(f"unknown contribution_type: {contribution_type}")
    basis_by_type = {
        "knowledge": "accepted_delta",
        "skill": "verified_skill_use",
        "data_shard": "curation_quality",
        "eval": "eval_improvement",
        "curriculum": "accepted_delta",
        "operator": "operator_adoption",
    }
    stage_by_type = {
        "knowledge": "seed",
        "skill": "expert_refinement",
        "data_shard": "seed",
        "eval": "eval_hardening",
        "curriculum": "router_training",
        "operator": "distillation_memory",
    }
    return {
        "receipt_version": RECEIPT_VERSION,
        "receipt_id": f"contrib.{contribution_type}.demo.001",
        "contributor_id": "contributor.demo.001",
        "contributor_node_id": "node.argentina.cordoba.7800x3d-rtx5070.demo",
        "contribution_type": contribution_type,
        "title": f"Demo {contribution_type} contribution",
        "content_commitment": {
            "content_hash": f"sha256:demo_{contribution_type}_hash",
            "format": "jsonl+markdown",
            "size_bytes": 2048,
            "redaction_level": "redacted",
        },
        "source_policy": {
            "origin": "human-authored contributor packet",
            "license": "contributor-owned-aem-network-use",
            "allowed_for_training": True,
            "allowed_for_commercial_use": True,
            "human_authored_or_owned": True,
            "contains_third_party_model_outputs": False,
            "third_party_terms_verified": True,
        },
        "training_use": {
            "target_domains": ["code_patch", "network_economy", "verification"],
            "allowed_uses": ["expert_refinement", "router_training", "eval_hardening"],
            "forbidden_uses": ["unauthorized_competitor_distillation", "terms_violating_teacher_extraction"],
            "bootstrap_stage": stage_by_type[contribution_type],
        },
        "credit_policy": {
            "settlement_currency": SETTLEMENT_CURRENCY,
            "credit_account": "aem_credit_account_demo_001",
            "credit_basis": basis_by_type[contribution_type],
            "base_credit_micros": 1000,
            "quality_multiplier_floor": 0,
            "quality_multiplier_cap": 5,
            "resale_allowed": True,
        },
        "evaluation": {
            "required_tests": sorted(REQUIRED_RECEIPTS[contribution_type]),
            "measurable_delta": "accepted contribution must improve routing, expert behavior, eval hardness, or operator adoption",
            "adoption_criteria": ["provenance accepted", "required receipts present", "delta test passes"],
            "kill_criteria": ["provenance missing", "no measurable delta", "terms-violating third-party output"],
        },
        "anti_distillation": {
            "no_unauthorized_competitor_distillation": True,
            "allowed_teacher_policy_required": True,
            "export_policy": "licensed_receipt",
        },
        "receipts_required": sorted(REQUIRED_RECEIPTS[contribution_type]),
        "signature": f"contribution_signature_{contribution_type}_demo_001",
    }


def validate_contribution(receipt: dict[str, Any]) -> None:
    _validate_with_schema_or_shape(receipt)
    errors: list[str] = []
    ctype = receipt["contribution_type"]
    source = receipt["source_policy"]
    credit = receipt["credit_policy"]
    evaluation = receipt["evaluation"]
    anti = receipt["anti_distillation"]
    receipts = set(receipt["receipts_required"])
    required = REQUIRED_RECEIPTS[ctype]
    if not source["allowed_for_training"]:
        errors.append("source_policy.allowed_for_training must be true")
    if not source["human_authored_or_owned"]:
        errors.append("source must be human-authored, owned, licensed, or explicitly allowed")
    if source["contains_third_party_model_outputs"] and not source["third_party_terms_verified"]:
        errors.append("third-party model outputs require verified terms")
    if not anti["no_unauthorized_competitor_distillation"]:
        errors.append("anti_distillation must forbid unauthorized competitor distillation")
    if not anti["allowed_teacher_policy_required"]:
        errors.append("allowed teacher policy must be required for distillation memory")
    if credit["settlement_currency"] != SETTLEMENT_CURRENCY:
        errors.append("settlement_currency must be AEM_CREDIT")
    if credit["credit_basis"] not in ALLOWED_CREDIT_BASIS:
        errors.append("credit_basis must be capability-delta based")
    if credit["quality_multiplier_cap"] < credit["quality_multiplier_floor"]:
        errors.append("quality multiplier cap must be >= floor")
    missing = sorted(required - receipts)
    if missing:
        errors.append(f"receipts_required missing: {missing}")
    tests = set(evaluation["required_tests"])
    if not required.issubset(tests):
        errors.append("evaluation.required_tests must include all required receipts")
    if not evaluation["kill_criteria"]:
        errors.append("kill_criteria must not be empty")
    if errors:
        raise SchemaValidationError("knowledge contribution validation failed: " + "; ".join(errors))


def contribution_report(receipt: dict[str, Any]) -> dict[str, Any]:
    try:
        validate_contribution(receipt)
        errors: list[str] = []
    except SchemaValidationError as exc:
        errors = [str(exc)]
    return {
        "ok": not errors,
        "errors": errors,
        "receipt_id": receipt.get("receipt_id"),
        "contribution_type": receipt.get("contribution_type"),
        "credit_account": receipt.get("credit_policy", {}).get("credit_account"),
        "credit_basis": receipt.get("credit_policy", {}).get("credit_basis"),
        "settlement_currency": receipt.get("credit_policy", {}).get("settlement_currency"),
        "receipts_required": receipt.get("receipts_required", []),
    }


def build_growth_ledger() -> dict[str, Any]:
    contributions = [build_demo_contribution(kind) for kind in sorted(REQUIRED_RECEIPTS)]
    for contribution in contributions:
        validate_contribution(contribution)
    counts = Counter(item["contribution_type"] for item in contributions)
    return {
        "ledger_version": RECEIPT_VERSION,
        "growth_third": GROWTH_THIRD,
        "contribution_count": len(contributions),
        "contribution_type_counts": dict(sorted(counts.items())),
        "credit_settlement_currency": SETTLEMENT_CURRENCY,
        "forbidden_reductions": [
            "unauthorized competitor distillation",
            "raw data upload as credit basis",
            "credit minting without provenance receipt",
            "skill claim without execution receipt",
        ],
        "contributions": contributions,
    }


def demo_report() -> dict[str, Any]:
    ledger = build_growth_ledger()
    return {
        "growth_third": GROWTH_THIRD,
        "ledger": ledger,
        "reports": [contribution_report(item) for item in ledger["contributions"]],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate AEM bootstrap growth contribution receipts")
    parser.add_argument("--check", action="store_true", help="validate demo bootstrap growth ledger")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    report = demo_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if all(item["ok"] for item in report["reports"]) else 1


if __name__ == "__main__":
    sys.exit(main())
