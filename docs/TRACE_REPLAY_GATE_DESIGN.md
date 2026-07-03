# Trace Replay Gate — design

## Rejected option A

```text
TraceStore validates only new appends
```

Death: old malformed rows can survive and poison replay.

## Rejected option B

```text
TraceStore read should always hard-fail on every old row
```

Death: migration/debug flows need a non-validating read path.

## Third

```text
TraceStore replay has explicit validation mode
```

## Contract

```text
read_all(validate=False)
  reads legacy rows without schema gate

read_all(validate=True)
  validates every row against route_trace.schema.json
  fails on invalid JSONL
  fails on malformed trace shape
```

## Files

```text
aem_poc/trace_store.py
tests/test_trace_validation.py
```

## Invariant

```text
validated replay cannot silently accept malformed evidence rows
```

## Death of this step

```text
old evidence rows are trusted because they are already written
```

Dead.

## Inheritance

```text
AEM evidence must be valid both on write and on replay.
```

## Next pressure

```text
add TraceStore compact/rewrite:
read validated rows
write canonical sorted JSONL to a new file
preserve row count and hashes
```
