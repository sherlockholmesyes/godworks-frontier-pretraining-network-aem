from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Sequence

from .evidence_demo import (
    EVIDENCE_BUNDLE_MANIFEST_ARTIFACT,
    EVIDENCE_SUMMARY_ARTIFACT,
    write_evidence_bundle_manifest,
    write_evidence_summary,
)
from .evidence_verify import EVIDENCE_VERIFY_REPORT_ARTIFACT, write_evidence_verify_report
from .hash_utils import sha256_file
from .patch_gate_demo import run as run_patch_gate_demo
from .schema_validation import validate_or_raise
from .trace_maint import compact_trace, write_trace_report


TRACE_ARTIFACT = "route_trace.jsonl"
COMPACT_TRACE_ARTIFACT = "route_trace.compact.jsonl"
TRACE_REWRITE_MANIFEST_ARTIFACT = "route_trace.compact.jsonl.manifest.json"
TRACE_REPORT_ARTIFACT = "trace_report.json"
PIPELINE_RESULT_ARTIFACT = "pipeline_result.json"
EVIDENCE_SEAL_MANIFEST_ARTIFACT = "evidence_seal_manifest.json"
WORKSPACE_DIRS = ("workspace_fake", "workspace_real")
SEALED_ARTIFACTS = (
    TRACE_ARTIFACT,
    COMPACT_TRACE_ARTIFACT,
    TRACE_REWRITE_MANIFEST_ARTIFACT,
    TRACE_REPORT_ARTIFACT,
    EVIDENCE_SUMMARY_ARTIFACT,
    EVIDENCE_BUNDLE_MANIFEST_ARTIFACT,
    EVIDENCE_VERIFY_REPORT_ARTIFACT,
    PIPELINE_RESULT_ARTIFACT,
)
GENERATED_ARTIFACTS = SEALED_ARTIFACTS + (EVIDENCE_SEAL_MANIFEST_ARTIFACT,)


def clear_known_outputs(run_dir: str | Path) -> None:
    root = Path(run_dir)
    for name in GENERATED_ARTIFACTS:
        path = root / name
        if path.exists():
            path.unlink()
    for name in WORKSPACE_DIRS:
        path = root / name
        if path.exists():
            shutil.rmtree(path)


def _write_json(data: dict[str, Any], output_path: str | Path, schema_name: str) -> None:
    validate_or_raise(data, schema_name)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def evidence_seal_manifest(run_dir: str | Path = "runs/patch_gate_demo") -> dict[str, Any]:
    root = Path(run_dir)
    sealed_artifacts: list[dict[str, Any]] = []
    for name in SEALED_ARTIFACTS:
        path = root / name
        if not path.exists():
            raise FileNotFoundError(f"missing evidence artifact to seal: {path}")
        sealed_artifacts.append(
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "run_dir": str(root),
        "artifact_count": len(sealed_artifacts),
        "sealed_artifacts": sealed_artifacts,
        "excluded_artifacts": [str(root / EVIDENCE_SEAL_MANIFEST_ARTIFACT)],
    }
    validate_or_raise(manifest, "evidence_seal_manifest.schema.json")
    return manifest


def write_evidence_seal_manifest(
    run_dir: str | Path = "runs/patch_gate_demo",
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    manifest = evidence_seal_manifest(run_dir)
    output = Path(output_path) if output_path is not None else Path(run_dir) / EVIDENCE_SEAL_MANIFEST_ARTIFACT
    _write_json(manifest, output, "evidence_seal_manifest.schema.json")
    return manifest


def run_evidence_pipeline(
    run_dir: str | Path = "runs/patch_gate_demo",
    *,
    clean: bool = True,
) -> dict[str, Any]:
    root = Path(run_dir)
    if clean:
        clear_known_outputs(root)
    root.mkdir(parents=True, exist_ok=True)

    patch_result = run_patch_gate_demo(output_dir=root)
    route_trace = root / TRACE_ARTIFACT
    compact_trace_path = root / COMPACT_TRACE_ARTIFACT
    trace_report_path = root / TRACE_REPORT_ARTIFACT
    evidence_summary_path = root / EVIDENCE_SUMMARY_ARTIFACT
    bundle_manifest_path = root / EVIDENCE_BUNDLE_MANIFEST_ARTIFACT
    verify_report_path = root / EVIDENCE_VERIFY_REPORT_ARTIFACT
    pipeline_result_path = root / PIPELINE_RESULT_ARTIFACT
    seal_manifest_path = root / EVIDENCE_SEAL_MANIFEST_ARTIFACT

    compact_manifest = compact_trace(route_trace, compact_trace_path)
    trace_report = write_trace_report(compact_trace_path, trace_report_path)
    evidence_summary = write_evidence_summary(root, evidence_summary_path)
    bundle_manifest = write_evidence_bundle_manifest(
        root,
        bundle_manifest_path,
        summary_path=evidence_summary_path,
    )
    verify_report = write_evidence_verify_report(bundle_manifest_path, verify_report_path)

    artifacts = [str(root / name) for name in GENERATED_ARTIFACTS]
    result = {
        "run_dir": str(root),
        "patch_gate": patch_result,
        "trace_compact": compact_manifest.to_dict(),
        "trace_report": trace_report,
        "evidence_summary": evidence_summary,
        "evidence_bundle_manifest": bundle_manifest,
        "evidence_verify_report": verify_report,
        "artifacts": artifacts,
        "ok": bool(verify_report["ok"]),
    }
    _write_json(result, pipeline_result_path, "evidence_pipeline_result.schema.json")
    write_evidence_seal_manifest(root, seal_manifest_path)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AEM evidence pipeline")
    parser.add_argument(
        "run_dir",
        nargs="?",
        default="runs/patch_gate_demo",
        help="directory where evidence artifacts are generated",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="do not remove known generated files before running",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = run_evidence_pipeline(args.run_dir, clean=not args.no_clean)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
