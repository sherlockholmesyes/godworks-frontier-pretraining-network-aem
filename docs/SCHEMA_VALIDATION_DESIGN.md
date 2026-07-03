# Schema Validation Gate — design

## Rejected option A

```text
schemas are documentation only
```

Death: runtime can accept malformed cards/tasks while schemas look correct.

## Rejected option B

```text
schema validation must require a hard dependency
```

Death: the PoC loses stdlib replayability.

## Third

```text
schema validation is optional-strong and structural-soft
```

If `jsonschema` is installed:

```text
validate with JSON Schema files
```

If not:

```text
run stdlib structural checks for core fields
```

## Files

```text
aem_poc/schema_validation.py
aem_poc/loaders.py
tests/test_schema_validation.py
```

## Invariant

```text
load_task_packet
load_expert_card
load_teacher_card
```

must validate before constructing runtime objects.

## Death of this step

```text
schema can drift away from loaders
```

Dead.

## Inheritance

```text
AEM JSON artifacts are admitted through validation first.
```

## Next pressure

```text
add schema-aware trace validation:
RouteTrace written by TraceStore must satisfy route_trace.schema.json before append.
```
