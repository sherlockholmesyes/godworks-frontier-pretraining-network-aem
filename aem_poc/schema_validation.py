from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class SchemaValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    mode: str
    errors: tuple[str, ...]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _require(data: dict[str, Any], keys: tuple[str, ...], errors: list[str]) -> None:
    for key in keys:
        if key not in data:
            errors.append(f"missing required key: {key}")


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 1


def _non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0


def _dict_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, dict) for item in value)


def _hash64(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64


def _hash64_or_none(value: Any) -> bool:
    return value is None or _hash64(value)


def _artifact_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("path"), str):
            return False
        if not isinstance(item.get("exists"), bool):
            return False
        if not _non_negative_int(item.get("size_bytes")):
            return False
    return True


def _bundle_artifact_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("path"), str):
            return False
        if not _non_negative_int(item.get("size_bytes")):
            return False
        if not _hash64(item.get("sha256")):
            return False
    return True


def _verify_check_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        for key in ("recorded_path", "resolved_path"):
            if not isinstance(item.get(key), str):
                return False
        for key in ("exists", "size_ok", "hash_ok", "ok"):
            if not isinstance(item.get(key), bool):
                return False
        for key in ("expected_size_bytes", "actual_size_bytes"):
            if not _non_negative_int(item.get(key)):
                return False
        if not _hash64(item.get("expected_sha256")):
            return False
        if not _hash64_or_none(item.get("actual_sha256")):
            return False
    return True


def _artifact_index_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    required = ("path", "producer", "schema", "verifier", "purpose", "seal_stage", "role")
    for item in value:
        if not isinstance(item, dict):
            return False
        for key in required:
            if not isinstance(item.get(key), str):
                return False
    return True


def _object(value: Any) -> bool:
    return isinstance(value, dict)


def structural_validate(schema_name: str, data: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []

    if schema_name == "task_packet.schema.json":
        _require(data, ("task_id", "task_type", "prompt"), errors)
        for key in ("task_id", "task_type", "prompt"):
            if key in data and not isinstance(data[key], str):
                errors.append(f"{key} must be string")
        constraints = data.get("constraints", {})
        if constraints is not None and not isinstance(constraints, dict):
            errors.append("constraints must be object")
        if isinstance(constraints, dict):
            backend = constraints.get("patch_backend")
            if backend is not None and backend not in {"stdlib_one_file", "auto", "external"}:
                errors.append("patch_backend invalid")
            for key in ("allowed_files", "blocked_prefixes", "test_command"):
                if key in constraints and not _str_list(constraints[key]):
                    errors.append(f"{key} must be list[str]")
            for key in ("max_patch_bytes", "max_changed_files"):
                if key in constraints and not _positive_int(constraints[key]):
                    errors.append(f"{key} must be positive int")

    elif schema_name == "expert_card.schema.json":
        _require(
            data,
            (
                "expert_id",
                "base_model_hash",
                "expert_type",
                "quantization",
                "vram_min_gb",
                "training_objective",
                "domains",
                "eval_delta",
                "license",
                "signature",
            ),
            errors,
        )
        if "domains" in data and not _str_list(data["domains"]):
            errors.append("domains must be list[str]")
        if "vram_min_gb" in data and not _positive_int(data["vram_min_gb"]):
            errors.append("vram_min_gb must be positive int")
        if "eval_delta" in data and not isinstance(data["eval_delta"], dict):
            errors.append("eval_delta must be object")

    elif schema_name == "teacher_policy_card.schema.json":
        _require(
            data,
            (
                "teacher_id",
                "teacher_type",
                "license",
                "allowed_for_training",
                "allowed_outputs_retention",
                "allowed_for_commercial_use",
                "terms_version",
            ),
            errors,
        )
        for key in (
            "allowed_for_training",
            "allowed_outputs_retention",
            "allowed_for_commercial_use",
        ):
            if key in data and not isinstance(data[key], bool):
                errors.append(f"{key} must be bool")

    elif schema_name == "route_trace.schema.json":
        _require(
            data,
            (
                "trace_id",
                "task_id",
                "task_type",
                "router_version",
                "candidate_experts",
                "created_at",
            ),
            errors,
        )
        for key in ("trace_id", "task_id", "task_type", "router_version", "created_at"):
            if key in data and not isinstance(data[key], str):
                errors.append(f"{key} must be string")
        if "candidate_experts" in data and not _str_list(data["candidate_experts"]):
            errors.append("candidate_experts must be list[str]")
        chosen = data.get("chosen_expert")
        if chosen is not None and not isinstance(chosen, str):
            errors.append("chosen_expert must be string or null")
        if "admission_reports" in data and not _dict_list(data["admission_reports"]):
            errors.append("admission_reports must be list[object]")
        if "verifier_reports" in data and not _dict_list(data["verifier_reports"]):
            errors.append("verifier_reports must be list[object]")

    elif schema_name == "trace_rewrite_manifest.schema.json":
        _require(
            data,
            (
                "source_path",
                "output_path",
                "row_count",
                "source_hash",
                "output_hash",
                "rows_hash",
            ),
            errors,
        )
        for key in ("source_path", "output_path"):
            if key in data and not isinstance(data[key], str):
                errors.append(f"{key} must be string")
        if "row_count" in data and not _non_negative_int(data["row_count"]):
            errors.append("row_count must be non-negative int")
        for key in ("source_hash", "output_hash", "rows_hash"):
            if key in data and not _hash64(data[key]):
                errors.append(f"{key} must be sha256 hex string")

    elif schema_name == "trace_report.schema.json":
        _require(
            data,
            (
                "path",
                "row_count",
                "task_types",
                "chosen_experts",
                "file_hash",
                "rows_hash",
            ),
            errors,
        )
        if "path" in data and not isinstance(data["path"], str):
            errors.append("path must be string")
        if "row_count" in data and not _non_negative_int(data["row_count"]):
            errors.append("row_count must be non-negative int")
        for key in ("task_types", "chosen_experts"):
            if key in data and not _str_list(data[key]):
                errors.append(f"{key} must be list[str]")
        for key in ("file_hash", "rows_hash"):
            if key in data and not _hash64(data[key]):
                errors.append(f"{key} must be sha256 hex string")

    elif schema_name == "evidence_summary.schema.json":
        _require(
            data,
            ("run_dir", "artifact_count", "missing_count", "missing", "artifacts"),
            errors,
        )
        if "run_dir" in data and not isinstance(data["run_dir"], str):
            errors.append("run_dir must be string")
        for key in ("artifact_count", "missing_count"):
            if key in data and not _non_negative_int(data[key]):
                errors.append(f"{key} must be non-negative int")
        if "missing" in data and not _str_list(data["missing"]):
            errors.append("missing must be list[str]")
        if "artifacts" in data and not _artifact_list(data["artifacts"]):
            errors.append("artifacts must be list[{path, exists, size_bytes}]")

    elif schema_name == "evidence_bundle_manifest.schema.json":
        _require(data, ("run_dir", "artifact_count", "artifacts"), errors)
        if "run_dir" in data and not isinstance(data["run_dir"], str):
            errors.append("run_dir must be string")
        if "artifact_count" in data and not _non_negative_int(data["artifact_count"]):
            errors.append("artifact_count must be non-negative int")
        if "artifacts" in data and not _bundle_artifact_list(data["artifacts"]):
            errors.append("artifacts must be list[{path, size_bytes, sha256}]")

    elif schema_name == "evidence_verify_report.schema.json":
        _require(
            data,
            (
                "manifest_path",
                "run_dir",
                "artifact_count",
                "checked_count",
                "count_ok",
                "failure_count",
                "ok",
                "checks",
            ),
            errors,
        )
        for key in ("manifest_path", "run_dir"):
            if key in data and not isinstance(data[key], str):
                errors.append(f"{key} must be string")
        for key in ("artifact_count", "checked_count", "failure_count"):
            if key in data and not _non_negative_int(data[key]):
                errors.append(f"{key} must be non-negative int")
        for key in ("count_ok", "ok"):
            if key in data and not isinstance(data[key], bool):
                errors.append(f"{key} must be bool")
        if "checks" in data and not _verify_check_list(data["checks"]):
            errors.append("checks must be list[verify-check]")

    elif schema_name == "evidence_pipeline_result.schema.json":
        _require(
            data,
            (
                "run_dir",
                "ok",
                "artifacts",
                "patch_gate",
                "trace_compact",
                "trace_report",
                "evidence_summary",
                "evidence_bundle_manifest",
                "evidence_verify_report",
            ),
            errors,
        )
        if "run_dir" in data and not isinstance(data["run_dir"], str):
            errors.append("run_dir must be string")
        if "ok" in data and not isinstance(data["ok"], bool):
            errors.append("ok must be bool")
        if "artifacts" in data and not _str_list(data["artifacts"]):
            errors.append("artifacts must be list[str]")
        for key in (
            "patch_gate",
            "trace_compact",
            "trace_report",
            "evidence_summary",
            "evidence_bundle_manifest",
            "evidence_verify_report",
        ):
            if key in data and not _object(data[key]):
                errors.append(f"{key} must be object")

    elif schema_name == "evidence_seal_manifest.schema.json":
        _require(data, ("run_dir", "artifact_count", "sealed_artifacts", "excluded_artifacts"), errors)
        if "run_dir" in data and not isinstance(data["run_dir"], str):
            errors.append("run_dir must be string")
        if "artifact_count" in data and not _non_negative_int(data["artifact_count"]):
            errors.append("artifact_count must be non-negative int")
        if "sealed_artifacts" in data and not _bundle_artifact_list(data["sealed_artifacts"]):
            errors.append("sealed_artifacts must be list[{path, size_bytes, sha256}]")
        if "excluded_artifacts" in data and not _str_list(data["excluded_artifacts"]):
            errors.append("excluded_artifacts must be list[str]")

    elif schema_name == "evidence_seal_verify_report.schema.json":
        _require(
            data,
            (
                "manifest_path",
                "run_dir",
                "artifact_count",
                "checked_count",
                "excluded_artifacts",
                "count_ok",
                "failure_count",
                "ok",
                "checks",
            ),
            errors,
        )
        for key in ("manifest_path", "run_dir"):
            if key in data and not isinstance(data[key], str):
                errors.append(f"{key} must be string")
        for key in ("artifact_count", "checked_count", "failure_count"):
            if key in data and not _non_negative_int(data[key]):
                errors.append(f"{key} must be non-negative int")
        if "excluded_artifacts" in data and not _str_list(data["excluded_artifacts"]):
            errors.append("excluded_artifacts must be list[str]")
        for key in ("count_ok", "ok"):
            if key in data and not isinstance(data[key], bool):
                errors.append(f"{key} must be bool")
        if "checks" in data and not _verify_check_list(data["checks"]):
            errors.append("checks must be list[verify-check]")

    elif schema_name == "evidence_artifact_index.schema.json":
        _require(data, ("index_version", "artifact_count", "artifacts"), errors)
        if "index_version" in data and not isinstance(data["index_version"], str):
            errors.append("index_version must be string")
        if "artifact_count" in data and not _non_negative_int(data["artifact_count"]):
            errors.append("artifact_count must be non-negative int")
        if "artifacts" in data and not _artifact_index_list(data["artifacts"]):
            errors.append("artifacts must be list[{path, producer, schema, verifier, purpose, seal_stage, role}]")
        if isinstance(data.get("artifacts"), list) and data.get("artifact_count") != len(data["artifacts"]):
            errors.append("artifact_count must equal len(artifacts)")

    elif schema_name == "credit_ledger_settlement.schema.json":
        _require(
            data,
            (
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
            ),
            errors,
        )
        if data.get("settlement_currency") != "AEM_CREDIT":
            errors.append("settlement_currency must be AEM_CREDIT")
        if "settlement_version" in data and not isinstance(data["settlement_version"], str):
            errors.append("settlement_version must be string")
        if "challenge_window_closed" in data and not isinstance(data["challenge_window_closed"], bool):
            errors.append("challenge_window_closed must be bool")
        for key in (
            "contribution_receipt_count",
            "skill_receipt_count",
            "inference_receipt_count",
            "accepted_event_count",
            "rejected_event_count",
            "total_minted_micros",
            "total_transferred_micros",
        ):
            if key in data and not _non_negative_int(data[key]):
                errors.append(f"{key} must be non-negative int")
        if "net_supply_delta_micros" in data and not isinstance(data["net_supply_delta_micros"], int):
            errors.append("net_supply_delta_micros must be int")
        if "ok" in data and not isinstance(data["ok"], bool):
            errors.append("ok must be bool")
        if "seen_spend_keys" in data and not _str_list(data["seen_spend_keys"]):
            errors.append("seen_spend_keys must be list[str]")
        if "accounts" in data:
            accounts = data["accounts"]
            if not isinstance(accounts, list):
                errors.append("accounts must be list[account-balance]")
            else:
                for item in accounts:
                    if not isinstance(item, dict):
                        errors.append("account entry must be object")
                        continue
                    if not isinstance(item.get("account"), str):
                        errors.append("account entry account must be string")
                    if not isinstance(item.get("balance_micros"), int):
                        errors.append("account entry balance_micros must be int")
        if "events" in data:
            allowed_event_types = {"contribution_mint", "skill_mint", "inference_debit", "inference_host_credit"}
            events = data["events"]
            if not isinstance(events, list):
                errors.append("events must be list[settlement-event]")
            else:
                for item in events:
                    if not isinstance(item, dict):
                        errors.append("event entry must be object")
                        continue
                    for key in ("event_id", "source_receipt_id", "account", "reason"):
                        if not isinstance(item.get(key), str):
                            errors.append(f"event {key} must be string")
                    if item.get("event_type") not in allowed_event_types:
                        errors.append("event_type invalid")
                    if not isinstance(item.get("amount_micros"), int):
                        errors.append("event amount_micros must be int")
                    if item.get("settlement_currency") != "AEM_CREDIT":
                        errors.append("event settlement_currency must be AEM_CREDIT")
        if "rejections" in data:
            rejections = data["rejections"]
            if not isinstance(rejections, list):
                errors.append("rejections must be list[rejection]")
            else:
                for item in rejections:
                    if not isinstance(item, dict):
                        errors.append("rejection entry must be object")
                        continue
                    if not isinstance(item.get("source_receipt_id"), str):
                        errors.append("rejection source_receipt_id must be string")
                    if not isinstance(item.get("reason"), str):
                        errors.append("rejection reason must be string")

    else:
        errors.append(f"unknown schema: {schema_name}")

    return ValidationResult(ok=not errors, mode="structural", errors=tuple(errors))


def validate_data(data: dict[str, Any], schema_name: str) -> ValidationResult:
    schema_path = _repo_root() / "schemas" / schema_name
    try:
        import jsonschema  # type: ignore
    except Exception:
        return structural_validate(schema_name, data)

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(instance=data, schema=schema)
        return ValidationResult(ok=True, mode="jsonschema", errors=())
    except Exception as exc:
        return ValidationResult(ok=False, mode="jsonschema", errors=(str(exc),))


def validate_or_raise(data: dict[str, Any], schema_name: str) -> ValidationResult:
    result = validate_data(data, schema_name)
    if not result.ok:
        raise SchemaValidationError(f"{schema_name} validation failed: {result.errors}")
    return result


def validate_json_file(path: str | Path, schema_name: str) -> ValidationResult:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SchemaValidationError(f"{path} must contain a JSON object")
    return validate_or_raise(data, schema_name)
