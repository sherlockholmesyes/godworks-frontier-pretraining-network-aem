# Evidence Status design

wrong1: reviewers can inspect README, Makefile, artifact index, upload policy, and workflow separately.
Death: current status becomes scattered across several files and can be misread.

wrong2: status should be a hand-written summary doc.
Death: hand-written status drifts from source tables.

Third: evidence status is generated from source tables, schema-gated, and checked in as an example JSON.

Command:

```bash
python -m aem_poc.evidence_status
make evidence-status
```

Optional output:

```bash
python -m aem_poc.evidence_status --output runs/evidence_status.json
```

Checked-in example:

```text
docs/evidence_status.example.json
```

Example check/sync:

```bash
python -m aem_poc.evidence_status --check-example
python -m aem_poc.evidence_status --sync-example
make evidence-status-example-check
make evidence-status-example-sync
make evidence-docs-check
make evidence-docs-sync
```

Docs-only target boundary:

```text
evidence-docs-check checks the status example
evidence-local-ci prints generated status but does not check the status example
```

Status includes:

```text
local_ci_command
local_ci_gates
docs_check_command
docs_check_gates
docs_sync_command
docs_sync_gates
artifact paths
artifact_count
seal_stage_counts
role_counts
upload policy class counts
terminal receipts
second-stage sealed artifacts
upload drift summary
```

Source tables:

```text
Makefile evidence-local-ci recipe
Makefile evidence-docs-check recipe
Makefile evidence-docs-sync recipe
aem_poc.evidence_artifact_index.build_artifact_index()
aem_poc.evidence_upload_policy.build_upload_policy()
aem_poc.evidence_upload_drift.upload_drift_report()
```

Schema:

```text
schemas/evidence_status.schema.json
```

Files:

```text
aem_poc/evidence_status.py
schemas/evidence_status.schema.json
docs/evidence_status.example.json
tests/test_evidence_status.py
tests/test_readme_local_verification.py
tests/test_evidence_docs_targets.py
Makefile
README.md
```

Death: evidence status is scattered and hand-audited.

Inheritance: AEM evidence state should be generated from executable source tables, not rewritten by hand.

Next pressure: add README/docs status line that says docs-check is separate and visible in evidence_status output.
