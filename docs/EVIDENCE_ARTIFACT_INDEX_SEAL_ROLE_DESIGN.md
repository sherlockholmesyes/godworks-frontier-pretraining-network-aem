# Evidence Artifact Index Seal Role design

wrong1: artifact index only needs producer/schema/verifier/purpose.
Death: that tells what generated the file, but not which seal boundary it belongs to.

wrong2: seal role can be inferred from path prefixes.
Death: path layout is weaker than explicit protocol metadata.

Third: every artifact index row includes seal_stage and role.

Fields added:

```text
seal_stage
role
```

Examples:

```text
first_stage_trace_seal / sealed_trace_evidence
first_stage_trace_seal_manifest / seal_manifest
second_stage_upload_receipt_seal / pre_evidence_metadata_receipt
second_stage_upload_receipt_seal / post_seal_verification_receipt
second_stage_upload_receipt_seal_manifest / second_stage_seal_manifest
terminal_receipt_boundary / terminal_second_stage_verify_receipt
```

Updated files:

```text
schemas/evidence_artifact_index.schema.json
aem_poc/evidence_artifact_index.py
docs/evidence_artifact_index.json
docs/EVIDENCE_ARTIFACT_INDEX.md
tests/test_evidence_artifact_index.py
```

Death: artifact index cannot explain seal boundaries.

Inheritance: AEM evidence metadata must state both artifact identity and seal role.

Next pressure: make structural fallback in schema_validation.py enforce seal_stage/role for evidence_artifact_index.schema.json.
