import tempfile
import unittest
from pathlib import Path

from aem_poc.objective_admission import ObjectiveAdmissionGate
from aem_poc.protocol import ExpertCard, ObjectiveGateConfig, ObjectiveVerifier, TaskPacket
from aem_poc.sandbox_verifier import PythonUnitVerifier
from aem_poc.trace_store import TraceStore, build_route_trace


TEST_CODE = '''
import unittest
from solution import add

class SolutionTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()
'''


def card(expert_id: str) -> ExpertCard:
    return ExpertCard(
        expert_id=expert_id,
        base_model_hash="base:demo",
        expert_type="code_patch",
        quantization="4bit_nf4+lora",
        vram_min_gb=12,
        training_objective="demo code patch",
        domains=("code", "python"),
        eval_delta={"code_patch": 0.10},
        latency_ms=100,
        signature=f"sig:{expert_id}",
    )


class ObjectiveGateTest(unittest.TestCase):
    def test_fake_claim_rejected_real_output_accepted_and_trace_written(self) -> None:
        verifier = PythonUnitVerifier()
        fake = card("fake_claim_expert")
        real = card("real_patch_expert")

        fake_report = verifier.verify_module(
            expert_id=fake.expert_id,
            task_id="task-code-1",
            module_code="def add(a, b):\n    return 0\n",
            test_code=TEST_CODE,
        )
        real_report = verifier.verify_module(
            expert_id=real.expert_id,
            task_id="task-code-1",
            module_code="def add(a, b):\n    return a + b\n",
            test_code=TEST_CODE,
        )

        gate = ObjectiveAdmissionGate(
            ObjectiveVerifier(ObjectiveGateConfig(target_eval_key="code_patch"))
        )
        fake_admission = gate.evaluate(fake, fake_report)
        real_admission = gate.evaluate(real, real_report)

        self.assertFalse(fake_admission.accepted)
        self.assertTrue(real_admission.accepted)

        task = TaskPacket(
            task_id="task-code-1",
            task_type="code_patch",
            prompt="make add pass tests",
        )
        trace = build_route_trace(
            task=task,
            candidates=[fake, real],
            chosen=real,
            admission_reports=[fake_admission, real_admission],
            verifier_reports=[fake_report.to_dict(), real_report.to_dict()],
        )

        with tempfile.TemporaryDirectory() as tmp:
            store = TraceStore(Path(tmp) / "route_trace.jsonl")
            store.append(trace)
            rows = store.read_all()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["chosen_expert"], "real_patch_expert")


if __name__ == "__main__":
    unittest.main()
