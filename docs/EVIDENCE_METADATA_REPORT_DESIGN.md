# Evidence Metadata Report design

wrong1: evidence metadata check can remain stdout-only.
Death: CI can pass metadata integrity while leaving no durable metadata receipt.

wrong2: metadata report should be folded into the sealed trace bundle immediately.
Death: metadata is checked before evidence generation and should remain a separate pre-evidence receipt until the sealing model is extended.

Third: CI writes and uploads a durable evidence metadata report artifact.

Artifact:

```text
runs/metadata/evidence_metadata_report.json
```

Schema:

```text
schemas/evidence_metadata_report.schema.json
```

Command:

```bash
python -m aem_poc.evidence_metadata_check --output runs/metadata/evidence_metadata_report.json
make evidence-metadata-check
```

Report sections:

```text
json_index
markdown_index
artifact_drift
ok
```

Checks captured:

```text
JSON artifact index validates
JSON artifact index matches generated Python source table
Markdown artifact index matches generated Python source table
indexed paths match generated evidence artifact constants
sealed artifacts mention evidence_seal_verify as verifier
```

CI order:

```text
unit tests
metadata check -> writes runs/metadata/evidence_metadata_report.json
evidence pipeline + seal verify
artifact upload
```

Current upload includes:

```text
runs/metadata/evidence_metadata_report.json
```

Death: metadata integrity has no downloadable receipt.

Inheritance: AEM metadata gates must leave durable receipts before evidence artifacts are generated.

Next pressure: add metadata report indexing/sealing policy: decide whether metadata receipts are separate pre-evidence artifacts or included in a second-stage seal.
