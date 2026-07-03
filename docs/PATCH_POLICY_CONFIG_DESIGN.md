# Patch Policy Config — design

## Rejected option A

```text
patch policy belongs inside RepoPatchPolicy defaults
```

Death: different nodes cannot replay why a patch was allowed or rejected.

## Rejected option B

```text
patch policy belongs to local environment config
```

Death: admission becomes machine-dependent.

## Third

```text
patch policy belongs to TaskPacket verifier constraints and is recorded in trace
```

## Contract

TaskPacket constraints may include:

```text
allowed_files
blocked_prefixes
max_patch_bytes
max_changed_files
```

Together with:

```text
patch_backend
test_command
```

## Files

```text
aem_poc/verifier_config.py
examples/task_code_patch.json
aem_poc/patch_gate_demo.py
tests/test_verifier_config.py
tests/test_patch_gate_demo.py
```

## Invariant

```text
PatchVerifierConfig.from_task(task)
creates RepoPatchPolicy from task constraints.
Patch gate demo passes that policy into WorkspacePrep.
Trace includes verifier_config payload with policy fields.
```

## Death of this step

```text
policy is hidden verifier state
```

Dead.

## Inheritance

```text
AEM verifier behavior must be replayable from TaskPacket constraints.
```

## Next pressure

```text
promote this into schemas/task_packet.schema.json and add a fixture where policy rejects a patch before tests run.
```
