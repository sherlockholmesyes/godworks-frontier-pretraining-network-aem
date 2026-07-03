import unittest
from contextlib import redirect_stdout
from io import StringIO

from aem_poc.evidence_metadata_check import EVIDENCE_METADATA_REPORT_ARTIFACT
from aem_poc.evidence_pipeline import EVIDENCE_SEAL_MANIFEST_ARTIFACT, SEALED_ARTIFACTS
from aem_poc.evidence_seal_verify import EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
from aem_poc.evidence_upload_policy import (
    METADATA_RUN_DIR,
    SECOND_STAGE_SEAL_MANIFEST_ARTIFACT,
    SECOND_STAGE_VERIFY_REPORT_ARTIFACT,
    TRACE_RUN_DIR,
    UPLOAD_RUN_DIR,
    build_upload_policy,
    main,
    validate_upload_policy,
)


class EvidenceUploadPolicyTest(unittest.TestCase):
    def test_upload_policy_matches_current_seal_constants(self) -> None:
        policy = build_upload_policy()
        validate_upload_policy(policy)
        classes = policy["classes"]
        sealed_paths = {artifact["path"] for artifact in classes["sealed_trace_evidence"]}
        expected_paths = {f"{TRACE_RUN_DIR}/{name}" for name in SEALED_ARTIFACTS}

        self.assertEqual(sealed_paths, expected_paths)
        self.assertEqual(policy["seal_manifest"], f"{TRACE_RUN_DIR}/{EVIDENCE_SEAL_MANIFEST_ARTIFACT}")

    def test_metadata_and_post_seal_receipts_are_second_stage_sealed(self) -> None:
        policy = build_upload_policy()
        classes = policy["classes"]
        sealed_paths = {artifact["path"] for artifact in classes["sealed_trace_evidence"]}
        metadata_path = f"{METADATA_RUN_DIR}/{EVIDENCE_METADATA_REPORT_ARTIFACT}"
        seal_verify_path = f"{TRACE_RUN_DIR}/{EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT}"
        second_stage_path = f"{UPLOAD_RUN_DIR}/{SECOND_STAGE_SEAL_MANIFEST_ARTIFACT}"

        self.assertNotIn(metadata_path, sealed_paths)
        self.assertNotIn(seal_verify_path, sealed_paths)
        self.assertEqual(set(policy["second_stage_sealed_artifacts"]), {metadata_path, seal_verify_path})
        self.assertEqual(policy["second_stage_seal_manifest"], second_stage_path)
        self.assertEqual(classes["pre_evidence_metadata_receipts"][0]["sealed_by"], second_stage_path)
        self.assertEqual(classes["post_seal_verification_receipts"][0]["sealed_by"], second_stage_path)

    def test_second_stage_verify_report_is_terminal_receipt_not_recursively_sealed(self) -> None:
        policy = build_upload_policy()
        classes = policy["classes"]
        terminal_path = f"{UPLOAD_RUN_DIR}/{SECOND_STAGE_VERIFY_REPORT_ARTIFACT}"

        self.assertEqual(policy["terminal_receipts"], [terminal_path])
        self.assertEqual(classes["terminal_verification_receipts"][0]["path"], terminal_path)
        self.assertIsNone(classes["terminal_verification_receipts"][0]["sealed_by"])
        self.assertNotIn(terminal_path, policy["second_stage_sealed_artifacts"])

    def test_cli_prints_and_checks_policy(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main(["--check"])

        self.assertEqual(code, 0)
        self.assertIn('"pre_evidence_metadata_receipts"', out.getvalue())
        self.assertIn('"second_stage_seal_manifests"', out.getvalue())
        self.assertIn('"second_stage_sealed_artifacts"', out.getvalue())
        self.assertIn('"terminal_verification_receipts"', out.getvalue())


if __name__ == "__main__":
    unittest.main()
