# Evidence Artifact Index CLI design

wrong1: tools can read docs/evidence_artifact_index.json directly.
Death: every consumer would reimplement path loading, schema validation, and lookup behavior.

wrong2: artifact index only needs tests, not a user-facing command.
Death: reviewers and scripts need a stable CLI surface.

Third: aem_poc.evidence_artifact_index provides validate/list/show commands.

Commands:

```bash
python -m aem_poc.evidence_artifact_index validate
python -m aem_poc.evidence_artifact_index list
python -m aem_poc.evidence_artifact_index show trace_report.json
make evidence-artifact-index
```

API:

```text
load_artifact_index()
artifact_paths()
artifact_by_path(path)
validation_summary()
```

Files:

```text
aem_poc/evidence_artifact_index.py
tests/test_evidence_artifact_index_cli.py
Makefile
README.md
```

Death: artifact metadata has no stable command surface.

Inheritance: AEM evidence metadata must be queryable by both humans and tools.

Next pressure: add artifact-index sync command to regenerate docs/evidence_artifact_index.json from a Python source table.
