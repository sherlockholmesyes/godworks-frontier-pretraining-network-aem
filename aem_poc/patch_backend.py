from __future__ import annotations

import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .diff_apply import apply_one_file, patch_target
from .hash_utils import sha256_text


@dataclass(frozen=True)
class PatchBackendReport:
    backend: str
    accepted: bool
    patch_hash: str
    target_file: str | None
    returncode: int | None
    stdout_hash: str
    stderr_hash: str
    checks: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def apply_patch_backend(workspace: str | Path, diff_text: str, backend: str = "auto") -> PatchBackendReport:
    work = Path(workspace)
    patch_hash = sha256_text(diff_text)

    if backend == "auto":
        backend = "external" if shutil.which("git") else "stdlib_one_file"

    if backend == "external":
        result = subprocess.run(
            ["git", "apply", "--whitespace=nowarn", "-"],
            cwd=work,
            input=diff_text,
            capture_output=True,
            text=True,
            check=False,
        )
        ok = result.returncode == 0
        target = None
        try:
            target = patch_target(diff_text)
        except ValueError:
            pass
        return PatchBackendReport(
            backend="external",
            accepted=ok,
            patch_hash=patch_hash,
            target_file=target,
            returncode=result.returncode,
            stdout_hash=sha256_text(result.stdout),
            stderr_hash=sha256_text(result.stderr),
            checks=("external_apply_passed",) if ok else ("external_apply_failed",),
        )

    if backend != "stdlib_one_file":
        return PatchBackendReport(
            backend=backend,
            accepted=False,
            patch_hash=patch_hash,
            target_file=None,
            returncode=None,
            stdout_hash=sha256_text(""),
            stderr_hash=sha256_text("unknown backend"),
            checks=("unknown_backend",),
        )

    try:
        target = patch_target(diff_text)
        target_path = work / target
        patched = apply_one_file(target_path.read_text(encoding="utf-8"), diff_text)
        target_path.write_text(patched, encoding="utf-8")
    except (ValueError, IndexError, FileNotFoundError) as exc:
        return PatchBackendReport(
            backend="stdlib_one_file",
            accepted=False,
            patch_hash=patch_hash,
            target_file=None,
            returncode=None,
            stdout_hash=sha256_text(""),
            stderr_hash=sha256_text(str(exc)),
            checks=("stdlib_apply_failed",),
        )

    return PatchBackendReport(
        backend="stdlib_one_file",
        accepted=True,
        patch_hash=patch_hash,
        target_file=target,
        returncode=0,
        stdout_hash=sha256_text(""),
        stderr_hash=sha256_text(""),
        checks=("stdlib_apply_passed",),
    )
