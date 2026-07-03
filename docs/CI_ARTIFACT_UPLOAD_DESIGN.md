# CI Artifact Upload — design

## Rejected option A

```text
CI only needs to check that trace artifacts exist
```

Death: existence checks do not preserve evidence after the run.

## Rejected option B

```text
trace artifacts only need to live in the local working directory
```

Death: reviewers and later agents cannot inspect the exact evidence from CI.

## Third

```text
CI uploads trace evidence as a named artifact
```

## Artifact

```text
aem-trace-evidence
```

Contents:

```text
runs/patch_gate_demo/route_trace.jsonl
runs/patch_gate_demo/route_trace.compact.jsonl
runs/patch_gate_demo/route_trace.compact.jsonl.manifest.json
```

## Files

```text
.github/workflows/ci.yml
docs/CI_ARTIFACT_UPLOAD_DESIGN.md
```

## Invariant

```text
Every CI run that passes trace maintenance preserves the trace evidence for review.
```

## Death of this step

```text
CI evidence disappears after command success
```

Dead.

## Inheritance

```text
AEM CI must make evidence artifacts downloadable, not just green.
```

## Next pressure

```text
add a minimal trace report command:
python -m aem_poc.trace_maint report <trace.jsonl>
It should print row_count, task_types, chosen_experts, and hash summary.
```
