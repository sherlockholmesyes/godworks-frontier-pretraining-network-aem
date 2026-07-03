from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

from .hash_utils import sha256_text


@dataclass(frozen=True)
class VerifierReport:
    expert_id: str
    task_id: str
    accepted: bool
    score: float
    checks: tuple[str, ...]
    stdout_hash: str = ""
    stderr_hash: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class PythonUnitVerifier:
    """Small objective verifier for PoC code-patch experts."""

    def __init__(self, timeout_seconds: float = 2.0) -> None:
        self.timeout_seconds = timeout_seconds

    def verify_module(
        self,
        *,
        expert_id: str,
        task_id: str,
        module_code: str,
        test_code: str,
    ) -> VerifierReport:
        with tempfile.TemporaryDirectory(prefix="aem_verify_") as raw_tmp:
            tmp = Path(raw_tmp)
            (tmp / "solution.py").write_text(module_code, encoding="utf-8")
            (tmp / "test_solution.py").write_text(test_code, encoding="utf-8")
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "unittest",
                        "discover",
                        "-s",
                        ".",
                        "-p",
                        "test_solution.py",
                    ],
                    cwd=tmp,
                    text=True,
                    capture_output=True,
                    timeout=self.timeout_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                return VerifierReport(
                    expert_id=expert_id,
                    task_id=task_id,
                    accepted=False,
                    score=0.0,
                    checks=("timeout",),
                    stdout_hash=sha256_text(""),
                    stderr_hash=sha256_text("timeout"),
                )

        accepted = result.returncode == 0
        checks = ("unit_tests_passed",) if accepted else ("unit_tests_failed",)
        return VerifierReport(
            expert_id=expert_id,
            task_id=task_id,
            accepted=accepted,
            score=1.0 if accepted else 0.0,
            checks=checks,
            stdout_hash=sha256_text(result.stdout),
            stderr_hash=sha256_text(result.stderr),
        )
