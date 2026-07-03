# Evidence Artifact Index Upload-Stage design

wrong1: artifact index only needs trace-run artifacts.
Death: CI uploads metadata and upload-stage artifacts too, so the reviewer map is incomplete.

wrong2: metadata/upload artifacts can be documented only in upload policy.
Death: artifact index is the unified file-to-producer/schema/verifier/purpose map.

Third: artifact index covers the whole current CI upload bundle.

Added artifact paths:

```text
runs/metadata/evidence_metadata_report.json
runs/upload/evidence_second_stage_seal_manifest.json
runs/upload/evidence_second_stage_verify_report.json
```

Current indexed artifact count:

```text
13
```

Updated sources:

```text
aem_poc/evidence_artifact_index.py
docs/evidence_artifact_index.json
docs/EVIDENCE_ARTIFACT_INDEX.md
tests/test_evidence_artifact_index.py
tests/test_evidence_artifact_index_cli.py
```

Death: artifact index does not match the real uploaded bundle.

Inheritance: AEM artifact metadata must track all uploaded evidence bytes, not only first-stage trace bytes.

Next pressure: make the artifact index include seal stage/role fields, not only producer/schema/verifier/purpose.
