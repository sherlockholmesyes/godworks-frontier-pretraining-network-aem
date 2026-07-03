# Evidence Seal Manifest — design

## Rejected option A

```text
pre-verification bundle manifest is enough
```

Death: later artifacts such as verify report and pipeline result remain outside the hash map.

## Rejected option B

```text
seal manifest should hash itself too
```

Death: self-hashing creates a circular artifact and blocks a simple reproducible PoC gate.

## Third

```text
evidence_pipeline writes a post-run seal manifest that hashes every uploaded evidence artifact except itself
```

## Schema

```text
evidence_seal_manifest.schema.json
  run_dir
  artifact_count
  sealed_artifacts[]:
    path
    size_bytes
    sha256
  excluded_artifacts[]
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
runs/patch_gate_demo/evidence_seal_manifest.json
```

## Sealed artifacts

```text
route_trace.jsonl
route_trace.compact.jsonl
route_trace.compact.jsonl.manifest.json
trace_report.json
evidence_summary.json
evidence_bundle_manifest.json
evidence_verify_report.json
pipeline_result.json
```

## Excluded artifact

```text
evidence_seal_manifest.json
```

## Files

```text
schemas/evidence_seal_manifest.schema.json
aem_poc/schema_validation.py
aem_poc/evidence_pipeline.py
tests/test_evidence_pipeline.py
.github/workflows/ci.yml
README.md
```

## Death of this step

```text
post-verification artifacts are uploaded without a hash handle
```

Dead.

## Inheritance

```text
AEM uploaded evidence must be sealed after the final receipt is written.
```

## Next pressure

```text
add a seal verification command:
read evidence_seal_manifest.json
recompute hashes for all sealed artifacts
fail if any uploaded artifact changed.
```
