# Evidence Summary — design

## Rejected option A

```text
evidence-demo can print artifact summary only
```

Death: console summary disappears after local or CI run.

## Rejected option B

```text
evidence summary can be schema-less metadata
```

Death: the artifact set proof can itself become malformed evidence.

## Third

```text
evidence-demo writes a schema-gated evidence_summary.json
```

## Contract

```text
evidence_summary.schema.json
  run_dir
  artifact_count
  missing_count
  missing
  artifacts[]:
    path
    exists
    size_bytes
```

## Command

```bash
make evidence-demo
```

## Output

```text
runs/patch_gate_demo/evidence_summary.json
```

## CI bundle

```text
aem-trace-evidence
```

Includes:

```text
route_trace.jsonl
route_trace.compact.jsonl
route_trace.compact.jsonl.manifest.json
trace_report.json
evidence_summary.json
```

## Death of this step

```text
evidence artifact set is only visible in stdout
```

Dead.

## Inheritance

```text
AEM evidence set summaries must be durable and schema-gated.
```

## Next pressure

```text
add an evidence bundle manifest:
one JSON file that records hashes for every uploaded evidence artifact.
```
