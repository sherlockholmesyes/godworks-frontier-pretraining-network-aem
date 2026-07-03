# Evidence Download Verify Two-Stage design

wrong1: downloaded bundle verification only needs the first-stage trace seal.
Death: metadata and post-seal receipts are uploaded too, and their bytes need verification.

wrong2: every terminal verify report must be sealed again immediately.
Death: that creates infinite receipt recursion unless a new third-stage trust boundary is explicitly introduced.

Third: downloaded bundle verification has two seal checks and one terminal receipt boundary.

First-stage check:

```bash
python -m aem_poc.evidence_seal_verify \
  <download-dir>/runs/patch_gate_demo/evidence_seal_manifest.json
```

Second-stage check:

```bash
python -m aem_poc.evidence_second_stage_seal_verify \
  <download-dir>/runs/upload/evidence_second_stage_seal_manifest.json
```

Terminal receipt:

```text
runs/upload/evidence_second_stage_verify_report.json
```

Review rule:

```text
first-stage seal verifies
second-stage seal verifies
terminal receipt exists
both local reports say ok=true and failure_count=0
```

Files updated:

```text
docs/EVIDENCE_DOWNLOAD_VERIFY.md
README.md
```

Death: download verification guide describes an obsolete one-stage bundle.

Inheritance: AEM downloaded evidence bundles must be verified according to the same seal boundaries CI used to produce them.

Next pressure: extend the artifact index to include metadata and upload-stage artifacts.
