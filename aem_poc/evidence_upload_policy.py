from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from .evidence_metadata_check import EVIDENCE_METADATA_REPORT_ARTIFACT
from .evidence_pipeline import EVIDENCE_SEAL_MANIFEST_ARTIFACT, SEALED_ARTIFACTS
from .evidence_seal_verify import EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT


POLICY_VERSION = "2026-07-01.v1"
SECOND_STAGE_SEAL_MANIFEST_ARTIFACT = "evidence_second_stage_seal_manifest.json"
SECOND_STAGE_VERIFY_REPORT_ARTIFACT = "evidence_second_stage_verify_report.json"
TRACE_RUN_DIR = "runs/patch_gate_demo"
METADATA_RUN_DIR = "runs/metadata"
UPLOAD_RUN_DIR = "runs/upload"


def _trace_path(name: str) -> str:
    return f"{TRACE_RUN_DIR}/{name}"


def _metadata_path(name: str) -> str:
    return f"{METADATA_RUN_DIR}/{name}"


def _upload_path(name: str) -> str:
    return f"{UPLOAD_RUN_DIR}/{name}"


def _artifact(path: str, role: str, sealed_by: str | None, reason: str) -> dict[str, Any]:
    return {
        "path": path,
        "role": role,
        "sealed_by": sealed_by,
        "reason": reason,
    }


def build_upload_policy() -> dict[str, Any]:
    seal_manifest_path = _trace_path(EVIDENCE_SEAL_MANIFEST_ARTIFACT)
    second_stage_seal_path = _upload_path(SECOND_STAGE_SEAL_MANIFEST_ARTIFACT)
    second_stage_verify_path = _upload_path(SECOND_STAGE_VERIFY_REPORT_ARTIFACT)
    metadata_report_path = _metadata_path(EVIDENCE_METADATA_REPORT_ARTIFACT)
    seal_verify_report_path = _trace_path(EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT)
    return {
        "policy_version": POLICY_VERSION,
        "decision": "metadata and post-seal receipts are sealed by evidence_second_stage_seal_manifest.json; evidence_second_stage_verify_report.json is a terminal uploaded receipt unless a third-stage policy is added",
        "seal_manifest": seal_manifest_path,
        "second_stage_seal_manifest": second_stage_seal_path,
        "terminal_receipts": [second_stage_verify_path],
        "classes": {
            "pre_evidence_metadata_receipts": [
                _artifact(
                    metadata_report_path,
                    "metadata_receipt",
                    second_stage_seal_path,
                    "Produced before evidence generation; sealed by the second-stage upload receipt seal.",
                )
            ],
            "sealed_trace_evidence": [
                _artifact(
                    _trace_path(name),
                    "sealed_trace_evidence",
                    seal_manifest_path,
                    "Hash and size are recorded in evidence_seal_manifest.json.",
                )
                for name in SEALED_ARTIFACTS
            ],
            "seal_manifests": [
                _artifact(
                    seal_manifest_path,
                    "seal_manifest",
                    None,
                    "A JSON file cannot contain a stable hash of itself; verify it with evidence_seal_verify.",
                )
            ],
            "post_seal_verification_receipts": [
                _artifact(
                    seal_verify_report_path,
                    "post_seal_receipt",
                    second_stage_seal_path,
                    "Produced after first-stage seal verification; sealed by the second-stage upload receipt seal.",
                )
            ],
            "second_stage_seal_manifests": [
                _artifact(
                    second_stage_seal_path,
                    "second_stage_seal_manifest",
                    None,
                    "Hashes metadata and post-seal receipts; it intentionally excludes itself.",
                )
            ],
            "terminal_verification_receipts": [
                _artifact(
                    second_stage_verify_path,
                    "terminal_second_stage_verify_receipt",
                    None,
                    "Produced after second-stage seal verification; not sealed again unless a third-stage policy is introduced.",
                )
            ],
        },
        "second_stage_sealed_artifacts": [
            metadata_report_path,
            seal_verify_report_path,
        ],
    }


def validate_upload_policy(policy: dict[str, Any]) -> None:
    classes = policy.get("classes")
    if not isinstance(classes, dict):
        raise ValueError("classes must be object")
    required_classes = (
        "pre_evidence_metadata_receipts",
        "sealed_trace_evidence",
        "seal_manifests",
        "post_seal_verification_receipts",
        "second_stage_seal_manifests",
        "terminal_verification_receipts",
    )
    for name in required_classes:
        if name not in classes or not isinstance(classes[name], list):
            raise ValueError(f"missing upload policy class: {name}")
    sealed_paths = {artifact["path"] for artifact in classes["sealed_trace_evidence"]}
    expected_sealed = {_trace_path(name) for name in SEALED_ARTIFACTS}
    if sealed_paths != expected_sealed:
        raise ValueError("sealed_trace_evidence does not match SEALED_ARTIFACTS")
    metadata_path = _metadata_path(EVIDENCE_METADATA_REPORT_ARTIFACT)
    post_seal_path = _trace_path(EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT)
    second_stage_path = _upload_path(SECOND_STAGE_SEAL_MANIFEST_ARTIFACT)
    second_stage_verify_path = _upload_path(SECOND_STAGE_VERIFY_REPORT_ARTIFACT)
    if metadata_path in sealed_paths:
        raise ValueError("metadata report must not be inside current sealed trace evidence")
    if post_seal_path in sealed_paths:
        raise ValueError("post-seal verification report must not be inside current sealed trace evidence")
    second_stage = set(policy.get("second_stage_sealed_artifacts", []))
    if second_stage != {metadata_path, post_seal_path}:
        raise ValueError("second-stage sealed artifacts must be metadata and post-seal receipts")
    second_stage_manifest_paths = {artifact["path"] for artifact in classes["second_stage_seal_manifests"]}
    if second_stage_manifest_paths != {second_stage_path}:
        raise ValueError("second-stage seal manifest class does not match expected path")
    terminal_paths = {artifact["path"] for artifact in classes["terminal_verification_receipts"]}
    if terminal_paths != {second_stage_verify_path}:
        raise ValueError("terminal verification receipt class does not match expected path")
    if second_stage_verify_path in set(policy.get("second_stage_sealed_artifacts", [])):
        raise ValueError("second-stage verify report must not be recursively sealed without third-stage policy")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print AEM evidence upload/sealing policy")
    parser.add_argument("--check", action="store_true", help="validate the generated upload policy")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    policy = build_upload_policy()
    if args.check:
        validate_upload_policy(policy)
    print(json.dumps(policy, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
