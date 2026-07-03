# Patch Policy Gate — design

## Rejected option A

```text
patch verifier = apply diff and run tests
```

Death: tests alone do not say whether the patch touched the right surface.

## Rejected option B

```text
patch verifier must wait for a hardened production sandbox
```

Death: waiting blocks the first repo-shaped gate.

## Third

```text
patch verifier = policy gate + objective tests + audit hashes
```

## New invariant

```text
patch accepted only if:
  target file is allowed
  patch size is below limit
  changed-file count is below limit
  tests pass
  patch_hash is recorded
  fixture_hash is recorded
  stdout/stderr hashes are recorded
```

## Files

```text
aem_poc/hash_utils.py
aem_poc/repo_patch_policy.py
aem_poc/patch_gate_demo.py
tests/test_repo_patch_policy.py
tests/test_patch_gate_demo.py
```

## Death of this step

```text
unit tests alone are enough for code expert admission
```

Dead.

## Inheritance

```text
AEM code expert admission must preserve audit handles:
patch_hash, fixture_hash, policy report, test report.
```

## Next pressure

```text
move from tiny one-file diff apply to isolated git-style workspace runner:
copy repo
apply patch
check changed files after apply
run selected test command
emit stdout/stderr hashes and file diff summary
```
