# Trace Maintenance CLI — design

## Rejected option A

```text
trace maintenance can stay as Python API
```

Death: evidence maintenance cannot be run reproducibly by nodes or CI without custom glue.

## Rejected option B

```text
trace maintenance must wait for a full ops tool
```

Death: waiting blocks the first maintenance gate.

## Third

```text
trace maintenance is a small CLI over validated TraceStore operations
```

## Command

```bash
python -m aem_poc.trace_maint compact <input> <output>
```

## Make target

```bash
make trace-compact-demo
```

## Flow

```text
run patch gate demo
read route_trace.jsonl with validate=True
write canonical route_trace.compact.jsonl
write route_trace.compact.jsonl.manifest.json
validate manifest schema
```

## Files

```text
aem_poc/trace_maint.py
Makefile
tests/test_trace_maint.py
```

## Death of this step

```text
trace compaction is only an internal library call
```

Dead.

## Inheritance

```text
AEM evidence maintenance must be runnable as a reproducible command.
```

## Next pressure

```text
add CI workflow:
python -m unittest discover -s tests
make trace-compact-demo
```
