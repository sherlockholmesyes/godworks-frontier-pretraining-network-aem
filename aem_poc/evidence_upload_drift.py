from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .evidence_artifact_index import source_artifact_paths


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"
UPLOAD_ARTIFACT_NAME = "aem-trace-evidence"
UPLOAD_PATHS_BEGIN_MARKER = "# BEGIN AEM GENERATED UPLOAD PATHS"
UPLOAD_PATHS_END_MARKER = "# END AEM GENERATED UPLOAD PATHS"


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _marker_path_block_bounds(lines: list[str]) -> tuple[int, int, int] | None:
    begin_indexes = [index for index, line in enumerate(lines) if line.strip() == UPLOAD_PATHS_BEGIN_MARKER]
    if not begin_indexes:
        return None
    if len(begin_indexes) != 1:
        raise ValueError("expected exactly one AEM upload begin marker")
    begin = begin_indexes[0]
    for end in range(begin + 1, len(lines)):
        if lines[end].strip() == UPLOAD_PATHS_END_MARKER:
            for path_index in range(begin + 1, end):
                if lines[path_index].strip() == "path: |":
                    return path_index, end, _indent(lines[path_index])
            raise ValueError("AEM upload markers found but no path block inside")
    raise ValueError("AEM upload begin marker found without end marker")


def _legacy_path_block_bounds(lines: list[str], artifact_name: str = UPLOAD_ARTIFACT_NAME) -> tuple[int, int, int]:
    for index, line in enumerate(lines):
        if line.strip() != f"name: {artifact_name}":
            continue
        for path_index in range(index + 1, len(lines)):
            path_line = lines[path_index]
            if path_line.strip() == "path: |":
                path_indent = _indent(path_line)
                end = path_index + 1
                while end < len(lines):
                    stripped = lines[end].strip()
                    if stripped and _indent(lines[end]) <= path_indent:
                        break
                    end += 1
                return path_index, end, path_indent
    raise ValueError(f"upload-artifact path block not found for artifact: {artifact_name}")


def _upload_path_block_bounds(lines: list[str], artifact_name: str = UPLOAD_ARTIFACT_NAME) -> tuple[int, int, int, bool]:
    marker_bounds = _marker_path_block_bounds(lines)
    if marker_bounds is not None:
        path_index, end, path_indent = marker_bounds
        return path_index, end, path_indent, True
    path_index, end, path_indent = _legacy_path_block_bounds(lines, artifact_name)
    return path_index, end, path_indent, False


def render_upload_artifact_paths(paths: Sequence[str] | None = None, *, indent: int = 12) -> list[str]:
    source_paths = list(paths) if paths is not None else list(source_artifact_paths())
    prefix = " " * indent
    return [f"{prefix}{path}" for path in source_paths]


def replace_upload_artifact_paths(
    workflow_text: str,
    paths: Sequence[str] | None = None,
    *,
    artifact_name: str = UPLOAD_ARTIFACT_NAME,
) -> str:
    lines = workflow_text.splitlines()
    path_index, end, path_indent, has_markers = _upload_path_block_bounds(lines, artifact_name)
    rendered_paths = render_upload_artifact_paths(paths, indent=path_indent + 2)
    if has_markers:
        new_lines = lines[: path_index + 1] + rendered_paths + lines[end:]
    else:
        marker_prefix = " " * path_indent
        new_lines = (
            lines[:path_index]
            + [f"{marker_prefix}{UPLOAD_PATHS_BEGIN_MARKER}", lines[path_index]]
            + rendered_paths
            + [f"{marker_prefix}{UPLOAD_PATHS_END_MARKER}"]
            + lines[end:]
        )
    trailing_newline = "\n" if workflow_text.endswith("\n") else ""
    return "\n".join(new_lines) + trailing_newline


def sync_upload_artifact_paths(workflow_path: str | Path = DEFAULT_WORKFLOW_PATH) -> dict[str, Any]:
    path = Path(workflow_path)
    before = path.read_text(encoding="utf-8")
    after = replace_upload_artifact_paths(before)
    changed = before != after
    if changed:
        path.write_text(after, encoding="utf-8")
    report = upload_drift_report(path)
    return {
        "workflow_path": str(path),
        "artifact_name": UPLOAD_ARTIFACT_NAME,
        "path_count": len(source_artifact_paths()),
        "changed": changed,
        "ok": report["ok"],
        "order_matches": report["order_matches"],
        "markers_present": upload_path_markers_present(path),
    }


def upload_path_markers_present(workflow_path: str | Path = DEFAULT_WORKFLOW_PATH) -> bool:
    text = Path(workflow_path).read_text(encoding="utf-8")
    lines = text.splitlines()
    return _marker_path_block_bounds(lines) is not None


def extract_upload_artifact_paths(workflow_text: str, artifact_name: str = UPLOAD_ARTIFACT_NAME) -> list[str]:
    lines = workflow_text.splitlines()
    path_index, end, _path_indent, _has_markers = _upload_path_block_bounds(lines, artifact_name)
    return [line.strip() for line in lines[path_index + 1 : end] if line.strip()]


def ci_upload_paths(workflow_path: str | Path = DEFAULT_WORKFLOW_PATH) -> list[str]:
    return extract_upload_artifact_paths(Path(workflow_path).read_text(encoding="utf-8"))


def upload_drift_report(workflow_path: str | Path = DEFAULT_WORKFLOW_PATH) -> dict[str, Any]:
    ci_paths = ci_upload_paths(workflow_path)
    index_paths = list(source_artifact_paths())
    ci_set = set(ci_paths)
    index_set = set(index_paths)
    duplicate_ci_paths = sorted(path for path in ci_set if ci_paths.count(path) > 1)
    missing_from_ci = sorted(index_set - ci_set)
    extra_in_ci = sorted(ci_set - index_set)
    order_matches = ci_paths == index_paths
    markers_present = upload_path_markers_present(workflow_path)
    ok = not duplicate_ci_paths and not missing_from_ci and not extra_in_ci and markers_present
    return {
        "workflow_path": str(Path(workflow_path)),
        "artifact_name": UPLOAD_ARTIFACT_NAME,
        "ci_upload_count": len(ci_paths),
        "artifact_index_count": len(index_paths),
        "duplicate_ci_paths": duplicate_ci_paths,
        "missing_from_ci": missing_from_ci,
        "extra_in_ci": extra_in_ci,
        "order_matches": order_matches,
        "markers_present": markers_present,
        "ok": ok,
        "ci_upload_paths": ci_paths,
        "artifact_index_paths": index_paths,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check or sync GitHub Actions upload artifact paths against the evidence artifact index")
    parser.add_argument("--workflow", default=str(DEFAULT_WORKFLOW_PATH), help="path to .github/workflows/ci.yml")
    parser.add_argument("--sync", action="store_true", help="rewrite the upload path block from source_artifact_paths()")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.sync:
        report = sync_upload_artifact_paths(args.workflow)
    else:
        report = upload_drift_report(args.workflow)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
