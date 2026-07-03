from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .hash_utils import sha256_file


@dataclass(frozen=True)
class FileChange:
    path: str
    before_hash: str | None
    after_hash: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def file_map(root: str | Path) -> dict[str, str]:
    base = Path(root)
    out: dict[str, str] = {}
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        rel = path.relative_to(base).as_posix()
        out[rel] = sha256_file(path)
    return out


def diff_maps(before: dict[str, str], after: dict[str, str]) -> tuple[FileChange, ...]:
    paths = sorted(set(before) | set(after))
    changes: list[FileChange] = []
    for path in paths:
        old = before.get(path)
        new = after.get(path)
        if old != new:
            changes.append(FileChange(path=path, before_hash=old, after_hash=new))
    return tuple(changes)
