# Evidence Artifact Index

This generated index maps each AEM evidence file to its producer, schema, verifier, seal stage, role, and purpose.

## Top-level command

```bash
make evidence-metadata-check
make evidence-seal-verify-demo
make evidence-second-stage-seal
make evidence-second-stage-seal-verify
```

This flow runs:

```text
aem_poc.evidence_metadata_check
aem_poc.evidence_pipeline
aem_poc.evidence_seal_verify
aem_poc.evidence_second_stage_seal
aem_poc.evidence_second_stage_seal_verify
```

## Artifact table

| Evidence file | Seal stage | Role | Producer | Schema | Verifier / gate | Purpose |
|---|---|---|---|---|---|---|
| `runs/metadata/evidence_metadata_report.json` | second_stage_upload_receipt_seal | pre_evidence_metadata_receipt | aem_poc.evidence_metadata_check.write_metadata_report | evidence_metadata_report.schema.json | aem_poc.evidence_metadata_check, evidence_second_stage_seal_verify | Durable pre-evidence receipt for metadata integrity checks before evidence generation. |
| `runs/patch_gate_demo/route_trace.jsonl` | first_stage_trace_seal | sealed_trace_evidence | aem_poc.patch_gate_demo.run via TraceStore.append | route_trace.schema.json per row | TraceStore.append, TraceStore.read_all(validate=True), evidence_seal_verify | Raw route, admission, workspace, and command evidence for the patch-gate demo. |
| `runs/patch_gate_demo/route_trace.compact.jsonl` | first_stage_trace_seal | sealed_trace_evidence | aem_poc.trace_maint.compact_trace via TraceStore.rewrite_canonical | route_trace.schema.json per row | canonical rewrite, validated replay, evidence_seal_verify | Canonical compact trace for deterministic replay and downstream reporting. |
| `runs/patch_gate_demo/route_trace.compact.jsonl.manifest.json` | first_stage_trace_seal | sealed_trace_evidence | TraceStore.rewrite_canonical | trace_rewrite_manifest.schema.json | schema validation, evidence_seal_verify | Records source trace hash, compact trace hash, canonical rows hash, and row count. |
| `runs/patch_gate_demo/trace_report.json` | first_stage_trace_seal | sealed_trace_evidence | aem_poc.trace_maint.write_trace_report | trace_report.schema.json | trace report schema validation, evidence_seal_verify | Reviewer readout of compact trace row count, task types, chosen experts, file hash, and rows hash. |
| `runs/patch_gate_demo/evidence_summary.json` | first_stage_trace_seal | sealed_trace_evidence | aem_poc.evidence_demo.write_evidence_summary | evidence_summary.schema.json | summary schema validation, evidence_seal_verify | Lists the expected pre-verification evidence artifacts and fails if any are missing. |
| `runs/patch_gate_demo/evidence_bundle_manifest.json` | first_stage_trace_seal | sealed_trace_evidence | aem_poc.evidence_demo.write_evidence_bundle_manifest | evidence_bundle_manifest.schema.json | aem_poc.evidence_verify, evidence_seal_verify | Hash map for the pre-verification evidence bundle. |
| `runs/patch_gate_demo/evidence_verify_report.json` | first_stage_trace_seal | sealed_trace_evidence | aem_poc.evidence_verify.write_evidence_verify_report | evidence_verify_report.schema.json | verify report schema validation, evidence_seal_verify | Durable result of recomputing the pre-verification bundle hashes. |
| `runs/patch_gate_demo/pipeline_result.json` | first_stage_trace_seal | sealed_trace_evidence | aem_poc.evidence_pipeline.run_evidence_pipeline | evidence_pipeline_result.schema.json | pipeline result schema validation, evidence_seal_verify | Durable receipt for the full orchestrated evidence run. |
| `runs/patch_gate_demo/evidence_seal_manifest.json` | first_stage_trace_seal_manifest | seal_manifest | aem_poc.evidence_pipeline.write_evidence_seal_manifest | evidence_seal_manifest.schema.json | aem_poc.evidence_seal_verify | First-stage trace seal: hashes uploaded trace evidence artifacts except itself. |
| `runs/patch_gate_demo/evidence_seal_verify_report.json` | second_stage_upload_receipt_seal | post_seal_verification_receipt | aem_poc.evidence_seal_verify.write_evidence_seal_verify_report or make evidence-seal-verify-demo stdout redirection | evidence_seal_verify_report.schema.json | evidence_second_stage_seal_verify | Durable post-seal receipt for first-stage trace seal verification. |
| `runs/upload/evidence_second_stage_seal_manifest.json` | second_stage_upload_receipt_seal_manifest | second_stage_seal_manifest | aem_poc.evidence_second_stage_seal.write_second_stage_seal_manifest | evidence_second_stage_seal_manifest.schema.json | aem_poc.evidence_second_stage_seal_verify | Second-stage upload receipt seal: hashes metadata and post-seal verification receipts except itself. |
| `runs/upload/evidence_second_stage_verify_report.json` | terminal_receipt_boundary | terminal_second_stage_verify_receipt | aem_poc.evidence_second_stage_seal_verify.write_second_stage_verify_report | evidence_second_stage_verify_report.schema.json | terminal_verification_receipts policy | Terminal verification receipt for the second-stage seal; not recursively sealed without a third-stage policy. |

## Sealing model

There are two hash layers plus one terminal receipt:

```text
evidence_seal_manifest.json
  first-stage trace seal for generated trace/evidence artifacts

evidence_second_stage_seal_manifest.json
  second-stage upload receipt seal for metadata and post-seal receipts

evidence_second_stage_verify_report.json
  terminal verification receipt under current policy
```

## Local reviewer commands

After downloading the CI artifact bundle, verify both seal stages:

```bash
python -m aem_poc.evidence_seal_verify \
  <download-dir>/runs/patch_gate_demo/evidence_seal_manifest.json

python -m aem_poc.evidence_second_stage_seal_verify \
  <download-dir>/runs/upload/evidence_second_stage_seal_manifest.json
```

The bundle is reviewable only if both commands exit `0` and both reports have:

```text
ok=true
failure_count=0
```

## Machine-readable source

```text
docs/evidence_artifact_index.json
schemas/evidence_artifact_index.schema.json
```

Regenerate both index forms with:

```bash
python -m aem_poc.evidence_artifact_index sync
python -m aem_poc.evidence_artifact_index md-sync
```
