# Evidence Artifact Index JSON design

wrong1: human-readable artifact index is enough.
Death: tools cannot safely consume a Markdown table as protocol.

wrong2: tools can infer artifact meaning from filenames.
Death: filenames do not encode producer, schema, verifier, seal stage, role, or purpose.

Third: the repo has a schema-gated JSON artifact index for tools.

Machine-readable index:

```text
docs/evidence_artifact_index.json
```

Schema:

```text
schemas/evidence_artifact_index.schema.json
```

Tests:

```text
tests/test_evidence_artifact_index.py
tests/test_evidence_artifact_index_cli.py
```

Contract:

```text
index_version
artifact_count
artifacts[]:
  path
  producer
  schema
  verifier
  purpose
  seal_stage
  role
```

Covered artifact classes:

```text
metadata report
first-stage trace evidence
first-stage seal manifest
first-stage seal verify report
second-stage seal manifest
terminal second-stage verify report
```

Current artifact count:

```text
13
```

Death: artifact map is human-only and not consumable by tools.

Inheritance: AEM evidence metadata must be both human-readable and machine-readable, including seal-stage semantics.

Next pressure: make structural fallback in schema_validation.py enforce seal_stage/role for evidence_artifact_index.schema.json.
