# Trace Report Schema — design

## Rejected option A

```text
trace_report.json is just a convenience summary
```

Death: summary artifacts can drift into malformed evidence.

## Rejected option B

```text
trace reports need a full analytics system before schema
```

Death: waiting for analytics delays the first evidence-summary gate.

## Third

```text
trace_report.json is a schema-gated evidence artifact
```

## Contract

```text
trace_report.schema.json
  path
  row_count
  task_types
  chosen_experts
  file_hash
  rows_hash
```

## Runtime gate

```text
trace_report(input)
  validates rows through TraceStore.read_all(validate=True)
  builds report
  validates trace_report.schema.json

write_trace_report(input, output)
  writes only validated report JSON
```

## Files

```text
schemas/trace_report.schema.json
aem_poc/schema_validation.py
aem_poc/trace_maint.py
tests/test_trace_maint.py
```

## Death of this step

```text
trace report can be schema-less
```

Dead.

## Inheritance

```text
AEM evidence summaries must validate before upload or review.
```

## Next pressure

```text
add a top-level evidence command:
make evidence-demo
It should run repo-demo, compact, report, and list generated artifacts.
```
