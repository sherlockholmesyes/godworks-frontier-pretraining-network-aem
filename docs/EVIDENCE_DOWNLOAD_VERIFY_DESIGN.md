# Evidence Download Verify design

wrong1: CI artifact upload is enough.
Death: a reviewer still needs to verify the downloaded bytes, not just trust CI UI.

wrong2: local verification can be tribal knowledge.
Death: undocumented verification becomes manual folklore instead of protocol.

Third: the repo includes a local verification guide for downloaded CI evidence bundles.

Guide:

```text
docs/EVIDENCE_DOWNLOAD_VERIFY.md
```

Core command:

```bash
python -m aem_poc.evidence_seal_verify \
  <download-dir>/evidence_seal_manifest.json \
  <download-dir>/evidence_seal_verify_report.local.json
```

Fallback layout command:

```bash
python -m aem_poc.evidence_seal_verify \
  <download-dir>/runs/patch_gate_demo/evidence_seal_manifest.json \
  <download-dir>/runs/patch_gate_demo/evidence_seal_verify_report.local.json
```

Review rule:

```text
local verification exits 0
local report ok=true
local report failure_count=0
```

Files:

```text
docs/EVIDENCE_DOWNLOAD_VERIFY.md
docs/EVIDENCE_DOWNLOAD_VERIFY_DESIGN.md
README.md
```

Death: downloaded evidence verification is not documented.

Inheritance: AEM CI evidence must be locally reproducible after download.

Next pressure: add an evidence artifact index doc mapping each evidence file to producer, schema, verifier, and purpose.
