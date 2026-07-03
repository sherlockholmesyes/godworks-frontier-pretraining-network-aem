# Evidence Artifact Index Markdown Sync design

wrong1: Markdown artifact index can be maintained separately from JSON.
Death: human docs can drift from the machine-readable protocol object.

wrong2: Markdown does not need a check because JSON is authoritative.
Death: reviewers read Markdown first; stale human docs become false evidence.

Third: Markdown artifact index is rendered and checked from the same Python source table as JSON.

Source table:

```text
aem_poc.evidence_artifact_index.ARTIFACT_METADATA
```

Generated Markdown:

```text
docs/EVIDENCE_ARTIFACT_INDEX.md
```

Commands:

```bash
python -m aem_poc.evidence_artifact_index md-check
python -m aem_poc.evidence_artifact_index md-sync
make evidence-artifact-index-md-check
make evidence-artifact-index-md-sync
```

Functions:

```text
render_markdown_index()
write_markdown_index()
markdown_matches_generated()
```

Tests:

```text
tests/test_evidence_artifact_index_cli.py
```

Checks:

```text
default Markdown matches generated output
md-sync writes generated Markdown
md-check exits 0 only when Markdown matches generated output
```

Death: reviewer-facing artifact index drifts from machine-readable metadata.

Inheritance: AEM evidence metadata has one Python source table, with JSON and Markdown renderers.

Next pressure: add CI/Make aggregate target for all metadata checks: JSON index validate, Markdown check, and artifact drift guard.
