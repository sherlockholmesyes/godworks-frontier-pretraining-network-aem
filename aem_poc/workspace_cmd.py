from __future__ import annotations

import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .hash_utils import sha256_text


@dataclass(frozen=True)
class CommandReport:
    accepted: bool
    returncode: int | None
    stdout_hash: str
    stderr_hash: str
    checks: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def run_workspace_command(workspace: str | Path, args: tuple[str, ...], timeout_seconds: float = 3.0) -> CommandReport:
    try:
        result = subprocess.run(
            list(args),
            cwd=Path(workspace),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CommandReport(
            accepted=False,
            returncode=None,
            stdout_hash=sha256_text(""),
            stderr_hash=sha256_text("timeout"),
            checks=("timeout",),
        )
    ok = result.returncode == 0
    return CommandReport(
        accepted=ok,
        returncode=result.returncode,
        stdout_hash=sha256_text(result.stdout),
        stderr_hash=sha256_text(result.stderr),
        checks=("command_passed",) if ok else ("command_failed",),
    )
