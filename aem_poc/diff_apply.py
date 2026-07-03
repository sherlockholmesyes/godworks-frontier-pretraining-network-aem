from __future__ import annotations


def patch_target(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("+++ "):
            raw = line[4:].strip()
            if raw.startswith("b/"):
                return raw[2:]
            return raw
    raise ValueError("missing target")


def apply_one_file(original: str, diff_text: str) -> str:
    src = original.splitlines()
    out: list[str] = []
    at = 0
    lines = diff_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("@@ "):
            i += 1
            continue
        old_part = line.split(" ")[1]
        start = int(old_part.split(",")[0][1:]) - 1
        out.extend(src[at:start])
        at = start
        i += 1
        while i < len(lines) and not lines[i].startswith("@@ "):
            h = lines[i]
            if h.startswith("--- ") or h.startswith("+++ ") or h.startswith("\\"):
                pass
            elif h.startswith(" "):
                expected = h[1:]
                if at >= len(src) or src[at] != expected:
                    raise ValueError("context mismatch")
                out.append(src[at])
                at += 1
            elif h.startswith("-"):
                expected = h[1:]
                if at >= len(src) or src[at] != expected:
                    raise ValueError("delete mismatch")
                at += 1
            elif h.startswith("+"):
                out.append(h[1:])
            else:
                raise ValueError("bad diff line")
            i += 1
    out.extend(src[at:])
    return "\n".join(out) + ("\n" if original.endswith("\n") else "")
