import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from aem_poc.evidence_artifact_index import source_artifact_paths
from aem_poc.evidence_status import (
    DEFAULT_STATUS_EXAMPLE_PATH,
    build_evidence_status,
    docs_check_gates,
    docs_sync_gates,
    evidence_status_example_report,
    local_ci_gates,
    main,
    sync_evidence_status_example,
    validate_evidence_status,
    write_evidence_status,
)


class EvidenceStatusTest(unittest.TestCase):
    def test_build_evidence_status_summarizes_current_sources(self) -> None:
        status = build_evidence_status()

        validate_evidence_status(status)
        self.assertEqual(status["local_ci_command"], "make evidence-local-ci")
        self.assertIn("evidence-status", status["local_ci_gates"])
        self.assertEqual(status["docs_check_command"], "make evidence-docs-check")
        self.assertEqual(status["docs_sync_command"], "make evidence-docs-sync")
        self.assertEqual(status["docs_check_gates"], docs_check_gates())
        self.assertEqual(status["docs_sync_gates"], docs_sync_gates())
        self.assertNotIn("evidence-docs-check", status["local_ci_gates"])
        self.assertEqual(status["artifact_index"]["artifact_count"], 13)
        self.assertEqual(status["artifact_index"]["paths"], list(source_artifact_paths()))
        self.assertEqual(len(status["artifacts"]), 13)
        self.assertIn("first_stage_trace_seal", status["artifact_index"]["seal_stage_counts"])
        self.assertIn("terminal_receipt_boundary", status["artifact_index"]["seal_stage_counts"])
        self.assertTrue(status["upload_drift"]["ok"])
        self.assertTrue(status["upload_drift"]["markers_present"])

    def test_checked_in_status_example_matches_generated_status(self) -> None:
        report = evidence_status_example_report(DEFAULT_STATUS_EXAMPLE_PATH)

        self.assertTrue(report["exists"])
        self.assertTrue(report["matches_generated"])
        self.assertTrue(report["ok"])
        self.assertEqual(report["generated_artifact_count"], 13)

    def test_local_ci_gates_reads_makefile_order(self) -> None:
        self.assertEqual(
            local_ci_gates(),
            [
                "test",
                "evidence-artifact-index",
                "evidence-artifact-index-md-check",
                "evidence-status",
                "evidence-metadata-check",
                "evidence-upload-policy",
                "evidence-upload-drift",
                "evidence-seal-verify-demo",
                "evidence-second-stage-seal",
                "evidence-second-stage-seal-verify",
            ],
        )

    def test_docs_gate_helpers_read_makefile_order(self) -> None:
        self.assertEqual(
            docs_check_gates(),
            [
                "evidence-artifact-index",
                "evidence-artifact-index-md-check",
                "evidence-status-example-check",
            ],
        )
        self.assertEqual(
            docs_sync_gates(),
            [
                "evidence-artifact-index-sync",
                "evidence-artifact-index-md-sync",
                "evidence-status-example-sync",
            ],
        )

    def test_write_evidence_status_outputs_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "status.json"
            status = write_evidence_status(output)
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(saved, status)
        validate_evidence_status(saved)

    def test_sync_evidence_status_example_outputs_generated_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "status.example.json"
            report = sync_evidence_status_example(output)
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertTrue(report["ok"])
        self.assertTrue(report["changed"])
        self.assertEqual(saved, build_evidence_status())

    def test_cli_prints_status(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main([])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertEqual(data["local_ci_command"], "make evidence-local-ci")
        self.assertEqual(data["docs_check_command"], "make evidence-docs-check")
        self.assertTrue(data["upload_drift"]["ok"])

    def test_cli_writes_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "status.json"
            out = StringIO()
            with redirect_stdout(out):
                code = main(["--output", str(output)])
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertEqual(saved, json.loads(out.getvalue()))
        validate_evidence_status(saved)

    def test_cli_checks_status_example(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main(["--check-example"])
        data = json.loads(out.getvalue())

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertTrue(data["matches_generated"])

    def test_cli_syncs_status_example(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "status.example.json"
            out = StringIO()
            with redirect_stdout(out):
                code = main(["--example", str(output), "--sync-example"])
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertEqual(saved, build_evidence_status())
        self.assertTrue(json.loads(out.getvalue())["ok"])


if __name__ == "__main__":
    unittest.main()
