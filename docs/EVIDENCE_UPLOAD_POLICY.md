# Evidence Upload and Sealing Policy

This policy defines how uploaded AEM CI artifacts relate to the current and second-stage seals.

## Decision

```text
metadata and post-seal receipts are sealed by evidence_second_stage_seal_manifest.json;
evidence_second_stage_verify_report.json is a terminal uploaded receipt unless a third-stage policy is added.
```

## Current upload classes

### Pre-evidence metadata receipts

```text
runs/metadata/evidence_metadata_report.json
```

Role: validates metadata before evidence generation.

Current seal status: sealed by:

```text
runs/upload/evidence_second_stage_seal_manifest.json
```

Reason: this receipt is produced before evidence generation. It cannot be part of the first-stage trace seal, but it can be sealed by the later upload receipt seal.

### Sealed trace evidence

The first-stage trace seal covers exactly `aem_poc.evidence_pipeline.SEALED_ARTIFACTS` under:

```text
runs/patch_gate_demo/
```

These files are recorded by size and sha256 in:

```text
runs/patch_gate_demo/evidence_seal_manifest.json
```

### First-stage seal manifest

```text
runs/patch_gate_demo/evidence_seal_manifest.json
```

Current seal status: not self-sealed.

Reason: a JSON file cannot contain a stable hash of itself. It is verified by:

```bash
python -m aem_poc.evidence_seal_verify runs/patch_gate_demo/evidence_seal_manifest.json
```

### Post-seal verification receipts

```text
runs/patch_gate_demo/evidence_seal_verify_report.json
```

Current seal status: sealed by:

```text
runs/upload/evidence_second_stage_seal_manifest.json
```

Reason: this receipt is produced after the first-stage seal verification step. It is the final receipt for the first-stage seal, not an input to that seal.

### Second-stage seal manifest

```text
runs/upload/evidence_second_stage_seal_manifest.json
```

Current seal status: not self-sealed.

Reason: it hashes metadata and post-seal receipts and intentionally excludes itself.

### Terminal verification receipts

```text
runs/upload/evidence_second_stage_verify_report.json
```

Current seal status: not sealed again under current policy.

Reason: this receipt is produced after second-stage seal verification. Sealing it would require an explicit third-stage policy to avoid silent infinite seal recursion.

## Executable policy

```bash
python -m aem_poc.evidence_upload_policy --check
make evidence-upload-policy
```

CI runs this check before evidence generation and artifact upload.
