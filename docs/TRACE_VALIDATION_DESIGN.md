# RouteTrace Validation Gate — design

## Rejected option A

```text
RouteTrace is just JSONL append
```

Death: malformed evidence can enter the ledger.

## Rejected option B

```text
RouteTrace validation must require a hard dependency
```

Death: PoC loses stdlib replayability.

## Third

```text
RouteTrace append validates schema first through optional-strong / structural-soft validation
```

## New invariant

```text
TraceStore.append(trace)
  converts trace to dict
  validates route_trace.schema.json
  writes only if validation passes
```

## Files

```text
aem_poc/schema_validation.py
aem_poc/trace_store.py
tests/test_trace_validation.py
```

## Death of this step

```text
evidence ledger can accept malformed trace rows
```

Dead.

## Inheritance

```text
AEM trace artifacts must be schema-gated before storage.
```

## Next pressure

```text
add TraceStore replay gate:
read_all(validate=True) should validate every stored row and fail if any old trace is malformed.
```
