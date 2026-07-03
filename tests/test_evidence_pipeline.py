import tempfile
import unittest
from pathlib import Path

from aem_poc.evidence_pipeline import (
    EVIDENCE_SEAL_MANIFEST_ARTIFACT,
    GENERATED_ARTIFACTS,
    SEALED_ARTIFACTS,
    evidence_seal_manifest,
    main,
    run_evidence_pipeline,
)
from aem_poc.schema_validation import validate_data, validate_json_file


class EvidencePipelineTest(unittest.TestCase):
    def test_run_evidence_pipeline_writes_all_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "evidence"
            result = run_evidence_pipeline(run_dir)
            artifacts_exist = [(run_dir / name).exists() for name in GENERATED_ARTIFACTS]
            verify_validation = validate_json_file(
                run_dir / "evidence_verify_report.json",
                "evidence_verify_report.schema.json",
            )
            bundle_validation = validate_json_file(
                run_dir / "evidence_bundle_manifest.json",
                "evidence_bundle_manifest.schema.json",
            )
            pipeline_validation = validate_json_file(
                run_dir / "pipeline_result.json",
                "evidence_pipeline_result.schema.json",
            )
            seal_validation = validate_json_file(
                run_dir / EVIDENCE_SEAL_MANIFEST_ARTIFACT,
                "evidence_seal_manifest.schema.json",
            )
            seal_manifest = evidence_seal_manifest(run_dir)

        self.assertTrue(result["ok"])
        self.assertIn(str(run_dir / "pipeline_result.json"), result["artifacts"])
        self.assertIn(str(run_dir / EVIDENCE_SEAL_MANIFEST_ARTIFACT), result["artifacts"])
        self.assertTrue(all(artifacts_exist))
        self.assertTrue(verify_validation.ok)
        self.assertTrue(bundle_validation.ok)
        self.assertTrue(pipeline_validation.ok)
        self.assertTrue(seal_validation.ok)
        self.assertTrue(validate_data(seal_manifest, "evidence_seal_manifest.schema.json").ok)
        self.assertEqual(seal_manifest["artifact_count"], len(SEALED_ARTIFACTS))
        self.assertEqual(len(seal_manifest["sealed_artifacts"]), len(SEALED_ARTIFACTS))
        self.assertEqual(
            seal_manifest["excluded_artifacts"],
            [str(run_dir / EVIDENCE_SEAL_MANIFEST_ARTIFACT)],
        )

    def test_pipeline_cli_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code = main([str(Path(tmp) / "evidence")])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
