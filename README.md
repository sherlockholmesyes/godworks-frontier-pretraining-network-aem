# Godworks Frontier Pretraining Network — AEM PoC

[![AEM CI](https://github.com/sherlockholmesyes/godworks-frontier-pretraining-network-aem/actions/workflows/ci.yml/badge.svg)](https://github.com/sherlockholmesyes/godworks-frontier-pretraining-network-aem/actions/workflows/ci.yml)

**AEM = Accretive Expert Mesh**

This repository is a proof-of-concept scaffold for a different route to open frontier pretraining:

```text
frontier_model(t) = core(t) + router(t) + expert_set(t) + verifier_set(t) + data_ledger(t) + distillation_memory(t)
```

The goal is not to imitate a corporate synchronous dense-model datacenter. The goal is to grow a frontier-capability network by adding, testing, routing, rewarding, pruning, and distilling many small quantized experts that can be trained or served by people with consumer GPUs.

## design root cut

### Rejected option A

```text
Frontier pretraining = one huge dense checkpoint trained synchronously in one datacenter.
```

Dead: this preserves the corporate form — one owner, one run, one checkpoint, one training fabric.

### Rejected option B

```text
Distributed MoE = split layers across random home GPUs and send token hidden states over the internet.
```

Dead: this turns the network into a latency-bound distributed tensor circus.

### Third

```text
MoE becomes a protocol for capability growth.
```

An expert is not merely a remote layer. An expert is a **capability capsule** that can be trained locally, admitted through objective gates, routed to narrowly useful tasks, rewarded with traffic, pruned when it regresses, and distilled into later generations.

## Strategic growth cut

### Rejected option A

```text
AEM catches up by distilling frontier competitors.
```

Dead: unauthorized competitor distillation is a legal/policy trap and keeps the network in a follower posture.

### Rejected option B

```text
AEM accepts arbitrary uploads and pays credits for raw content.
```

Dead: raw uploads can be unlicensed, duplicated, poisoned, low quality, or impossible to evaluate.

### Third

```text
AEM grows through credit-eligible contribution receipts:
licensed/human-owned knowledge, skills, data shards, evals, curricula, and operators earn credits only after provenance, anti-distillation, and measurable-delta gates.
```

The network should be built so others try to distill **AEM's verified receipts and experts**, not so AEM depends on unauthorized extraction from others.

## PoC status

This repo is not yet a real trainer. It is a runnable architecture seed that demonstrates the minimum control loop:

```text
TaskPacket → ExpertRegistry → Router → Objective Verifier → Objective Gate → RouteTrace
```

The first target domain is code-patch experts because unit tests can act as an objective verifier.

## Quick start

The PoC is stdlib-compatible by default:

```bash
python -m aem_poc.demo
python -m aem_poc.patch_gate_demo
make evidence-local-ci
make aem-network-economy-check
```

`make evidence-local-ci` is the canonical local command and evidence gate. `make aem-network-economy-check` is the canonical local network/economy gate.

## AEM network and economy foundation

Network participation is represented by protocol objects, not vibes:

```bash
make aem-network-bricks
make aem-network-cards
make aem-bootstrap-growth
make aem-inference-receipts
make aem-credit-ledger
make aem-network-economy-check
```

`aem-network-economy-check` runs:

```text
aem-network-bricks-check
aem-network-cards-check
aem-bootstrap-growth-check
aem-inference-receipts-check
aem-credit-ledger-check
```

Network cards:

```text
NodeCard:
  host identity, locality bucket, capacity envelope, economic policy, host policy, earning roles, credit account, receipt requirements

HostAdvertisement:
  concrete expert offer by a node, AEM_CREDIT price, accepted roles, availability, task policy, required work receipts
```

Bootstrap growth receipts:

```text
KnowledgeContributionReceipt:
  contributor id
  contributor node id
  contribution type
  content commitment
  source policy
  training use
  credit policy
  evaluation gate
  anti-distillation policy
  receipt requirements
```

Inference work receipts:

```text
InferenceWorkReceipt:
  task hash
  expert id
  node id
  host advertisement id
  credit account
  AEM_CREDIT charge
  prompt/output commitments
  route trace id
  duplicate-spend key
  challenge surface
  policy receipt requirements
```

Credit settlement:

```text
CreditLedger:
  consumes contribution receipts and inference receipts
  mints AEM_CREDIT for accepted contribution deltas
  debits payer credits for inference work
  credits host account for inference work
  rejects duplicate spend keys and open challenge windows
  emits replayable settlement events and account balances
```

Contribution types:

```text
knowledge
skill
data_shard
eval
curriculum
operator
```

Credit basis is not raw upload size. Credit basis must be one of:

```text
accepted_delta
verified_skill_use
eval_improvement
curation_quality
operator_adoption
```

Economy rules already encoded in schemas/tests:

```text
training and inference both produce receipts
knowledge/skills/data/evals/curricula/operators can earn credits
credits settle as AEM_CREDIT
credits may be spent on inference/training/verification or resold when policy allows
no earning role without required receipt
no inference credit without InferenceWorkReceipt
no balance change without CreditLedger settlement event
no credit minting from raw self-report
no duplicate spend key reuse
no unauthorized competitor distillation
third-party model outputs require verified terms
```

Commands:

```bash
python -m aem_poc.aem_network_bricks
python -m aem_poc.aem_network_cards
python -m aem_poc.aem_bootstrap_growth
python -m aem_poc.aem_inference_receipts
python -m aem_poc.aem_credit_ledger
make aem-network-bricks-check
make aem-network-cards-check
make aem-bootstrap-growth-check
make aem-inference-receipts-check
make aem-credit-ledger-check
make aem-network-economy-check
```

Docs:

```text
docs/AEM_NETWORK_BRICKS_DESIGN.md
docs/AEM_NODECARD_HOSTADVERTISEMENT_DESIGN.md
docs/AEM_BOOTSTRAP_GROWTH_DESIGN.md
docs/AEM_INFERENCE_WORK_RECEIPT_DESIGN.md
docs/AEM_CREDIT_LEDGER_SETTLEMENT_DESIGN.md
docs/AEM_NETWORK_ECONOMY_CHECK_DESIGN.md
```

Contributor process:

```text
CONTRIBUTOR_RIGOR.md
```

## Canonical local verification

Run:

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

GitHub Actions delegates to this same local gate:

```text
run: make evidence-local-ci
```

Then CI uploads the generated artifact bundle.

## Evidence status

Print the generated status summary:

```bash
python -m aem_poc.evidence_status
make evidence-status
```

Checked-in generated example:

```text
docs/evidence_status.example.json
schemas/evidence_status.schema.json
```

The generated status includes seal stage counts and the docs gate status line:

```text
Docs gate status line
docs_check_command
docs_check_gates
docs_sync_command
docs_sync_gates
```

Docs-only drift gate:

```bash
make evidence-docs-check
make evidence-docs-sync
```

`evidence-docs-check` includes the status example check but stays out of `evidence-local-ci`, so the local CI status does not become self-referential.

## Evidence seal model

The evidence flow has two seal stages:

```text
1. First-stage trace seal
   runs/patch_gate_demo/evidence_seal_manifest.json
   seals generated trace/evidence artifacts.

2. Second-stage upload receipt seal
   runs/upload/evidence_second_stage_seal_manifest.json
   seals metadata and post-seal receipts.

Terminal receipt
   runs/upload/evidence_second_stage_verify_report.json
   verifies the second-stage seal and is not sealed again unless a third-stage policy is added.
```

## Evidence artifact index

For a reviewer-oriented map of evidence files, producer, schema, verifier, seal stage, role, and purpose, use:

```text
docs/EVIDENCE_ARTIFACT_INDEX.md
```

For tool consumption, use the schema-gated machine-readable index:

```text
docs/evidence_artifact_index.json
schemas/evidence_artifact_index.schema.json
```

CLI access:

```bash
python -m aem_poc.evidence_artifact_index validate
python -m aem_poc.evidence_artifact_index list
python -m aem_poc.evidence_artifact_index show trace_report.json
python -m aem_poc.evidence_artifact_index sync
python -m aem_poc.evidence_artifact_index md-check
python -m aem_poc.evidence_artifact_index md-sync
make evidence-artifact-index
make evidence-artifact-index-sync
make evidence-artifact-index-md-check
make evidence-artifact-index-md-sync
```

## Downloaded CI artifact verification

When reviewing a downloaded GitHub Actions artifact bundle, use:

```text
docs/EVIDENCE_DOWNLOAD_VERIFY.md
```

Verify the first-stage trace seal:

```bash
python -m aem_poc.evidence_seal_verify \
  <download-dir>/runs/patch_gate_demo/evidence_seal_manifest.json
```

Verify the second-stage upload receipt seal:

```bash
python -m aem_poc.evidence_second_stage_seal_verify \
  <download-dir>/runs/upload/evidence_second_stage_seal_manifest.json
```

A downloaded evidence bundle is reviewable only if both local verification commands exit `0`, both reports say `ok=true` and `failure_count=0`, and the terminal receipt exists:

```text
runs/upload/evidence_second_stage_verify_report.json
```

## Current executable gates

```text
1. ExpertCard / TaskPacket / TeacherPolicyCard validation
2. Objective admission gate
3. Repo-shaped patch gate
4. Patch policy gate
5. Workspace prep + selected command runner
6. RouteTrace schema validation on append
7. RouteTrace validated replay
8. Canonical trace rewrite
9. Trace rewrite manifest validation
10. Trace report schema validation
11. Evidence summary schema validation
12. Evidence bundle manifest schema validation
13. Evidence bundle hash verification
14. Evidence verify report schema validation
15. Evidence pipeline orchestrator
16. Evidence pipeline result schema validation
17. First-stage evidence seal manifest
18. First-stage evidence seal verification
19. Evidence metadata check/report
20. Evidence upload policy check
21. Evidence upload path drift guard
22. Evidence upload path sync command
23. Generated workflow upload block marker
24. Generated evidence status summary and checked-in example
25. Docs-only evidence check/sync target group
26. Downloaded CI artifact verification guide
27. Evidence artifact index JSON/Markdown checks
28. Second-stage upload receipt seal manifest
29. Second-stage upload receipt seal verification
30. Terminal second-stage verification receipt
31. Aggregate local CI target
32. AEM network brick ledger
33. NodeCard + HostAdvertisement network economy cards
34. Bootstrap growth contribution receipts
35. InferenceWorkReceipt duplicate-spend/challenge-surface receipt
36. CreditLedger settlement simulator
37. Aggregate AEM network/economy check target
```

## Core architecture

```text
CORE:
  tokenizer / base model / common task protocol / router interface

EXPERT_CAPSULE:
  manifest + quantized weights/adapter + eval claims + runtime endpoint

ROUTER:
  task-level selection, not per-token remote hidden-state routing

VERIFIER_MESH:
  independent objective gates for target improvement, regression, duplicate risk, trigger risk, latency/cost, and node fit

DATA_LEDGER:
  provenance, shard hashes, contamination checks, eval impact

DISTILLATION_LOOP:
  successful traces → distillation memory → next router/core/expert generation

BOOTSTRAP_GROWTH_LOOP:
  human-owned/licensed knowledge + skills + data + evals + curricula + operators
  → contribution receipts
  → provenance / anti-distillation / delta gates
  → credits
  → expert/router/eval improvement

NETWORK_ECONOMY_LOOP:
  NodeCard + HostAdvertisement
  → InferenceWorkReceipt / TrainingReceipt / ContributionReceipt
  → duplicate-spend guard + challenge surface + policy gates
  → CreditLedger settlement events
  → AEM_CREDIT balances
  → inference/training/verification demand
```

## objective gates for expert admission

An expert is admitted only if it satisfies the current gates:

```text
1. improves the target eval
2. does not regress general evals beyond the threshold
3. is not a near-duplicate of an existing expert
4. does not show obvious trigger risk
5. fits the target node VRAM budget
6. provides a usable manifest and signature
7. passes objective verifier reports
8. writes replayable RouteTrace evidence
```

## Consumer GPU role

```text
12GB node:
  7B/8B quantized inference, QLoRA-style small expert training, verifier jobs, code test runner, data cleaning

16GB node:
  larger context, larger adapters, 14B quantized inference/training with constraints

24GB+ node:
  heavy expert training, multi-expert serving, distillation jobs
```

The network treats small nodes as organs, not as failed H100s.

## Death of this PoC

```text
"A good architecture repo is a manifesto."
```

Dead. This PoC must stay runnable: every new AEM gate should either have tests or an executable command.

## Inheritance

```text
expert = capability capsule, not just a LoRA file or a remote layer
model growth = admission-controlled expert accretion + routing + verification + distillation
network growth = bootstrap contributions + receipts + credits + verified capability deltas
inference economy = signed work receipts + duplicate-spend guard + challenge surface
credit economy = receipt settlement events + replayable AEM_CREDIT balances
```

## Next pressure

```text
update network brick ledger status for credit_ledger_settlement from research_packet to proto_brick.
```
