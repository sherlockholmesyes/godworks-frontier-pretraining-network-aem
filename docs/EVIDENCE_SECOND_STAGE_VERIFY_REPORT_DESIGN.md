# Evidence Second-Stage Verify Report design

wrong1: every uploaded report must be recursively sealed by another manifest.
Death: without a new external trust boundary this creates infinite seal recursion.

wrong2: avoiding recursion means no durable second-stage verification report.
Death: reviewers still need a downloadable receipt for the second-stage seal verification.

Third: write a durable terminal second-stage verify report, but do not seal it again under the current policy.

Report:

```text
runs/upload/evidence_second_stage_verify_report.json
```

Schema:

```text
schemas/evidence_second_stage_verify_report.schema.json
```

Command:

```bash
python -m aem_poc.evidence_second_stage_seal_verify \
  runs/upload/evidence_second_stage_seal_manifest.json \
  --output runs/upload/evidence_second_stage_verify_report.json
```

Policy class:

```text
terminal_verification_receipts
```

Terminal means:

```text
uploaded as final verification receipt
not sealed again unless a third-stage policy is explicitly added
```

Files:

```text
aem_poc/evidence_second_stage_seal_verify.py
aem_poc/evidence_upload_policy.py
tests/test_evidence_second_stage_seal_verify.py
tests/test_evidence_upload_policy.py
Makefile
.github/workflows/ci.yml
```

Death: second-stage verification either vanishes or recurses forever.

Inheritance: AEM can stop seal recursion only by naming the terminal receipt boundary explicitly.

Next pressure: add README/download guide update for two-stage verification plus terminal receipt boundary.
