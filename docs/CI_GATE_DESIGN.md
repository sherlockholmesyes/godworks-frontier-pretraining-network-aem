# CI Gate — design

## Rejected option A

```text
AEM PoC works if local commands work once
```

Death: local success is not a network admission gate.

## Rejected option B

```text
CI can wait until the project is production-ready
```

Death: broken evidence plumbing can accumulate before anyone notices.

## Third

```text
CI must execute the current admission and evidence gates now
```

## CI contract

```text
python -m unittest discover -s tests
make trace-compact-demo
```

Then assert:

```text
runs/patch_gate_demo/route_trace.compact.jsonl exists
runs/patch_gate_demo/route_trace.compact.jsonl.manifest.json exists
```

## Files

```text
.github/workflows/ci.yml
docs/CI_GATE_DESIGN.md
```

## Invariant

```text
AEM cannot claim a green build unless tests and trace maintenance both pass.
```

## Death of this step

```text
evidence pipeline is manually checked
```

Dead.

## Inheritance

```text
Every new AEM gate must either be covered by tests or run in CI as an executable command.
```

## Next pressure

```text
add a CI status badge to README and a short local verification section.
```
