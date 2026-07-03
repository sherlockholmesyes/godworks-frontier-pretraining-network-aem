# Evidence Upload Policy design

wrong1: metadata and post-seal receipts can be claimed as first-stage sealed artifacts.
Death: they are not inputs to evidence_seal_manifest.json and must not be overclaimed.

wrong2: metadata and post-seal receipts can remain only policy-classified, not sealed.
Death: uploaded receipts still need hashes after they are produced.

Third: metadata and post-seal receipts are sealed by a second-stage upload receipt seal.

Classes:

```text
pre_evidence_metadata_receipts
sealed_trace_evidence
seal_manifests
post_seal_verification_receipts
second_stage_seal_manifests
```

Executable policy:

```bash
python -m aem_poc.evidence_upload_policy --check
make evidence-upload-policy
```

Policy decision:

```text
metadata and post-seal receipts are sealed by evidence_second_stage_seal_manifest.json,
not by the first-stage trace seal.
```

Second-stage sealed artifacts:

```text
runs/metadata/evidence_metadata_report.json
runs/patch_gate_demo/evidence_seal_verify_report.json
```

Second-stage seal manifest:

```text
runs/upload/evidence_second_stage_seal_manifest.json
```

Files:

```text
aem_poc/evidence_upload_policy.py
tests/test_evidence_upload_policy.py
Makefile
.github/workflows/ci.yml
docs/EVIDENCE_UPLOAD_POLICY.md
```

Death: uploaded artifacts have ambiguous sealing status.

Inheritance: AEM upload bundles distinguish first-stage sealed evidence, first-stage seal manifests, pre-evidence receipts, post-seal receipts, and second-stage seal manifests.

Next pressure: add second-stage seal verification command.
