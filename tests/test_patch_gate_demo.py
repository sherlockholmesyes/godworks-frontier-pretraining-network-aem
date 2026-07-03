import tempfile
import unittest
from pathlib import Path

from aem_poc.patch_gate_demo import run


class PatchGateDemoTest(unittest.TestCase):
    def test_patch_gate_demo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp))
            self.assertFalse(result["fake_admitted"])
            self.assertTrue(result["real_admitted"])
            self.assertEqual(result["chosen_expert"], "real_patch_expert")
            self.assertTrue((Path(tmp) / "route_trace.jsonl").exists())
            self.assertEqual(len(result["fake_patch_hash"]), 64)
            self.assertEqual(len(result["real_patch_hash"]), 64)
            self.assertEqual(len(result["fixture_hash"]), 64)
            self.assertEqual(result["backend"], "stdlib_one_file")
            self.assertEqual(result["configured_backend"], "stdlib_one_file")
            self.assertEqual(result["configured_allowed_files"], ("calc.py",))
            self.assertEqual(result["configured_max_patch_bytes"], 4096)


if __name__ == "__main__":
    unittest.main()
