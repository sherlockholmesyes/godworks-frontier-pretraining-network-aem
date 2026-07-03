# Evidence Artifact Index Drift Guard design

wrong1: artifact index completeness can be tested with a hardcoded duplicate list.
Death: the test can drift together with the JSON index and miss pipeline changes.

wrong2: pipeline constants are implementation detail only.
Death: producer constants are the executable source of truth for generated and sealed artifacts.

Third: the artifact index test compares JSON metadata against pipeline constants.

Guarded files:

```text
docs/evidence_artifact_index.json
tests/test_evidence_artifact_index.py
aem_poc/evidence_pipeline.py
aem_poc/evidence_seal_verify.py
```

Imported source-of-truth constants:

```text
aem_poc.evidence_pipeline.GENERATED_ARTIFACTS
aem_poc.evidence_pipeline.SEALED_ARTIFACTS
aem_poc.evidence_seal_verify.EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
```

Checks:

```text
evidence_artifact_index.schema.json validates
artifact_count == len(artifacts)
paths are unique
JSON path set equals generated artifacts plus final seal-verify report
every sealed artifact mentions evidence_seal_verify as a verifier
```

Death: artifact index can silently drift away from the evidence pipeline.

Inheritance: AEM machine-readable evidence metadata must be tied to producer constants.

Next pressure: add an artifact index CLI to print, validate, and list evidence artifact metadata from docs/evidence_artifact_index.json.
