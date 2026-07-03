# Repo Patch Gate — design

## Rejected option A

```text
code expert output = replacement module body
```

Death: this is not a real patch workflow.

## Rejected option B

```text
code expert output must be accepted only after a full production sandbox exists
```

Death: waiting for perfect sandbox blocks the first objective gate.

## Third

```text
code expert output = unified diff over a fixture repo, checked by objective tests
```

## Executable path

```bash
python -m aem_poc.patch_gate_demo
make repo-demo
python -m unittest discover -s tests
```

## Expected invariant

```text
fixture repo starts with failing calc.py
fake patch keeps tests failing
passing patch makes tests pass
fake expert admission = false
real expert admission = true
route_trace.jsonl is written
```

## Files

```text
fixtures/code_patch_repo/calc.py
fixtures/code_patch_repo/test_calc.py
examples/patches/fake_calc.patch
examples/patches/pass_calc.txt
aem_poc/diff_apply.py
aem_poc/patch_gate_demo.py
tests/test_patch_gate_demo.py
```

## Death of this step

```text
module replacement verifier is enough for code experts
```

Dead.

## Inheritance

```text
AEM code experts must move toward patch-shaped outputs and repo-shaped verifiers.
```

## Next pressure

```text
replace the tiny diff applier with a real isolated git-apply style runner and forbidden-file policy
```
