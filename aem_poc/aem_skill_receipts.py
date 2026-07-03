from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from typing import Any, Sequence

from .schema_validation import SchemaValidationError, validate_data


SKILL_RECEIPT_SCHEMA = "skill_receipt.schema.json"
RECEIPT_VERSION = "2026-07-01.v1"
SETTLEMENT_CURRENCY = "AEM_CREDIT"
REQUIRED_RECEIPTS = {
    "provenance_receipt",
    "skill_execution_receipt",
    "skill_delta_eval_receipt",
    "operator_reality_gate_receipt",
}
REQUIRED_TESTS = {
    "skill_execution_receipt",
    "skill_delta_eval_receipt",
    "operator_reality_gate_receipt",
}
SKILL_TYPES = {
    "prompt_operator",
    "tool_workflow",
    "verification_skill",
    "training_recipe",
    "routing_policy",
    "domain_procedure",
    "data_curation_procedure",
}
DETERMINISM_LEVELS = {"deterministic", "bounded_stochastic", "human_assisted"}
REDACTION_LEVELS = {"public", "redacted", "private_commitment"}
EXPORT_POLICIES = {"open_receipt", "licensed_receipt", "private_commitment"}


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _object(value: Any) -> bool:
    return isinstance(value, dict)


def _non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 1


def _number(value: Any) -> bool:
    return isinstance(value, (int, float))


def _shape_ok(receipt: dict[str, Any]) -> bool:
    required = (
        "receipt_version",
        "skill_receipt_id",
        "contributor_id",
        "contributor_node_id",
        "skill_id",
        "skill_version",
        "title",
        "skill_type",
        "skill_contract",
        "content_commitment",
        "source_policy",
        "execution_evidence",
        "evaluation",
        "credit_policy",
        "anti_distillation",
        "receipt_requirements",
        "verifier_report_refs",
        "signature",
    )
    if not all(key in receipt for key in required):
        return False
    for key in ("receipt_version", "skill_receipt_id", "contributor_id", "contributor_node_id", "skill_id", "skill_version", "title", "signature"):
        if not isinstance(receipt.get(key), str):
            return False
    if receipt.get("skill_type") not in SKILL_TYPES:
        return False
    contract = receipt.get("skill_contract")
    if not _object(contract):
        return False
    for key in ("input_contract", "operation", "output_contract"):
        if not isinstance(contract.get(key), str):
            return False
    if not _str_list(contract.get("required_tools")) or not _str_list(contract.get("runtime_constraints")):
        return False
    if contract.get("determinism_level") not in DETERMINISM_LEVELS:
        return False
    content = receipt.get("content_commitment")
    if not _object(content):
        return False
    if not isinstance(content.get("skill_hash"), str) or not isinstance(content.get("format"), str):
        return False
    if not _positive_int(content.get("size_bytes")):
        return False
    if content.get("redaction_level") not in REDACTION_LEVELS:
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
    execution = receipt.get("execution_evidence")
    if not _object(execution):
        return False
    if not _str_list(execution.get("demo_task_ids")) or not _str_list(execution.get("execution_receipts")):
        return False
    for key in ("before_score", "after_score", "delta_score"):
        if not _number(execution.get(key)):
            return False
    if not _positive_int(execution.get("sample_count")):
        return False
    evaluation = receipt.get("evaluation")
    if not _object(evaluation):
        return False
    if not _str_list(evaluation.get("target_domains")) or not _str_list(evaluation.get("required_tests")):
        return False
    if not isinstance(evaluation.get("measurable_delta"), str):
        return False
    if not _str_list(evaluation.get("adoption_criteria")) or not _str_list(evaluation.get("kill_criteria")):
        return False
    credit = receipt.get("credit_policy")
    if not _object(credit):
        return False
    if credit.get("settlement_currency") != SETTLEMENT_CURRENCY:
        return False
    if not isinstance(credit.get("credit_account"), str) or credit.get("credit_basis") != "verified_skill_use":
        return False
    if not _non_negative_int(credit.get("base_credit_micros")):
        return False
    if not _number(credit.get("quality_multiplier_floor")) or not _number(credit.get("quality_multiplier_cap")):
        return False
    if not isinstance(credit.get("resale_allowed"), bool):
        return False
    anti = receipt.get("anti_distillation")
    if not _object(anti):
        return False
    if not isinstance(anti.get("no_unauthorized_competitor_distillation"), bool):
        return False
    if not isinstance(anti.get("allowed_teacher_policy_required"), bool):
        return False
    if anti.get("export_policy") not in EXPORT_POLICIES:
        return False
    return _str_list(receipt.get("receipt_requirements")) and _str_list(receipt.get("verifier_report_refs"))


def _validate_with_schema_or_shape(receipt: dict[str, Any]) -> None:
    result = validate_data(receipt, SKILL_RECEIPT_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {SKILL_RECEIPT_SCHEMA}",) and _shape_ok(receipt):
        return
    raise SchemaValidationError(f"{SKILL_RECEIPT_SCHEMA} validation failed: {result.errors}")


def build_demo_skill_receipt() -> dict[str, Any]:
    return {
        "receipt_version": RECEIPT_VERSION,
        "skill_receipt_id": "skill.receipt.code_patch_triage.demo.001",
        "contributor_id": "contributor.demo.001",
        "contributor_node_id": "node.argentina.cordoba.7800x3d-rtx5070.demo",
        "skill_id": "skill.code_patch_triage.design.demo",
        "skill_version": "2026-07-01.v1",
        "title": "design code patch triage skill",
        "skill_type": "tool_workflow",
        "skill_contract": {
            "input_contract": "repo snapshot + issue text + failing test command",
            "operation": "classify failure, propose minimal patch, run verifier, emit patch candidate with kill criteria",
            "output_contract": "patch proposal + verifier command + route trace evidence",
            "required_tools": ["python", "unittest", "git_diff_reader"],
            "runtime_constraints": ["stdlib_only", "workspace_limited", "no_network"],
            "determinism_level": "bounded_stochastic",
        },
        "content_commitment": {
            "skill_hash": "sha256:demo_skill_code_patch_triage_hash",
            "format": "markdown+json",
            "size_bytes": 4096,
            "redaction_level": "redacted",
        },
        "source_policy": {
            "origin": "human-authored skill workflow",
            "license": "contributor-owned-aem-network-use",
            "allowed_for_training": True,
            "allowed_for_commercial_use": True,
            "human_authored_or_owned": True,
            "contains_third_party_model_outputs": False,
            "third_party_terms_verified": True,
        },
        "execution_evidence": {
            "demo_task_ids": ["task.code_patch.demo.001", "task.code_patch.demo.002"],
            "execution_receipts": ["skill_execution_receipt.demo.001", "skill_execution_receipt.demo.002"],
            "before_score": 0.40,
            "after_score": 0.70,
            "delta_score": 0.30,
            "sample_count": 2,
        },
        "evaluation": {
            "target_domains": ["code_patch", "repo_debugging", "verification"],
            "required_tests": sorted(REQUIRED_TESTS),
            "measurable_delta": "skill must improve verified patch success rate on demo code_patch tasks",
            "adoption_criteria": ["provenance accepted", "execution receipts present", "delta_score > 0", "verifier report present"],
            "kill_criteria": ["no positive delta", "missing execution receipt", "unauthorized distillation source", "workflow cannot be executed by another node"],
        },
        "credit_policy": {
            "settlement_currency": SETTLEMENT_CURRENCY,
            "credit_account": "aem_credit_account_demo_001",
            "credit_basis": "verified_skill_use",
            "base_credit_micros": 1500,
            "quality_multiplier_floor": 0,
            "quality_multiplier_cap": 5,
            "resale_allowed": True,
        },
        "anti_distillation": {
            "no_unauthorized_competitor_distillation": True,
            "allowed_teacher_policy_required": True,
            "export_policy": "licensed_receipt",
        },
        "receipt_requirements": sorted(REQUIRED_RECEIPTS),
        "verifier_report_refs": ["verifier.skill_delta.demo.001"],
        "signature": "skill_receipt_signature_demo_001",
    }


def validate_skill_receipt(receipt: dict[str, Any]) -> None:
    credit_policy = receipt.get("credit_policy")
    if isinstance(credit_policy, dict) and "credit_basis" in credit_policy and credit_policy["credit_basis"] != "verified_skill_use":
        raise SchemaValidationError("skill credit_basis must be verified_skill_use")
    _validate_with_schema_or_shape(receipt)
    errors: list[str] = []
    source = receipt["source_policy"]
    anti = receipt["anti_distillation"]
    credit = receipt["credit_policy"]
    execution = receipt["execution_evidence"]
    evaluation = receipt["evaluation"]
    requirements = set(receipt["receipt_requirements"])
    required_tests = set(evaluation["required_tests"])
    if not source["allowed_for_training"]:
        errors.append("source_policy.allowed_for_training must be true")
    if not source["human_authored_or_owned"]:
        errors.append("skill source must be human-authored, owned, licensed, or explicitly allowed")
    if source["contains_third_party_model_outputs"] and not source["third_party_terms_verified"]:
        errors.append("third-party model outputs require verified terms")
    if not anti["no_unauthorized_competitor_distillation"]:
        errors.append("anti_distillation must forbid unauthorized competitor distillation")
    if not anti["allowed_teacher_policy_required"]:
        errors.append("allowed teacher policy must be required")
    if credit["settlement_currency"] != SETTLEMENT_CURRENCY:
        errors.append("settlement_currency must be AEM_CREDIT")
    if credit["credit_basis"] != "verified_skill_use":
        errors.append("skill credit_basis must be verified_skill_use")
    if credit["quality_multiplier_cap"] < credit["quality_multiplier_floor"]:
        errors.append("quality multiplier cap must be >= floor")
    missing_requirements = sorted(REQUIRED_RECEIPTS - requirements)
    if missing_requirements:
        errors.append(f"receipt_requirements missing: {missing_requirements}")
    missing_tests = sorted(REQUIRED_TESTS - required_tests)
    if missing_tests:
        errors.append(f"evaluation.required_tests missing: {missing_tests}")
    if execution["delta_score"] <= 0:
        errors.append("execution_evidence.delta_score must be positive")
    if execution["after_score"] < execution["before_score"]:
        errors.append("after_score must be >= before_score")
    if not execution["execution_receipts"]:
        errors.append("execution_evidence.execution_receipts must not be empty")
    if not receipt["verifier_report_refs"]:
        errors.append("verifier_report_refs must not be empty")
    if not evaluation["kill_criteria"]:
        errors.append("kill_criteria must not be empty")
    if errors:
        raise SchemaValidationError("skill_receipt validation failed: " + "; ".join(errors))


def skill_receipt_report(receipt: dict[str, Any]) -> dict[str, Any]:
    try:
        validate_skill_receipt(receipt)
        errors: list[str] = []
    except SchemaValidationError as exc:
        errors = [str(exc)]
    return {
        "ok": not errors,
        "errors": errors,
        "skill_receipt_id": receipt.get("skill_receipt_id"),
        "skill_id": receipt.get("skill_id"),
        "skill_type": receipt.get("skill_type"),
        "credit_account": receipt.get("credit_policy", {}).get("credit_account"),
        "credit_basis": receipt.get("credit_policy", {}).get("credit_basis"),
        "settlement_currency": receipt.get("credit_policy", {}).get("settlement_currency"),
        "delta_score": receipt.get("execution_evidence", {}).get("delta_score"),
        "receipt_requirements": receipt.get("receipt_requirements", []),
    }


def demo_report() -> dict[str, Any]:
    receipt = build_demo_skill_receipt()
    return {"skill_receipt": receipt, "eligibility_report": skill_receipt_report(receipt)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate AEM product-grade SkillReceipt")
    parser.add_argument("--check", action="store_true", help="validate demo SkillReceipt")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    report = demo_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["eligibility_report"]["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
