import tempfile
import unittest
from pathlib import Path

from aem_poc.evidence_demo import (
    EVIDENCE_BUNDLE_MANIFEST_ARTIFACT,
    EXPECTED_ARTIFACTS,
    write_evidence_bundle_manifest,
    write_evidence_summary,
)
from aem_poc.evidence_verify import (
    EVIDENCE_VERIFY_REPORT_ARTIFACT,
    main,
    verify_evidence_bundle,
    write_evidence_verify_report,
)
from aem_poc.schema_validation import validate_data, validate_json_file


class EvidenceVerifyTest(unittest.TestCase):
    def _write_complete_bundle(self, root: Path) -> Path:
        for name in EXPECTED_ARTIFACTS:
            (root / name).write_text(name, encoding="utf-8")
        summary_path = root / "evidence_summary.json"
        manifest_path = root / EVIDENCE_BUNDLE_MANIFEST_ARTIFACT
        write_evidence_summary(root, summary_path)
        write_evidence_bundle_manifest(root, manifest_path, summary_path=summary_path)
        return manifest_path

    def test_verify_evidence_bundle_accepts_unchanged_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_bundle(root)
            report = verify_evidence_bundle(manifest_path)
            code = main([str(manifest_path)])

        self.assertTrue(report["ok"])
        self.assertEqual(report["failure_count"], 0)
        self.assertTrue(validate_data(report, "evidence_verify_report.schema.json").ok)
        self.assertEqual(code, 0)

    def test_write_evidence_verify_report_outputs_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_bundle(root)
            output = root / EVIDENCE_VERIFY_REPORT_ARTIFACT
            report = write_evidence_verify_report(manifest_path, output)
            exists = output.exists()
            validation = validate_json_file(output, "evidence_verify_report.schema.json")

        self.assertTrue(report["ok"])
        self.assertTrue(exists)
        self.assertTrue(validation.ok)

    def test_cli_writes_evidence_verify_report_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_bundle(root)
            output = root / EVIDENCE_VERIFY_REPORT_ARTIFACT
            code = main([str(manifest_path), str(output)])
            exists = output.exists()
            validation = validate_json_file(output, "evidence_verify_report.schema.json")

        self.assertEqual(code, 0)
        self.assertTrue(exists)
        self.assertTrue(validation.ok)

    def test_verify_evidence_bundle_rejects_tampered_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_bundle(root)
            (root / "trace_report.json").write_text("tampered", encoding="utf-8")
            report = verify_evidence_bundle(manifest_path)
            code = main([str(manifest_path)])

        self.assertFalse(report["ok"])
        self.assertGreaterEqual(report["failure_count"], 1)
        self.assertEqual(code, 1)

    def test_verify_evidence_bundle_rejects_missing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_bundle(root)
            (root / "route_trace.jsonl").unlink()
            report = verify_evidence_bundle(manifest_path)
            code = main([str(manifest_path)])

        self.assertFalse(report["ok"])
        self.assertGreaterEqual(report["failure_count"], 1)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
