# AEM Public Handoff Pack

Repository: https://github.com/sherlockholmesyes/frontier-pretraining-network-aem  
Public framing name: **AEM - expert/adaptation admission PoC**  
Audience: OSS contributors, evaluator builders, adapter/training pipeline builders  
Status: **early runnable PoC, not a real trainer, not a product**

## 0. One-line public pitch

AEM is a small Python PoC for admitting and routing specialized model adapters/experts using expert cards, objective verifier reports, route traces, and evidence artifacts.

Use this pitch publicly:

```text
I'm looking for small boring infrastructure patches for an expert/adaptation admission PoC: ExpertCard schema, verifier receipts, route traces, adapter artifact manifests, eval/regression gates, and evidence bundle checks. No token launch, no fundraising, no broad capability claims, no broad architecture rewrite.
```

## 1. Current scope

The repo already has a runnable skeleton for task-level routing and admission gates. The immediate goal is to harden the boring infrastructure around expert/adaptation artifacts: schemas, receipts, eval evidence, traces, and small local interfaces.

Current baseline:

```bash
python -m aem_poc.demo
python -m aem_poc.patch_gate_demo
make evidence-local-ci
make aem-network-economy-check
python -m unittest discover -s tests
```

Current objects and flows to preserve:

- `TaskPacket`: task-level packet for routing.
- `ExpertCard`: capability/adaptation manifest.
- `ObjectiveVerifier`: admission gate using eval delta, regression, duplicate risk, backdoor risk, latency, VRAM, and signature.
- `ObjectiveAdmissionGate`: requires verifier reports before admission.
- `RouteTrace`: evidence for route/admission decisions.
- Evidence pipeline: local artifacts, manifests, verification reports, and seals.
- Network/economy simulators: receipts and in-memory credit settlement used as protocol tests, not as a public token.

Current limitations:

- There is no real training backend.
- There is no real adapter runtime.
- There is no distributed training.
- There is no public verifier network.
- There is no production artifact registry.
- There is no privacy-preserving inference/training primitive.
- Credit/accounting code is a simulator and should not be marketed publicly.

## 2. Non-goals for public tasks

Do not add any of the following in contributor patches:

- token launch, marketplace, resale, investment, or fundraising language
- hype, revolution, or civilization-scale claims
- unauthorized scraping or third-party model distillation
- claims that this trains a large production model today
- distributed dense model training across random home GPUs
- remote hidden-state model parallelism
- raw prompt, raw output, or private dataset logging
- broad architecture rewrites
- new dependencies unless the task explicitly allows them
- blockchain claims without implementation
- governance/economy expansion unless specifically assigned

Public contributions should look like evaluator/training-infrastructure work.

## 3. Contributor rules

- One small task per PR or diff.
- Keep diffs under roughly 300 lines when possible.
- Prefer Python stdlib.
- Use `unittest` for tests.
- Keep `make evidence-local-ci` or the relevant narrower test command working.
- Keep existing demos working.
- Preserve existing schema/evidence style.
- Do not log raw prompts, outputs, or private datasets.
- Use hashes/commitments for sensitive artifacts.
- Include test command and result in every handoff.
- Do not turn research simulators into public token/economy claims.

## 4. Missing bricks

| Brick | Current state | Why it matters | Smallest useful task |
|---|---:|---|---|
| Real adapter trainer | missing | Expert admission needs actual LoRA/adapter training path eventually. | Add trainer interface + mock trainer receipt. |
| Adapter artifact manifest | missing/partial | Admitted experts need portable artifact contracts. | Manifest schema with base hash, adapter hash, eval evidence. |
| TrainingReceipt hardening | partial/proto | Useful training should be recorded without rewarding compute burn. | Receipt schema/test for eval delta + provenance. |
| Eval runner interface | partial | Verifiers need a generic command-runner contract. | `EvalJob` + `EvalReport` dataclasses and tests. |
| Regression eval gate | partial | Target improvement must not break general ability. | Add explicit regression report format. |
| Anti-overfit challenge | missing | Eval gains can be gamed. | Add challenge packet schema + placeholder test. |
| Dataset/provenance ledger | partial/missing | Training data needs source/use policy and hashes. | `DataShardReceipt` schema + validation. |
| Contamination check | missing | Eval leakage breaks trust. | Add contamination report schema stub. |
| Duplicate/near-duplicate expert check | partial | Prevent farming copies of the same adapter. | Deterministic hash/Jaccard placeholder and tests. |
| Backdoor/trigger risk report | partial | Admission needs explicit safety evidence. | Risk report schema + gate integration test. |
| Artifact registry | missing | Experts need content-addressed storage and lookup. | Local filesystem registry with hashes. |
| Verifier challenge network | missing | Single verifier is not enough for public network. | Challenge packet + local replay verifier. |
| Node capacity binding | partial/proto | Training/verification jobs need hardware bounds. | Node capacity receipt stub. |
| AEM-to-GOWN bridge | missing/proto | Admitted experts need serving cards. | Convert `ExpertCard` to GOWN-style `ModelCard` draft. |
| Sandbox/privacy policy | partial | Running unknown code/tasks is risky. | Sandbox policy schema + blocked path tests. |
| Settlement/fraud finality | simulator only | Receipts need challenge windows before accounting. | Keep private; only add tests if assigned. |
| Governance/migration | research only | Protocol changes need versioning later. | Do not expose first; add version compatibility tests only. |

## 5. High-priority contributor task queue

### AEM-001  Public README status and safety pass

Goal: make the repo readable as an early evaluator/admission PoC.

Change:

- Add `Status: early runnable PoC, not a real trainer, not a product` near the top.
- Add `What this is` and `What this is not` sections.
- Make clear that current work is local/test/evidence infrastructure.
- Do not market token/economy components.
- Do not claim production training exists today.
- Preserve technical docs and commands.

Acceptance:

- README does not read like a fundraising, token, or broad capability pitch.
- A new contributor understands the next small technical task.
- No code changes.

Patch prompt:

```text
Make a README-only public framing pass. Keep technical content and commands, but make status and non-goals clear: early PoC, not a real trainer, not a product, no token launch, no fundraising, no unauthorized distillation. Do not rewrite architecture. Output a unified diff.
```

### AEM-002  Adapter artifact manifest schema

Goal: define a portable contract for an admitted adapter/expert artifact.

Add:

- `schemas/adapter_artifact_manifest.schema.json`
- `examples/adapter_artifact_manifest.example.json`
- structural validation test

Fields:

- `artifact_id`
- `base_model_hash`
- `adapter_hash`
- `adapter_format`
- `quantization`
- `domains`
- `license`
- `training_receipt_id`
- `eval_report_ids`
- `created_at`
- `signature`

Acceptance:

- Valid example passes structural validation.
- Missing required fields fail.
- No real model files required.

Patch prompt:

```text
Add a minimal adapter artifact manifest schema, one example, and tests. This is only a manifest contract, not a trainer. Use existing schema validation style where possible. Keep patch small.
```

### AEM-003  TrainingReceipt schema hardening

Goal: make training/adaptation work recordable without rewarding raw compute time.

Add or update schema/example for a receipt containing:

- `receipt_id`
- `expert_id`
- `base_model_hash`
- `adapter_hash`
- `training_objective`
- `data_receipt_ids`
- `eval_report_ids`
- `target_eval_delta`
- `regression_report_id`
- `policy_receipt_id`
- `created_at`
- `signature`

Acceptance:

- Receipt with no eval delta is rejected or marked ineligible.
- Receipt with missing provenance/policy is rejected or marked incomplete.
- No credit/accounting expansion.

Patch prompt:

```text
Harden or add a TrainingReceipt schema and tests. It must bind training/adaptation work to data/provenance, eval delta, regression report, and policy receipt. Do not add token or marketplace language. Keep it as evidence infrastructure.
```

### AEM-004  Mock trainer interface

Goal: prepare for real adapter training without adding ML dependencies.

Add:

- `aem_poc/training_backend.py`
- mock trainer that emits a deterministic `TrainingRunReport`
- tests

Interface idea:

```python
class TrainingBackend:
    def train(self, job):
        ...
```

Acceptance:

- No PyTorch dependency.
- Mock report includes input hashes, output adapter hash, duration, and status.
- Existing demos unaffected.

Patch prompt:

```text
Add a minimal training backend interface and mock trainer. Do not perform real ML training and do not add PyTorch. The mock should emit deterministic hashes and a TrainingRunReport with tests.
```

### AEM-005  EvalJob and EvalReport interface

Goal: make objective evaluation jobs portable.

Add:

- `aem_poc/eval_jobs.py`
- `EvalJob`
- `EvalReport`
- tests

Fields:

- eval id
- task/domain
- command or verifier name
- input artifact hash
- output/report hash
- score
- pass/fail
- stderr/stdout hashes only

Acceptance:

- No raw output stored by default.
- Report shape is serializable.
- Tests cover pass/fail report creation.

Patch prompt:

```text
Add small EvalJob and EvalReport dataclasses plus serialization tests. Store stdout/stderr hashes, not raw output. Do not integrate with real ML evals yet. Keep it narrow.
```

### AEM-006  RegressionReport gate shape

Goal: separate target improvement from general regression checks.

Add:

- `schemas/regression_report.schema.json`
- example report
- test or small validator

Fields:

- `report_id`
- `expert_id`
- `baseline_artifact_hash`
- `candidate_artifact_hash`
- `evals`
- `max_allowed_regression`
- `accepted`
- `reasons`

Acceptance:

- Example accepted report validates.
- Example rejected report validates.
- Gate logic can consume the shape later.

Patch prompt:

```text
Add a minimal RegressionReport schema, accepted and rejected examples, and structural tests. Do not change admission scoring yet unless needed for tests. Keep patch small.
```

### AEM-007  DataShardReceipt schema

Goal: record data/provenance without putting raw data in the repo.

Add:

- `schemas/data_shard_receipt.schema.json`
- example receipt
- tests

Fields:

- `receipt_id`
- `shard_hash`
- `source_type`
- `license`
- `allowed_for_training`
- `allowed_for_eval`
- `contains_personal_data`
- `redaction_policy`
- `created_at`
- `signature`

Acceptance:

- Raw dataset content is not included.
- Receipt can mark shard as disallowed for training.
- Invalid missing license/policy fails.

Patch prompt:

```text
Add a DataShardReceipt schema and examples for allowed and disallowed training use. Do not include raw data. Validate required source/license/policy fields. Keep this as provenance infrastructure.
```

### AEM-008  ContaminationReport placeholder

Goal: reserve a checkable shape for eval/data contamination evidence.

Add:

- `schemas/contamination_report.schema.json`
- example clean report
- example contaminated report
- tests

Fields:

- `report_id`
- `artifact_hash`
- `eval_set_id`
- `method`
- `matched_items_count`
- `sample_commitments`
- `accepted`
- `reasons`

Acceptance:

- Does not claim strong detection.
- Clear language: placeholder/report format only.
- No raw eval items stored.

Patch prompt:

```text
Add a minimal ContaminationReport schema and examples. Make clear this is a report format placeholder, not a complete contamination detector. Do not store raw eval items. Keep patch small.
```

### AEM-009  Duplicate expert check stub

Goal: prevent obvious duplicate adapter farming in the PoC.

Add:

- deterministic duplicate check using hashes and metadata overlap
- tests for exact duplicate and non-duplicate

Rules:

- Keep it explicitly simple.
- Do not claim semantic duplicate detection.
- Integrate only where low-risk.

Acceptance:

- Same adapter hash is rejected as duplicate.
- Different adapter hash with different metadata passes.
- Test names make limitations clear.

Patch prompt:

```text
Add a simple duplicate expert check stub based on adapter hash and basic metadata overlap. Do not claim semantic detection. Include exact-duplicate and non-duplicate tests. Keep it narrow.
```

### AEM-010  Backdoor/trigger risk report schema

Goal: make risk evidence explicit rather than buried in ad hoc fields.

Add:

- `schemas/risk_report.schema.json`
- example low-risk report
- example rejected report
- tests

Fields:

- `report_id`
- `expert_id`
- `artifact_hash`
- `risk_type`
- `score`
- `threshold`
- `accepted`
- `method`
- `evidence_commitments`
- `created_at`

Acceptance:

- No raw malicious prompts stored.
- Report supports multiple risk types later.
- Existing admission logic can still use `risk_scores`.

Patch prompt:

```text
Add a RiskReport schema for backdoor/trigger/duplicate-style risk evidence. Include safe examples and tests. Use commitments or hashes instead of raw trigger prompts. Do not expand safety claims beyond the schema.
```

### AEM-011  Local artifact registry

Goal: store and verify local artifact manifests by content hash.

Add:

- `aem_poc/artifact_registry.py`
- tests using temporary directory

Functions:

- add artifact manifest
- compute/verify hash
- list artifacts
- reject missing file or hash mismatch

Acceptance:

- Uses stdlib only.
- No model files required.
- Works with small text fixtures.

Patch prompt:

```text
Add a tiny local artifact registry using the filesystem and sha256 hashes. Test add/list/verify/hash-mismatch using temporary files. Do not add external storage or network code.
```

### AEM-012  Verifier challenge packet

Goal: define a replayable challenge request for verifier sampling.

Add:

- `schemas/verifier_challenge_packet.schema.json`
- example packet
- tests

Fields:

- `challenge_id`
- `target_receipt_id`
- `artifact_hash`
- `verifier_type`
- `challenge_method`
- `input_commitments`
- `expected_report_schema`
- `deadline_seconds`
- `created_at`

Acceptance:

- No raw private input required.
- Packet can target training, inference, or eval receipt later.
- Schema only; no network protocol.

Patch prompt:

```text
Add a verifier challenge packet schema and example. This is a local/replayable challenge shape, not a public network. Do not add networking or economy logic. Keep patch small.
```

### AEM-013  AEM-to-GOWN serving bridge draft

Goal: convert an admitted `ExpertCard` into a GOWN-style serving card draft.

Add:

- `aem_poc/gown_bridge.py`
- tests

Mapping:

- `expert_id` -> `model_id` or `expert_model_id`
- `base_model_hash` + expert hash -> `weight_hash` or artifact hash
- `domains` -> capabilities
- `quantization` -> quantization
- `vram_min_gb` -> vram requirement
- `license` -> license

Acceptance:

- Pure function.
- No import dependency on GOWN repo unless optional and justified.
- Tests verify stable mapping.

Patch prompt:

```text
Add a pure-function bridge that maps an AEM ExpertCard-like dict to a GOWN-style ModelCard-like dict. Do not add cross-repo dependency. Include tests. This is just a serving-card draft.
```

### AEM-014  Sandbox policy schema

Goal: make verifier/training command boundaries explicit.

Add:

- `schemas/sandbox_policy.schema.json`
- examples for verifier and trainer policy
- tests

Fields:

- `policy_id`
- `allowed_commands`
- `allowed_paths`
- `blocked_prefixes`
- `network_access`
- `timeout_seconds`
- `max_output_bytes`
- `created_at`

Acceptance:

- Default example denies network access.
- Blocked prefix example exists.
- No actual container runtime required.

Patch prompt:

```text
Add a SandboxPolicy schema and examples for verifier/trainer command limits. Do not implement Docker or containers. Include tests for blocked prefixes and default no-network policy if existing validators support it.
```

### AEM-015  Evidence bundle index for new artifacts

Goal: when new schemas/examples are added, they should appear in the evidence artifact index.

Change:

- update or add index entries for any new schema/example/report artifacts
- keep evidence docs consistent

Acceptance:

- Relevant evidence/index check passes.
- New artifact has producer, schema, verifier, purpose, role.
- No self-referential evidence loop.

Patch prompt:

```text
Update the evidence artifact index for newly added schemas/examples/reports. Follow existing artifact index style. Run the narrow evidence/index checks. Do not change unrelated artifacts.
```

### AEM-016  Public issue templates for small bricks

Goal: make external contributions small and safe.

Add:

- `.github/ISSUE_TEMPLATE/small_brick.md`
- `.github/pull_request_template.md`
- optional `CONTRIBUTING.md`

Must include:

- one task per PR
- tests required
- no raw prompt/output/private data logs
- no token/fundraising/broad capability claims
- no broad rewrites
- disclose AI-assisted patches if used

Acceptance:

- A contributor can submit a small patch without reading the full architecture.
- No code changes required.

Patch prompt:

```text
Add public contribution hygiene files for small technical tasks. Keep it neutral and OSS-friendly. Include no-token/no-fundraising/no-broad capability/no-raw-data-log rules. Do not add project mythology or broad vision text.
```

## 6. Tasks to avoid publicly for now

Do not hand these to random contributors as first tasks:

- credit resale or market design
- slashing/fraud economics
- governance voting
- public token mechanics
- public distributed training claims
- large-scale data acquisition
- competitor model distillation
- privacy-preserving cryptographic inference claims
- full rewrite into another framework

These areas may exist as research notes, but they are not first-contact OSS tasks.

## 7. Standard patch prompt wrapper

Use this wrapper around any task card:

```text
You are helping with a small open-source Python PoC for expert/adaptation admission and evidence checks.

Do not expand the project vision.
Do not add token/economy/hype language.
Do not add fundraising language.
Do not claim this trains a large production model today.
Do not add unauthorized scraping or distillation language.
Do not rewrite the architecture.
Do not add unnecessary dependencies.
Make the smallest useful patch.

Repo:
https://github.com/sherlockholmesyes/frontier-pretraining-network-aem

Task:
<PASTE ONE TASK CARD HERE>

Constraints:
- Python >=3.10
- stdlib-first unless task explicitly allows more
- unittest tests
- keep existing demos/checks working
- do not log raw prompts, raw outputs, or private data
- use hashes/commitments for sensitive artifacts

Output:
1. brief summary
2. files changed
3. test command
4. unified diff
5. risks or assumptions
```

## 8. Contributor response template

Ask contributors to respond with:

```text
Task ID:
Summary:
Files changed:
Test command:
Test result:
Sensitive-data logging check:
Diff or PR link:
Risks/assumptions:
```

## 9. Review checklist

Before accepting a patch, verify:

- [ ] Patch stays inside task scope.
- [ ] Tests added or updated.
- [ ] Existing demo/check still runs or narrow test command is justified.
- [ ] No raw prompt/output/private dataset logs.
- [ ] No token/economy/fundraising language.
- [ ] No hype/revolution claims.
- [ ] No unauthorized scraping or distillation language.
- [ ] No new dependency without clear reason.
- [ ] Schema examples are valid JSON.
- [ ] Evidence/index updates are included when relevant.
- [ ] Error paths are tested.

## 10. Suggested GitHub labels

- `small-brick`
- `good-first-patch`
- `schema`
- `evidence`
- `verifier`
- `adapter-manifest`
- `training-receipt`
- `provenance`
- `sandbox`
- `bridge`
- `tests-needed`
- `do-not-broaden-scope`

## 11. Suggested Reddit reply for task distribution

```text
Task for you: AEM-002  adapter artifact manifest schema.

Scope:
- add a small JSON schema
- add one example manifest
- add structural validation test
- fields: artifact id, base model hash, adapter hash, adapter format, domains, license, training receipt id, eval report ids, signature
- no real trainer, no ML dependency, no economy/token language

Output a small diff, test command, and assumptions. No architecture rewrite.
```
