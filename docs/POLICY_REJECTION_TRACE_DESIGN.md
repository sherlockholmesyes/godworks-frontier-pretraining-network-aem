# Policy Rejection Trace — design

## Rejected option A

```text
policy rejection is only a local precheck
```

Death: if it is not traced, another node cannot replay why no tests ran.

## Rejected option B

```text
all candidate patches should reach the command runner
```

Death: unsafe or out-of-surface patches waste verifier work and blur admission cause.

## Third

```text
policy rejection is a first-class verifier event recorded in RouteTrace
```

## New invariant

```text
forbidden patch:
  rejected by WorkspacePrep policy
  workspace_path is None
  changed_files is empty
  command runner is not needed
  RouteTrace records rejection reason
```

## Files

```text
schemas/task_packet.schema.json
examples/patches/forbidden_file.patch
tests/test_policy_rejection_trace.py
```

## Death of this step

```text
schema can lag runtime verifier constraints
```

Dead.

## Inheritance

```text
TaskPacket schema now declares patch verifier policy fields.
Policy rejection must be auditable without running tests.
```

## Next pressure

```text
add a JSON schema validation helper using stdlib-friendly optional validation path:
if jsonschema is installed, validate cards and task packets;
if not, fail softly in PoC with structural checks.
```
