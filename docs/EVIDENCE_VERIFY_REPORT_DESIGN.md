# Evidence Verify Report — design

## Rejected option A

```text
evidence verification can be stdout plus exit code
```

Death: stdout is not a durable review artifact.

## Rejected option B

```text
evidence_verify_report.json can be added later after the verifier is useful
```

Death: the first verifier already creates reviewable evidence and needs a schema now.

## Third

```text
evidence_verify writes a schema-gated verification report JSON
```

## Schema

```text
evidence_verify_report.schema.json
  manifest_path
  run_dir
  artifact_count
  checked_count
  count_ok
  failure_count
  ok
  checks[]:
    recorded_path
    resolved_path
    exists
    expected_size_bytes
    actual_size_bytes
    size_ok
    expected_sha256
    actual_sha256
    hash_ok
    ok
```

## Command

```bash
python -m aem_poc.evidence_verify \
  runs/patch_gate_demo/evidence_bundle_manifest.json \
  runs/patch_gate_demo/evidence_verify_report.json
```

Top-level target:

```bash
make evidence-verify-demo
```

## CI artifact

```text
runs/patch_gate_demo/evidence_verify_report.json
```

## Files

```text
schemas/evidence_verify_report.schema.json
aem_poc/schema_validation.py
aem_poc/evidence_verify.py
tests/test_evidence_verify.py
Makefile
.github/workflows/ci.yml
README.md
```

## Death of this step

```text
verification result disappears after command output
```

Dead.

## Inheritance

```text
AEM evidence verification results must be durable, schema-gated artifacts.
```

## Next pressure

```text
add a reusable evidence pipeline module so Makefile is only a thin wrapper,
not the place where pipeline order lives.
```
