# Evidence Upload Drift design

wrong1: CI upload paths can be maintained separately from the artifact index.
Death: CI can upload files that the reviewer map does not describe, or omit files the artifact index claims exist.

wrong2: artifact index can be trusted without checking or regenerating the upload-artifact path list.
Death: the index is only useful if it matches the actual published GitHub Actions bundle.

Third: CI upload paths are parsed, compared, marked, and optionally regenerated from source_artifact_paths().

Check command:

```bash
python -m aem_poc.evidence_upload_drift
make evidence-upload-drift
```

Sync command:

```bash
python -m aem_poc.evidence_upload_drift --sync
make evidence-upload-sync
```

Compares:

```text
.github/workflows/ci.yml upload-artifact path list
against
aem_poc.evidence_artifact_index.source_artifact_paths()
```

Checks:

```text
missing_from_ci
extra_in_ci
duplicate_ci_paths
markers_present
order_matches
```

Hard failures:

```text
missing_from_ci
extra_in_ci
duplicate_ci_paths
markers_present=false
```

Diagnostic after sync:

```text
order_matches=true
```

Markers:

```text
# BEGIN AEM GENERATED UPLOAD PATHS
# END AEM GENERATED UPLOAD PATHS
```

CI order:

```text
unit tests
metadata check
upload policy check
upload drift check
evidence generation / sealing
artifact upload
```

Files:

```text
aem_poc/evidence_upload_drift.py
tests/test_evidence_upload_drift.py
Makefile
.github/workflows/ci.yml
```

Death: uploaded bundle and artifact index drift apart.

Inheritance: AEM published evidence bytes must match the machine-readable artifact index exactly.

Next pressure: add one aggregate local CI target that runs metadata check, upload policy, upload drift, and two-stage seal verification in workflow order.
