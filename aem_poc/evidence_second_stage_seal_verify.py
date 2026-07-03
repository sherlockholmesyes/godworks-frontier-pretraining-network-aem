from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .evidence_second_stage_seal import (
    DEFAULT_OUTPUT_PATH,
    SECOND_STAGE_SEAL_MANIFEST_ARTIFACT,
    validate_second_stage_manifest,
)
from .hash_utils import sha256_file
from .schema_validation import SchemaValidationError, validate_data


EVIDENCE_SECOND_STAGE_VERIFY_REPORT_ARTIFACT = "evidence_second_stage_verify_report.json"
SECOND_STAGE_VERIFY_REPORT_SCHEMA = "evidence_second_stage_verify_report.schema.json"
DEFAULT_VERIFY_REPORT_PATH = Path("runs") / "upload" / EVIDENCE_SECOND_STAGE_VERIFY_REPORT_ARTIFACT


def _load_second_stage_manifest(manifest_path: str | Path) -> dict[str, Any]:
    path = Path(manifest_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SchemaValidationError(f"{path} must contain a JSON object")
    validate_second_stage_manifest(data)
    return data


def _resolve_artifact_path(manifest_file: Path, recorded_path: str) -> Path:
    path = Path(recorded_path)
    if path.exists():
        return path
    sibling = manifest_file.parent / path.name
    if sibling.exists():
        return sibling
    for parent in manifest_file.parents:
        candidate = parent / recorded_path
        if candidate.exists():
            return candidate
    return path


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _hash64_or_none(value: Any) -> bool:
    return value is None or (isinstance(value, str) and len(value) == 64)


def _verify_report_shape_ok(report: dict[str, Any]) -> bool:
    required = (
        "manifest_path",
        "stage",
        "policy_version",
        "inherits_first_stage_seal",
        "artifact_count",
        "checked_count",
        "excluded_artifacts",
        "count_ok",
        "failure_count",
        "ok",
        "checks",
    )
    if not all(key in report for key in required):
        return False
    for key in ("manifest_path", "stage", "policy_version", "inherits_first_stage_seal"):
        if not isinstance(report[key], str):
            return False
    for key in ("artifact_count", "checked_count", "failure_count"):
        if not isinstance(report[key], int) or report[key] < 0:
            return False
    if not _str_list(report["excluded_artifacts"]):
        return False
    for key in ("count_ok", "ok"):
        if not isinstance(report[key], bool):
            return False
    if not isinstance(report["checks"], list):
        return False
    for check in report["checks"]:
        if not isinstance(check, dict):
            return False
        for key in ("recorded_path", "resolved_path", "role"):
            if not isinstance(check.get(key), str):
                return False
        for key in ("exists", "size_ok", "hash_ok", "ok"):
            if not isinstance(check.get(key), bool):
                return False
        for key in ("expected_size_bytes", "actual_size_bytes"):
            if not isinstance(check.get(key), int) or check[key] < 0:
                return False
        if not isinstance(check.get("expected_sha256"), str) or len(check["expected_sha256"]) != 64:
            return False
        if not _hash64_or_none(check.get("actual_sha256")):
            return False
    return True


def validate_second_stage_verify_report(report: dict[str, Any]) -> None:
    result = validate_data(report, SECOND_STAGE_VERIFY_REPORT_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {SECOND_STAGE_VERIFY_REPORT_SCHEMA}",):
        if _verify_report_shape_ok(report):
            return
    raise SchemaValidationError(f"{SECOND_STAGE_VERIFY_REPORT_SCHEMA} validation failed: {result.errors}")


def verify_second_stage_seal(manifest_path: str | Path = DEFAULT_OUTPUT_PATH) -> dict[str, Any]:
    manifest_file = Path(manifest_path)
    manifest = _load_second_stage_manifest(manifest_file)
    checks: list[dict[str, Any]] = []
    count_ok = manifest.get("artifact_count") == len(manifest.get("sealed_artifacts", []))

    for artifact in manifest["sealed_artifacts"]:
        path = _resolve_artifact_path(manifest_file, artifact["path"])
        exists = path.exists()
        actual_size = path.stat().st_size if exists else 0
        actual_hash = sha256_file(path) if exists else None
        size_ok = exists and actual_size == artifact["size_bytes"]
        hash_ok = exists and actual_hash == artifact["sha256"]
        ok = exists and size_ok and hash_ok
        checks.append(
            {
                "recorded_path": artifact["path"],
                "resolved_path": str(path),
                "role": artifact["role"],
                "exists": exists,
                "expected_size_bytes": artifact["size_bytes"],
                "actual_size_bytes": actual_size,
                "size_ok": size_ok,
                "expected_sha256": artifact["sha256"],
                "actual_sha256": actual_hash,
                "hash_ok": hash_ok,
                "ok": ok,
            }
        )

    failure_count = sum(1 for check in checks if not check["ok"])
    if not count_ok:
        failure_count += 1
    report = {
        "manifest_path": str(manifest_file),
        "stage": manifest["stage"],
        "policy_version": manifest["policy_version"],
        "inherits_first_stage_seal": manifest["inherits_first_stage_seal"],
        "artifact_count": manifest["artifact_count"],
        "checked_count": len(checks),
        "excluded_artifacts": manifest.get("excluded_artifacts", []),
        "count_ok": count_ok,
        "failure_count": failure_count,
        "ok": failure_count == 0,
        "checks": checks,
    }
    validate_second_stage_verify_report(report)
    return report


def write_second_stage_verify_report(
    manifest_path: str | Path = DEFAULT_OUTPUT_PATH,
    output_path: str | Path = DEFAULT_VERIFY_REPORT_PATH,
) -> dict[str, Any]:
    report = verify_second_stage_seal(manifest_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify AEM second-stage seal manifest hashes")
    parser.add_argument(
        "manifest",
        nargs="?",
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"path to {SECOND_STAGE_SEAL_MANIFEST_ARTIFACT}",
    )
    parser.add_argument("--output", help=f"optional {EVIDENCE_SECOND_STAGE_VERIFY_REPORT_ARTIFACT} output path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.output:
        report = write_second_stage_verify_report(args.manifest, args.output)
    else:
        report = verify_second_stage_seal(args.manifest)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
