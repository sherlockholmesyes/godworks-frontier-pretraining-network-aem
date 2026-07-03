import tempfile
import unittest
from pathlib import Path

from aem_poc.evidence_pipeline import (
    EVIDENCE_SEAL_MANIFEST_ARTIFACT,
    SEALED_ARTIFACTS,
    write_evidence_seal_manifest,
)
from aem_poc.evidence_seal_verify import (
    EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT,
    main,
    verify_evidence_seal,
    write_evidence_seal_verify_report,
)
from aem_poc.schema_validation import validate_data, validate_json_file


class EvidenceSealVerifyTest(unittest.TestCase):
    def _write_complete_sealed_set(self, root: Path) -> Path:
        for name in SEALED_ARTIFACTS:
            (root / name).write_text(name, encoding="utf-8")
        manifest_path = root / EVIDENCE_SEAL_MANIFEST_ARTIFACT
        write_evidence_seal_manifest(root, manifest_path)
        return manifest_path

    def test_verify_evidence_seal_accepts_unchanged_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_sealed_set(root)
            report = verify_evidence_seal(manifest_path)
            code = main([str(manifest_path)])

        self.assertTrue(report["ok"])
        self.assertEqual(report["failure_count"], 0)
        self.assertTrue(validate_data(report, "evidence_seal_verify_report.schema.json").ok)
        self.assertEqual(code, 0)

    def test_write_evidence_seal_verify_report_outputs_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_sealed_set(root)
            output = root / EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
            report = write_evidence_seal_verify_report(manifest_path, output)
            exists = output.exists()
            validation = validate_json_file(output, "evidence_seal_verify_report.schema.json")

        self.assertTrue(report["ok"])
        self.assertTrue(exists)
        self.assertTrue(validation.ok)

    def test_cli_writes_evidence_seal_verify_report_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_sealed_set(root)
            output = root / EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
            code = main([str(manifest_path), str(output)])
            exists = output.exists()
            validation = validate_json_file(output, "evidence_seal_verify_report.schema.json")

        self.assertEqual(code, 0)
        self.assertTrue(exists)
        self.assertTrue(validation.ok)

    def test_verify_evidence_seal_rejects_changed_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_sealed_set(root)
            (root / "pipeline_result.json").write_text("changed", encoding="utf-8")
            report = verify_evidence_seal(manifest_path)
            code = main([str(manifest_path)])

        self.assertFalse(report["ok"])
        self.assertGreaterEqual(report["failure_count"], 1)
        self.assertEqual(code, 1)

    def test_verify_evidence_seal_rejects_missing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = self._write_complete_sealed_set(root)
            (root / "trace_report.json").unlink()
            report = verify_evidence_seal(manifest_path)
            code = main([str(manifest_path)])

        self.assertFalse(report["ok"])
        self.assertGreaterEqual(report["failure_count"], 1)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
