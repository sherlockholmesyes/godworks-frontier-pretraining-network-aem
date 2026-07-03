# Evidence Bundle Manifest — design

## Rejected option A

```text
evidence upload is enough if all files are present
```

Death: presence does not prove the downloadable files were not changed later.

## Rejected option B

```text
each artifact can carry its own proof separately
```

Death: reviewers need one bundle-level hash map for the uploaded evidence set.

## Third

```text
evidence-demo writes a schema-gated bundle manifest with sha256 for each evidence artifact
```

## Contract

```text
evidence_bundle_manifest.schema.json
  run_dir
  artifact_count
  artifacts[]:
    path
    size_bytes
    sha256
```

## Command

```bash
make evidence-demo
```

## Output

```text
runs/patch_gate_demo/evidence_bundle_manifest.json
```

The bundle manifest records hashes for:

```text
route_trace.jsonl
route_trace.compact.jsonl
route_trace.compact.jsonl.manifest.json
trace_report.json
evidence_summary.json
```

It does not hash itself.

## Files

```text
schemas/evidence_bundle_manifest.schema.json
aem_poc/schema_validation.py
aem_poc/evidence_demo.py
tests/test_evidence_demo.py
Makefile
.github/workflows/ci.yml
README.md
```

## Death of this step

```text
uploaded evidence has no bundle-level hash map
```

Dead.

## Inheritance

```text
AEM downloadable evidence must be hash-addressed as a bundle.
```

## Next pressure

```text
add an evidence verify command:
read evidence_bundle_manifest.json
recompute hashes
fail if any artifact changed or disappeared.
```
