# Evidence Pipeline Result — design

## Rejected option A

```text
evidence pipeline result can be stdout only
```

Death: stdout cannot serve as the durable receipt for the full orchestrated run.

## Rejected option B

```text
individual evidence artifacts are enough
```

Death: individual artifacts do not explain the full sequence and final outcome in one object.

## Third

```text
evidence_pipeline writes a schema-gated pipeline_result.json
```

## Schema

```text
evidence_pipeline_result.schema.json
  run_dir
  ok
  artifacts
  patch_gate
  trace_compact
  trace_report
  evidence_summary
  evidence_bundle_manifest
  evidence_verify_report
```

## Command

```bash
python -m aem_poc.evidence_pipeline
```

Thin wrapper:

```bash
make evidence-verify-demo
```

## Output

```text
runs/patch_gate_demo/pipeline_result.json
```

## Files

```text
schemas/evidence_pipeline_result.schema.json
aem_poc/schema_validation.py
aem_poc/evidence_pipeline.py
tests/test_evidence_pipeline.py
.github/workflows/ci.yml
README.md
```

## Death of this step

```text
full evidence pipeline has no durable final receipt
```

Dead.

## Inheritance

```text
AEM evidence orchestration must end in a schema-gated run receipt.
```

## Next pressure

```text
add post-run seal manifest for verification/pipeline artifacts,
so every uploaded evidence file has a hash handle.
```
