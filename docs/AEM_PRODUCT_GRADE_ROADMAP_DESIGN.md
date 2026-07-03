# AEM Product-Grade Roadmap design

This roadmap turns the current AEM/AEM prototype into a product-grade network for:

```text
models
expert growth
training
inference
routing
verification
economy
settlement
node participation
operator/product readiness
```

It is not a generic project plan. It is a design roadmap: every phase kills two tempting wrong architectures and defines the Third that must become executable.

## Root design

### wrong1

```text
Product-grade AEM = one open model checkpoint plus a marketplace around it.
```

Death:

```text
A checkpoint does not create continuous growth, contributor rewards, routing, verifier gates, or decentralized inference/training economics.
```

### wrong2

```text
Product-grade AEM = distributed volunteers running random experts and getting credits.
```

Death:

```text
Without admission, verifier reports, receipts, routing policy, credit settlement, and abuse resistance, it becomes a spam network and fake-work economy.
```

### Third

```text
Product-grade AEM = admission-controlled expert-growth network:
Core + Router + ExpertCapsules + NodeCards + HostAdvertisements + Training/Inference/ContributionReceipts + VerifierMesh + CreditLedger + EvidenceSeals.
```

Product grade means:

```text
no expert without verifier report
no training credit without measurable delta
no inference credit without InferenceWorkReceipt
no credit movement without CreditLedger settlement event
no routing without NodeCard + HostAdvertisement + policy fit
no release without replayable evidence and operational SLOs
```

## Product-grade definition

AEM is product grade only when all of these are true:

```text
1. A user can submit inference tasks through a stable gateway.
2. Router selects experts/hosts using capability, price, locality, policy, and receipt quality.
3. Hosts can earn AEM_CREDIT from valid InferenceWorkReceipts.
4. Contributors can earn AEM_CREDIT from accepted knowledge/skill/data/eval/curriculum/operator receipts.
5. New experts can be trained, packaged, verified, admitted, routed, rewarded, and retired.
6. Credits settle through replayable CreditLedger events.
7. Fraud paths are caught by duplicate-spend, challenge, slashing, and reputation gates.
8. Private tasks are not routed to untrusted nodes by default.
9. Evidence artifacts are reproducible and sealed.
10. The system survives node churn, malicious submissions, broken experts, and bad economic incentives.
```

## Maturity levels

```text
P0 — Architecture Ledger
  schemas, docs, fake/demo receipts, no real network

P1 — Local Closed Loop
  one machine runs expert admission, routing, verification, receipts, settlement

P2 — LAN Multi-Node Alpha
  several trusted nodes, real network messages, signed receipts, local registry

P3 — Public Testnet
  untrusted nodes, challenge windows, duplicate-spend guard, simple credits, public tasks only

P4 — Economic Beta
  credit balances, transfer/spend flows, reputation, slashing, privacy policy, stable gateway

P5 — Product Grade
  stable APIs, real users, real contributor rewards, monitoring, abuse handling, upgrade governance, reproducible releases
```

---

# Phase 0 — Architecture to executable spec

## wrong1

```text
Roadmap = more docs.
```

Death:

```text
Docs without schemas/tests keep the system as manifesto.
```

## wrong2

```text
Roadmap = jump directly into distributed training.
```

Death:

```text
Distributed training before local receipts, admission, and settlement creates unverifiable compute theater.
```

## Third

```text
Every architecture claim gets a schema, module, test, command, and kill gate.
```

### Build

```text
schemas/aem_model_state.schema.json
schemas/expert_artifact.schema.json
schemas/training_receipt.schema.json
schemas/verifier_report.schema.json
schemas/data_shard.schema.json
schemas/router_decision.schema.json
schemas/credit_transfer.schema.json
schemas/slashing_receipt.schema.json
```

```text
aem_poc/aem_model_state.py
aem_poc/aem_training_receipts.py
aem_poc/aem_data_shards.py
aem_poc/aem_router_policy.py
aem_poc/aem_verifier_reports.py
aem_poc/aem_credit_transfers.py
```

### Current basis already present

```text
ExpertCard
TaskPacket
RouteTrace
NodeCard
HostAdvertisement
KnowledgeContributionReceipt
InferenceWorkReceipt
CreditLedger settlement
AEM unified architecture
AEM network brick ledger
```

### Kill gate

```text
If a concept cannot be represented as schema + test + command, it is not product architecture yet.
```

### Exit criteria

```text
make aem-network-economy-check passes
make evidence-local-ci passes
all new schemas have stdlib fallback tests
all core docs point to the unified architecture file
```

---

# Phase 1 — AEM model state and Expert Capsule v1

## wrong1

```text
AEM model = one base model checkpoint.
```

Death:

```text
A single checkpoint does not encode mesh growth, expert admission, router state, verifier reports, or distillation memory.
```

## wrong2

```text
AEM model = loose folder of experts.
```

Death:

```text
Loose experts cannot be selected, versioned, verified, rewarded, or retired reliably.
```

## Third

```text
AEM model = versioned state: CoreSpec + ExpertSet + RouterPolicy + VerifierSet + DistillationMemory + EconomyPolicy.
```

### Build

```text
AEMModelState:
  model_state_id
  core_spec
  tokenizer_hash
  router_policy_version
  compatible_expert_card_version
  admitted_expert_ids
  verifier_set_id
  distillation_memory_id
  economy_policy_version
  evidence_seal_refs
```

```text
ExpertArtifact:
  expert_id
  artifact_type: adapter | gguf | verifier | router | dataset | skill
  base_model_hash
  tokenizer_hash
  quantization
  storage_uri_or_commitment
  artifact_hash
  runtime_contract
  training_receipt_refs
  verifier_report_refs
  license
  signature
```

### MVP expert

```text
Expert Capsule v0:
  type: code_patch_expert
  base: open 7B coder, 4-bit
  training: QLoRA adapter
  input: issue + repo snippet + failing test
  output: patch
  verifier: unit tests in sandbox
  admission: improves held-out bugfix pass rate
```

### Kill gates

```text
No ExpertArtifact without ExpertCard.
No ExpertCard without verifier report.
No model state update without evidence reference.
No expert admitted only because manifest is attractive.
```

### Exit criteria

```text
fake expert artifact rejected
real demo code_patch_expert admitted only after verifier report
AEMModelState lists admitted expert
route trace references model_state_id and expert_id
```

---

# Phase 2 — Training receipts and contributor growth

## wrong1

```text
Training = GPU hours burned.
```

Death:

```text
GPU hours do not prove useful learning, policy compliance, or generalization.
```

## wrong2

```text
Training = leaderboard score.
```

Death:

```text
Leaderboard-only training rewards overfit and hides provenance.
```

## Third

```text
Training = receipt-backed capability delta.
```

Training or contribution earns only when it produces measurable delta under provenance/policy gates.

### Build

```text
TrainingReceipt:
  receipt_id
  trainer_node_id
  expert_id
  base_model_hash
  recipe_hash
  data_shard_refs
  compute_profile
  before_eval
  after_eval
  eval_delta
  regression_delta
  anti_overfit_checks
  verifier_report_refs
  credit_policy
  signature
```

```text
DataShardManifest:
  shard_id
  content_hash
  source_policy
  license
  pii_status
  contamination_checks
  target_domains
  used_by_experts
  eval_impact
  contributor_credit_policy
```

### Contributor receipts already started

```text
KnowledgeContributionReceipt:
  knowledge / skill / data_shard / eval / curriculum / operator
  source_policy
  training_use
  credit_policy
  anti_distillation
  evaluation
  receipt_requirements
```

### Training modes

```text
Mode A — QLoRA expert
  frozen 4-bit base + train adapter

Mode B — continued-pretrain small expert
  domain corpus + small model/expert

Mode C — verifier expert
  trained to judge/reject/route

Mode D — distilled expert
  trained from successful mesh traces

Mode E — native low-bit experimental expert
  BitNet-like / ternary / sparse low-bit branch
```

### Kill gates

```text
No training credit without TrainingReceipt.
No TrainingReceipt without data/provenance refs.
No admission without eval_delta + regression_delta.
No distillation from unauthorized competitor outputs.
No data shard without license/provenance/contamination status.
```

### Exit criteria

```text
QLoRA code_patch recipe exists
training emits TrainingReceipt
training receipt references DataShardManifest
verifier confirms eval delta
CreditLedger can mint training/contribution credits from accepted receipts
```

---

# Phase 3 — Local inference loop

## wrong1

```text
Inference = call any expert endpoint and trust output.
```

Death:

```text
Unbound output cannot be credited, challenged, replayed, or debited safely.
```

## wrong2

```text
Inference = chain verifies every token.
```

Death:

```text
On-chain inference is too slow and expensive.
```

## Third

```text
Inference = off-chain execution + InferenceWorkReceipt + challenge surface + CreditLedger settlement.
```

### Already present

```text
InferenceWorkReceipt:
  task_hash
  expert_id
  node_id
  host_advertisement_id
  credit_account
  AEM_CREDIT charge
  prompt/output commitments
  route_trace_id
  nonce
  duplicate spend key
  challenge surface
  policy receipt requirements
```

```text
CreditLedger:
  contribution_mint
  inference_debit
  inference_host_credit
  account balances
  seen_spend_keys
  rejections
```

### Build

```text
InferenceGateway:
  OpenAI-compatible /v1/chat/completions
  internal TaskPacket creation
  RouterPolicy selection
  HostAdvertisement match
  expert call
  InferenceWorkReceipt emission
  CreditLedger settlement call
```

### Kill gates

```text
No inference credit without InferenceWorkReceipt.
No settlement while challenge window open.
No duplicate spend key reuse.
No host offer outside NodeCard policy/capacity/economic floor.
No private task routed to untrusted host.
```

### Exit criteria

```text
local user calls gateway
router selects demo expert
host emits InferenceWorkReceipt
CreditLedger debits payer and credits host
route trace and receipt can be replayed
```

---

# Phase 4 — Router and verifier mesh

## wrong1

```text
Router = nearest host wins.
```

Death:

```text
Nearest can be weak, stale, expensive, low quality, or policy incompatible.
```

## wrong2

```text
Router = strongest expert wins globally.
```

Death:

```text
Global-best ignores latency, locality, price, privacy, availability, and exploration.
```

## Third

```text
Router = task-level immune scheduler.
```

It routes by:

```text
capability_fit
locality_bucket
quality_score
receipt_quality
credit_price
availability
privacy_policy
freshness
reputation
exploration/canary budget
```

### Build

```text
RouterDecision:
  task_id
  model_state_id
  candidate_experts
  candidate_hosts
  rejected_candidates
  selected_expert
  selected_host
  score_breakdown
  policy_constraints
  expected_credit_charge
  fallback_set
  route_trace_id
```

```text
VerifierReport:
  report_id
  verifier_node_id
  target_receipt_id
  verifier_type
  checks_run
  pass_fail
  findings
  challenge_refs
  signature
```

### Verifier types

```text
target_eval_verifier
general_regression_verifier
duplicate_detector
backdoor_trigger_detector
latency_cost_verifier
sandbox_verifier
data_contamination_verifier
signature_repro_verifier
```

### Kill gates

```text
Router cannot be central unversioned brain.
Router decisions must be traceable.
Verifier cannot be the expert author alone.
Admission cannot depend on one central evaluator.
Routing must support canary traffic and fallback.
```

### Exit criteria

```text
router emits RouterDecision
verifier mesh emits VerifierReport
bad expert gets canary traffic only or rejected
successful route becomes distillation memory
```

---

# Phase 5 — Product-grade node runtime

## wrong1

```text
Node = GPU server.
```

Death:

```text
GPU server alone does not prove identity, policy, credit account, receipts, or safe task handling.
```

## wrong2

```text
Node = generic inference API.
```

Death:

```text
Generic API does not train, verify, sign receipts, run sandbox, or participate in settlement.
```

## Third

```text
Node = worker-organ.
```

### Build

```text
aem node profile
  emits NodeCard draft

aem node serve
  loads ExpertArtifact and HostAdvertisement

aem node infer
  serves TaskPacket and emits InferenceWorkReceipt

aem node verify
  runs verifier jobs and emits VerifierReport

aem node train
  runs recipe and emits TrainingReceipt

aem node settle
  submits receipts to CreditLedger simulator/testnet
```

### Runtime capabilities by hardware

```text
12GB:
  7B/8B quantized inference
  QLoRA small expert
  verifier jobs
  code test runner
  data cleaning
  embedding/rerank

16GB:
  larger adapters
  longer context
  14B quantized inference/training with constraints
  expert serving + verifier

24GB+:
  heavy expert training
  multi-expert serving
  distillation jobs
```

### Kill gates

```text
Node without NodeCard cannot join.
Node without receipt signing cannot earn.
Node without sandbox cannot run untrusted verification.
Node without privacy policy cannot receive sensitive tasks.
```

### Exit criteria

```text
node profile generates valid NodeCard
node serve publishes valid HostAdvertisement
node infer emits valid InferenceWorkReceipt
node verify emits valid VerifierReport
node train emits valid TrainingReceipt
```

---

# Phase 6 — Credit economy and settlement hardening

## wrong1

```text
Credits = centralized mutable balances.
```

Death:

```text
Mutable balances hide why value moved and recreate a platform operator.
```

## wrong2

```text
Credits = speculative token before product utility.
```

Death:

```text
This attracts speculation before useful inference/training exists.
```

## Third

```text
Credits = receipt-backed compute/accounting unit.
```

### Current CreditLedger

```text
consumes contribution receipts
consumes inference receipts
validates policy/challenge/duplicate-spend
emits settlement events
updates balances
```

### Build next

```text
CreditTransferReceipt:
  from_account
  to_account
  amount_micros
  reason
  nonce
  signature

CreditSpendAuthorization:
  account
  max_amount
  task_scope
  expiry
  nonce
  signature

SlashingReceipt:
  offender_id
  bad_receipt_id
  proof_type
  verifier_reports
  amount_micros
  appeal_window
  signature
```

### Kill gates

```text
No balance change without settlement event.
No transfer without signature and nonce.
No slashing without proof receipt.
No mint without accepted work/contribution receipt.
No inference spend without spend authorization.
```

### Exit criteria

```text
CreditLedger supports mint, debit, host credit, transfer, spend authorization, slashing stub
settlement report is replayable
supply delta is computed
all duplicate nonces rejected
```

---

# Phase 7 — Multi-node alpha

## wrong1

```text
If local loop works, public network works.
```

Death:

```text
Public network adds churn, malicious nodes, stale advertisements, route failures, and economic attacks.
```

## wrong2

```text
Launch public permissionless immediately.
```

Death:

```text
Without staged trust, fraud and privacy failures dominate signal.
```

## Third

```text
LAN alpha → trusted testnet → permissioned public alpha → permissionless public beta.
```

### Build

```text
Registry service
Node heartbeat
HostAdvertisement expiry
Task dispatch
Receipt collection
Verifier dispatch
CreditLedger testnet
Gateway API
Dashboard
```

### Kill gates

```text
Node drop does not break task permanently.
Expired host ads are not routable.
Bad receipt does not settle.
Duplicate spend across nodes rejected.
Router fallback works.
```

### Exit criteria

```text
3-node LAN demo
10-node private testnet
100-node public alpha with public tasks only
stable API and metrics dashboard
```

---

# Phase 8 — Product-grade inference API

## wrong1

```text
Product = internal mesh only.
```

Death:

```text
Users need a stable API, billing, logs, privacy policy, and predictable behavior.
```

## wrong2

```text
Product = pretty UI over unstable protocol.
```

Death:

```text
UI cannot compensate for missing receipts, routing, and settlement correctness.
```

## Third

```text
OpenAI-compatible gateway over AEM mesh protocol.
```

### Build

```text
/v1/chat/completions
/v1/embeddings
/v1/experts
/v1/routes
/v1/receipts
/v1/credits/balance
/v1/credits/transfer
/v1/contributions
/v1/training/jobs
```

### Product SLOs

```text
p50 latency per task class
p95 latency per task class
receipt emission success rate
settlement success rate
duplicate rejection rate
router fallback rate
expert error rate
privacy-policy rejection rate
```

### Kill gates

```text
No API response without route_trace_id.
No paid response without receipt_id.
No failed settlement hidden from user.
No private task to public untrusted host.
No model/expert change without version id.
```

### Exit criteria

```text
SDK can submit task and retrieve receipt
gateway exposes balance and settlement events
logs are redacted by privacy class
API versioning stable
```

---

# Phase 9 — Training product

## wrong1

```text
Training product = people submit datasets and wait.
```

Death:

```text
Datasets without provenance/eval/receipts cannot safely enter growth loop.
```

## wrong2

```text
Training product = automatic LoRA marketplace.
```

Death:

```text
Marketplace without admission and verifier gates is adapter spam.
```

## Third

```text
Training product = recipe-backed expert growth with receipts and admission.
```

### Build

```text
Recipe registry
Data shard intake
Contributor dashboard
Training job planner
Node trainer assignment
TrainingReceipt emission
EvalDelta report
Admission queue
Canary routing
Credit settlement
```

### First production recipe

```text
qlora_code_patch_7b:
  target: code_patch_expert
  VRAM: 12GB baseline
  verifier: repo tests
  admission: held-out bugfix pass rate improves
  output: ExpertArtifact + TrainingReceipt + VerifierReport
```

### Kill gates

```text
No training job without recipe hash.
No data shard without source policy.
No expert admission without held-out eval.
No credit without accepted delta.
No overfit-only expert enters main routing.
```

### Exit criteria

```text
user contributes skill/data/eval
network creates training job
node trains adapter
verifier reports delta
expert admitted to canary traffic
contributor/trainer earns credits
```

---

# Phase 10 — Security, privacy, and abuse resistance

## wrong1

```text
Permissionless means trust everyone.
```

Death:

```text
Fraud, data leakage, prompt theft, fake experts, and Sybil nodes will dominate.
```

## wrong2

```text
Security means close the network.
```

Death:

```text
Closed network loses the open growth advantage.
```

## Third

```text
Permissionless edge with staged trust, policy routing, challenges, slashing, and privacy classes.
```

### Build

```text
privacy classes:
  public
  redacted
  trusted_nodes_only
  local_only

fraud controls:
  challenge sampling
  duplicate-spend guard
  slashing receipt
  reputation decay
  collusion detector
  rate limits
  node quarantine
```

### Kill gates

```text
Unknown node cannot receive private tasks.
Fake receipts lose expected value.
Verifier cartel can be challenged.
Slashing requires evidence receipt.
Collusive traffic cannot mint unlimited credits.
```

### Exit criteria

```text
bad node quarantine demo
duplicate-spend attack demo
privacy routing demo
slashing stub demo
collusion detector prototype
```

---

# Phase 11 — Product operations

## wrong1

```text
If protocol works, product is ready.
```

Death:

```text
Users need reliability, support, observability, billing clarity, upgrade policy, and incident handling.
```

## wrong2

```text
Ops can be added later.
```

Death:

```text
Economy and inference failures become irreversible trust failures.
```

## Third

```text
Product grade = protocol correctness + operational reliability.
```

### Build

```text
release channels
schema migration policy
protocol upgrade receipts
node version compatibility
metrics dashboard
incident playbooks
abuse reports
support tooling
credit dispute flow
backup/replay tooling
```

### SLO gates

```text
receipt validation failure rate
settlement replay mismatch rate
router failure rate
node timeout rate
gateway uptime
privacy policy violation count
credit accounting mismatch count
```

### Exit criteria

```text
versioned releases
rollback plan
migration receipts
replay settlement from events
public status page
incident drill passed
```

---

# Timeline by milestones, not dates

## M0 — Current state baseline

```text
Already present:
  unified architecture
  network brick ledger
  NodeCard + HostAdvertisement
  contribution receipts
  inference receipts
  CreditLedger settlement simulator
  evidence pipeline
  aggregate economy check
```

Exit command:

```bash
make evidence-local-ci
make aem-network-economy-check
```

## M1 — AEM model state executable

Deliver:

```text
AEMModelState schema/module/test
ExpertArtifact schema/module/test
TrainingReceipt schema/module/test
DataShardManifest schema/module/test
```

Kill gate:

```text
Expert cannot be admitted without TrainingReceipt + VerifierReport.
```

## M2 — Local Code Patch Expert MVP

Deliver:

```text
qlora_code_patch_7b recipe stub
synthetic repo bug benchmark
patch verifier
expert admission demo
router decision trace
```

Kill gate:

```text
fake expert rejected, real expert passes held-out tests.
```

## M3 — Local inference product loop

Deliver:

```text
local gateway
TaskPacket creation
RouterDecision
HostAdvertisement selection
InferenceWorkReceipt
CreditLedger settlement
receipt lookup API
```

Kill gate:

```text
user gets answer + route_trace_id + receipt_id + settlement event.
```

## M4 — Training/contribution product loop

Deliver:

```text
contribution intake
data shard manifests
training job receipt
eval delta reports
credit mint for accepted delta
```

Kill gate:

```text
raw upload earns zero; verified skill/data/operator contribution can mint credits.
```

## M5 — Multi-node alpha

Deliver:

```text
node daemon
registry
heartbeats
host advertisement expiry
remote verifier dispatch
signed receipts across nodes
```

Kill gate:

```text
one node can serve, another verifies, ledger settles, router fallback works.
```

## M6 — Public testnet

Deliver:

```text
public tasks only
AEM_CREDIT test balances
node reputation
basic slashing stub
public dashboard
gateway API
```

Kill gate:

```text
unknown nodes can earn only through receipts and cannot receive private tasks.
```

## M7 — Product beta

Deliver:

```text
user accounts
credit spend/transfer
contributor dashboard
node operator dashboard
expert marketplace filtered by admission
stable API
monitoring
```

Kill gate:

```text
real users can spend/earn credits without manual operator intervention.
```

## M8 — Product grade

Deliver:

```text
security review
privacy review
load tests
settlement replay audits
migration protocol
incident response
support workflow
versioned stable APIs
```

Kill gate:

```text
AEM survives malicious nodes, broken experts, duplicate receipts, failed routes, and replay audits.
```

---

# Product-grade backlog by domain

## Models

```text
AEMModelState
ExpertArtifact
ExpertCard v2
compatible_core_version
adapter/runtime package format
model state migration
expert retirement/supersession
```

## Training

```text
TrainingReceipt
DataShardManifest
QLoRA code patch recipe
eval delta report
anti-overfit challenge
recipe registry
training job scheduler
```

## Inference

```text
Gateway API
RouterDecision
InferenceWorkReceipt hardening
challenge methods implementation
receipt lookup
privacy-class routing
fallback routing
```

## Router

```text
task classifier
capability index
host-expert scorer
price/locality/quality/reputation score
canary traffic
fallback policy
router training from traces
```

## Verifier

```text
VerifierReport
code sandbox verifier
duplicate expert detector
backdoor/trigger probes
data contamination verifier
latency/cost verifier
challenge sampler
```

## Economy

```text
CreditLedger hardening
CreditTransferReceipt
CreditSpendAuthorization
SlashingReceipt
reputation ledger
market order primitive
settlement finality rule
```

## Node/runtime

```text
node daemon
profile command
serve command
train command
verify command
receipt signer
sandbox runner
health reporting
```

## Product/API

```text
OpenAI-compatible gateway
admin dashboard
node dashboard
contributor dashboard
receipt explorer
credit explorer
status page
SDK
```

## Security/privacy

```text
privacy classes
trusted node sets
local-only routing
redacted logs
sandbox isolation
rate limits
abuse reports
quarantine
slashing workflow
```

## Ops/release

```text
protocol versioning
schema migrations
release channels
rollback
settlement replay audit
incident playbook
load tests
observability
```

---

# Product-grade kill gates

AEM is not product grade if any of these fail:

```text
1. Expert admission can be faked with a pretty manifest.
2. Router is a central opaque brain.
3. Host self-report can mint credits.
4. Duplicate spend key can settle twice.
5. Private tasks can route to unknown nodes.
6. Raw content upload can mint credits.
7. Unauthorized competitor distillation can enter training memory.
8. Settlement cannot be replayed from events.
9. Node crash loses task/receipt state.
10. Evidence artifacts cannot be verified after CI.
11. Training recipe cannot reproduce eval delta.
12. Credits can move without signed event.
```

---

# Next implementation sequence

Immediate next files:

```text
schemas/aem_model_state.schema.json
schemas/expert_artifact.schema.json
schemas/training_receipt.schema.json
schemas/data_shard.schema.json
schemas/verifier_report.schema.json
schemas/router_decision.schema.json
```

Immediate next modules:

```text
aem_poc/aem_model_state.py
aem_poc/aem_training_receipts.py
aem_poc/aem_data_shards.py
aem_poc/aem_verifier_reports.py
aem_poc/aem_router_policy.py
```

Immediate next tests:

```text
tests/test_aem_model_state.py
tests/test_aem_training_receipts.py
tests/test_aem_data_shards.py
tests/test_aem_verifier_reports.py
tests/test_aem_router_policy.py
```

Immediate next target:

```text
make aem-model-growth-check
```

## Final next pressure

```text
Build AEMModelState + ExpertArtifact + TrainingReceipt.
Then prove the first product-grade model loop:
fake expert rejected;
real code_patch expert admitted only after verifier report;
TrainingReceipt mints credits only after measurable held-out delta.
```
