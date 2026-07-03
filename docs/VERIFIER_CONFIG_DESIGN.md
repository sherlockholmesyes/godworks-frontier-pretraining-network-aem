# Verifier Config — design

## Rejected option A

```text
patch backend belongs inside workspace runner
```

Death: task traces cannot explain why a backend was selected.

## Rejected option B

```text
backend must be a global environment setting
```

Death: runs become non-replayable across nodes.

## Third

```text
backend selection belongs to task/verifier config and is recorded in trace
```

## Contract

TaskPacket constraints may include:

```text
patch_backend = stdlib_one_file | auto | external
test_command = selected command args
```

## Files

```text
aem_poc/verifier_config.py
examples/task_code_patch.json
aem_poc/patch_gate_demo.py
tests/test_verifier_config.py
```

## Invariant

```text
patch gate demo reads backend from TaskPacket constraints
trace includes verifier_config payload
```

## Death of this step

```text
backend selection is hidden runner state
```

Dead.

## Inheritance

```text
AEM verifier behavior must be declared by task/config, not hidden inside implementation.
```

## Next pressure

```text
move policy config into TaskPacket too:
allowed_files
blocked_prefixes
max_patch_bytes
max_changed_files
```
