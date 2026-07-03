from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import PurePosixPath

from .diff_apply import patch_target
from .hash_utils import sha256_text


@dataclass(frozen=True)
class RepoPatchPolicy:
    allowed_files: tuple[str, ...] = ("calc.py",)
    blocked_prefixes: tuple[str, ...] = (".git/", "secrets/", "private/")
    max_patch_bytes: int = 4096
    max_changed_files: int = 1


@dataclass(frozen=True)
class RepoPatchPolicyReport:
    accepted: bool
    patch_hash: str
    target_files: tuple[str, ...]
    patch_bytes: int
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _targets(diff_text: str) -> tuple[str, ...]:
    out: list[str] = []
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            raw = line[4:].strip()
            if raw == "/dev/null":
                out.append(raw)
            elif raw.startswith("b/"):
                out.append(raw[2:])
            else:
                out.append(raw)
    if not out:
        out.append(patch_target(diff_text))
    return tuple(out)


def check_repo_patch_policy(diff_text: str, policy: RepoPatchPolicy = RepoPatchPolicy()) -> RepoPatchPolicyReport:
    reasons: list[str] = []
    patch_bytes = len(diff_text.encode("utf-8"))
    if patch_bytes > policy.max_patch_bytes:
        reasons.append("patch too large")

    try:
        targets = _targets(diff_text)
    except ValueError as exc:
        targets = ()
        reasons.append(str(exc))

    if len(targets) > policy.max_changed_files:
        reasons.append("too many changed files")

    for target in targets:
        path = PurePosixPath(target)
        if path.is_absolute() or ".." in path.parts:
            reasons.append("unsafe path")
        if target not in policy.allowed_files:
            reasons.append(f"file not allowed: {target}")
        if any(target.startswith(prefix) for prefix in policy.blocked_prefixes):
            reasons.append(f"blocked path: {target}")

    return RepoPatchPolicyReport(
        accepted=not reasons,
        patch_hash=sha256_text(diff_text),
        target_files=targets,
        patch_bytes=patch_bytes,
        reasons=tuple(reasons) if reasons else ("policy accepted",),
    )
