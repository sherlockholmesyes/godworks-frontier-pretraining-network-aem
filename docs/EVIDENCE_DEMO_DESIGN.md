# Evidence Demo — design

## Rejected option A

```text
AEM evidence pipeline can be multiple separate demo commands
```

Death: users and agents can run only part of the gate and think the evidence layer passed.

## Rejected option B

```text
top-level evidence command can just print success
```

Death: success without artifact enumeration hides missing evidence files.

## Third

```text
make evidence-demo runs the pipeline and lists expected evidence artifacts
```

## Command

```bash
make evidence-demo
```

## Flow

```text
repo-demo
trace compact
trace report JSON
artifact set verification
artifact listing
```

## Expected artifacts

```text
runs/patch_gate_demo/route_trace.jsonl
runs/patch_gate_demo/route_trace.compact.jsonl
runs/patch_gate_demo/route_trace.compact.jsonl.manifest.json
runs/patch_gate_demo/trace_report.json
```

## Files

```text
aem_poc/evidence_demo.py
tests/test_evidence_demo.py
Makefile
.github/workflows/ci.yml
README.md
```

## Death of this step

```text
evidence verification is scattered across commands
```

Dead.

## Inheritance

```text
AEM evidence should have one top-level reproducible gate.
```

## Next pressure

```text
write evidence_summary.json from make evidence-demo,
then validate and upload it beside the trace evidence bundle.
```
