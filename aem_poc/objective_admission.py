from __future__ import annotations

from .protocol import AdmissionReport, ExpertCard, ObjectiveVerifier
from .sandbox_verifier import VerifierReport


class ObjectiveAdmissionGate:
    def __init__(self, objective: ObjectiveVerifier) -> None:
        self.objective = objective

    def evaluate(self, card: ExpertCard, report: VerifierReport | None) -> AdmissionReport:
        base = self.objective.evaluate(card)
        reasons = list(base.reasons)

        report_ok = False
        if report is None:
            reasons.append("no verifier report")
        elif report.expert_id != card.expert_id:
            reasons.append("verifier id mismatch")
        elif not report.accepted:
            reasons.append("verifier did not accept output")
        else:
            report_ok = True
            reasons.append("verifier accepted output")

        accepted = base.accepted and report_ok
        score = base.score + ((report.score if report else 0.0) * 0.5)
        return AdmissionReport(
            expert_id=card.expert_id,
            accepted=accepted,
            score=round(score, 6),
            reasons=tuple(reasons),
        )
