# Evidence Upload Path Sync design

wrong1: upload drift guard is enough.
Death: it detects drift but still leaves repair as manual YAML editing.

wrong2: CI workflow path order should be hand-curated for readability.
Death: hand order can diverge from the canonical artifact index source order.

Third: workflow upload paths can be regenerated from source_artifact_paths() inside a marked generated block.

Sync command:

```bash
python -m aem_poc.evidence_upload_drift --sync
make evidence-upload-sync
```

Source:

```text
aem_poc.evidence_artifact_index.source_artifact_paths()
```

Target:

```text
.github/workflows/ci.yml upload-artifact path block for aem-trace-evidence
```

Generated markers:

```yaml
# BEGIN AEM GENERATED UPLOAD PATHS
path: |
  ...generated paths...
# END AEM GENERATED UPLOAD PATHS
```

The markers are outside the `path: |` literal block, so GitHub upload-artifact does not treat them as file patterns.

Checks after sync:

```text
missing_from_ci=[]
extra_in_ci=[]
duplicate_ci_paths=[]
markers_present=true
order_matches=true
```

Files:

```text
aem_poc/evidence_upload_drift.py
tests/test_evidence_upload_drift.py
Makefile
.github/workflows/ci.yml
README.md
```

Death: upload path drift is detected but not repairable by command.

Inheritance: AEM workflow upload paths must be renderable from the same source as the artifact index.

Next pressure: add one aggregate local CI target that runs metadata check, upload policy, upload drift, and two-stage seal verification in workflow order.
