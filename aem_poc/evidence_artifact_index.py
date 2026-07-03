from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .evidence_pipeline import GENERATED_ARTIFACTS
from .evidence_seal_verify import EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
from .schema_validation import validate_json_file, validate_or_raise


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_PATH = REPO_ROOT / "docs" / "evidence_artifact_index.json"
DEFAULT_MARKDOWN_INDEX_PATH = REPO_ROOT / "docs" / "EVIDENCE_ARTIFACT_INDEX.md"
INDEX_SCHEMA = "evidence_artifact_index.schema.json"
INDEX_VERSION = "2026-07-01.v3"
RUN_DIR = "runs/patch_gate_demo"
METADATA_RUN_DIR = "runs/metadata"
UPLOAD_RUN_DIR = "runs/upload"
EVIDENCE_METADATA_REPORT_ARTIFACT = "evidence_metadata_report.json"
SECOND_STAGE_SEAL_MANIFEST_ARTIFACT = "evidence_second_stage_seal_manifest.json"
SECOND_STAGE_VERIFY_REPORT_ARTIFACT = "evidence_second_stage_verify_report.json"


def _trace_path(name: str) -> str:
    return f"{RUN_DIR}/{name}"


def _metadata_path(name: str) -> str:
    return f"{METADATA_RUN_DIR}/{name}"


def _upload_path(name: str) -> str:
    return f"{UPLOAD_RUN_DIR}/{name}"


def _meta(
    *,
    producer: str,
    schema: str,
    verifier: str,
    purpose: str,
    seal_stage: str,
    role: str,
) -> dict[str, str]:
    return {
        "producer": producer,
        "schema": schema,
        "verifier": verifier,
        "purpose": purpose,
        "seal_stage": seal_stage,
        "role": role,
    }


ARTIFACT_METADATA: dict[str, dict[str, str]] = {
    _metadata_path(EVIDENCE_METADATA_REPORT_ARTIFACT): _meta(
        producer="aem_poc.evidence_metadata_check.write_metadata_report",
        schema="evidence_metadata_report.schema.json",
        verifier="aem_poc.evidence_metadata_check, evidence_second_stage_seal_verify",
        purpose="Durable pre-evidence receipt for metadata integrity checks before evidence generation.",
        seal_stage="second_stage_upload_receipt_seal",
        role="pre_evidence_metadata_receipt",
    ),
    _trace_path("route_trace.jsonl"): _meta(
        producer="aem_poc.patch_gate_demo.run via TraceStore.append",
        schema="route_trace.schema.json per row",
        verifier="TraceStore.append, TraceStore.read_all(validate=True), evidence_seal_verify",
        purpose="Raw route, admission, workspace, and command evidence for the patch-gate demo.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("route_trace.compact.jsonl"): _meta(
        producer="aem_poc.trace_maint.compact_trace via TraceStore.rewrite_canonical",
        schema="route_trace.schema.json per row",
        verifier="canonical rewrite, validated replay, evidence_seal_verify",
        purpose="Canonical compact trace for deterministic replay and downstream reporting.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("route_trace.compact.jsonl.manifest.json"): _meta(
        producer="TraceStore.rewrite_canonical",
        schema="trace_rewrite_manifest.schema.json",
        verifier="schema validation, evidence_seal_verify",
        purpose="Records source trace hash, compact trace hash, canonical rows hash, and row count.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("trace_report.json"): _meta(
        producer="aem_poc.trace_maint.write_trace_report",
        schema="trace_report.schema.json",
        verifier="trace report schema validation, evidence_seal_verify",
        purpose="Reviewer readout of compact trace row count, task types, chosen experts, file hash, and rows hash.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("evidence_summary.json"): _meta(
        producer="aem_poc.evidence_demo.write_evidence_summary",
        schema="evidence_summary.schema.json",
        verifier="summary schema validation, evidence_seal_verify",
        purpose="Lists the expected pre-verification evidence artifacts and fails if any are missing.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("evidence_bundle_manifest.json"): _meta(
        producer="aem_poc.evidence_demo.write_evidence_bundle_manifest",
        schema="evidence_bundle_manifest.schema.json",
        verifier="aem_poc.evidence_verify, evidence_seal_verify",
        purpose="Hash map for the pre-verification evidence bundle.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("evidence_verify_report.json"): _meta(
        producer="aem_poc.evidence_verify.write_evidence_verify_report",
        schema="evidence_verify_report.schema.json",
        verifier="verify report schema validation, evidence_seal_verify",
        purpose="Durable result of recomputing the pre-verification bundle hashes.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("pipeline_result.json"): _meta(
        producer="aem_poc.evidence_pipeline.run_evidence_pipeline",
        schema="evidence_pipeline_result.schema.json",
        verifier="pipeline result schema validation, evidence_seal_verify",
        purpose="Durable receipt for the full orchestrated evidence run.",
        seal_stage="first_stage_trace_seal",
        role="sealed_trace_evidence",
    ),
    _trace_path("evidence_seal_manifest.json"): _meta(
        producer="aem_poc.evidence_pipeline.write_evidence_seal_manifest",
        schema="evidence_seal_manifest.schema.json",
        verifier="aem_poc.evidence_seal_verify",
        purpose="First-stage trace seal: hashes uploaded trace evidence artifacts except itself.",
        seal_stage="first_stage_trace_seal_manifest",
        role="seal_manifest",
    ),
    _trace_path(EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT): _meta(
        producer="aem_poc.evidence_seal_verify.write_evidence_seal_verify_report or make evidence-seal-verify-demo stdout redirection",
        schema="evidence_seal_verify_report.schema.json",
        verifier="evidence_second_stage_seal_verify",
        purpose="Durable post-seal receipt for first-stage trace seal verification.",
        seal_stage="second_stage_upload_receipt_seal",
        role="post_seal_verification_receipt",
    ),
    _upload_path(SECOND_STAGE_SEAL_MANIFEST_ARTIFACT): _meta(
        producer="aem_poc.evidence_second_stage_seal.write_second_stage_seal_manifest",
        schema="evidence_second_stage_seal_manifest.schema.json",
        verifier="aem_poc.evidence_second_stage_seal_verify",
        purpose="Second-stage upload receipt seal: hashes metadata and post-seal verification receipts except itself.",
        seal_stage="second_stage_upload_receipt_seal_manifest",
        role="second_stage_seal_manifest",
    ),
    _upload_path(SECOND_STAGE_VERIFY_REPORT_ARTIFACT): _meta(
        producer="aem_poc.evidence_second_stage_seal_verify.write_second_stage_verify_report",
        schema="evidence_second_stage_verify_report.schema.json",
        verifier="terminal_verification_receipts policy",
        purpose="Terminal verification receipt for the second-stage seal; not recursively sealed without a third-stage policy.",
        seal_stage="terminal_receipt_boundary",
        role="terminal_second_stage_verify_receipt",
    ),
}


def source_artifact_paths() -> tuple[str, ...]:
    trace_paths = tuple(_trace_path(name) for name in GENERATED_ARTIFACTS)
    return (
        _metadata_path(EVIDENCE_METADATA_REPORT_ARTIFACT),
        *trace_paths,
        _trace_path(EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT),
        _upload_path(SECOND_STAGE_SEAL_MANIFEST_ARTIFACT),
        _upload_path(SECOND_STAGE_VERIFY_REPORT_ARTIFACT),
    )


def build_artifact_index() -> dict[str, Any]:
    artifacts: list[dict[str, str]] = []
    for path in source_artifact_paths():
        artifacts.append({"path": path, **ARTIFACT_METADATA[path]})
    index = {
        "index_version": INDEX_VERSION,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }
    validate_or_raise(index, INDEX_SCHEMA)
    return index


def write_artifact_index(output_path: str | Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    index = build_artifact_index()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return index


def _md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_markdown_index(index: dict[str, Any] | None = None) -> str:
    data = index if index is not None else build_artifact_index()
    lines = [
        "# Evidence Artifact Index",
        "",
        "This generated index maps each AEM evidence file to its producer, schema, verifier, seal stage, role, and purpose.",
        "",
        "## Top-level command",
        "",
        "```bash",
        "make evidence-metadata-check",
        "make evidence-seal-verify-demo",
        "make evidence-second-stage-seal",
        "make evidence-second-stage-seal-verify",
        "```",
        "",
        "This flow runs:",
        "",
        "```text",
        "aem_poc.evidence_metadata_check",
        "aem_poc.evidence_pipeline",
        "aem_poc.evidence_seal_verify",
        "aem_poc.evidence_second_stage_seal",
        "aem_poc.evidence_second_stage_seal_verify",
        "```",
        "",
        "## Artifact table",
        "",
        "| Evidence file | Seal stage | Role | Producer | Schema | Verifier / gate | Purpose |",
        "|---|---|---|---|---|---|---|",
    ]
    for artifact in data["artifacts"]:
        lines.append(
            f"| `{_md(artifact['path'])}` | {_md(artifact['seal_stage'])} | {_md(artifact['role'])} | {_md(artifact['producer'])} | {_md(artifact['schema'])} | {_md(artifact['verifier'])} | {_md(artifact['purpose'])} |"
        )
    lines.extend(
        [
            "",
            "## Sealing model",
            "",
            "There are two hash layers plus one terminal receipt:",
            "",
            "```text",
            "evidence_seal_manifest.json",
            "  first-stage trace seal for generated trace/evidence artifacts",
            "",
            "evidence_second_stage_seal_manifest.json",
            "  second-stage upload receipt seal for metadata and post-seal receipts",
            "",
            "evidence_second_stage_verify_report.json",
            "  terminal verification receipt under current policy",
            "```",
            "",
            "## Local reviewer commands",
            "",
            "After downloading the CI artifact bundle, verify both seal stages:",
            "",
            "```bash",
            "python -m aem_poc.evidence_seal_verify \\",
            "  <download-dir>/runs/patch_gate_demo/evidence_seal_manifest.json",
            "",
            "python -m aem_poc.evidence_second_stage_seal_verify \\",
            "  <download-dir>/runs/upload/evidence_second_stage_seal_manifest.json",
            "```",
            "",
            "The bundle is reviewable only if both commands exit `0` and both reports have:",
            "",
            "```text",
            "ok=true",
            "failure_count=0",
            "```",
            "",
            "## Machine-readable source",
            "",
            "```text",
            "docs/evidence_artifact_index.json",
            "schemas/evidence_artifact_index.schema.json",
            "```",
            "",
            "Regenerate both index forms with:",
            "",
            "```bash",
            "python -m aem_poc.evidence_artifact_index sync",
            "python -m aem_poc.evidence_artifact_index md-sync",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown_index(output_path: str | Path = DEFAULT_MARKDOWN_INDEX_PATH) -> str:
    content = render_markdown_index()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return content


def markdown_matches_generated(markdown_path: str | Path = DEFAULT_MARKDOWN_INDEX_PATH) -> bool:
    path = Path(markdown_path)
    return path.exists() and path.read_text(encoding="utf-8") == render_markdown_index()


def load_artifact_index(index_path: str | Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    path = Path(index_path)
    validate_json_file(path, INDEX_SCHEMA)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def artifact_paths(index_path: str | Path = DEFAULT_INDEX_PATH) -> list[str]:
    index = load_artifact_index(index_path)
    return [artifact["path"] for artifact in index["artifacts"]]


def artifact_by_path(path: str, index_path: str | Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    index = load_artifact_index(index_path)
    for artifact in index["artifacts"]:
        if artifact["path"] == path or Path(artifact["path"]).name == path:
            return artifact
    raise KeyError(f"artifact not found in evidence index: {path}")


def validation_summary(index_path: str | Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    index = load_artifact_index(index_path)
    generated = build_artifact_index()
    paths = [artifact["path"] for artifact in index["artifacts"]]
    return {
        "index_path": str(Path(index_path)),
        "index_version": index["index_version"],
        "artifact_count": index["artifact_count"],
        "unique_path_count": len(set(paths)),
        "matches_generated": index == generated,
        "ok": index["artifact_count"] == len(paths) == len(set(paths)) and index == generated,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read AEM evidence artifact index metadata")
    parser.add_argument(
        "--index",
        default=str(DEFAULT_INDEX_PATH),
        help="path to evidence_artifact_index.json",
    )
    parser.add_argument(
        "--markdown",
        default=str(DEFAULT_MARKDOWN_INDEX_PATH),
        help="path to EVIDENCE_ARTIFACT_INDEX.md",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate the artifact index and print a JSON summary")
    subparsers.add_parser("list", help="print artifact paths, one per line")
    show = subparsers.add_parser("show", help="print one artifact record or the whole index as JSON")
    show.add_argument("artifact", nargs="?", help="artifact path or filename")
    subparsers.add_parser("sync", help="regenerate the artifact index JSON from the Python source table")
    subparsers.add_parser("md-sync", help="regenerate the Markdown artifact index from the Python source table")
    subparsers.add_parser("md-check", help="check that the Markdown artifact index matches the Python source table")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        summary = validation_summary(args.index)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0 if summary["ok"] else 1

    if args.command == "list":
        for path in artifact_paths(args.index):
            print(path)
        return 0

    if args.command == "show":
        if args.artifact:
            data = artifact_by_path(args.artifact, args.index)
        else:
            data = load_artifact_index(args.index)
        print(json.dumps(data, indent=2, sort_keys=True))
        return 0

    if args.command == "sync":
        index = write_artifact_index(args.index)
        print(json.dumps({"index_path": args.index, "artifact_count": index["artifact_count"], "ok": True}, indent=2, sort_keys=True))
        return 0

    if args.command == "md-sync":
        write_markdown_index(args.markdown)
        print(json.dumps({"markdown_path": args.markdown, "ok": True}, indent=2, sort_keys=True))
        return 0

    if args.command == "md-check":
        ok = markdown_matches_generated(args.markdown)
        print(json.dumps({"markdown_path": args.markdown, "matches_generated": ok, "ok": ok}, indent=2, sort_keys=True))
        return 0 if ok else 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
