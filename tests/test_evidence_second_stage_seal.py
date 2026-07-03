import json
import tempfile
import unittest
from pathlib import Path

from aem_poc.evidence_second_stage_seal import (
    SECOND_STAGE_SEAL_MANIFEST_ARTIFACT,
    main,
    second_stage_seal_manifest,
    validate_second_stage_manifest,
    write_second_stage_seal_manifest,
)
from aem_poc.schema_validation import SchemaValidationError


class EvidenceSecondStageSealTest(unittest.TestCase):
    def _write_receipts(self, root: Path) -> tuple[Path, Path, Path, Path]:
        metadata_report = root / "runs" / "metadata" / "evidence_metadata_report.json"
        seal_verify_report = root / "runs" / "patch_gate_demo" / "evidence_seal_verify_report.json"
        first_stage_seal = root / "runs" / "patch_gate_demo" / "evidence_seal_manifest.json"
        output = root / "runs" / "upload" / SECOND_STAGE_SEAL_MANIFEST_ARTIFACT
        metadata_report.parent.mkdir(parents=True, exist_ok=True)
        seal_verify_report.parent.mkdir(parents=True, exist_ok=True)
        first_stage_seal.parent.mkdir(parents=True, exist_ok=True)
        metadata_report.write_text('{"ok": true}\n', encoding="utf-8")
        seal_verify_report.write_text('{"ok": true}\n', encoding="utf-8")
        first_stage_seal.write_text('{"stage": "first"}\n', encoding="utf-8")
        return metadata_report, seal_verify_report, first_stage_seal, output

    def test_second_stage_manifest_seals_metadata_and_post_seal_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            metadata_report, seal_verify_report, first_stage_seal, output = self._write_receipts(Path(tmp))
            manifest = second_stage_seal_manifest(
                metadata_report_path=metadata_report,
                seal_verify_report_path=seal_verify_report,
                first_stage_seal_path=first_stage_seal,
                output_path=output,
            )

        paths = {artifact["path"] for artifact in manifest["sealed_artifacts"]}
        roles = {artifact["role"] for artifact in manifest["sealed_artifacts"]}
        self.assertEqual(paths, {str(metadata_report), str(seal_verify_report)})
        self.assertEqual(roles, {"pre_evidence_metadata_receipt", "post_seal_verification_receipt"})
        self.assertEqual(manifest["excluded_artifacts"], [str(output)])
        self.assertEqual(manifest["artifact_count"], 2)
        validate_second_stage_manifest(manifest)

    def test_write_second_stage_manifest_outputs_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            metadata_report, seal_verify_report, first_stage_seal, output = self._write_receipts(Path(tmp))
            manifest = write_second_stage_seal_manifest(
                output,
                metadata_report_path=metadata_report,
                seal_verify_report_path=seal_verify_report,
                first_stage_seal_path=first_stage_seal,
            )
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(saved, manifest)
        validate_second_stage_manifest(saved)

    def test_second_stage_manifest_fails_when_receipt_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            metadata_report, seal_verify_report, first_stage_seal, output = self._write_receipts(Path(tmp))
            seal_verify_report.unlink()
            with self.assertRaises(FileNotFoundError):
                second_stage_seal_manifest(
                    metadata_report_path=metadata_report,
                    seal_verify_report_path=seal_verify_report,
                    first_stage_seal_path=first_stage_seal,
                    output_path=output,
                )

    def test_second_stage_manifest_shape_rejects_bad_data(self) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_second_stage_manifest({"stage": "bad"})

    def test_cli_writes_second_stage_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            metadata_report, seal_verify_report, first_stage_seal, output = self._write_receipts(Path(tmp))
            code = main([
                "--metadata-report", str(metadata_report),
                "--seal-verify-report", str(seal_verify_report),
                "--first-stage-seal", str(first_stage_seal),
                "--output", str(output),
            ])
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertEqual(saved["artifact_count"], 2)
        validate_second_stage_manifest(saved)


if __name__ == "__main__":
    unittest.main()
