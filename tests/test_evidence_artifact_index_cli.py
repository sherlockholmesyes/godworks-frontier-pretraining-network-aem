import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from aem_poc.evidence_artifact_index import (
    DEFAULT_MARKDOWN_INDEX_PATH,
    artifact_by_path,
    artifact_paths,
    build_artifact_index,
    main,
    markdown_matches_generated,
    render_markdown_index,
    validation_summary,
    write_artifact_index,
    write_markdown_index,
)
from aem_poc.schema_validation import validate_json_file


class EvidenceArtifactIndexCliTest(unittest.TestCase):
    def test_validation_summary_accepts_default_index(self) -> None:
        summary = validation_summary()
        self.assertTrue(summary["ok"])
        self.assertTrue(summary["matches_generated"])
        self.assertEqual(summary["artifact_count"], 13)
        self.assertEqual(summary["unique_path_count"], 13)

    def test_default_markdown_index_matches_generated(self) -> None:
        self.assertTrue(markdown_matches_generated(DEFAULT_MARKDOWN_INDEX_PATH))

    def test_artifact_paths_lists_default_index_paths(self) -> None:
        paths = artifact_paths()
        self.assertIn("runs/patch_gate_demo/evidence_seal_manifest.json", paths)
        self.assertIn("runs/metadata/evidence_metadata_report.json", paths)
        self.assertIn("runs/upload/evidence_second_stage_verify_report.json", paths)
        self.assertEqual(len(paths), 13)

    def test_artifact_by_path_accepts_exact_path_and_filename(self) -> None:
        exact = artifact_by_path("runs/patch_gate_demo/pipeline_result.json")
        by_name = artifact_by_path("pipeline_result.json")
        self.assertEqual(exact["path"], "runs/patch_gate_demo/pipeline_result.json")
        self.assertEqual(by_name["path"], exact["path"])

    def test_cli_validate_and_list(self) -> None:
        validate_out = StringIO()
        with redirect_stdout(validate_out):
            validate_code = main(["validate"])
        list_out = StringIO()
        with redirect_stdout(list_out):
            list_code = main(["list"])

        self.assertEqual(validate_code, 0)
        self.assertIn('"ok": true', validate_out.getvalue())
        self.assertIn('"matches_generated": true', validate_out.getvalue())
        self.assertEqual(list_code, 0)
        self.assertIn("runs/patch_gate_demo/trace_report.json", list_out.getvalue())
        self.assertIn("runs/upload/evidence_second_stage_seal_manifest.json", list_out.getvalue())

    def test_cli_show_by_filename(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main(["show", "trace_report.json"])

        self.assertEqual(code, 0)
        self.assertIn('"schema": "trace_report.schema.json"', out.getvalue())

    def test_write_artifact_index_outputs_generated_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "index.json"
            generated = write_artifact_index(index_path)
            saved = json.loads(index_path.read_text(encoding="utf-8"))
            validation = validate_json_file(index_path, "evidence_artifact_index.schema.json")

        self.assertEqual(saved, generated)
        self.assertEqual(saved, build_artifact_index())
        self.assertTrue(validation.ok)

    def test_write_markdown_index_outputs_generated_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            markdown_path = Path(tmp) / "index.md"
            generated = write_markdown_index(markdown_path)
            saved = markdown_path.read_text(encoding="utf-8")

        self.assertEqual(saved, generated)
        self.assertEqual(saved, render_markdown_index())

    def test_cli_sync_outputs_generated_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "index.json"
            out = StringIO()
            with redirect_stdout(out):
                code = main(["--index", str(index_path), "sync"])
            saved = json.loads(index_path.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertEqual(saved, build_artifact_index())
        self.assertIn('"ok": true', out.getvalue())

    def test_cli_markdown_sync_and_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            markdown_path = Path(tmp) / "index.md"
            sync_out = StringIO()
            with redirect_stdout(sync_out):
                sync_code = main(["--markdown", str(markdown_path), "md-sync"])
            check_out = StringIO()
            with redirect_stdout(check_out):
                check_code = main(["--markdown", str(markdown_path), "md-check"])

        self.assertEqual(sync_code, 0)
        self.assertEqual(check_code, 0)
        self.assertIn('"ok": true', sync_out.getvalue())
        self.assertIn('"matches_generated": true', check_out.getvalue())

    def test_custom_index_can_validate_schema_but_not_generated_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "index.json"
            index_path.write_text(
                '{"index_version":"test","artifact_count":0,"artifacts":[]}',
                encoding="utf-8",
            )
            schema_validation = validate_json_file(index_path, "evidence_artifact_index.schema.json")
            summary = validation_summary(index_path)

        self.assertTrue(schema_validation.ok)
        self.assertFalse(summary["ok"])
        self.assertFalse(summary["matches_generated"])
        self.assertEqual(summary["artifact_count"], 0)


if __name__ == "__main__":
    unittest.main()
