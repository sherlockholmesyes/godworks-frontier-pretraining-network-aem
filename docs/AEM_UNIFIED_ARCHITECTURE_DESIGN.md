# AEM Unified Architecture design

This file is the single current architecture map for AEM/AEM as of this repo state.

It unifies:

```text
models
training
human knowledge/skill contribution
inference
routing
economy
receipts
credit settlement
evidence gates
missing primitives
```

It is intentionally written in design form: each major layer names two dead reductions and the Third that becomes the actual protocol shape.

## Root cut

### wrong1

```text
AEM = catch up by distilling stronger closed/open frontier models.
```

Death:

```text
That keeps AEM in follower posture, creates policy/legal risk, and makes the network dependent on other people's budget and terms.
```

### wrong2

```text
AEM = upload anything from humans and pay credits for raw content or raw compute.
```

Death:

```text
That rewards spam, poisoned data, unlicensed content, fake expertise, GPU-hour burning, and self-reported work.
```

### Third

```text
AEM = bootstrap growth network:
human-owned/licensed knowledge + skills + data + evals + curricula + operators
→ contribution receipts
→ provenance / anti-distillation / measurable-delta gates
→ admitted experts / router memory / eval hardening
→ inference + training + verification receipts
→ CreditLedger settlement
→ AEM_CREDIT balances
→ more inference/training/verification demand.
```

The strategic target is not to distill competitors. The target is to become the network whose verified experts, skills, receipts, and deltas others try to chase.

## One-line system

```text
AEM(t) = Core(t)
       + Router(t)
       + ExpertCapsules(t)
       + NodeCards(t)
       + HostAdvertisements(t)
       + ContributionReceipts(t)
       + TrainingReceipts(t)
       + InferenceWorkReceipts(t)
       + VerifierReports(t)
       + CreditLedger(t)
       + EvidenceSeals(t)
```

## Layer 0 — Signal guard / anti-collapse

### wrong1

```text
New architecture = rename existing MoE / RAG / blockchain / marketplace pieces.
```

Death:

```text
This is novelty collapse. Old bricks steal the vector and produce a familiar system with new labels.
```

### wrong2

```text
New architecture = pure vision without schemas, tests, receipts, or kill criteria.
```

Death:

```text
That becomes manifesto, not executable protocol.
```

### Third

```text
Every new claim must become a brick:
operator + interface + node decomposition + primitive closure + minimal test + kill criteria.
```

Current embodiment:

```text
docs/AEM_NETWORK_BRICKS_DESIGN.md
schemas/aem_network_brick_ledger.schema.json
aem_poc/aem_network_bricks.py
tests/test_aem_network_bricks.py
```

## Layer 1 — Model architecture

### wrong1

```text
Model = one huge dense checkpoint trained in a datacenter.
```

Death:

```text
This preserves the corporate form: one owner, one training run, one model, one infrastructure fabric.
```

### wrong2

```text
Model = remote per-token MoE layers scattered over consumer GPUs.
```

Death:

```text
This becomes latency-bound distributed tensor traffic, not a useful global model.
```

### Third

```text
Model = accretive expert mesh.
```

AEM model state is not only weights. It is:

```text
Core:
  tokenizer, base model, common task protocol, router interface

ExpertCapsule:
  ExpertCard + quantized weights/adapters + eval claims + runtime constraints + policy + signature

Router:
  task-level expert/host selection, not remote hidden-state token routing

VerifierMesh:
  objective gates for capability delta, regression, duplicate risk, trigger risk, latency/cost, node fit

DistillationMemory:
  successful traces and admitted deltas used to train future routers/core/experts
```

Current embodiment:

```text
schemas/expert_card.schema.json
schemas/task_packet.schema.json
schemas/route_trace.schema.json
aem_poc/demo.py
aem_poc/patch_gate_demo.py
aem_poc/trace_store.py
aem_poc/e2e_gate_demo.py
```

## Layer 2 — Expert admission

### wrong1

```text
Expert = a model file somebody claims is useful.
```

Death:

```text
A file without eval deltas, license, domain claims, runtime bounds, and receipts cannot be routed or rewarded safely.
```

### wrong2

```text
Expert = a staked identity or wallet with reputation.
```

Death:

```text
Stake/reputation does not prove capability, node fit, policy compliance, or usefulness.
```

### Third

```text
Expert = capability capsule.
```

A capability capsule must have:

```text
expert_id
base_model_hash
expert_type
quantization
vram_min_gb
training_objective
domains
eval_delta
license
signature
objective verifier reports
route trace evidence
```

Current gate logic:

```text
fake expert rejected
real patch expert accepted
route trace written
trace replayable
artifacts sealed
```

Current embodiment:

```text
aem_poc/e2e_gate_demo.py
aem_poc/patch_gate_demo.py
aem_poc/evidence_pipeline.py
```

## Layer 3 — Human knowledge / skill / data contribution

### wrong1

```text
Users upload data/skills/knowledge and automatically earn credits.
```

Death:

```text
This rewards spam, copyright risk, poison, duplicates, unverifiable expertise, and raw volume instead of capability gain.
```

### wrong2

```text
Only model training compute earns credits; human knowledge stays outside protocol economics.
```

Death:

```text
That excludes the strongest bootstrap source: human-owned knowledge, skills, evals, curricula, and operators.
```

### Third

```text
Human contribution = KnowledgeContributionReceipt with provenance, training-use, credit-policy, anti-distillation, evaluation, and required receipts.
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

Credit basis:

```text
accepted_delta
verified_skill_use
eval_improvement
curation_quality
operator_adoption
```

Forbidden:

```text
raw upload size as credit basis
credit without provenance receipt
skill claim without execution receipt
unauthorized competitor distillation
terms-violating teacher extraction
```

Current embodiment:

```text
schemas/aem_knowledge_contribution.schema.json
aem_poc/aem_bootstrap_growth.py
tests/test_aem_bootstrap_growth.py
docs/AEM_BOOTSTRAP_GROWTH_DESIGN.md
```

Command:

```bash
make aem-bootstrap-growth-check
```

## Layer 4 — Training architecture

### wrong1

```text
Training reward = GPU hours burned.
```

Death:

```text
GPU hours can be useless, duplicated, poisoned, or adversarial.
```

### wrong2

```text
Training reward = leaderboard score only.
```

Death:

```text
Leaderboard-only rewards overfit, ignore provenance, and erase contribution granularity.
```

### Third

```text
Training reward = verified training/contribution receipts with measurable delta and policy gates.
```

Training pipeline shape:

```text
ContributionReceipt / TrainingReceipt
→ source policy check
→ allowed teacher/contribution policy
→ eval delta
→ anti-overfit challenge
→ verifier reports
→ credit eligibility
→ admitted expert/router/eval update
```

Currently closed/proto pieces:

```text
TeacherPolicyCard
TrainingReceipt concept in network brick ledger
ContributionReceipt schema
Evidence pipeline and verifier reports
```

Missing primitives:

```text
anti_overfit_challenge
training receipt credit settlement beyond demo contribution mint
quality multiplier from real eval delta
```

## Layer 5 — Node and host architecture

### wrong1

```text
Node = wallet address.
```

Death:

```text
A wallet cannot expose GPU capacity, locality bucket, uptime window, sandbox policy, earning roles, credit account, or receipt requirements.
```

### wrong2

```text
Host offer = URL saying an expert is online.
```

Death:

```text
A URL does not bind expert id, node capacity, credit price, payment class, task policy, or challengeable receipt requirements.
```

### Third

```text
NodeCard + HostAdvertisement.
```

NodeCard binds:

```text
node_id
owner_key
locality bucket
capacity envelope
economic_policy
host_policy
available_roles
advertised_experts
receipts_required
```

HostAdvertisement binds:

```text
advertisement_id
node_id
expert_id
expert_card_hash
locality_bucket
offer roles
accepted payment = AEM_CREDIT
credit rates
availability
policy
receipt_requirements
signature
```

Current embodiment:

```text
schemas/node_card.schema.json
schemas/host_advertisement.schema.json
aem_poc/aem_network_cards.py
tests/test_aem_network_cards.py
docs/AEM_NODECARD_HOSTADVERTISEMENT_DESIGN.md
```

Command:

```bash
make aem-network-cards-check
```

## Layer 6 — Inference architecture

### wrong1

```text
Inference credit = host says it answered.
```

Death:

```text
Self-report mints fake credits.
```

### wrong2

```text
Inference credit = chain re-executes model inference.
```

Death:

```text
On-chain model execution is too expensive, too slow, and leaks execution details.
```

### Third

```text
Off-chain inference emits signed InferenceWorkReceipt.
```

InferenceWorkReceipt binds:

```text
receipt_id
task_hash
task_class
expert_id
expert_card_hash
node_id
host_advertisement_id
credit_account
settlement_currency = AEM_CREDIT
credit_charge_micros
input/output token meter
prompt_commitment
output_commitment
route_trace_id
nonce
duplicate_spend.spend_key
challenge_surface
policy.receipt_requirements
signature
```

Duplicate-spend primitive:

```text
spend_key = task_hash | expert_id | node_id | nonce
```

Challenge surface:

```text
output_commitment_open
route_trace_replay
metered_cost_audit
expert_hash_check
```

Current embodiment:

```text
schemas/inference_work_receipt.schema.json
aem_poc/aem_inference_receipts.py
tests/test_aem_inference_receipts.py
docs/AEM_INFERENCE_WORK_RECEIPT_DESIGN.md
```

Command:

```bash
make aem-inference-receipts-check
```

## Layer 7 — Routing architecture

### wrong1

```text
Route to nearest host.
```

Death:

```text
Nearest host may be weak, stale, policy-incompatible, unavailable, or too expensive.
```

### wrong2

```text
Route to globally strongest expert.
```

Death:

```text
Global best ignores latency, cost, availability, privacy class, and local credit economics.
```

### Third

```text
Router ranks host-expert pairs by capability fit, locality, receipt quality, price, policy, and freshness.
```

Current pieces:

```text
TaskPacket
ExpertCard
NodeCard
HostAdvertisement
RouteTrace
InferenceWorkReceipt
```

Missing primitives:

```text
availability_challenge_receipt
credit_price_score
locality_quality_score
reputation_decay
fallback route market
```

## Layer 8 — Economy architecture

### wrong1

```text
Economy = centralized balance table.
```

Death:

```text
Central balances recreate a platform operator and do not prove why balances changed.
```

### wrong2

```text
Economy = every inference/payment is on-chain execution.
```

Death:

```text
Per-inference chain execution is too expensive and too slow.
```

### Third

```text
CreditLedger consumes signed contribution and inference receipts, applies policy/challenge/duplicate-spend gates, then emits deterministic AEM_CREDIT settlement events.
```

Settlement events:

```text
contribution_mint
inference_debit
inference_host_credit
```

Supply rule:

```text
contribution_mint increases net supply
inference_debit + inference_host_credit transfer existing credits with zero net supply delta
```

Current embodiment:

```text
schemas/credit_ledger_settlement.schema.json
aem_poc/aem_credit_ledger.py
tests/test_aem_credit_ledger.py
docs/AEM_CREDIT_LEDGER_SETTLEMENT_DESIGN.md
```

Command:

```bash
make aem-credit-ledger-check
```

Aggregate economy gate:

```bash
make aem-network-economy-check
```

Runs:

```text
aem-network-bricks-check
aem-network-cards-check
aem-bootstrap-growth-check
aem-inference-receipts-check
aem-credit-ledger-check
```

## Layer 9 — Evidence and artifact integrity

### wrong1

```text
If code runs, evidence is enough.
```

Death:

```text
Without durable receipts, hashes, seals, and replayable traces, reviewers cannot verify what happened.
```

### wrong2

```text
One summary artifact is enough.
```

Death:

```text
Summary is not a replayable evidence chain and can hide missing or mutated artifacts.
```

### Third

```text
Two-stage evidence seal plus terminal verification receipt.
```

Current evidence flow:

```text
route_trace.jsonl
→ compact trace
→ trace report
→ evidence summary
→ bundle manifest
→ verify report
→ first-stage seal
→ first-stage seal verify report
→ second-stage upload receipt seal
→ second-stage verify report
```

Current commands:

```bash
make evidence-local-ci
make evidence-docs-check
make evidence-status
```

## Full current command surface

Evidence:

```bash
make evidence-local-ci
make evidence-docs-check
make evidence-docs-sync
```

Network/economy:

```bash
make aem-network-bricks-check
make aem-network-cards-check
make aem-bootstrap-growth-check
make aem-inference-receipts-check
make aem-credit-ledger-check
make aem-network-economy-check
```

Individual demos:

```bash
python -m aem_poc.aem_network_bricks
python -m aem_poc.aem_network_cards
python -m aem_poc.aem_bootstrap_growth
python -m aem_poc.aem_inference_receipts
python -m aem_poc.aem_credit_ledger
```

## Current closed/proto/research map

Closed / executable now:

```text
ExpertCard schema
TaskPacket schema
RouteTrace schema
patch gate demo
evidence pipeline
NodeCard schema
HostAdvertisement schema
KnowledgeContributionReceipt schema
InferenceWorkReceipt schema
CreditLedger settlement simulator
network/economy aggregate check
```

Proto-bricks:

```text
node_identity_capacity
expert_host_registry
locality_quality_router
training_work_receipt
privacy_sandbox_policy
credit_ledger_settlement
bootstrap growth contribution receipts
inference receipt challenge surface
```

Research packets / missing primitives:

```text
availability_challenge_receipt
runtime_cost_meter hardening
inference_challenge_protocol hardening
anti_overfit_challenge
settlement_finality_rule
scarcity_multiplier
anti_monopoly_cap
challenge_sampling
slashing_receipt
collusion_detector
market_order
regulatory_boundary
private_inference_primitive
proposal_schema
migration_receipt
bounded_vote
```

## Economic non-negotiables

```text
No AEM_CREDIT without receipt.
No receipt without policy/provenance binding.
No contribution credit for unauthorized competitor distillation.
No inference credit without InferenceWorkReceipt.
No inference settlement before challenge window closes.
No duplicate spend key reuse.
No host offer outside NodeCard policy/capacity/economic floor.
No raw upload size as credit basis.
No model size alone as reward basis.
```

## Architecture as loops

```text
BOOTSTRAP_GROWTH_LOOP:
  human-owned/licensed knowledge + skills + data + evals + curricula + operators
  → contribution receipts
  → provenance / anti-distillation / delta gates
  → AEM_CREDIT
  → expert/router/eval improvement

INFERENCE_LOOP:
  user task
  → router selects ExpertCard + NodeCard + HostAdvertisement
  → host performs inference off-chain
  → InferenceWorkReceipt
  → challenge surface / duplicate-spend guard
  → CreditLedger settlement

TRAINING_LOOP:
  contribution/training packet
  → provenance and policy gates
  → eval delta / anti-overfit challenge
  → admitted expert or router/eval update
  → TrainingReceipt / ContributionReceipt
  → CreditLedger settlement

ECONOMY_LOOP:
  receipts
  → verifier/policy gates
  → settlement events
  → AEM_CREDIT balances
  → spend/resale/inference/training demand
```

## Next pressure

```text
Update network brick ledger status for credit_ledger_settlement from research_packet to proto_brick,
then add settlement_finality_rule and slashing_receipt primitives.
```
