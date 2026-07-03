import unittest

from aem_poc.repo_patch_policy import RepoPatchPolicy, check_repo_patch_policy


class RepoPatchPolicyTest(unittest.TestCase):
    def test_rejects_unlisted_target(self) -> None:
        diff = """--- a/secret.txt
+++ b/secret.txt
@@ -1 +1 @@
-old
+new
"""
        report = check_repo_patch_policy(diff)
        self.assertFalse(report.accepted)
        self.assertTrue(any("file not allowed" in reason for reason in report.reasons))

    def test_rejects_large_patch(self) -> None:
        diff = "--- a/calc.py\n+++ b/calc.py\n@@ -1 +1 @@\n-old\n+" + ("x" * 32)
        report = check_repo_patch_policy(diff, RepoPatchPolicy(max_patch_bytes=20))
        self.assertFalse(report.accepted)
        self.assertIn("patch too large", report.reasons)

    def test_accepts_small_calc_patch(self) -> None:
        diff = """--- a/calc.py
+++ b/calc.py
@@ -1 +1 @@
-old
+new
"""
        report = check_repo_patch_policy(diff)
        self.assertTrue(report.accepted)
        self.assertEqual(len(report.patch_hash), 64)


if __name__ == "__main__":
    unittest.main()
