# Evidence Status Example design

wrong1: evidence_status command output is enough.
Death: reviewers cannot inspect a stable checked-in example without running the command.

wrong2: checked-in status example can be maintained by hand.
Death: hand-maintained examples drift from executable source tables.

Third: docs/evidence_status.example.json is generated and exact-match checked.

Example:

```text
docs/evidence_status.example.json
```

Check command:

```bash
python -m aem_poc.evidence_status --check-example
make evidence-status-example-check
make evidence-docs-check
```

Sync command:

```bash
python -m aem_poc.evidence_status --sync-example
make evidence-status-example-sync
make evidence-docs-sync
```

Docs-only target boundary:

```text
evidence-docs-check includes evidence-status-example-check
evidence-local-ci does not include evidence-status-example-check
```

Tests:

```text
tests/test_evidence_status.py::test_checked_in_status_example_matches_generated_status
tests/test_evidence_status.py::test_cli_checks_status_example
tests/test_evidence_status.py::test_cli_syncs_status_example
tests/test_evidence_docs_targets.py
```

Death: evidence status example exists but is not generated from current source tables.

Inheritance: AEM checked-in examples must be executable receipts, not stale docs.

Next pressure: add README mention for evidence-docs-check and evidence-docs-sync.
