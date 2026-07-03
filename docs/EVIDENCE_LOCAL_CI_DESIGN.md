# Evidence Local CI design

wrong1: evidence-local-ci only needs runtime evidence gates.
Death: artifact-index JSON, Markdown, and generated status can drift while the runtime evidence pipeline still passes.

wrong2: status can stay as a hand-read combination of README, Makefile, index, policy, and workflow.
Death: local CI should expose current evidence state as a generated gate.

Third: evidence-local-ci runs artifact-index checks and generated evidence status before evidence generation.

Command:

```bash
make evidence-local-ci
```

Gate order:

```text
test
evidence-artifact-index
evidence-artifact-index-md-check
evidence-status
evidence-metadata-check
evidence-upload-policy
evidence-upload-drift
evidence-seal-verify-demo
evidence-second-stage-seal
evidence-second-stage-seal-verify
```

CI runs:

```text
run: make evidence-local-ci
```

README names this as the canonical local verification command.

Then CI uploads the generated artifact bundle.

Files:

```text
Makefile
.github/workflows/ci.yml
tests/test_evidence_local_ci_target.py
tests/test_readme_local_verification.py
tests/test_evidence_status.py
README.md
```

Death: evidence status drifts outside the local CI gate.

Inheritance: AEM CI must be reproducible locally with one command before artifact upload, including reviewer-map and generated-status checks.

Next pressure: add README mention for evidence-status and include it in the canonical gate list.
