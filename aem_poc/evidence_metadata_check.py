from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .evidence_artifact_index import (
    DEFAULT_INDEX_PATH,
    DEFAULT_MARKDOWN_INDEX_PATH,
    RUN_DIR,
    build_artifact_index,
    load_artifact_index,
    markdown_matches_generated,
    validation_summary,
)
from .evidence_pipeline import SEALED_ARTIFACTS
from .schema_validation import SchemaValidationError, validate_data


EVIDENCE_METADATA_REPORT_ARTIFACT = "evidence_metadata_report.json"
DEFAULT_REPORT_PATH = Path("runs") / "metadata" / EVIDENCE_METADATA_REPORT_ARTIFACT
REPORT_SCHEMA = "evidence_metadata_report.schema.json"


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0


def _metadata_report_shape_ok(report: dict[str, Any]) -> bool:
    if not all(key in report for key in ("index_path", "markdown_path", "json_index", "markdown_index", "artifact_drift", "ok")):
        return False
    if not isinstance(report["index_path"], str) or not isinstance(report["markdown_path"], str):
        return False
    if not isinstance(report["ok"], bool):
        return False
    json_index = report["json_index"]
    markdown_index = report["markdown_index"]
    artifact_drift = report["artifact_drift"]
    if not isinstance(json_index, dict) or not isinstance(markdown_index, dict) or not isinstance(artifact_drift, dict):
        return False
    if not all(key in json_index for key in ("index_path", "index_version", "artifact_count", "unique_path_count", "matches_generated", "ok")):
        return False
    if not isinstance(json_index["index_path"], str) or not isinstance(json_index["index_version"], str):
        return False
    if not _non_negative_int(json_index["artifact_count"]) or not _non_negative_int(json_index["unique_path_count"]):
        return False
    if not isinstance(json_index["matches_generated"], bool) or not isinstance(json_index["ok"], bool):
        return False
    if not all(key in markdown_index for key in ("matches_generated", "ok")):
        return False
    if not isinstance(markdown_index["matches_generated"], bool) or not isinstance(markdown_index["ok"], bool):
        return False
    if not all(
        key in artifact_drift
        for key in ("index_path", "expected_count", "indexed_count", "missing_paths", "extra_paths", "sealed_without_verifier", "ok")
    ):
        return False
    if not isinstance(artifact_drift["index_path"], str):
        return False
    if not _non_negative_int(artifact_drift["expected_count"]) or not _non_negative_int(artifact_drift["indexed_count"]):
        return False
    if not _str_list(artifact_drift["missing_paths"]):
        return False
    if not _str_list(artifact_drift["extra_paths"]):
        return False
    if not _str_list(artifact_drift["sealed_without_verifier"]):
        return False
    return isinstance(artifact_drift["ok"], bool)


def validate_metadata_report(report: dict[str, Any]) -> None:
    result = validate_data(report, REPORT_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {REPORT_SCHEMA}",):
        if _metadata_report_shape_ok(report):
            return
    raise SchemaValidationError(f"{REPORT_SCHEMA} validation failed: {result.errors}")


def artifact_index_drift_report(index_path: str | Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    index = load_artifact_index(index_path)
    generated = build_artifact_index()
    indexed_paths = {artifact["path"] for artifact in index["artifacts"]}
    expected_paths = {artifact["path"] for artifact in generated["artifacts"]}
    by_path = {artifact["path"]: artifact for artifact in index["artifacts"]}
    sealed_paths = {f"{RUN_DIR}/{name}" for name in SEALED_ARTIFACTS}
    sealed_without_verifier = sorted(
        path for path in sealed_paths
        if path not in by_path or "evidence_seal_verify" not in by_path[path]["verifier"]
    )
    missing_paths = sorted(expected_paths - indexed_paths)
    extra_paths = sorted(indexed_paths - expected_paths)
    return {
        "index_path": str(Path(index_path)),
        "expected_count": len(expected_paths),
        "indexed_count": len(indexed_paths),
        "missing_paths": missing_paths,
        "extra_paths": extra_paths,
        "sealed_without_verifier": sealed_without_verifier,
        "ok": not missing_paths and not extra_paths and not sealed_without_verifier,
    }


def metadata_check(
    index_path: str | Path = DEFAULT_INDEX_PATH,
    markdown_path: str | Path = DEFAULT_MARKDOWN_INDEX_PATH,
) -> dict[str, Any]:
    json_summary = validation_summary(index_path)
    markdown_ok = markdown_matches_generated(markdown_path)
    drift = artifact_index_drift_report(index_path)
    ok = bool(json_summary["ok"] and markdown_ok and drift["ok"])
    report = {
        "index_path": str(Path(index_path)),
        "markdown_path": str(Path(markdown_path)),
        "json_index": json_summary,
        "markdown_index": {
            "matches_generated": markdown_ok,
            "ok": markdown_ok,
        },
        "artifact_drift": drift,
        "ok": ok,
    }
    validate_metadata_report(report)
    return report


def write_metadata_report(
    output_path: str | Path = DEFAULT_REPORT_PATH,
    *,
    index_path: str | Path = DEFAULT_INDEX_PATH,
    markdown_path: str | Path = DEFAULT_MARKDOWN_INDEX_PATH,
) -> dict[str, Any]:
    report = metadata_check(index_path=index_path, markdown_path=markdown_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run AEM evidence metadata checks")
    parser.add_argument("--index", default=str(DEFAULT_INDEX_PATH), help="path to evidence_artifact_index.json")
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN_INDEX_PATH), help="path to EVIDENCE_ARTIFACT_INDEX.md")
    parser.add_argument("--output", help="optional evidence metadata report output path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.output:
        report = write_metadata_report(args.output, index_path=args.index, markdown_path=args.markdown)
    else:
        report = metadata_check(args.index, args.markdown)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
