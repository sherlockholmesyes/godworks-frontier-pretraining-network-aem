# AEM Trace and Receipt Spec

This file defines the missing audit artifacts without relying on prose summaries.

## TrainingReceipt

### Rejected option A

```text
training receipt = nice description of how an expert was trained
```

Death: descriptions are not replayable evidence.

### Rejected option B

```text
training receipt = full private training dump
```

Death: it makes participation impossible and leaks data.

### Third

```text
training receipt = minimal replay/audit handle
```

Required fields:

```text
receipt_id
expert_id
base_model_hash
recipe_hash
data_shard_ids
node_profile_hash
eval_before
eval_after
artifact_hashes
signature
```

## RouteTrace

### Rejected option A

```text
route trace = logs for debugging
```

Death: debug logs do not become learning material.

### Rejected option B

```text
route trace = full private prompt dump
```

Death: privacy leak.

### Third

```text
route trace = privacy-aware distillation memory unit
```

Required fields:

```text
trace_id
task_hash
task_type
router_version
candidate_experts
chosen_expert
verifier_reports
outcome_label
latency_ms
cost_units
privacy_level
redaction_status
```

## DataShardManifest

### Rejected option A

```text
data shard = dataset file path
```

Death: no provenance, no contamination control.

### Rejected option B

```text
data shard = central approved dataset
```

Death: central data authority.

### Third

```text
data shard = content-addressed training claim
```

Required fields:

```text
shard_id
content_hash
source_type
license
pii_status
dedup_status
contamination_report_hash
used_by_experts
eval_impact
```
