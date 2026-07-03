from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .protocol import TaskPacket
from .repo_patch_policy import RepoPatchPolicy


def _str_tuple(value: Any, default: tuple[str, ...]) -> tuple[str, ...]:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return tuple(value)
    return default


@dataclass(frozen=True)
class PatchVerifierConfig:
    backend: str = "stdlib_one_file"
    test_command: tuple[str, ...] = ("python", "-m", "unittest", "discover", "-s", ".")
    policy: RepoPatchPolicy = RepoPatchPolicy()

    @classmethod
    def from_task(cls, task: TaskPacket) -> "PatchVerifierConfig":
        defaults = cls()
        backend = str(task.constraints.get("patch_backend", defaults.backend))
        raw_command = task.constraints.get("test_command")
        if isinstance(raw_command, list) and all(isinstance(part, str) for part in raw_command):
            command = tuple(raw_command)
        else:
            command = defaults.test_command

        default_policy = defaults.policy
        policy = RepoPatchPolicy(
            allowed_files=_str_tuple(task.constraints.get("allowed_files"), default_policy.allowed_files),
            blocked_prefixes=_str_tuple(task.constraints.get("blocked_prefixes"), default_policy.blocked_prefixes),
            max_patch_bytes=int(task.constraints.get("max_patch_bytes", default_policy.max_patch_bytes)),
            max_changed_files=int(task.constraints.get("max_changed_files", default_policy.max_changed_files)),
        )
        return cls(backend=backend, test_command=command, policy=policy)

    def to_trace_payload(self) -> dict[str, object]:
        return {
            "backend": self.backend,
            "test_command": self.test_command,
            "allowed_files": self.policy.allowed_files,
            "blocked_prefixes": self.policy.blocked_prefixes,
            "max_patch_bytes": self.policy.max_patch_bytes,
            "max_changed_files": self.policy.max_changed_files,
        }
