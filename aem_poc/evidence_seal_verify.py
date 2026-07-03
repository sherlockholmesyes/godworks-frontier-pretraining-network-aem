from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .hash_utils import sha256_file
from .schema_validation import SchemaValidationError, validate_or_raise


EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT = "evidence_seal_verify_report.json"


def _load_seal_manifest(manifest_path: str | Path) -> dict[str, Any]:
    path = Path(manifest_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SchemaValidationError(f"{path} must contain a JSON object")
    validate_or_raise(data, "evidence_seal_manifest.schema.json")
    return data


def _resolve_artifact_path(manifest_path: Path, recorded_path: str) -> Path:
    path = Path(recorded_path)
    if path.exists():
        return path
    sibling = manifest_path.parent / path.name
    if sibling.exists():
        return sibling
    return path


def verify_evidence_seal(manifest_path: str | Path) -> dict[str, Any]:
    manifest_file = Path(manifest_path)
    manifest = _load_seal_manifest(manifest_file)
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
        "run_dir": manifest["run_dir"],
        "artifact_count": manifest["artifact_count"],
        "checked_count": len(checks),
        "excluded_artifacts": manifest.get("excluded_artifacts", []),
        "count_ok": count_ok,
        "failure_count": failure_count,
        "ok": failure_count == 0,
        "checks": checks,
    }
    validate_or_raise(report, "evidence_seal_verify_report.schema.json")
    return report


def write_evidence_seal_verify_report(
    manifest_path: str | Path,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    report = verify_evidence_seal(manifest_path)
    manifest_file = Path(manifest_path)
    output = Path(output_path) if output_path is not None else manifest_file.parent / EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify AEM evidence seal manifest hashes")
    parser.add_argument("manifest", help="evidence_seal_manifest.json path")
    parser.add_argument("output", nargs="?", help="optional evidence_seal_verify_report.json output path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.output:
        report = write_evidence_seal_verify_report(args.manifest, args.output)
    else:
        report = verify_evidence_seal(args.manifest)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
