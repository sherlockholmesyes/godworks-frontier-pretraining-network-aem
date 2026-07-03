from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .distill_gate import TeacherCard
from .protocol import ExpertCard, TaskPacket
from .schema_validation import validate_or_raise


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected object at {path}")
    return data


def load_expert_card(path: str | Path) -> ExpertCard:
    data = load_json(path)
    validate_or_raise(data, "expert_card.schema.json")
    return ExpertCard(
        expert_id=str(data["expert_id"]),
        base_model_hash=str(data["base_model_hash"]),
        expert_type=str(data["expert_type"]),
        quantization=str(data["quantization"]),
        vram_min_gb=int(data["vram_min_gb"]),
        training_objective=str(data["training_objective"]),
        domains=tuple(str(item) for item in data["domains"]),
        eval_delta={str(k): float(v) for k, v in data.get("eval_delta", {}).items()},
        negative_eval_delta={
            str(k): float(v) for k, v in data.get("negative_eval_delta", {}).items()
        },
        risk_scores={str(k): float(v) for k, v in data.get("risk_scores", {}).items()},
        latency_ms=int(data.get("latency_ms", 0)),
        license=str(data.get("license", "unspecified")),
        signature=str(data.get("signature", "")),
        data_hashes=tuple(str(item) for item in data.get("data_hashes", ())),
    )


def load_task_packet(path: str | Path) -> TaskPacket:
    data = load_json(path)
    validate_or_raise(data, "task_packet.schema.json")
    return TaskPacket(
        task_id=str(data["task_id"]),
        task_type=str(data["task_type"]),
        prompt=str(data["prompt"]),
        required_capabilities=tuple(str(item) for item in data.get("required_capabilities", ())),
        constraints=dict(data.get("constraints", {})),
        budget=dict(data.get("budget", {})),
        privacy_level=str(data.get("privacy_level", "public")),
    )


def load_teacher_card(path: str | Path) -> TeacherCard:
    data = load_json(path)
    validate_or_raise(data, "teacher_policy_card.schema.json")
    return TeacherCard(
        teacher_id=str(data["teacher_id"]),
        allowed_for_training=bool(data["allowed_for_training"]),
        allowed_outputs_retention=bool(data["allowed_outputs_retention"]),
        allowed_for_commercial_use=bool(data["allowed_for_commercial_use"]),
        terms_version=str(data["terms_version"]),
        signature=str(data.get("signature", "")),
    )
