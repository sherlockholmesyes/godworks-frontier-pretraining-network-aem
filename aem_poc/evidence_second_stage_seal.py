from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .evidence_metadata_check import EVIDENCE_METADATA_REPORT_ARTIFACT
from .evidence_pipeline import EVIDENCE_SEAL_MANIFEST_ARTIFACT
from .evidence_seal_verify import EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
from .evidence_upload_policy import POLICY_VERSION
from .hash_utils import sha256_file
from .schema_validation import SchemaValidationError, validate_data


SECOND_STAGE_SEAL_MANIFEST_ARTIFACT = "evidence_second_stage_seal_manifest.json"
SECOND_STAGE_SCHEMA = "evidence_second_stage_seal_manifest.schema.json"
DEFAULT_METADATA_REPORT_PATH = Path("runs") / "metadata" / EVIDENCE_METADATA_REPORT_ARTIFACT
DEFAULT_SEAL_VERIFY_REPORT_PATH = Path("runs") / "patch_gate_demo" / EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
DEFAULT_FIRST_STAGE_SEAL_PATH = Path("runs") / "patch_gate_demo" / EVIDENCE_SEAL_MANIFEST_ARTIFACT
DEFAULT_OUTPUT_PATH = Path("runs") / "upload" / SECOND_STAGE_SEAL_MANIFEST_ARTIFACT


def _hash64(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64


def _second_stage_manifest_shape_ok(data: dict[str, Any]) -> bool:
    required = ("stage", "policy_version", "inherits_first_stage_seal", "artifact_count", "sealed_artifacts", "excluded_artifacts")
    if not all(key in data for key in required):
        return False
    if not isinstance(data["stage"], str) or not isinstance(data["policy_version"], str):
        return False
    if not isinstance(data["inherits_first_stage_seal"], str):
        return False
    if not isinstance(data["artifact_count"], int) or data["artifact_count"] < 0:
        return False
    if not isinstance(data["excluded_artifacts"], list) or not all(isinstance(item, str) for item in data["excluded_artifacts"]):
        return False
    artifacts = data["sealed_artifacts"]
    if not isinstance(artifacts, list) or data["artifact_count"] != len(artifacts):
        return False
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            return False
        for key in ("path", "role"):
            if not isinstance(artifact.get(key), str):
                return False
        if not isinstance(artifact.get("size_bytes"), int) or artifact["size_bytes"] < 0:
            return False
        if not _hash64(artifact.get("sha256")):
            return False
    return True


def validate_second_stage_manifest(manifest: dict[str, Any]) -> None:
    result = validate_data(manifest, SECOND_STAGE_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {SECOND_STAGE_SCHEMA}",):
        if _second_stage_manifest_shape_ok(manifest):
            return
    raise SchemaValidationError(f"{SECOND_STAGE_SCHEMA} validation failed: {result.errors}")


def second_stage_sealed_artifacts(
    metadata_report_path: str | Path = DEFAULT_METADATA_REPORT_PATH,
    seal_verify_report_path: str | Path = DEFAULT_SEAL_VERIFY_REPORT_PATH,
) -> tuple[tuple[Path, str], ...]:
    return (
        (Path(metadata_report_path), "pre_evidence_metadata_receipt"),
        (Path(seal_verify_report_path), "post_seal_verification_receipt"),
    )


def second_stage_seal_manifest(
    *,
    metadata_report_path: str | Path = DEFAULT_METADATA_REPORT_PATH,
    seal_verify_report_path: str | Path = DEFAULT_SEAL_VERIFY_REPORT_PATH,
    first_stage_seal_path: str | Path = DEFAULT_FIRST_STAGE_SEAL_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    sealed_artifacts: list[dict[str, Any]] = []
    for path, role in second_stage_sealed_artifacts(metadata_report_path, seal_verify_report_path):
        if not path.exists():
            raise FileNotFoundError(f"missing second-stage artifact to seal: {path}")
        sealed_artifacts.append(
            {
                "path": str(path),
                "role": role,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "stage": "second_stage_upload_receipts",
        "policy_version": POLICY_VERSION,
        "inherits_first_stage_seal": str(Path(first_stage_seal_path)),
        "artifact_count": len(sealed_artifacts),
        "sealed_artifacts": sealed_artifacts,
        "excluded_artifacts": [str(Path(output_path))],
    }
    validate_second_stage_manifest(manifest)
    return manifest


def write_second_stage_seal_manifest(
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    *,
    metadata_report_path: str | Path = DEFAULT_METADATA_REPORT_PATH,
    seal_verify_report_path: str | Path = DEFAULT_SEAL_VERIFY_REPORT_PATH,
    first_stage_seal_path: str | Path = DEFAULT_FIRST_STAGE_SEAL_PATH,
) -> dict[str, Any]:
    manifest = second_stage_seal_manifest(
        metadata_report_path=metadata_report_path,
        seal_verify_report_path=seal_verify_report_path,
        first_stage_seal_path=first_stage_seal_path,
        output_path=output_path,
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write AEM second-stage seal manifest for upload receipts")
    parser.add_argument("--metadata-report", default=str(DEFAULT_METADATA_REPORT_PATH))
    parser.add_argument("--seal-verify-report", default=str(DEFAULT_SEAL_VERIFY_REPORT_PATH))
    parser.add_argument("--first-stage-seal", default=str(DEFAULT_FIRST_STAGE_SEAL_PATH))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    manifest = write_second_stage_seal_manifest(
        args.output,
        metadata_report_path=args.metadata_report,
        seal_verify_report_path=args.seal_verify_report,
        first_stage_seal_path=args.first_stage_seal,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
