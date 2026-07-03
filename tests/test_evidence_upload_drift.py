import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from aem_poc.evidence_artifact_index import source_artifact_paths
from aem_poc.evidence_upload_drift import (
    UPLOAD_PATHS_BEGIN_MARKER,
    UPLOAD_PATHS_END_MARKER,
    extract_upload_artifact_paths,
    main,
    replace_upload_artifact_paths,
    render_upload_artifact_paths,
    sync_upload_artifact_paths,
    upload_drift_report,
)


def _workflow(paths: list[str], *, markers: bool = True) -> str:
    header = [
        "name: test",
        "jobs:",
        "  x:",
        "    steps:",
        "      - name: upload",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: aem-trace-evidence",
    ]
    if markers:
        header.append(f"          {UPLOAD_PATHS_BEGIN_MARKER}")
    header.append("          path: |")
    body = [f"            {path}" for path in paths]
    if markers:
        body.append(f"          {UPLOAD_PATHS_END_MARKER}")
    return "\n".join(header + body)


def _write_workflow(root: Path, paths: list[str], *, markers: bool = True) -> Path:
    path = root / "ci.yml"
    path.write_text(_workflow(paths, markers=markers), encoding="utf-8")
    return path


class EvidenceUploadDriftTest(unittest.TestCase):
    def test_ci_upload_paths_match_artifact_index_path_set(self) -> None:
        report = upload_drift_report()

        self.assertTrue(report["ok"])
        self.assertTrue(report["markers_present"])
        self.assertEqual(set(report["ci_upload_paths"]), set(source_artifact_paths()))
        self.assertEqual(report["missing_from_ci"], [])
        self.assertEqual(report["extra_in_ci"], [])
        self.assertEqual(report["duplicate_ci_paths"], [])
        self.assertTrue(report["order_matches"])

    def test_render_upload_artifact_paths_uses_source_paths(self) -> None:
        rendered = render_upload_artifact_paths(indent=2)

        self.assertEqual(rendered, [f"  {path}" for path in source_artifact_paths()])

    def test_extract_upload_artifact_paths_from_marked_yaml_text(self) -> None:
        self.assertEqual(extract_upload_artifact_paths(_workflow(["runs/a.json", "runs/b.json"])), ["runs/a.json", "runs/b.json"])

    def test_extract_upload_artifact_paths_from_legacy_yaml_text(self) -> None:
        self.assertEqual(extract_upload_artifact_paths(_workflow(["runs/a.json"], markers=False)), ["runs/a.json"])

    def test_replace_upload_artifact_paths_adds_markers_to_legacy_block(self) -> None:
        replaced = replace_upload_artifact_paths(_workflow(["old.json"], markers=False))

        self.assertIn(UPLOAD_PATHS_BEGIN_MARKER, replaced)
        self.assertIn(UPLOAD_PATHS_END_MARKER, replaced)
        self.assertEqual(extract_upload_artifact_paths(replaced), list(source_artifact_paths()))

    def test_sync_upload_artifact_paths_updates_workflow(self) -> None:
        expected = list(source_artifact_paths())
        with tempfile.TemporaryDirectory() as tmp:
            workflow_path = _write_workflow(Path(tmp), expected[:-1])
            report = sync_upload_artifact_paths(workflow_path)
            saved = workflow_path.read_text(encoding="utf-8")
            saved_paths = extract_upload_artifact_paths(saved)

        self.assertTrue(report["ok"])
        self.assertTrue(report["changed"])
        self.assertTrue(report["markers_present"])
        self.assertTrue(report["order_matches"])
        self.assertIn(UPLOAD_PATHS_BEGIN_MARKER, saved)
        self.assertIn(UPLOAD_PATHS_END_MARKER, saved)
        self.assertEqual(saved_paths, expected)

    def test_sync_upload_artifact_paths_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workflow_path = _write_workflow(Path(tmp), list(source_artifact_paths()))
            report = sync_upload_artifact_paths(workflow_path)

        self.assertTrue(report["ok"])
        self.assertFalse(report["changed"])
        self.assertTrue(report["order_matches"])

    def test_upload_drift_report_rejects_missing_ci_path(self) -> None:
        expected = list(source_artifact_paths())
        with tempfile.TemporaryDirectory() as tmp:
            workflow_path = _write_workflow(Path(tmp), expected[:-1])
            report = upload_drift_report(workflow_path)

        self.assertFalse(report["ok"])
        self.assertEqual(report["missing_from_ci"], [expected[-1]])
        self.assertEqual(report["extra_in_ci"], [])

    def test_upload_drift_report_rejects_extra_ci_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workflow_path = _write_workflow(Path(tmp), list(source_artifact_paths()) + ["runs/extra.json"])
            report = upload_drift_report(workflow_path)

        self.assertFalse(report["ok"])
        self.assertEqual(report["missing_from_ci"], [])
        self.assertEqual(report["extra_in_ci"], ["runs/extra.json"])

    def test_upload_drift_report_rejects_duplicate_ci_path(self) -> None:
        expected = list(source_artifact_paths())
        with tempfile.TemporaryDirectory() as tmp:
            workflow_path = _write_workflow(Path(tmp), expected + [expected[0]])
            report = upload_drift_report(workflow_path)

        self.assertFalse(report["ok"])
        self.assertEqual(report["duplicate_ci_paths"], [expected[0]])

    def test_upload_drift_report_rejects_unmarked_current_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workflow_path = _write_workflow(Path(tmp), list(source_artifact_paths()), markers=False)
            report = upload_drift_report(workflow_path)

        self.assertFalse(report["ok"])
        self.assertFalse(report["markers_present"])

    def test_cli_returns_zero_for_default_workflow(self) -> None:
        out = StringIO()
        with redirect_stdout(out):
            code = main([])

        self.assertEqual(code, 0)
        self.assertIn('"ok": true', out.getvalue())
        self.assertIn('"markers_present": true', out.getvalue())
        self.assertIn('"order_matches": true', out.getvalue())

    def test_cli_sync_updates_temp_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workflow_path = _write_workflow(Path(tmp), ["old.json"], markers=False)
            out = StringIO()
            with redirect_stdout(out):
                code = main(["--workflow", str(workflow_path), "--sync"])
            saved = workflow_path.read_text(encoding="utf-8")
            saved_paths = extract_upload_artifact_paths(saved)

        self.assertEqual(code, 0)
        self.assertIn('"changed": true', out.getvalue())
        self.assertIn(UPLOAD_PATHS_BEGIN_MARKER, saved)
        self.assertIn(UPLOAD_PATHS_END_MARKER, saved)
        self.assertEqual(saved_paths, list(source_artifact_paths()))


if __name__ == "__main__":
    unittest.main()
