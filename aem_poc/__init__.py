"""AEM PoC: Accretive Expert Mesh.

This package is intentionally small. It models the first control loop:
TaskPacket -> Registry -> Router -> Objective admission gates -> ExpertReply.
"""

from .protocol import (
    AdmissionReport,
    ExpertCard,
    ExpertRegistry,
    ExpertReply,
    ObjectiveGateConfig,
    ObjectiveVerifier,
    Router,
    TaskPacket,
)

__all__ = [
    "AdmissionReport",
    "ExpertCard",
    "ExpertRegistry",
    "ExpertReply",
    "ObjectiveGateConfig",
    "ObjectiveVerifier",
    "Router",
    "TaskPacket",
]
