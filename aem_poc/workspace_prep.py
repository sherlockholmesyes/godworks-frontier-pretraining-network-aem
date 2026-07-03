from __future__ import annotations

import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from .patch_backend import PatchBackendReport, apply_patch_backend
from .repo_patch_policy import RepoPatchPolicy, check_repo_patch_policy
from .hash_utils import sha256_tree
from .workspace_diff import FileChange, diff_maps, file_map


@dataclass(frozen=True)
class WorkspacePrepReport:
    accepted: bool
    patch_hash: str
    fixture_hash: str
    workspace_path: str | None
    target_file: str | None
    changed_files: tuple[FileChange, ...]
    checks: tuple[str, ...]
    backend_report: PatchBackendReport | None = None

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["changed_files"] = [change.to_dict() for change in self.changed_files]
        if self.backend_report is not None:
            data["backend_report"] = self.backend_report.to_dict()
        return data


class WorkspacePrep:
    def __init__(self, policy: RepoPatchPolicy = RepoPatchPolicy(), backend: str = "stdlib_one_file") -> None:
        self.policy = policy
        self.backend = backend

    def prepare(self, *, fixture_repo: str | Path, diff_text: str, output_dir: str | Path) -> WorkspacePrepReport:
        fixture = Path(fixture_repo)
        workspace = Path(output_dir)
        if workspace.exists():
            shutil.rmtree(workspace)

        fixture_hash = sha256_tree(fixture)
        policy_report = check_repo_patch_policy(diff_text, self.policy)
        if not policy_report.accepted:
            return WorkspacePrepReport(
                accepted=False,
                patch_hash=policy_report.patch_hash,
                fixture_hash=fixture_hash,
                workspace_path=None,
                target_file=None,
                changed_files=(),
                checks=policy_report.reasons,
            )

        shutil.copytree(fixture, workspace)
        before = file_map(workspace)
        backend_report = apply_patch_backend(workspace, diff_text, self.backend)
        after = file_map(workspace)
        changes = diff_maps(before, after)
        if not backend_report.accepted:
            return WorkspacePrepReport(
                accepted=False,
                patch_hash=backend_report.patch_hash,
                fixture_hash=fixture_hash,
                workspace_path=str(workspace),
                target_file=backend_report.target_file,
                changed_files=changes,
                checks=backend_report.checks,
                backend_report=backend_report,
            )
        return WorkspacePrepReport(
            accepted=True,
            patch_hash=backend_report.patch_hash,
            fixture_hash=fixture_hash,
            workspace_path=str(workspace),
            target_file=backend_report.target_file,
            changed_files=changes,
            checks=("workspace_prepared",),
            backend_report=backend_report,
        )
