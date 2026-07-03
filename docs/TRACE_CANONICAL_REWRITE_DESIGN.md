# Trace Canonical Rewrite — design

## Rejected option A

```text
TraceStore replay validation is enough
```

Death: validated rows can still remain in non-canonical mixed formatting, making audit diffs noisy.

## Rejected option B

```text
Trace compaction can rewrite traces without proof handles
```

Death: cleaning the ledger can silently alter evidence.

## Third

```text
TraceStore rewrite validates rows, writes canonical JSONL, and emits a rewrite manifest
```

## Contract

```text
rewrite_canonical(output_path)
  read_all(validate=True)
  write sorted canonical JSONL
  preserve row count
  emit source_hash
  emit output_hash
  emit rows_hash
```

## Files

```text
aem_poc/trace_store.py
tests/test_trace_validation.py
```

## Invariant

```text
malformed old rows cannot be compacted.
canonical rewrite produces a manifest with row_count and hashes.
```

## Death of this step

```text
trace cleanup is only formatting
```

Dead.

## Inheritance

```text
AEM evidence maintenance must be validated and hash-addressed.
```

## Next pressure

```text
add TraceRewriteManifest schema and write manifest JSON beside compacted trace.
```
