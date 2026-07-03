import json
import tempfile
import unittest
from pathlib import Path

from aem_poc.evidence_demo import (
    EVIDENCE_BUNDLE_MANIFEST_ARTIFACT,
    EXPECTED_ARTIFACTS,
    evidence_bundle_manifest,
    evidence_summary,
    main,
    write_evidence_bundle_manifest,
    write_evidence_summary,
)
from aem_poc.schema_validation import validate_data, validate_json_file


class EvidenceDemoTest(unittest.TestCase):
    def test_evidence_summary_accepts_complete_artifact_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in EXPECTED_ARTIFACTS:
                (root / name).write_text("x", encoding="utf-8")
            summary = evidence_summary(root)
            code = main([str(root)])

        self.assertEqual(summary["missing_count"], 0)
        self.assertEqual(summary["artifact_count"], len(EXPECTED_ARTIFACTS))
        self.assertTrue(validate_data(summary, "evidence_summary.schema.json").ok)
        self.assertEqual(code, 0)

    def test_evidence_summary_fails_on_missing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in EXPECTED_ARTIFACTS[:-1]:
                (root / name).write_text("x", encoding="utf-8")
            summary = evidence_summary(root)
            code = main([str(root)])

        self.assertEqual(summary["missing_count"], 1)
        self.assertTrue(validate_data(summary, "evidence_summary.schema.json").ok)
        self.assertEqual(code, 1)

    def test_write_evidence_summary_outputs_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "evidence_summary.json"
            for name in EXPECTED_ARTIFACTS:
                (root / name).write_text("x", encoding="utf-8")
            summary = write_evidence_summary(root, output)
            saved = json.loads(output.read_text(encoding="utf-8"))
            validation = validate_json_file(output, "evidence_summary.schema.json")

        self.assertEqual(summary["missing_count"], 0)
        self.assertEqual(saved["artifact_count"], len(EXPECTED_ARTIFACTS))
        self.assertTrue(validation.ok)

    def test_evidence_bundle_manifest_hashes_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary_path = root / "evidence_summary.json"
            for name in EXPECTED_ARTIFACTS:
                (root / name).write_text(name, encoding="utf-8")
            write_evidence_summary(root, summary_path)
            manifest = evidence_bundle_manifest(root, summary_path=summary_path)

        self.assertEqual(manifest["artifact_count"], len(EXPECTED_ARTIFACTS) + 1)
        self.assertTrue(validate_data(manifest, "evidence_bundle_manifest.schema.json").ok)
        for artifact in manifest["artifacts"]:
            self.assertEqual(len(artifact["sha256"]), 64)
            self.assertGreater(artifact["size_bytes"], 0)

    def test_write_evidence_bundle_manifest_outputs_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary_path = root / "evidence_summary.json"
            output = root / EVIDENCE_BUNDLE_MANIFEST_ARTIFACT
            for name in EXPECTED_ARTIFACTS:
                (root / name).write_text(name, encoding="utf-8")
            write_evidence_summary(root, summary_path)
            manifest = write_evidence_bundle_manifest(root, output, summary_path=summary_path)
            saved = json.loads(output.read_text(encoding="utf-8"))
            validation = validate_json_file(output, "evidence_bundle_manifest.schema.json")

        self.assertEqual(manifest["artifact_count"], len(EXPECTED_ARTIFACTS) + 1)
        self.assertEqual(saved["artifact_count"], len(EXPECTED_ARTIFACTS) + 1)
        self.assertTrue(validation.ok)

    def test_cli_writes_evidence_summary_and_bundle_manifest_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary_output = root / "evidence_summary.json"
            bundle_output = root / EVIDENCE_BUNDLE_MANIFEST_ARTIFACT
            for name in EXPECTED_ARTIFACTS:
                (root / name).write_text("x", encoding="utf-8")
            code = main([str(root), str(summary_output), str(bundle_output)])
            summary_exists = summary_output.exists()
            bundle_exists = bundle_output.exists()
            summary_validation = validate_json_file(summary_output, "evidence_summary.schema.json")
            bundle_validation = validate_json_file(bundle_output, "evidence_bundle_manifest.schema.json")

        self.assertEqual(code, 0)
        self.assertTrue(summary_exists)
        self.assertTrue(bundle_exists)
        self.assertTrue(summary_validation.ok)
        self.assertTrue(bundle_validation.ok)


if __name__ == "__main__":
    unittest.main()
