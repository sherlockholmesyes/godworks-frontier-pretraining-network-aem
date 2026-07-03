from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TaskPacket:
    """Task-level packet routed through the AEM mesh.

    AEM deliberately routes task packets, candidate answers, verifier scores, and
    adapter deltas. It does not route per-token hidden states over the public internet.
    """

    task_id: str
    task_type: str
    prompt: str
    required_capabilities: tuple[str, ...] = ()
    constraints: dict[str, Any] = field(default_factory=dict)
    budget: dict[str, Any] = field(default_factory=dict)
    privacy_level: str = "public"


@dataclass(frozen=True)
class ExpertCard:
    """Capability capsule manifest.

    An expert is admitted by contract and evidence, not by vibes. In a real mesh,
    the `signature`, `data_hashes`, `training_recipe`, and eval reports would be
    independently checked by verifier nodes.
    """

    expert_id: str
    base_model_hash: str
    expert_type: str
    quantization: str
    vram_min_gb: int
    training_objective: str
    domains: tuple[str, ...]
    eval_delta: dict[str, float]
    negative_eval_delta: dict[str, float] = field(default_factory=dict)
    risk_scores: dict[str, float] = field(default_factory=dict)
    latency_ms: int = 0
    license: str = "unspecified"
    signature: str = ""
    data_hashes: tuple[str, ...] = ()

    def supports(self, task: TaskPacket) -> bool:
        if self.expert_type == task.task_type:
            return True
        return any(cap in self.domains for cap in task.required_capabilities)


@dataclass(frozen=True)
class ExpertReply:
    expert_id: str
    task_id: str
    answer: str
    confidence: float
    latency_ms: int
    cost_units: float = 0.0
    signature: str = ""


@dataclass(frozen=True)
class ObjectiveGateConfig:
    """Admission thresholds.

    Defaults are intentionally conservative for a 12GB consumer-GPU node.
    """

    target_eval_key: str
    min_target_delta: float = 0.02
    max_general_regression: float = -0.01
    max_duplicate_score: float = 0.92
    max_backdoor_score: float = 0.05
    max_latency_ms: int = 8_000
    node_vram_gb: int = 12
    require_signature: bool = True


@dataclass(frozen=True)
class AdmissionReport:
    expert_id: str
    accepted: bool
    score: float
    reasons: tuple[str, ...]


class ExpertRegistry:
    """Tiny in-memory expert registry for PoC use."""

    def __init__(self) -> None:
        self._experts: dict[str, ExpertCard] = {}

    def register(self, card: ExpertCard) -> None:
        if card.expert_id in self._experts:
            raise ValueError(f"duplicate expert_id: {card.expert_id}")
        self._experts[card.expert_id] = card

    def all(self) -> list[ExpertCard]:
        return list(self._experts.values())

    def search(self, task: TaskPacket) -> list[ExpertCard]:
        return [expert for expert in self._experts.values() if expert.supports(task)]


class ObjectiveVerifier:
    """Admission gate for expert capsules.

    The verifier rejects experts that do not improve the target task, regress broad
    evals too much, duplicate existing experts, carry obvious trigger risk, exceed
    node constraints, or lack a signature.
    """

    def __init__(self, config: ObjectiveGateConfig) -> None:
        self.config = config

    def evaluate(self, card: ExpertCard) -> AdmissionReport:
        reasons: list[str] = []

        target_delta = card.eval_delta.get(self.config.target_eval_key, 0.0)
        if target_delta < self.config.min_target_delta:
            reasons.append(
                f"target_delta {target_delta:.3f} < min {self.config.min_target_delta:.3f}"
            )

        regressions = [
            (name, delta)
            for name, delta in card.negative_eval_delta.items()
            if delta < self.config.max_general_regression
        ]
        for name, delta in regressions:
            reasons.append(
                f"regression {name}={delta:.3f} < allowed {self.config.max_general_regression:.3f}"
            )

        duplicate_score = card.risk_scores.get("duplicate", 0.0)
        if duplicate_score > self.config.max_duplicate_score:
            reasons.append(
                f"duplicate_score {duplicate_score:.3f} > max {self.config.max_duplicate_score:.3f}"
            )

        backdoor_score = card.risk_scores.get("backdoor", 0.0)
        if backdoor_score > self.config.max_backdoor_score:
            reasons.append(
                f"backdoor_score {backdoor_score:.3f} > max {self.config.max_backdoor_score:.3f}"
            )

        if card.latency_ms > self.config.max_latency_ms:
            reasons.append(f"latency_ms {card.latency_ms} > max {self.config.max_latency_ms}")

        if card.vram_min_gb > self.config.node_vram_gb:
            reasons.append(f"vram_min_gb {card.vram_min_gb} > node {self.config.node_vram_gb}")

        if self.config.require_signature and not card.signature:
            reasons.append("missing signature")

        accepted = not reasons
        latency_penalty = card.latency_ms / max(self.config.max_latency_ms, 1)
        risk_penalty = duplicate_score + (2.0 * backdoor_score)
        regression_penalty = sum(abs(delta) for _, delta in regressions)
        score = target_delta - 0.05 * latency_penalty - risk_penalty - regression_penalty

        if accepted:
            reasons.append("accepted: all objective gates passed")

        return AdmissionReport(
            expert_id=card.expert_id,
            accepted=accepted,
            score=round(score, 6),
            reasons=tuple(reasons),
        )


class Router:
    """Task-level expert router.

    The PoC router admits candidate experts through objective gates, then ranks accepted
    experts by simple score. A real router would use traffic shaping, reputation,
    redundancy, cost markets, and verifier consensus.
    """

    def __init__(self, registry: ExpertRegistry, verifier: ObjectiveVerifier) -> None:
        self.registry = registry
        self.verifier = verifier

    def route(self, task: TaskPacket) -> tuple[ExpertCard | None, list[AdmissionReport]]:
        candidates = self.registry.search(task)
        reports = [self.verifier.evaluate(card) for card in candidates]
        accepted_ids = {report.expert_id for report in reports if report.accepted}
        accepted_cards = [card for card in candidates if card.expert_id in accepted_ids]
        if not accepted_cards:
            return None, reports

        report_by_id = {report.expert_id: report for report in reports}
        accepted_cards.sort(key=lambda card: report_by_id[card.expert_id].score, reverse=True)
        return accepted_cards[0], reports

    def call(self, task: TaskPacket, card: ExpertCard) -> ExpertReply:
        # This is a PoC stub. The real runtime would call an expert endpoint,
        # local adapter, sandboxed container, or remote worker daemon.
        return ExpertReply(
            expert_id=card.expert_id,
            task_id=task.task_id,
            answer=(
                f"PoC reply from {card.expert_id}: produce a patch candidate for {task.task_type}."
            ),
            confidence=min(0.99, max(0.0, card.eval_delta.get(task.task_type, 0.0) + 0.75)),
            latency_ms=card.latency_ms,
            signature=f"reply:{card.expert_id}:{task.task_id}",
        )
