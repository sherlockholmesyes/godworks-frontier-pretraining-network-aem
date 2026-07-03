# Evidence Second-Stage Seal Verify design

wrong1: second-stage verification can stay stdout-only.
Death: CI can verify the second-stage seal but leave no durable receipt for reviewers.

wrong2: durable second-stage verification must immediately be sealed by a third-stage seal.
Death: that starts another receipt recursion without a new external trust boundary.

Third: second-stage verification writes a durable terminal receipt and policy says it is not recursively sealed yet.

Command:

```bash
python -m aem_poc.evidence_second_stage_seal_verify \
  runs/upload/evidence_second_stage_seal_manifest.json \
  --output runs/upload/evidence_second_stage_verify_report.json

make evidence-second-stage-seal-verify
```

Durable report:

```text
runs/upload/evidence_second_stage_verify_report.json
```

Verifies:

```text
runs/metadata/evidence_metadata_report.json
runs/patch_gate_demo/evidence_seal_verify_report.json
```

Checks:

```text
manifest shape
artifact_count
file exists
size_bytes
sha256
```

Supported layouts:

```text
normal repo paths
preserved runs prefix
flat artifact folder by filename
```

Files:

```text
schemas/evidence_second_stage_verify_report.schema.json
aem_poc/evidence_second_stage_seal_verify.py
tests/test_evidence_second_stage_seal_verify.py
Makefile
.github/workflows/ci.yml
```

Death: second-stage verify result disappears after stdout.

Inheritance: AEM second-stage upload receipt seal must be machine-verified and leave a durable report before artifact publication.

Next pressure: add README/download guide update for two-stage verification plus terminal receipt boundary.
