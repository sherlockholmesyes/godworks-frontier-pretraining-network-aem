# Evidence Pipeline — design

## Rejected option A

```text
evidence pipeline order can live in Makefile
```

Death: shell glue becomes the real protocol and Python APIs drift.

## Rejected option B

```text
every evidence step should stay separately runnable only
```

Death: separate tools are useful, but CI and reviewers need one canonical gate.

## Third

```text
aem_poc.evidence_pipeline orchestrates the evidence run; Makefile is a thin wrapper
```

## Command

```bash
python -m aem_poc.evidence_pipeline
```

Thin wrapper:

```bash
make evidence-verify-demo
```

## Pipeline order

```text
patch gate demo
trace compact
trace report JSON
evidence summary JSON
evidence bundle manifest JSON
evidence verify report JSON
```

## Artifacts

```text
route_trace.jsonl
route_trace.compact.jsonl
route_trace.compact.jsonl.manifest.json
trace_report.json
evidence_summary.json
evidence_bundle_manifest.json
evidence_verify_report.json
```

## Files

```text
aem_poc/evidence_pipeline.py
tests/test_evidence_pipeline.py
Makefile
README.md
```

## Death of this step

```text
Makefile is the source of truth for evidence sequencing
```

Dead.

## Inheritance

```text
AEM evidence sequencing is a reusable Python module with an executable CLI.
```

## Next pressure

```text
add evidence_pipeline_result.schema.json and persist pipeline_result.json
for the full orchestrated run.
```
