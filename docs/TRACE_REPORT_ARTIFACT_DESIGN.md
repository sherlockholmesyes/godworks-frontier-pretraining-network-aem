# Trace Report Artifact — design

## Rejected option A

```text
trace report can be stdout only
```

Death: stdout is not preserved as a reviewable evidence artifact.

## Rejected option B

```text
trace report must wait for a full report schema and dashboard
```

Death: waiting blocks the first persisted evidence summary.

## Third

```text
trace report is written to JSON and uploaded beside trace artifacts
```

## Command

```bash
python -m aem_poc.trace_maint report <trace.jsonl> <trace_report.json>
```

## CI artifact bundle

```text
aem-trace-evidence
```

Contains:

```text
route_trace.jsonl
route_trace.compact.jsonl
route_trace.compact.jsonl.manifest.json
trace_report.json
```

## Invariant

```text
Every passing CI trace run produces raw trace, compact trace, manifest, and report JSON.
```

## Files

```text
aem_poc/trace_maint.py
tests/test_trace_maint.py
Makefile
.github/workflows/ci.yml
```

## Death of this step

```text
trace summary is only transient console output
```

Dead.

## Inheritance

```text
AEM evidence summaries must be durable artifacts.
```

## Next pressure

```text
add trace_report.schema.json and validate trace_report.json before upload.
```
