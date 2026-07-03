import json
import tempfile
import unittest
from pathlib import Path

from aem_poc.protocol import TaskPacket
from aem_poc.schema_validation import SchemaValidationError, validate_data, validate_json_file
from aem_poc.trace_store import RouteTrace, TraceReplayError, TraceStore, build_route_trace


class RouteTraceValidationTest(unittest.TestCase):
    def test_valid_route_trace_validates_and_writes(self) -> None:
        task = TaskPacket(task_id="t1", task_type="code_patch", prompt="x")
        trace = build_route_trace(
            task=task,
            candidates=[],
            chosen=None,
            admission_reports=[],
            verifier_reports=[{"kind": "demo"}],
        )
        result = validate_data(trace.to_dict(), "route_trace.schema.json")
        self.assertTrue(result.ok)

        with tempfile.TemporaryDirectory() as tmp:
            store = TraceStore(Path(tmp) / "trace.jsonl")
            store.append(trace)
            rows = store.read_all(validate=True)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["task_id"], "t1")

    def test_invalid_route_trace_rejected_before_write(self) -> None:
        trace = RouteTrace(
            trace_id="trace-bad",
            task_id="t-bad",
            task_type="code_patch",
            router_version="router",
            candidate_experts=("ok",),
            chosen_expert=123,  # type: ignore[arg-type]
            admission_reports=(),
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.jsonl"
            store = TraceStore(path)
            with self.assertRaises(SchemaValidationError):
                store.append(trace)
            self.assertFalse(path.exists())

    def test_replay_rejects_old_malformed_schema_row(self) -> None:
        bad_row = {
            "trace_id": "bad-old-row",
            "task_id": "t-old",
            "task_type": "code_patch",
            "router_version": "router",
            "candidate_experts": "not-a-list",
            "created_at": "now",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.jsonl"
            path.write_text(json.dumps(bad_row) + "\n", encoding="utf-8")
            store = TraceStore(path)
            self.assertEqual(len(store.read_all(validate=False)), 1)
            with self.assertRaises(TraceReplayError):
                store.read_all(validate=True)

    def test_replay_rejects_invalid_jsonl_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.jsonl"
            path.write_text("not-json\n", encoding="utf-8")
            store = TraceStore(path)
            with self.assertRaises(TraceReplayError):
                store.read_all(validate=True)

    def test_rewrite_canonical_preserves_rows_hashes_and_manifest_file(self) -> None:
        task = TaskPacket(task_id="t-rewrite", task_type="code_patch", prompt="x")
        trace = build_route_trace(
            task=task,
            candidates=[],
            chosen=None,
            admission_reports=[],
            verifier_reports=[{"kind": "demo"}],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "trace.jsonl"
            output = Path(tmp) / "trace.compact.jsonl"
            manifest_path = Path(str(output) + ".manifest.json")
            store = TraceStore(source)
            store.append(trace)
            manifest = store.rewrite_canonical(output)
            compact_store = TraceStore(output)
            rows = compact_store.read_all(validate=True)
            manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_validation = validate_json_file(
                manifest_path,
                "trace_rewrite_manifest.schema.json",
            )

        self.assertEqual(manifest.row_count, 1)
        self.assertEqual(manifest_data["row_count"], 1)
        self.assertTrue(manifest_validation.ok)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["task_id"], "t-rewrite")
        self.assertEqual(len(manifest.source_hash), 64)
        self.assertEqual(len(manifest.output_hash), 64)
        self.assertEqual(len(manifest.rows_hash), 64)

    def test_rewrite_canonical_rejects_malformed_rows(self) -> None:
        bad_row = {
            "trace_id": "bad-old-row",
            "task_id": "t-old",
            "task_type": "code_patch",
            "router_version": "router",
            "candidate_experts": "not-a-list",
            "created_at": "now",
        }
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "trace.jsonl"
            output = Path(tmp) / "trace.compact.jsonl"
            manifest_path = Path(str(output) + ".manifest.json")
            source.write_text(json.dumps(bad_row) + "\n", encoding="utf-8")
            store = TraceStore(source)
            with self.assertRaises(TraceReplayError):
                store.rewrite_canonical(output)
            self.assertFalse(output.exists())
            self.assertFalse(manifest_path.exists())


if __name__ == "__main__":
    unittest.main()
