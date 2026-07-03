import json
import tempfile
import unittest
from pathlib import Path

from aem_poc.protocol import TaskPacket
from aem_poc.schema_validation import validate_data, validate_json_file
from aem_poc.trace_maint import compact_trace, main, trace_report, write_trace_report
from aem_poc.trace_store import TraceStore, build_route_trace


class TraceMaintTest(unittest.TestCase):
    def test_compact_trace_writes_output_and_manifest(self) -> None:
        task = TaskPacket(task_id="t-maint", task_type="code_patch", prompt="x")
        trace = build_route_trace(
            task=task,
            candidates=[],
            chosen=None,
            admission_reports=[],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "route_trace.jsonl"
            output = Path(tmp) / "route_trace.compact.jsonl"
            TraceStore(source).append(trace)
            manifest = compact_trace(source, output)
            manifest_path = Path(str(output) + ".manifest.json")

            self.assertTrue(output.exists())
            self.assertTrue(manifest_path.exists())
            self.assertEqual(manifest.row_count, 1)
            self.assertTrue(validate_json_file(manifest_path, "trace_rewrite_manifest.schema.json").ok)

    def test_cli_compact_returns_zero(self) -> None:
        task = TaskPacket(task_id="t-cli", task_type="code_patch", prompt="x")
        trace = build_route_trace(
            task=task,
            candidates=[],
            chosen=None,
            admission_reports=[],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "route_trace.jsonl"
            output = Path(tmp) / "route_trace.compact.jsonl"
            TraceStore(source).append(trace)
            code = main(["compact", str(source), str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertTrue(Path(str(output) + ".manifest.json").exists())

    def test_trace_report_summarizes_valid_trace(self) -> None:
        task = TaskPacket(task_id="t-report", task_type="code_patch", prompt="x")
        trace = build_route_trace(
            task=task,
            candidates=[],
            chosen=None,
            admission_reports=[],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "route_trace.jsonl"
            TraceStore(source).append(trace)
            report = trace_report(source)

        self.assertEqual(report["row_count"], 1)
        self.assertEqual(report["task_types"], ["code_patch"])
        self.assertEqual(report["chosen_experts"], [])
        self.assertEqual(len(report["file_hash"]), 64)
        self.assertEqual(len(report["rows_hash"]), 64)
        self.assertTrue(validate_data(report, "trace_report.schema.json").ok)

    def test_write_trace_report_outputs_valid_json(self) -> None:
        task = TaskPacket(task_id="t-report-json", task_type="code_patch", prompt="x")
        trace = build_route_trace(
            task=task,
            candidates=[],
            chosen=None,
            admission_reports=[],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "route_trace.jsonl"
            output = Path(tmp) / "trace_report.json"
            TraceStore(source).append(trace)
            report = write_trace_report(source, output)
            saved = json.loads(output.read_text(encoding="utf-8"))
            validation = validate_json_file(output, "trace_report.schema.json")

        self.assertEqual(report["row_count"], 1)
        self.assertEqual(saved["row_count"], 1)
        self.assertEqual(len(saved["rows_hash"]), 64)
        self.assertTrue(validation.ok)

    def test_cli_report_returns_zero_and_can_write_json(self) -> None:
        task = TaskPacket(task_id="t-report-cli", task_type="code_patch", prompt="x")
        trace = build_route_trace(
            task=task,
            candidates=[],
            chosen=None,
            admission_reports=[],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "route_trace.jsonl"
            output = Path(tmp) / "trace_report.json"
            TraceStore(source).append(trace)
            code = main(["report", str(source), str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertTrue(validate_json_file(output, "trace_report.schema.json").ok)


if __name__ == "__main__":
    unittest.main()
