# Evidence Download Verification Guide

This guide explains how to verify a downloaded `aem-trace-evidence` artifact bundle from GitHub Actions.

## Goal

A passing CI run uploads an artifact bundle named:

```text
aem-trace-evidence
```

The bundle now has two seal stages plus one terminal verification receipt:

```text
first-stage trace seal:
  runs/patch_gate_demo/evidence_seal_manifest.json

second-stage upload receipt seal:
  runs/upload/evidence_second_stage_seal_manifest.json

terminal verification receipt:
  runs/upload/evidence_second_stage_verify_report.json
```

## Expected files

The downloaded bundle should contain these evidence files:

```text
runs/metadata/evidence_metadata_report.json
runs/upload/evidence_second_stage_seal_manifest.json
runs/upload/evidence_second_stage_verify_report.json
runs/patch_gate_demo/route_trace.jsonl
runs/patch_gate_demo/route_trace.compact.jsonl
runs/patch_gate_demo/route_trace.compact.jsonl.manifest.json
runs/patch_gate_demo/trace_report.json
runs/patch_gate_demo/evidence_summary.json
runs/patch_gate_demo/evidence_bundle_manifest.json
runs/patch_gate_demo/evidence_verify_report.json
runs/patch_gate_demo/pipeline_result.json
runs/patch_gate_demo/evidence_seal_manifest.json
runs/patch_gate_demo/evidence_seal_verify_report.json
```

Depending on how GitHub unpacks the artifact, files may be directly in the download directory, under the original `runs/...` paths, or flattened by filename. The verifier commands resolve normal paths, preserved `runs/...` paths, and flattened artifact folders by basename.

## Verify after download

From the repository root, unpack the artifact bundle into a temporary directory:

```bash
mkdir -p /tmp/aem-trace-evidence
unzip aem-trace-evidence.zip -d /tmp/aem-trace-evidence
```

### 1. Verify the first-stage trace seal

If the artifact preserves paths, run:

```bash
python -m aem_poc.evidence_seal_verify \
  /tmp/aem-trace-evidence/runs/patch_gate_demo/evidence_seal_manifest.json
```

If the artifact is flattened, run:

```bash
python -m aem_poc.evidence_seal_verify \
  /tmp/aem-trace-evidence/evidence_seal_manifest.json
```

This verifies the trace evidence artifacts recorded in:

```text
evidence_seal_manifest.json
```

### 2. Verify the second-stage upload receipt seal

If the artifact preserves paths, run:

```bash
python -m aem_poc.evidence_second_stage_seal_verify \
  /tmp/aem-trace-evidence/runs/upload/evidence_second_stage_seal_manifest.json
```

If the artifact is flattened, run:

```bash
python -m aem_poc.evidence_second_stage_seal_verify \
  /tmp/aem-trace-evidence/evidence_second_stage_seal_manifest.json
```

This verifies exactly:

```text
runs/metadata/evidence_metadata_report.json
runs/patch_gate_demo/evidence_seal_verify_report.json
```

## Expected result

Both verification commands must exit with code `0` and report:

```text
ok: true
failure_count: 0
count_ok: true
```

Any missing, edited, truncated, or moved sealed artifact should make the relevant command exit with code `1`.

## What is verified

`evidence_seal_verify` checks every artifact recorded in `evidence_seal_manifest.json`:

```text
exists
size_bytes
sha256
```

`evidence_second_stage_seal_verify` checks every receipt recorded in `evidence_second_stage_seal_manifest.json`:

```text
exists
size_bytes
sha256
```

Both seal manifests intentionally exclude themselves, because a self-hashing JSON file would be circular.

## Terminal receipt boundary

The terminal receipt is:

```text
runs/upload/evidence_second_stage_verify_report.json
```

It is uploaded as the final verification receipt for the second-stage seal. It is not sealed again under the current policy. Sealing it would require an explicit third-stage policy to avoid silent infinite seal recursion.

## Reviewer rule

A downloaded AEM evidence bundle is reviewable only if:

```text
evidence_seal_manifest.json validates
local evidence_seal_verify exits 0
evidence_second_stage_seal_manifest.json validates
local evidence_second_stage_seal_verify exits 0
evidence_second_stage_verify_report.json exists from CI
both local reports say ok=true and failure_count=0
```
