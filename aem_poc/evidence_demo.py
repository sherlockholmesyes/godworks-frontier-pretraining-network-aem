from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .hash_utils import sha256_file
from .schema_validation import validate_or_raise


EXPECTED_ARTIFACTS = (
    "route_trace.jsonl",
    "route_trace.compact.jsonl",
    "route_trace.compact.jsonl.manifest.json",
    "trace_report.json",
)
EVIDENCE_SUMMARY_ARTIFACT = "evidence_summary.json"
EVIDENCE_BUNDLE_MANIFEST_ARTIFACT = "evidence_bundle_manifest.json"


def evidence_summary(run_dir: str | Path = "runs/patch_gate_demo") -> dict[str, Any]:
    root = Path(run_dir)
    artifacts: list[dict[str, Any]] = []
    missing: list[str] = []
    for name in EXPECTED_ARTIFACTS:
        path = root / name
        exists = path.exists()
        if not exists:
            missing.append(str(path))
        artifacts.append(
            {
                "path": str(path),
                "exists": exists,
                "size_bytes": path.stat().st_size if exists else 0,
            }
        )
    summary = {
        "run_dir": str(root),
        "artifact_count": len(artifacts),
        "missing_count": len(missing),
        "missing": missing,
        "artifacts": artifacts,
    }
    validate_or_raise(summary, "evidence_summary.schema.json")
    return summary


def write_evidence_summary(
    run_dir: str | Path = "runs/patch_gate_demo",
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    summary = evidence_summary(run_dir)
    output = Path(output_path) if output_path is not None else Path(run_dir) / EVIDENCE_SUMMARY_ARTIFACT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def evidence_bundle_manifest(
    run_dir: str | Path = "runs/patch_gate_demo",
    summary_path: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(run_dir)
    artifact_paths = [root / name for name in EXPECTED_ARTIFACTS]
    artifact_paths.append(Path(summary_path) if summary_path is not None else root / EVIDENCE_SUMMARY_ARTIFACT)
    artifacts: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not path.exists():
            raise FileNotFoundError(f"missing evidence artifact: {path}")
        artifacts.append(
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "run_dir": str(root),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }
    validate_or_raise(manifest, "evidence_bundle_manifest.schema.json")
    return manifest


def write_evidence_bundle_manifest(
    run_dir: str | Path = "runs/patch_gate_demo",
    output_path: str | Path | None = None,
    summary_path: str | Path | None = None,
) -> dict[str, Any]:
    manifest = evidence_bundle_manifest(run_dir, summary_path=summary_path)
    output = Path(output_path) if output_path is not None else Path(run_dir) / EVIDENCE_BUNDLE_MANIFEST_ARTIFACT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List and verify AEM evidence demo artifacts")
    parser.add_argument(
        "run_dir",
        nargs="?",
        default="runs/patch_gate_demo",
        help="directory containing evidence artifacts",
    )
    parser.add_argument(
        "summary_output",
        nargs="?",
        help="optional evidence_summary.json output path",
    )
    parser.add_argument(
        "bundle_output",
        nargs="?",
        help="optional evidence_bundle_manifest.json output path",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.summary_output:
        summary = write_evidence_summary(args.run_dir, args.summary_output)
        if summary["missing"]:
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 1
        bundle = write_evidence_bundle_manifest(
            args.run_dir,
            args.bundle_output,
            summary_path=args.summary_output,
        )
        print(json.dumps({"bundle_manifest": bundle, "summary": summary}, indent=2, sort_keys=True))
        return 0

    summary = evidence_summary(args.run_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if summary["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())
