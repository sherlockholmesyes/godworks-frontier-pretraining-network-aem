from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .sandbox_verifier import VerifierReport


@dataclass(frozen=True)
class TeacherCard:
    teacher_id: str
    allowed_for_training: bool
    allowed_outputs_retention: bool
    allowed_for_commercial_use: bool
    terms_version: str
    signature: str = ""


@dataclass(frozen=True)
class DistillSample:
    sample_id: str
    teacher_id: str
    task_type: str
    prompt_hash: str
    answer: str
    verifier_report: VerifierReport


@dataclass(frozen=True)
class DistillReceipt:
    run_id: str
    student_base_model: str
    student_output_model: str
    teacher_ids: tuple[str, ...]
    accepted_count: int
    rejected_count: int
    rejection_breakdown: dict[str, int]
    eval_before: dict[str, float]
    eval_after: dict[str, float]
    signature: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DistillGate:
    def accept_sample(self, card: TeacherCard, sample: DistillSample) -> tuple[bool, str]:
        if sample.teacher_id != card.teacher_id:
            return False, "teacher mismatch"
        if not card.allowed_for_training:
            return False, "teacher not allowed for training"
        if not card.allowed_outputs_retention:
            return False, "teacher output retention unavailable"
        if not sample.verifier_report.accepted:
            return False, "verifier rejected sample"
        return True, "accepted"

    def receipt(
        self,
        *,
        run_id: str,
        student_base_model: str,
        student_output_model: str,
        teacher_ids: tuple[str, ...],
        decisions: tuple[tuple[bool, str], ...],
        eval_before: dict[str, float],
        eval_after: dict[str, float],
    ) -> DistillReceipt:
        accepted_count = sum(1 for ok, _ in decisions if ok)
        rejected_count = len(decisions) - accepted_count
        breakdown: dict[str, int] = {}
        for ok, reason in decisions:
            if not ok:
                breakdown[reason] = breakdown.get(reason, 0) + 1
        return DistillReceipt(
            run_id=run_id,
            student_base_model=student_base_model,
            student_output_model=student_output_model,
            teacher_ids=teacher_ids,
            accepted_count=accepted_count,
            rejected_count=rejected_count,
            rejection_breakdown=breakdown,
            eval_before=eval_before,
            eval_after=eval_after,
            signature=f"receipt:{run_id}",
        )
