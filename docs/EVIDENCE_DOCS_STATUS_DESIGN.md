# Evidence Docs Status design

wrong1: evidence-docs-check can be visible only in README and Makefile.
Death: generated evidence status would still omit the docs/example gate boundary.

wrong2: evidence-docs-check should be folded into evidence-local-ci to appear in status.
Death: that makes the status example check self-referential.

Third: evidence_status reports docs-check and docs-sync commands as separate fields, and README names that status line.

Status fields:

```text
docs_check_command
docs_check_gates
docs_sync_command
docs_sync_gates
```

Generated values:

```text
docs_check_command = make evidence-docs-check
docs_sync_command = make evidence-docs-sync
```

README status line:

```text
Docs gate status line in evidence_status
```

Boundary:

```text
evidence_status includes docs gate fields
evidence-local-ci does not include evidence-docs-check
evidence-docs-check still includes evidence-status-example-check
README exposes the docs gate status line
```

Files:

```text
aem_poc/evidence_status.py
schemas/evidence_status.schema.json
docs/evidence_status.example.json
tests/test_evidence_status.py
tests/test_readme_docs_status_line.py
README.md
```

Death: docs-check is visible as a command but absent from generated status.

Inheritance: AEM generated status should show both runtime evidence CI and docs/example drift gates without merging them.

Next pressure: add a lightweight docs-status check to evidence-docs-check that validates README names the docs gate status fields.
