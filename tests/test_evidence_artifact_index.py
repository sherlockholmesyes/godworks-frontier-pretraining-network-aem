import json
import unittest
from pathlib import Path

from aem_poc.evidence_artifact_index import (
    EVIDENCE_METADATA_REPORT_ARTIFACT,
    METADATA_RUN_DIR,
    SECOND_STAGE_SEAL_MANIFEST_ARTIFACT,
    SECOND_STAGE_VERIFY_REPORT_ARTIFACT,
    UPLOAD_RUN_DIR,
    build_artifact_index,
    source_artifact_paths,
)
from aem_poc.evidence_pipeline import SEALED_ARTIFACTS
from aem_poc.schema_validation import structural_validate, validate_json_file


RUN_DIR = "runs/patch_gate_demo"


def _pipeline_paths(names: tuple[str, ...]) -> set[str]:
    return {f"{RUN_DIR}/{name}" for name in names}


class EvidenceArtifactIndexTest(unittest.TestCase):
    def test_machine_readable_artifact_index_is_valid_and_complete(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        index_path = repo_root / "docs" / "evidence_artifact_index.json"
        validation = validate_json_file(index_path, "evidence_artifact_index.schema.json")
        data = json.loads(index_path.read_text(encoding="utf-8"))
        paths = [artifact["path"] for artifact in data["artifacts"]]
        expected_paths = set(source_artifact_paths())

        self.assertTrue(validation.ok)
        self.assertEqual(data["artifact_count"], len(data["artifacts"]))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(set(paths), expected_paths)
        self.assertEqual(data["artifact_count"], 13)
        for artifact in data["artifacts"]:
            self.assertIsInstance(artifact["seal_stage"], str)
            self.assertIsInstance(artifact["role"], str)
            self.assertTrue(artifact["seal_stage"])
            self.assertTrue(artifact["role"])

    def test_structural_fallback_accepts_generated_artifact_index(self) -> None:
        result = structural_validate("evidence_artifact_index.schema.json", build_artifact_index())

        self.assertTrue(result.ok)
        self.assertEqual(result.mode, "structural")

    def test_structural_fallback_rejects_old_artifact_index_shape_without_seal_role(self) -> None:
        old_shape = {
            "index_version": "old",
            "artifact_count": 1,
            "artifacts": [
                {
                    "path": "runs/patch_gate_demo/trace_report.json",
                    "producer": "producer",
                    "schema": "trace_report.schema.json",
                    "verifier": "verifier",
                    "purpose": "purpose",
                }
            ],
        }
        result = structural_validate("evidence_artifact_index.schema.json", old_shape)

        self.assertFalse(result.ok)
        self.assertIn(
            "artifacts must be list[{path, producer, schema, verifier, purpose, seal_stage, role}]",
            result.errors,
        )

    def test_machine_readable_artifact_index_marks_every_first_stage_sealed_artifact(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        index_path = repo_root / "docs" / "evidence_artifact_index.json"
        data = json.loads(index_path.read_text(encoding="utf-8"))
        by_path = {artifact["path"]: artifact for artifact in data["artifacts"]}

        for path in _pipeline_paths(SEALED_ARTIFACTS):
            self.assertIn(path, by_path)
            self.assertIn("evidence_seal_verify", by_path[path]["verifier"])
            self.assertEqual(by_path[path]["seal_stage"], "first_stage_trace_seal")
            self.assertEqual(by_path[path]["role"], "sealed_trace_evidence")

    def test_machine_readable_artifact_index_includes_metadata_and_upload_stage(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        index_path = repo_root / "docs" / "evidence_artifact_index.json"
        data = json.loads(index_path.read_text(encoding="utf-8"))
        by_path = {artifact["path"]: artifact for artifact in data["artifacts"]}
        metadata_path = f"{METADATA_RUN_DIR}/{EVIDENCE_METADATA_REPORT_ARTIFACT}"
        second_stage_path = f"{UPLOAD_RUN_DIR}/{SECOND_STAGE_SEAL_MANIFEST_ARTIFACT}"
        terminal_path = f"{UPLOAD_RUN_DIR}/{SECOND_STAGE_VERIFY_REPORT_ARTIFACT}"

        self.assertIn(metadata_path, by_path)
        self.assertIn(second_stage_path, by_path)
        self.assertIn(terminal_path, by_path)
        self.assertIn("evidence_second_stage_seal_verify", by_path[metadata_path]["verifier"])
        self.assertIn("evidence_second_stage_seal_verify", by_path[second_stage_path]["verifier"])
        self.assertIn("terminal_verification_receipts", by_path[terminal_path]["verifier"])
        self.assertEqual(by_path[metadata_path]["seal_stage"], "second_stage_upload_receipt_seal")
        self.assertEqual(by_path[metadata_path]["role"], "pre_evidence_metadata_receipt")
        self.assertEqual(by_path[second_stage_path]["seal_stage"], "second_stage_upload_receipt_seal_manifest")
        self.assertEqual(by_path[second_stage_path]["role"], "second_stage_seal_manifest")
        self.assertEqual(by_path[terminal_path]["seal_stage"], "terminal_receipt_boundary")
        self.assertEqual(by_path[terminal_path]["role"], "terminal_second_stage_verify_receipt")


if __name__ == "__main__":
    unittest.main()
