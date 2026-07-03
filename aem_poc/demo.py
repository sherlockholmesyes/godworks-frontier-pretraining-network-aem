from __future__ import annotations

from .protocol import (
    ExpertCard,
    ExpertRegistry,
    ObjectiveGateConfig,
    ObjectiveVerifier,
    Router,
    TaskPacket,
)


def build_registry() -> ExpertRegistry:
    registry = ExpertRegistry()

    registry.register(
        ExpertCard(
            expert_id="code_patch_7b_q4_lora_v0",
            base_model_hash="base:open-coder-7b:q4:demo",
            expert_type="code_patch",
            quantization="4bit_nf4+lora",
            vram_min_gb=12,
            training_objective="patch small bugs from issue + failing test context",
            domains=("code", "python", "unit_tests", "bugfix"),
            eval_delta={"code_patch": 0.071, "python_unit_tests": 0.054},
            negative_eval_delta={"general_reasoning": -0.004, "instruction_following": -0.003},
            risk_scores={"duplicate": 0.31, "backdoor": 0.01},
            latency_ms=2100,
            license="research-demo",
            signature="sig:code_patch_7b_q4_lora_v0",
            data_hashes=("sha256:demo-bugfix-shard",),
        )
    )

    registry.register(
        ExpertCard(
            expert_id="echo_lora_bad_v0",
            base_model_hash="base:open-coder-7b:q4:demo",
            expert_type="code_patch",
            quantization="4bit_nf4+lora",
            vram_min_gb=10,
            training_objective="echo training prompts",
            domains=("code", "bugfix"),
            eval_delta={"code_patch": 0.006},
            negative_eval_delta={"general_reasoning": -0.018},
            risk_scores={"duplicate": 0.96, "backdoor": 0.02},
            latency_ms=900,
            license="research-demo",
            signature="sig:echo_lora_bad_v0",
        )
    )

    registry.register(
        ExpertCard(
            expert_id="heavy_32b_patch_expert_v0",
            base_model_hash="base:open-coder-32b:q4:demo",
            expert_type="code_patch",
            quantization="4bit_nf4+lora",
            vram_min_gb=24,
            training_objective="larger patch expert that does not fit 12GB nodes",
            domains=("code", "bugfix"),
            eval_delta={"code_patch": 0.088},
            negative_eval_delta={"general_reasoning": -0.006},
            risk_scores={"duplicate": 0.22, "backdoor": 0.01},
            latency_ms=3200,
            license="research-demo",
            signature="sig:heavy_32b_patch_expert_v0",
        )
    )

    return registry


def main() -> None:
    task = TaskPacket(
        task_id="demo-task-001",
        task_type="code_patch",
        prompt="A Python function fails a unit test. Produce a minimal patch.",
        required_capabilities=("code", "python", "unit_tests"),
        constraints={"must_run_tests": True, "output": "patch"},
        budget={"max_latency_ms": 8000, "node_vram_gb": 12},
        privacy_level="public-demo",
    )

    registry = build_registry()
    verifier = ObjectiveVerifier(
        ObjectiveGateConfig(
            target_eval_key="code_patch",
            min_target_delta=0.02,
            max_general_regression=-0.01,
            max_duplicate_score=0.92,
            max_backdoor_score=0.05,
            max_latency_ms=8000,
            node_vram_gb=12,
            require_signature=True,
        )
    )
    router = Router(registry, verifier)

    chosen, reports = router.route(task)

    print("AEM PoC routing reports")
    print("=" * 28)
    for report in reports:
        verdict = "ACCEPT" if report.accepted else "REJECT"
        print(f"{verdict:6} {report.expert_id:28} score={report.score}")
        for reason in report.reasons:
            print(f"  - {reason}")

    print()
    if chosen is None:
        print("No expert admitted.")
        return

    reply = router.call(task, chosen)
    print(f"Chosen expert: {chosen.expert_id}")
    print(f"Reply: {reply.answer}")


if __name__ == "__main__":
    main()
