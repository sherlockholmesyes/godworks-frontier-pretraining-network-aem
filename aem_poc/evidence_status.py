from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

from .evidence_artifact_index import build_artifact_index
from .evidence_upload_drift import DEFAULT_WORKFLOW_PATH, upload_drift_report
from .evidence_upload_policy import build_upload_policy
from .schema_validation import SchemaValidationError, validate_data


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAKEFILE_PATH = REPO_ROOT / "Makefile"
DEFAULT_STATUS_EXAMPLE_PATH = REPO_ROOT / "docs" / "evidence_status.example.json"
STATUS_SCHEMA = "evidence_status.schema.json"
STATUS_VERSION = "2026-07-01.v1"


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _int_dict(value: Any) -> bool:
    return isinstance(value, dict) and all(isinstance(key, str) and isinstance(item, int) and item >= 0 for key, item in value.items())


def _make_target_commands(makefile_path: str | Path, target: str) -> list[str]:
    lines = Path(makefile_path).read_text(encoding="utf-8").splitlines()
    header = f"{target}:"
    try:
        start = lines.index(header) + 1
    except ValueError as exc:
        raise ValueError(f"Make target not found: {target}") from exc
    commands: list[str] = []
    for line in lines[start:]:
        if line and not line.startswith("\t") and line.endswith(":"):
            break
        if line.startswith("\t"):
            commands.append(line[1:])
    return commands


def make_target_gates(makefile_path: str | Path, target: str) -> list[str]:
    gates: list[str] = []
    for command in _make_target_commands(makefile_path, target):
        if command.startswith("$(MAKE) "):
            gates.append(command.removeprefix("$(MAKE) "))
        else:
            gates.append(command)
    return gates


def local_ci_gates(makefile_path: str | Path = DEFAULT_MAKEFILE_PATH) -> list[str]:
    return make_target_gates(makefile_path, "evidence-local-ci")


def docs_check_gates(makefile_path: str | Path = DEFAULT_MAKEFILE_PATH) -> list[str]:
    return make_target_gates(makefile_path, "evidence-docs-check")


def docs_sync_gates(makefile_path: str | Path = DEFAULT_MAKEFILE_PATH) -> list[str]:
    return make_target_gates(makefile_path, "evidence-docs-sync")


def _counter(values: Sequence[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def _status_shape_ok(data: dict[str, Any]) -> bool:
    required = (
        "status_version",
        "local_ci_command",
        "local_ci_gates",
        "docs_check_command",
        "docs_check_gates",
        "docs_sync_command",
        "docs_sync_gates",
        "artifact_index",
        "artifacts",
        "upload_policy",
        "upload_drift",
    )
    if not all(key in data for key in required):
        return False
    for key in ("status_version", "local_ci_command", "docs_check_command", "docs_sync_command"):
        if not isinstance(data[key], str):
            return False
    for key in ("local_ci_gates", "docs_check_gates", "docs_sync_gates"):
        if not _str_list(data[key]):
            return False
    artifact_index = data["artifact_index"]
    if not isinstance(artifact_index, dict):
        return False
    if not isinstance(artifact_index.get("index_version"), str):
        return False
    if not isinstance(artifact_index.get("artifact_count"), int) or artifact_index["artifact_count"] < 0:
        return False
    if not _str_list(artifact_index.get("paths")):
        return False
    if not _int_dict(artifact_index.get("seal_stage_counts")) or not _int_dict(artifact_index.get("role_counts")):
        return False
    artifacts = data["artifacts"]
    if not isinstance(artifacts, list) or artifact_index["artifact_count"] != len(artifacts):
        return False
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            return False
        for key in ("path", "seal_stage", "role", "schema", "verifier"):
            if not isinstance(artifact.get(key), str):
                return False
    policy = data["upload_policy"]
    if not isinstance(policy, dict):
        return False
    if not isinstance(policy.get("policy_version"), str):
        return False
    if not _int_dict(policy.get("class_counts")):
        return False
    if not _str_list(policy.get("terminal_receipts")) or not _str_list(policy.get("second_stage_sealed_artifacts")):
        return False
    drift = data["upload_drift"]
    if not isinstance(drift, dict):
        return False
    for key in ("ok", "markers_present", "order_matches"):
        if not isinstance(drift.get(key), bool):
            return False
    for key in ("missing_from_ci", "extra_in_ci", "duplicate_ci_paths"):
        if not _str_list(drift.get(key)):
            return False
    return True


def validate_evidence_status(status: dict[str, Any]) -> None:
    result = validate_data(status, STATUS_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {STATUS_SCHEMA}",):
        if _status_shape_ok(status):
            return
    raise SchemaValidationError(f"{STATUS_SCHEMA} validation failed: {result.errors}")


def build_evidence_status(
    *,
    makefile_path: str | Path = DEFAULT_MAKEFILE_PATH,
    workflow_path: str | Path = DEFAULT_WORKFLOW_PATH,
) -> dict[str, Any]:
    index = build_artifact_index()
    artifacts = [
        {
            "path": artifact["path"],
            "seal_stage": artifact["seal_stage"],
            "role": artifact["role"],
            "schema": artifact["schema"],
            "verifier": artifact["verifier"],
        }
        for artifact in index["artifacts"]
    ]
    policy = build_upload_policy()
    drift = upload_drift_report(workflow_path)
    status = {
        "status_version": STATUS_VERSION,
        "local_ci_command": "make evidence-local-ci",
        "local_ci_gates": local_ci_gates(makefile_path),
        "docs_check_command": "make evidence-docs-check",
        "docs_check_gates": docs_check_gates(makefile_path),
        "docs_sync_command": "make evidence-docs-sync",
        "docs_sync_gates": docs_sync_gates(makefile_path),
        "artifact_index": {
            "index_version": index["index_version"],
            "artifact_count": index["artifact_count"],
            "paths": [artifact["path"] for artifact in artifacts],
            "seal_stage_counts": _counter([artifact["seal_stage"] for artifact in artifacts]),
            "role_counts": _counter([artifact["role"] for artifact in artifacts]),
        },
        "artifacts": artifacts,
        "upload_policy": {
            "policy_version": policy["policy_version"],
            "class_counts": {name: len(items) for name, items in sorted(policy["classes"].items())},
            "terminal_receipts": list(policy.get("terminal_receipts", [])),
            "second_stage_sealed_artifacts": list(policy.get("second_stage_sealed_artifacts", [])),
        },
        "upload_drift": {
            "ok": drift["ok"],
            "markers_present": drift["markers_present"],
            "order_matches": drift["order_matches"],
            "missing_from_ci": drift["missing_from_ci"],
            "extra_in_ci": drift["extra_in_ci"],
            "duplicate_ci_paths": drift["duplicate_ci_paths"],
        },
    }
    validate_evidence_status(status)
    return status


def write_evidence_status(output_path: str | Path, **kwargs: Any) -> dict[str, Any]:
    status = build_evidence_status(**kwargs)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return status


def load_evidence_status(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SchemaValidationError(f"{path} must contain a JSON object")
    validate_evidence_status(data)
    return data


def evidence_status_example_report(
    example_path: str | Path = DEFAULT_STATUS_EXAMPLE_PATH,
    *,
    makefile_path: str | Path = DEFAULT_MAKEFILE_PATH,
    workflow_path: str | Path = DEFAULT_WORKFLOW_PATH,
) -> dict[str, Any]:
    expected = build_evidence_status(makefile_path=makefile_path, workflow_path=workflow_path)
    example = load_evidence_status(example_path) if Path(example_path).exists() else None
    matches_generated = example == expected
    return {
        "example_path": str(Path(example_path)),
        "exists": example is not None,
        "matches_generated": matches_generated,
        "ok": matches_generated,
        "generated_artifact_count": expected["artifact_index"]["artifact_count"],
    }


def sync_evidence_status_example(
    example_path: str | Path = DEFAULT_STATUS_EXAMPLE_PATH,
    *,
    makefile_path: str | Path = DEFAULT_MAKEFILE_PATH,
    workflow_path: str | Path = DEFAULT_WORKFLOW_PATH,
) -> dict[str, Any]:
    before = Path(example_path).read_text(encoding="utf-8") if Path(example_path).exists() else None
    status = write_evidence_status(example_path, makefile_path=makefile_path, workflow_path=workflow_path)
    after = Path(example_path).read_text(encoding="utf-8")
    return {
        "example_path": str(Path(example_path)),
        "changed": before != after,
        "ok": True,
        "artifact_count": status["artifact_index"]["artifact_count"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print generated AEM evidence status summary")
    parser.add_argument("--output", help="optional path to write status JSON")
    parser.add_argument("--makefile", default=str(DEFAULT_MAKEFILE_PATH), help="path to Makefile")
    parser.add_argument("--workflow", default=str(DEFAULT_WORKFLOW_PATH), help="path to GitHub Actions workflow")
    parser.add_argument("--example", default=str(DEFAULT_STATUS_EXAMPLE_PATH), help="path to checked-in example status JSON")
    parser.add_argument("--check-example", action="store_true", help="check that the example status JSON matches generated status")
    parser.add_argument("--sync-example", action="store_true", help="rewrite the example status JSON from generated status")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    kwargs = {"makefile_path": args.makefile, "workflow_path": args.workflow}
    if args.check_example:
        report = evidence_status_example_report(args.example, **kwargs)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.sync_example:
        report = sync_evidence_status_example(args.example, **kwargs)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.output:
        status = write_evidence_status(args.output, **kwargs)
    else:
        status = build_evidence_status(**kwargs)
    print(json.dumps(status, indent=2, sort_keys=True))
    return 0 if status["upload_drift"]["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
