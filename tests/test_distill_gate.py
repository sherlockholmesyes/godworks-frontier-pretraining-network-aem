import unittest

from aem_poc.distill_gate import DistillGate, DistillSample, TeacherCard
from aem_poc.sandbox_verifier import VerifierReport


class DistillGateTest(unittest.TestCase):
    def test_blocked_sample_rejected_allowed_sample_receipted(self) -> None:
        blocked = TeacherCard(
            teacher_id="blocked-teacher-demo",
            allowed_for_training=False,
            allowed_outputs_retention=True,
            allowed_for_commercial_use=False,
            terms_version="demo",
            signature="sig:blocked",
        )
        allowed = TeacherCard(
            teacher_id="allowed-open-teacher-demo",
            allowed_for_training=True,
            allowed_outputs_retention=True,
            allowed_for_commercial_use=True,
            terms_version="demo",
            signature="sig:allowed",
        )
        report = VerifierReport(
            expert_id="distill-checker",
            task_id="distill-task-1",
            accepted=True,
            score=1.0,
            checks=("accepted",),
        )
        blocked_sample = DistillSample(
            sample_id="sample-blocked",
            teacher_id=blocked.teacher_id,
            task_type="code_patch",
            prompt_hash="hash:prompt",
            answer="candidate answer",
            verifier_report=report,
        )
        allowed_sample = DistillSample(
            sample_id="sample-allowed",
            teacher_id=allowed.teacher_id,
            task_type="code_patch",
            prompt_hash="hash:prompt",
            answer="verified answer",
            verifier_report=report,
        )

        gate = DistillGate()
        decisions = (
            gate.accept_sample(blocked, blocked_sample),
            gate.accept_sample(allowed, allowed_sample),
        )
        receipt = gate.receipt(
            run_id="distill-run-1",
            student_base_model="student-base-demo",
            student_output_model="student-output-demo",
            teacher_ids=(blocked.teacher_id, allowed.teacher_id),
            decisions=decisions,
            eval_before={"code_patch": 0.10},
            eval_after={"code_patch": 0.20},
        )

        self.assertFalse(decisions[0][0])
        self.assertTrue(decisions[1][0])
        self.assertEqual(receipt.accepted_count, 1)
        self.assertEqual(receipt.rejected_count, 1)
        self.assertIn("teacher not allowed for training", receipt.rejection_breakdown)
        self.assertEqual(receipt.signature, "receipt:distill-run-1")


if __name__ == "__main__":
    unittest.main()
