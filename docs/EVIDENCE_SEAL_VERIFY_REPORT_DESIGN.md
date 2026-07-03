# Evidence Seal Verify Report design

wrong1: final seal verification can be stdout plus exit code.
Death: CI can pass while the final verification receipt disappears.

wrong2: evidence_seal_manifest.json is enough for reviewers.
Death: reviewers still need to know whether the seal was actually recomputed and passed.

Third: evidence_seal_verify writes a schema-gated final verification report JSON.

Schema:

```text
evidence_seal_verify_report.schema.json
  manifest_path
  run_dir
  artifact_count
  checked_count
  excluded_artifacts
  count_ok
  failure_count
  ok
  checks[]
```

Command:

```bash
python -m aem_poc.evidence_seal_verify \
  runs/patch_gate_demo/evidence_seal_manifest.json \
  runs/patch_gate_demo/evidence_seal_verify_report.json
```

Make target:

```bash
make evidence-seal-verify-demo
```

CI artifact:

```text
runs/patch_gate_demo/evidence_seal_verify_report.json
```

Death: final verification result disappears after command output.

Inheritance: AEM final uploaded evidence needs a durable verification receipt.

Next pressure: add an evidence download verify guide for CI artifacts.
