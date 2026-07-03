# Evidence Docs Targets design

wrong1: status example check belongs in evidence-local-ci.
Death: evidence-local-ci feeds evidence_status.local_ci_gates, so checking an example that records that gate list inside the same gate risks self-reference.

wrong2: status example check can remain a loose standalone command.
Death: checked-in docs/examples need one explicit docs-only gate.

Third: docs/example drift checks live in evidence-docs-check, with a matching evidence-docs-sync generator target.

Check command:

```bash
make evidence-docs-check
```

Check order:

```text
evidence-artifact-index
evidence-artifact-index-md-check
evidence-status-example-check
```

Sync command:

```bash
make evidence-docs-sync
```

Sync order:

```text
evidence-artifact-index-sync
evidence-artifact-index-md-sync
evidence-status-example-sync
```

Boundary:

```text
evidence-local-ci includes evidence-status
evidence-local-ci does not include evidence-status-example-check
evidence-docs-check includes evidence-status-example-check
README exposes evidence-docs-check and evidence-docs-sync
evidence_status exposes docs_check_command and docs_sync_command
```

Files:

```text
Makefile
tests/test_evidence_docs_targets.py
tests/test_readme_local_verification.py
tests/test_evidence_status.py
README.md
```

Death: docs drift checks are either self-referential or loose commands.

Inheritance: AEM generated docs/examples need their own gate group separate from runtime evidence CI.

Next pressure: add docs-check status line to README evidence-status section.
