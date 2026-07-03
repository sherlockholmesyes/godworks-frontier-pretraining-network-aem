from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .hash_utils import sha256_file, sha256_text
from .protocol import AdmissionReport, ExpertCard, TaskPacket
from .schema_validation import SchemaValidationError, validate_or_raise


def _json_ready(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    return value


@dataclass(frozen=True)
class RouteTrace:
    trace_id: str
    task_id: str
    task_type: str
    router_version: str
    candidate_experts: tuple[str, ...]
    chosen_expert: str | None
    admission_reports: tuple[dict[str, Any], ...]
    verifier_reports: tuple[dict[str, Any], ...] = ()
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))


@dataclass(frozen=True)
class TraceRewriteManifest:
    source_path: str
    output_path: str
    row_count: int
    source_hash: str
    output_hash: str
    rows_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))


class TraceReplayError(SchemaValidationError):
    pass


class TraceStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    @staticmethod
    def canonical_line(row: dict[str, Any]) -> str:
        return json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"

    def append(self, trace: RouteTrace) -> None:
        payload = trace.to_dict()
        validate_or_raise(payload, "route_trace.schema.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(self.canonical_line(payload))

    def read_all(self, validate: bool = False) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise TraceReplayError(f"invalid JSONL row {line_number}: {exc}") from exc
                if not isinstance(row, dict):
                    raise TraceReplayError(f"trace row {line_number} must be object")
                if validate:
                    try:
                        validate_or_raise(row, "route_trace.schema.json")
                    except SchemaValidationError as exc:
                        raise TraceReplayError(f"trace row {line_number} invalid: {exc}") from exc
                rows.append(row)
        return rows

    def rewrite_canonical(
        self,
        output_path: str | Path,
        manifest_path: str | Path | None = None,
    ) -> TraceRewriteManifest:
        rows = self.read_all(validate=True)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        canonical = "".join(self.canonical_line(row) for row in rows)
        output.write_text(canonical, encoding="utf-8")
        source_hash = sha256_file(self.path) if self.path.exists() else sha256_text("")
        output_hash = sha256_file(output)
        manifest = TraceRewriteManifest(
            source_path=str(self.path),
            output_path=str(output),
            row_count=len(rows),
            source_hash=source_hash,
            output_hash=output_hash,
            rows_hash=sha256_text(canonical),
        )
        manifest_payload = manifest.to_dict()
        validate_or_raise(manifest_payload, "trace_rewrite_manifest.schema.json")
        manifest_output = Path(manifest_path) if manifest_path is not None else output.with_suffix(output.suffix + ".manifest.json")
        manifest_output.parent.mkdir(parents=True, exist_ok=True)
        manifest_output.write_text(
            json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return manifest


def build_route_trace(
    *,
    task: TaskPacket,
    candidates: list[ExpertCard],
    chosen: ExpertCard | None,
    admission_reports: list[AdmissionReport],
    verifier_reports: list[dict[str, Any]] | None = None,
    router_version: str = "aem-poc-router-v0",
) -> RouteTrace:
    return RouteTrace(
        trace_id=f"trace:{task.task_id}",
        task_id=task.task_id,
        task_type=task.task_type,
        router_version=router_version,
        candidate_experts=tuple(card.expert_id for card in candidates),
        chosen_expert=chosen.expert_id if chosen else None,
        admission_reports=tuple(asdict(report) for report in admission_reports),
        verifier_reports=tuple(verifier_reports or ()),
    )
