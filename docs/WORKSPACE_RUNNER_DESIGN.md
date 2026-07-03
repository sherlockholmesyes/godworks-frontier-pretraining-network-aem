# Workspace Runner design

wrong1: repo patch gate is tiny in-memory diff apply.
Death: no workspace evidence.

wrong2: repo patch gate must wait for a full container runner.
Death: blocks the next objective gate.

Third: repo patch gate is workspace prep plus selected command plus audit hashes.

Flow:

```text
copy fixture repo
apply allowed patch
record changed files
run selected command
record stdout hash
record stderr hash
write route trace
```

Files:

```text
aem_poc/workspace_diff.py
aem_poc/workspace_prep.py
aem_poc/workspace_cmd.py
tests/test_workspace_runner.py
```

Invariant:

```text
patch_hash exists
fixture_hash exists
changed_files exists
stdout_hash exists
stderr_hash exists
```

Next pressure:

```text
add optional external patch backend while preserving the same report shape
```
