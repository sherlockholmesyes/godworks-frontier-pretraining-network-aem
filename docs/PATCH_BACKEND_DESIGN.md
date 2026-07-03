# Patch Backend — design

## Rejected option A

```text
patch apply backend is hidden inside workspace prep
```

Death: the report cannot say how the patch was applied.

## Rejected option B

```text
only external apply is acceptable
```

Death: the PoC becomes dependent on host tooling and stops being stdlib-replayable.

## Third

```text
patch backend is explicit and report-shaped
```

Backends:

```text
stdlib_one_file
external
auto
```

Report shape:

```text
backend
accepted
patch_hash
target_file
returncode
stdout_hash
stderr_hash
checks
```

## Invariant

```text
WorkspacePrep always preserves the same report shape even when backend changes.
```

## Files

```text
aem_poc/patch_backend.py
aem_poc/workspace_prep.py
tests/test_patch_backend.py
tests/test_workspace_runner.py
```

## Death of this step

```text
patch application is an implementation detail
```

Dead.

## Inheritance

```text
AEM admission traces must record the patch backend used for every code expert output.
```

## Next pressure

```text
add backend selection to TaskPacket or verifier config:
  backend=stdlib_one_file for deterministic tests
  backend=auto for local real runs
  backend=external for git-like environments
```
