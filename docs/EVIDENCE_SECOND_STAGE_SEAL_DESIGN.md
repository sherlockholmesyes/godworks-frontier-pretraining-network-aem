# Evidence Second-Stage Seal design

wrong1: metadata and post-seal receipts can be left unsealed because they are not trace evidence.
Death: CI uploads them, so reviewers need a hash receipt for those bytes too.

wrong2: metadata and post-seal receipts should be inserted into the first-stage trace seal.
Death: they are produced before and after the first-stage seal boundary, so adding them there would lie about execution order.

Third: write a second-stage upload seal for metadata and post-seal receipts.

Second-stage manifest:

```text
runs/upload/evidence_second_stage_seal_manifest.json
```

Sealed by this manifest:

```text
runs/metadata/evidence_metadata_report.json
runs/patch_gate_demo/evidence_seal_verify_report.json
```

Write command:

```bash
python -m aem_poc.evidence_second_stage_seal --output runs/upload/evidence_second_stage_seal_manifest.json
make evidence-second-stage-seal
```

Verify command:

```bash
python -m aem_poc.evidence_second_stage_seal_verify runs/upload/evidence_second_stage_seal_manifest.json
make evidence-second-stage-seal-verify
```

Schema:

```text
schemas/evidence_second_stage_seal_manifest.schema.json
```

Files:

```text
aem_poc/evidence_second_stage_seal.py
aem_poc/evidence_second_stage_seal_verify.py
tests/test_evidence_second_stage_seal.py
tests/test_evidence_second_stage_seal_verify.py
Makefile
.github/workflows/ci.yml
docs/EVIDENCE_UPLOAD_POLICY.md
```

Death: uploaded receipt bytes have no seal.

Inheritance: AEM evidence has two seal stages: trace evidence seal, then upload receipt seal.

Next pressure: add durable second-stage seal verify report only if we accept a third-stage final receipt boundary.
