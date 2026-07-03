# Evidence Artifact Index Structural Fallback design

wrong1: JSON Schema requiring seal_stage/role is enough.
Death: the repo intentionally supports stdlib-only validation when jsonschema is unavailable.

wrong2: stdlib fallback can accept an older, weaker artifact-index shape.
Death: CI or reviewers without jsonschema would silently miss seal-stage metadata drift.

Third: structural fallback enforces the same artifact-index row contract: path, producer, schema, verifier, purpose, seal_stage, and role.

Enforced row fields:

```text
path
producer
schema
verifier
purpose
seal_stage
role
```

Updated fallback:

```text
aem_poc/schema_validation.py::_artifact_index_list
```

Tests:

```text
tests/test_evidence_artifact_index.py::test_structural_fallback_accepts_generated_artifact_index
tests/test_evidence_artifact_index.py::test_structural_fallback_rejects_old_artifact_index_shape_without_seal_role
```

Death: stdlib validation accepts artifact index rows that JSON Schema rejects.

Inheritance: AEM schema contracts must hold with or without optional jsonschema dependency.

Next pressure: add upload artifact list drift guard comparing CI upload path list against artifact index paths.
