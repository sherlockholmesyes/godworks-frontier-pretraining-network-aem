import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from aem_poc.evidence_artifact_index import DEFAULT_INDEX_PATH
from aem_poc.evidence_metadata_check import (
    EVIDENCE_METADATA_REPORT_ARTIFACT,
    artifact_index_drift_report,
    main,
    metadata_check,
    validate_metadata_report,
    write_metadata_report,
)


class EvidenceMetadataCheckTest(unittest.TestCase):
    def test_metadata_check_accepts_default_indexes(self) -> None:
        report = metadata_check()

        self.assertTrue(report["ok"])
        self.assertTrue(report["json_index"]["ok"])
        self.assertTrue(report["markdown_index"]["ok"])
        self.assertTrue(report["artifact_drift"]["ok"])
        validate_metadata_report(report)

    def test_artifact_index_drift_report_accepts_default_index(self) -> None:
        report = artifact_index_drift_report(DEFAULT_INDEX_PATH)

        self.assertTrue(report["ok"])
        self.assertEqual(report["missing_paths"], [])
        self.assertEqual(report["extra_paths"], [])
        self.assertEqual(report["sealed_without_verifier"], [])

    def test_write_metadata_report_outputs_json_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / EVIDENCE_METADATA_REPORT_ARTIFACT
            report = write_metadata_report(output)
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(saved, report)
        self.assertTrue(saved["ok"])
        validate_metadata_report(saved)

    def test_metadata_check_rejects_markdown_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            markdown_path = Path(tmp) / "index.md"
            markdown_path.write_text("stale", encoding="utf-8")
            report = metadata_check(markdown_path=markdown_path)

        self.assertFalse(report["ok"])
        self.assertFalse(report["markdown_index"]["ok"])
        self.assertTrue(report["json_index"]["ok"])

    def test_cli_returns_zero_for_default_indexes(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main([])

        self.assertEqual(code, 0)
        self.assertIn('"ok": true', out.getvalue())
        self.assertIn('"artifact_drift"', out.getvalue())

    def test_cli_writes_metadata_report_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / EVIDENCE_METADATA_REPORT_ARTIFACT
            out = StringIO()
            with redirect_stdout(out):
                code = main(["--output", str(output)])
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertTrue(saved["ok"])
        self.assertIn('"ok": true', out.getvalue())
        validate_metadata_report(saved)


if __name__ == "__main__":
    unittest.main()
