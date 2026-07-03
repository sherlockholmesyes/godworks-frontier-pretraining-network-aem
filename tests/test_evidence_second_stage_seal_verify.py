import json
import tempfile
import unittest
from pathlib import Path

from aem_poc.evidence_second_stage_seal import (
    SECOND_STAGE_SEAL_MANIFEST_ARTIFACT,
    write_second_stage_seal_manifest,
)
from aem_poc.evidence_second_stage_seal_verify import (
    EVIDENCE_SECOND_STAGE_VERIFY_REPORT_ARTIFACT,
    main,
    validate_second_stage_verify_report,
    verify_second_stage_seal,
    write_second_stage_verify_report,
)


class EvidenceSecondStageSealVerifyTest(unittest.TestCase):
    def _write_receipts_and_manifest(self, root: Path) -> tuple[Path, Path, Path]:
        metadata_report = root / "runs" / "metadata" / "evidence_metadata_report.json"
        seal_verify_report = root / "runs" / "patch_gate_demo" / "evidence_seal_verify_report.json"
        first_stage_seal = root / "runs" / "patch_gate_demo" / "evidence_seal_manifest.json"
        manifest = root / "runs" / "upload" / SECOND_STAGE_SEAL_MANIFEST_ARTIFACT
        metadata_report.parent.mkdir(parents=True, exist_ok=True)
        seal_verify_report.parent.mkdir(parents=True, exist_ok=True)
        first_stage_seal.parent.mkdir(parents=True, exist_ok=True)
        metadata_report.write_text('{"metadata": true}\n', encoding="utf-8")
        seal_verify_report.write_text('{"seal_verify": true}\n', encoding="utf-8")
        first_stage_seal.write_text('{"stage": "first"}\n', encoding="utf-8")
        write_second_stage_seal_manifest(
            manifest,
            metadata_report_path=metadata_report,
            seal_verify_report_path=seal_verify_report,
            first_stage_seal_path=first_stage_seal,
        )
        return metadata_report, seal_verify_report, manifest

    def test_verify_second_stage_seal_accepts_unchanged_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _metadata_report, _seal_verify_report, manifest = self._write_receipts_and_manifest(Path(tmp))
            report = verify_second_stage_seal(manifest)
            code = main([str(manifest)])

        self.assertTrue(report["ok"])
        self.assertEqual(report["failure_count"], 0)
        self.assertEqual(report["checked_count"], 2)
        self.assertEqual(code, 0)
        validate_second_stage_verify_report(report)

    def test_write_second_stage_verify_report_outputs_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _metadata_report, _seal_verify_report, manifest = self._write_receipts_and_manifest(root)
            output = root / "runs" / "upload" / EVIDENCE_SECOND_STAGE_VERIFY_REPORT_ARTIFACT
            report = write_second_stage_verify_report(manifest, output)
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(saved, report)
        self.assertTrue(saved["ok"])
        validate_second_stage_verify_report(saved)

    def test_cli_writes_second_stage_verify_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _metadata_report, _seal_verify_report, manifest = self._write_receipts_and_manifest(root)
            output = root / "runs" / "upload" / EVIDENCE_SECOND_STAGE_VERIFY_REPORT_ARTIFACT
            code = main([str(manifest), "--output", str(output)])
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertTrue(saved["ok"])
        validate_second_stage_verify_report(saved)

    def test_verify_second_stage_seal_rejects_changed_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            metadata_report, _seal_verify_report, manifest = self._write_receipts_and_manifest(Path(tmp))
            metadata_report.write_text("changed", encoding="utf-8")
            report = verify_second_stage_seal(manifest)
            code = main([str(manifest)])

        self.assertFalse(report["ok"])
        self.assertGreaterEqual(report["failure_count"], 1)
        self.assertEqual(code, 1)

    def test_verify_second_stage_seal_rejects_missing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _metadata_report, seal_verify_report, manifest = self._write_receipts_and_manifest(Path(tmp))
            seal_verify_report.unlink()
            report = verify_second_stage_seal(manifest)
            code = main([str(manifest)])

        self.assertFalse(report["ok"])
        self.assertGreaterEqual(report["failure_count"], 1)
        self.assertEqual(code, 1)

    def test_verify_second_stage_seal_accepts_flattened_download_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata_report, seal_verify_report, manifest = self._write_receipts_and_manifest(root)
            flat = root / "flat"
            flat.mkdir()
            flat_manifest = flat / SECOND_STAGE_SEAL_MANIFEST_ARTIFACT
            flat_metadata = flat / metadata_report.name
            flat_seal_verify = flat / seal_verify_report.name
            flat_manifest.write_text(manifest.read_text(encoding="utf-8"), encoding="utf-8")
            flat_metadata.write_text(metadata_report.read_text(encoding="utf-8"), encoding="utf-8")
            flat_seal_verify.write_text(seal_verify_report.read_text(encoding="utf-8"), encoding="utf-8")
            report = verify_second_stage_seal(flat_manifest)

        self.assertTrue(report["ok"])
        self.assertEqual(report["failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
