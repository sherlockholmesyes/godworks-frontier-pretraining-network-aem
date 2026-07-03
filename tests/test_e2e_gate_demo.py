import tempfile
import unittest
from pathlib import Path

from aem_poc.e2e_gate_demo import run


class E2EGateDemoTest(unittest.TestCase):
    def test_e2e_gate_demo_outputs_trace_and_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp))

            self.assertFalse(result["fake_admitted"])
            self.assertTrue(result["real_admitted"])
            self.assertEqual(result["chosen_expert"], "real_patch_expert")
            self.assertTrue(Path(result["route_trace"]).exists())
            self.assertTrue(Path(result["distill_receipt"]).exists())

            receipt = result["receipt"]
            self.assertEqual(receipt["accepted_count"], 1)
            self.assertEqual(receipt["rejected_count"], 1)


if __name__ == "__main__":
    unittest.main()
