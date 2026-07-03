# Evidence Artifact Index Sync design

wrong1: checked-in evidence_artifact_index.json is the source of truth.
Death: manual JSON editing can drift from producer constants and metadata.

wrong2: drift tests are enough without regeneration.
Death: a failed drift test needs a canonical repair command.

Third: artifact index JSON is regenerated from a Python source table.

Source table:

```text
aem_poc.evidence_artifact_index.ARTIFACT_METADATA
```

Producer constants:

```text
aem_poc.evidence_pipeline.GENERATED_ARTIFACTS
aem_poc.evidence_pipeline.SEALED_ARTIFACTS
aem_poc.evidence_seal_verify.EVIDENCE_SEAL_VERIFY_REPORT_ARTIFACT
```

Commands:

```bash
python -m aem_poc.evidence_artifact_index sync
make evidence-artifact-index-sync
```

Validation:

```bash
python -m aem_poc.evidence_artifact_index validate
make evidence-artifact-index
```

Behavior:

```text
build_artifact_index() builds the protocol object
write_artifact_index() writes docs/evidence_artifact_index.json
validate checks schema and matches_generated=true
```

Tests:

```text
tests/test_evidence_artifact_index_cli.py
```

Death: artifact index repair is manual JSON editing.

Inheritance: AEM machine-readable evidence metadata is generated from Python source, then checked into docs.

Next pressure: add artifact-index Markdown sync/check so docs/EVIDENCE_ARTIFACT_INDEX.md stays aligned with the same Python source table.
