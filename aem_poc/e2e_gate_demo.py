from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .distill_gate import DistillGate, DistillSample
from .loaders import load_expert_card, load_task_packet, load_teacher_card
from .objective_admission import ObjectiveAdmissionGate
from .protocol import ObjectiveGateConfig, ObjectiveVerifier
from .sandbox_verifier import PythonUnitVerifier, VerifierReport
from .trace_store import TraceStore, build_route_trace


TEST_CODE = '''
import unittest
from solution import add

class SolutionTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()
'''


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(output_dir: str | Path = "runs/e2e_gate_demo") -> dict[str, object]:
    root = repo_root()
    out = root / output_dir
    out.mkdir(parents=True, exist_ok=True)

    task = load_task_packet(root / "examples" / "task_code_patch.json")
    fake = load_expert_card(root / "examples" / "fake_code_patch_expert_card.json")
    real = load_expert_card(root / "examples" / "real_code_patch_expert_card.json")

    verifier = PythonUnitVerifier()
    fake_report = verifier.verify_module(
        expert_id=fake.expert_id,
        task_id=task.task_id,
        module_code="def add(a, b):\n    return 0\n",
        test_code=TEST_CODE,
    )
    real_report = verifier.verify_module(
        expert_id=real.expert_id,
        task_id=task.task_id,
        module_code="def add(a, b):\n    return a + b\n",
        test_code=TEST_CODE,
    )

    gate = ObjectiveAdmissionGate(
        ObjectiveVerifier(ObjectiveGateConfig(target_eval_key="code_patch"))
    )
    fake_admission = gate.evaluate(fake, fake_report)
    real_admission = gate.evaluate(real, real_report)

    chosen = real if real_admission.accepted else None
    trace = build_route_trace(
        task=task,
        candidates=[fake, real],
        chosen=chosen,
        admission_reports=[fake_admission, real_admission],
        verifier_reports=[fake_report.to_dict(), real_report.to_dict()],
    )
    trace_path = out / "route_trace.jsonl"
    TraceStore(trace_path).append(trace)

    blocked_teacher = load_teacher_card(root / "examples" / "teacher_policy_blocked.json")
    allowed_teacher = load_teacher_card(root / "examples" / "teacher_policy_allowed.json")
    distill_gate = DistillGate()

    passed_report = VerifierReport(
        expert_id="distill-checker",
        task_id="distill-task-1",
        accepted=True,
        score=1.0,
        checks=("accepted",),
    )
    blocked_sample = DistillSample(
        sample_id="sample-blocked",
        teacher_id=blocked_teacher.teacher_id,
        task_type="code_patch",
        prompt_hash="hash:prompt",
        answer="candidate answer",
        verifier_report=passed_report,
    )
    allowed_sample = DistillSample(
        sample_id="sample-allowed",
        teacher_id=allowed_teacher.teacher_id,
        task_type="code_patch",
        prompt_hash="hash:prompt",
        answer="verified answer",
        verifier_report=passed_report,
    )

    decisions = (
        distill_gate.accept_sample(blocked_teacher, blocked_sample),
        distill_gate.accept_sample(allowed_teacher, allowed_sample),
    )
    receipt = distill_gate.receipt(
        run_id="distill-run-e2e-1",
        student_base_model="student-base-demo",
        student_output_model="student-output-demo",
        teacher_ids=(blocked_teacher.teacher_id, allowed_teacher.teacher_id),
        decisions=decisions,
        eval_before={"code_patch": 0.10},
        eval_after={"code_patch": 0.20},
    )
    receipt_path = out / "distill_receipt.json"
    receipt_path.write_text(json.dumps(receipt.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    return {
        "fake_admitted": fake_admission.accepted,
        "real_admitted": real_admission.accepted,
        "chosen_expert": chosen.expert_id if chosen else None,
        "route_trace": str(trace_path),
        "distill_decisions": decisions,
        "distill_receipt": str(receipt_path),
        "receipt": asdict(receipt),
    }


def main() -> None:
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
