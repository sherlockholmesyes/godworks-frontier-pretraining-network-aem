# Evidence Metadata Check design

wrong1: metadata checks can stay as separate commands.
Death: JSON validation, Markdown check, and drift guard can pass or fail in different places with no single metadata gate.

wrong2: unit tests alone are enough for metadata integrity.
Death: CI and reviewers need one executable metadata check with a JSON report.

Third: evidence_metadata_check aggregates JSON index validation, Markdown check, and artifact drift guard.

Command:

```bash
python -m aem_poc.evidence_metadata_check
make evidence-metadata-check
```

Checks:

```text
JSON artifact index validates
JSON artifact index matches generated Python source table
Markdown artifact index matches generated Python source table
indexed paths match generated evidence artifact constants
sealed artifacts mention evidence_seal_verify as verifier
```

Files:

```text
aem_poc/evidence_metadata_check.py
tests/test_evidence_metadata_check.py
Makefile
.github/workflows/ci.yml
```

CI order:

```text
unit tests
metadata check
evidence pipeline + seal verify
artifact upload
```

Death: evidence metadata integrity has no single executable gate.

Inheritance: AEM metadata must fail fast before evidence artifacts are generated and uploaded.

Next pressure: add a CI metadata report artifact, so evidence metadata checks also leave a durable receipt.
