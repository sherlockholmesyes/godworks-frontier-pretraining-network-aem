# Trace Rewrite Manifest — design

## Rejected option A

```text
TraceRewriteManifest can be an in-memory return value
```

Death: the compacted trace can travel without its proof handle.

## Rejected option B

```text
manifest JSON can be written without schema validation
```

Death: the proof handle itself can become malformed evidence.

## Third

```text
canonical trace rewrite writes a schema-gated manifest JSON beside the compacted trace
```

## Contract

```text
rewrite_canonical(output_path)
  validates source rows
  writes canonical JSONL
  builds TraceRewriteManifest
  validates trace_rewrite_manifest.schema.json
  writes <output>.manifest.json
```

## Files

```text
schemas/trace_rewrite_manifest.schema.json
aem_poc/schema_validation.py
aem_poc/trace_store.py
tests/test_trace_validation.py
```

## Invariant

```text
compacted trace and manifest are inseparable artifacts:
  compacted JSONL has validated rows
  manifest has row_count/source_hash/output_hash/rows_hash
  manifest itself validates before write
```

## Death of this step

```text
rewrite manifest is optional metadata
```

Dead.

## Inheritance

```text
AEM trace maintenance must emit validated proof handles beside rewritten evidence.
```

## Next pressure

```text
add a trace-maintenance CLI/demo:
python -m aem_poc.trace_maint compact <input> <output>
Then add make target trace-compact-demo.
```
