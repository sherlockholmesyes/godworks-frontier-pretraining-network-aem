# Trace Report — design

## Rejected option A

```text
trace artifact is enough if it can be downloaded
```

Death: reviewers still need to manually inspect JSONL.

## Rejected option B

```text
trace report should wait for a full dashboard
```

Death: waiting blocks the first evidence readout.

## Third

```text
trace report is a minimal validated summary over TraceStore replay
```

## Command

```bash
python -m aem_poc.trace_maint report <trace.jsonl>
```

## Output

```text
row_count
task_types
chosen_experts
file_hash
rows_hash
```

## CI

```text
CI runs trace report after trace compact demo.
```

## Files

```text
aem_poc/trace_maint.py
Makefile
.github/workflows/ci.yml
tests/test_trace_maint.py
```

## Death of this step

```text
trace evidence has no quick readout
```

Dead.

## Inheritance

```text
Every evidence artifact should eventually have a small report command.
```

## Next pressure

```text
write trace report JSON to disk and upload it in CI beside trace artifacts.
```
