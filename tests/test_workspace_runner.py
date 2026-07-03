import sys
import tempfile
import unittest
from pathlib import Path

from aem_poc.workspace_cmd import run_workspace_command
from aem_poc.workspace_prep import WorkspacePrep


DIFF = """--- a/calc.py
+++ b/calc.py
@@ -1,2 +1,2 @@
 def add(a, b):
-    return a - b
+    return sum((a, b))
"""


class WorkspaceRunnerTest(unittest.TestCase):
    def test_workspace_prep_reports_changed_file_and_backend(self) -> None:
        repo = Path(__file__).resolve().parents[1] / "fixtures" / "code_patch_repo"
        with tempfile.TemporaryDirectory() as tmp:
            report = WorkspacePrep().prepare(
                fixture_repo=repo,
                diff_text=DIFF,
                output_dir=Path(tmp) / "work",
            )
            self.assertTrue(report.accepted)
            self.assertEqual(report.target_file, "calc.py")
            self.assertEqual([change.path for change in report.changed_files], ["calc.py"])
            self.assertEqual(len(report.patch_hash), 64)
            self.assertEqual(len(report.fixture_hash), 64)
            self.assertIsNotNone(report.backend_report)
            assert report.backend_report is not None
            self.assertEqual(report.backend_report.backend, "stdlib_one_file")

    def test_workspace_command_hashes_output(self) -> None:
        repo = Path(__file__).resolve().parents[1] / "fixtures" / "code_patch_repo"
        with tempfile.TemporaryDirectory() as tmp:
            prep = WorkspacePrep().prepare(
                fixture_repo=repo,
                diff_text=DIFF,
                output_dir=Path(tmp) / "work",
            )
            assert prep.workspace_path is not None
            report = run_workspace_command(
                prep.workspace_path,
                (sys.executable, "-m", "unittest", "discover", "-s", "."),
            )
            self.assertTrue(report.accepted)
            self.assertEqual(len(report.stdout_hash), 64)
            self.assertEqual(len(report.stderr_hash), 64)


if __name__ == "__main__":
    unittest.main()
