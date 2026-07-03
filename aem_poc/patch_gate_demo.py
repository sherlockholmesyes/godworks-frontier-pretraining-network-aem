from __future__ import annotations

import json
from pathlib import Path

from .loaders import load_expert_card, load_task_packet
from .objective_admission import ObjectiveAdmissionGate
from .protocol import ObjectiveGateConfig, ObjectiveVerifier
from .sandbox_verifier import VerifierReport
from .trace_store import TraceStore, build_route_trace
from .verifier_config import PatchVerifierConfig
from .workspace_cmd import run_workspace_command
from .workspace_prep import WorkspacePrep


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def verify_patch(expert_id: str, task_id: str, diff_path: Path, work_dir: Path, config: PatchVerifierConfig):
    base = root()
    repo = base / "fixtures" / "code_patch_repo"
    diff_text = diff_path.read_text(encoding="utf-8")
    prep = WorkspacePrep(policy=config.policy, backend=config.backend).prepare(
        fixture_repo=repo,
        diff_text=diff_text,
        output_dir=work_dir,
    )
    if not prep.accepted or prep.workspace_path is None:
        report = VerifierReport(
            expert_id=expert_id,
            task_id=task_id,
            accepted=False,
            score=0.0,
            checks=("workspace_policy_failed",),
        )
        return prep, report

    cmd = run_workspace_command(
        prep.workspace_path,
        config.test_command,
    )
    report = VerifierReport(
        expert_id=expert_id,
        task_id=task_id,
        accepted=cmd.accepted,
        score=1.0 if cmd.accepted else 0.0,
        checks=cmd.checks,
        stdout_hash=cmd.stdout_hash,
        stderr_hash=cmd.stderr_hash,
    )
    return prep, report


def run(output_dir: str | Path = "runs/patch_gate_demo") -> dict[str, object]:
    base = root()
    out = base / output_dir
    out.mkdir(parents=True, exist_ok=True)

    task = load_task_packet(base / "examples" / "task_code_patch.json")
    config = PatchVerifierConfig.from_task(task)
    fake = load_expert_card(base / "examples" / "fake_code_patch_expert_card.json")
    real = load_expert_card(base / "examples" / "real_code_patch_expert_card.json")

    fake_prep, fake_report = verify_patch(
        fake.expert_id,
        task.task_id,
        base / "examples" / "patches" / "fake_calc.patch",
        out / "workspace_fake",
        config,
    )
    real_prep, real_report = verify_patch(
        real.expert_id,
        task.task_id,
        base / "examples" / "patches" / "pass_calc.txt",
        out / "workspace_real",
        config,
    )

    gate = ObjectiveAdmissionGate(ObjectiveVerifier(ObjectiveGateConfig(target_eval_key="code_patch")))
    fake_admission = gate.evaluate(fake, fake_report)
    real_admission = gate.evaluate(real, real_report)
    chosen = real if real_admission.accepted else None

    verifier_payload = [
        {"kind": "verifier_config", **config.to_trace_payload()},
        {"kind": "workspace", "expert_id": fake.expert_id, **fake_prep.to_dict()},
        {"kind": "command", **fake_report.to_dict()},
        {"kind": "workspace", "expert_id": real.expert_id, **real_prep.to_dict()},
        {"kind": "command", **real_report.to_dict()},
    ]
    trace = build_route_trace(
        task=task,
        candidates=[fake, real],
        chosen=chosen,
        admission_reports=[fake_admission, real_admission],
        verifier_reports=verifier_payload,
    )
    TraceStore(out / "route_trace.jsonl").append(trace)

    real_backend = real_prep.backend_report.backend if real_prep.backend_report else None
    return {
        "fake_admitted": fake_admission.accepted,
        "real_admitted": real_admission.accepted,
        "chosen_expert": chosen.expert_id if chosen else None,
        "fake_patch_hash": fake_prep.patch_hash,
        "real_patch_hash": real_prep.patch_hash,
        "fixture_hash": real_prep.fixture_hash,
        "backend": real_backend,
        "configured_backend": config.backend,
        "configured_allowed_files": config.policy.allowed_files,
        "configured_max_patch_bytes": config.policy.max_patch_bytes,
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
