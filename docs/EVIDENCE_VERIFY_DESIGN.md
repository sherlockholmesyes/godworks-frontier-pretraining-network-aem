# Evidence Verify — design

## Rejected option A

```text
evidence bundle manifest is proof by itself
```

Death: a manifest is only a claim until hashes are recomputed.

## Rejected option B

```text
verification can be manual reviewer work
```

Death: manual review cannot be the network gate.

## Third

```text
evidence verification is an executable hash check over the bundle manifest
```

## Command

```bash
python -m aem_poc.evidence_verify runs/patch_gate_demo/evidence_bundle_manifest.json
```

Top-level target:

```bash
make evidence-verify-demo
```

## Contract

```text
read evidence_bundle_manifest.json
validate evidence_bundle_manifest.schema.json
for every artifact:
  check file exists
  check size_bytes matches
  recompute sha256
  check sha256 matches
exit 1 on any missing or changed artifact
```

## Files

```text
aem_poc/evidence_verify.py
tests/test_evidence_verify.py
Makefile
.github/workflows/ci.yml
README.md
```

## Death of this step

```text
evidence bundle integrity is trusted but not rechecked
```

Dead.

## Inheritance

```text
AEM evidence bundles must be machine-verifiable after download.
```

## Next pressure

```text
write evidence_verify_report.json and upload it beside the evidence bundle.
```
