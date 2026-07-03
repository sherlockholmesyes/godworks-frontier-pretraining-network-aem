# Evidence Seal Verify design

wrong1: evidence_seal_manifest.json is final proof.
Death: seal is still a claim until artifacts are rehashed.

wrong2: bundle verification is enough.
Death: bundle verification checks the earlier set, not the final post-run set.

Third: evidence_seal_verify recomputes hashes for every sealed artifact before publication.

Command:

```bash
python -m aem_poc.evidence_seal_verify runs/patch_gate_demo/evidence_seal_manifest.json
```

Top-level target:

```bash
make evidence-seal-verify-demo
```

Contract:

```text
read evidence_seal_manifest.json
validate evidence_seal_manifest.schema.json
check every sealed artifact exists
check size_bytes
recompute sha256
fail on missing or changed artifact
```

Files:

```text
aem_poc/evidence_seal_verify.py
tests/test_evidence_seal_verify.py
Makefile
.github/workflows/ci.yml
README.md
```

Death: final evidence set is sealed but not rechecked.

Inheritance: AEM final evidence must be sealed and machine-verified.

Next pressure: write evidence_seal_verify_report.json and publish it as the final verification receipt.
