import tempfile
import unittest
from pathlib import Path

from aem_poc.patch_backend import apply_patch_backend


DIFF = """--- a/calc.py
+++ b/calc.py
@@ -1,2 +1,2 @@
 def add(a, b):
-    return a - b
+    return sum((a, b))
"""


class PatchBackendTest(unittest.TestCase):
    def test_stdlib_backend_applies_one_file_patch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "calc.py"
            path.write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
            report = apply_patch_backend(tmp, DIFF, "stdlib_one_file")
            self.assertTrue(report.accepted)
            self.assertEqual(report.backend, "stdlib_one_file")
            self.assertEqual(report.target_file, "calc.py")
            self.assertIn("sum((a, b))", path.read_text(encoding="utf-8"))
            self.assertEqual(len(report.patch_hash), 64)

    def test_unknown_backend_returns_report_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = apply_patch_backend(tmp, DIFF, "unknown")
            self.assertFalse(report.accepted)
            self.assertEqual(report.backend, "unknown")
            self.assertEqual(len(report.patch_hash), 64)
            self.assertIn("unknown_backend", report.checks)


if __name__ == "__main__":
    unittest.main()
