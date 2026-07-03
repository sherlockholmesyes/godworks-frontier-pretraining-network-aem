from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .hash_utils import sha256_file, sha256_text
from .schema_validation import validate_or_raise
from .trace_store import TraceRewriteManifest, TraceStore


def compact_trace(input_path: str | Path, output_path: str | Path) -> TraceRewriteManifest:
    return TraceStore(input_path).rewrite_canonical(output_path)


def trace_report(input_path: str | Path) -> dict[str, Any]:
    path = Path(input_path)
    store = TraceStore(path)
    rows = store.read_all(validate=True)
    task_types = sorted({str(row.get("task_type")) for row in rows})
    chosen_experts = sorted(
        {str(row.get("chosen_expert")) for row in rows if row.get("chosen_expert") is not None}
    )
    canonical_rows = "".join(TraceStore.canonical_line(row) for row in rows)
    report = {
        "path": str(path),
        "row_count": len(rows),
        "task_types": task_types,
        "chosen_experts": chosen_experts,
        "file_hash": sha256_file(path) if path.exists() else sha256_text(""),
        "rows_hash": sha256_text(canonical_rows),
    }
    validate_or_raise(report, "trace_report.schema.json")
    return report


def write_trace_report(input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    report = trace_report(input_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AEM trace maintenance utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    compact = sub.add_parser("compact", help="validate and rewrite a trace JSONL file")
    compact.add_argument("input", help="input route_trace.jsonl")
    compact.add_argument("output", help="output canonical JSONL path")

    report = sub.add_parser("report", help="validate and summarize a trace JSONL file")
    report.add_argument("input", help="input route_trace.jsonl")
    report.add_argument("output", nargs="?", help="optional report JSON output path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "compact":
        manifest = compact_trace(args.input, args.output)
        print(json.dumps(manifest.to_dict(), indent=2, sort_keys=True))
        return 0

    if args.command == "report":
        if args.output:
            report = write_trace_report(args.input, args.output)
        else:
            report = trace_report(args.input)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
