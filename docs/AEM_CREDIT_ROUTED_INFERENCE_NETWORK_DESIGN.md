# AEM Credit-Routed Inference Network design

This file expands the concrete plan:

```text
A network for running AEM / AEM experts where people host experts, run inference, train experts, verify work, contribute knowledge/skills/data, earn AEM_CREDIT, spend credits on their own tasks, or transfer/sell credits when policy allows.
```

Working description:

```text
blockchain-like receipt settlement + inference/training expert network
```

Important boundary:

```text
The ledger settles receipts.
The ledger does not execute model inference.
```

## 0. Root design

### wrong1

```text
AEM network = blockchain executes inference.
```

Death:

```text
On-chain inference is too slow, too expensive, and leaks execution details. It also fails the consumer-GPU mesh goal.
```

### wrong2

```text
AEM network = centralized inference marketplace with internal points.
```

Death:

```text
Centralized points recreate a platform operator: opaque balances, opaque routing, opaque pricing, and one off-switch.
```

### Third

```text
AEM network = off-chain expert work + signed receipts + verifier challenges + CreditLedger settlement.
```

The network runs inference/training/verification off-chain, but the economic truth is replayable:

```text
work → receipt → challenge/policy gate → settlement event → AEM_CREDIT balance
```

## 1. Participants

```text
User:
  spends credits to run inference/training/verification tasks.

Host node:
  runs local experts and earns credits for valid inference/training/verification work.

Expert author / trainer:
  creates useful experts and earns credits after verifier-approved training/admission.

Contributor:
  contributes owned/licensed knowledge, skills, data shards, evals, curricula, or operators and earns credits after measurable-delta gates.

Verifier node:
  checks expert claims, inference receipts, training receipts, data provenance, and fraud challenges.

Router / gateway:
  receives user tasks and chooses expert+host routes under quality, price, locality, policy, and freshness constraints.

CreditLedger:
  settles accepted receipts into AEM_CREDIT balance changes.
```

## 2. What a person needs to join

### wrong1

```text
A person joins with only a wallet address.
```

Death:

```text
A wallet does not prove GPU, expert availability, sandbox policy, credit floor, or receipt obligations.
```

### wrong2

```text
A person joins by exposing a raw inference API endpoint.
```

Death:

```text
A raw endpoint cannot safely earn credits because it is not bound to capacity, policy, price, receipts, or challenges.
```

### Third

```text
A person joins by publishing NodeCard + HostAdvertisement.
```

A participating host must publish:

```text
NodeCard:
  node identity
  locality bucket
  capacity envelope
  economic policy
  host policy
  earning roles
  credit account
  receipt requirements

HostAdvertisement:
  concrete expert offer
  expert id
  expert card hash
  AEM_CREDIT price
  accepted roles
  availability
  task policy
  required work receipts
  signature
```

Current repo files:

```text
schemas/node_card.schema.json
schemas/host_advertisement.schema.json
aem_poc/aem_network_cards.py
tests/test_aem_network_cards.py
docs/AEM_NODECARD_HOSTADVERTISEMENT_DESIGN.md
```

## 3. Expert hosting model

### wrong1

```text
Host earns more just because their model is bigger.
```

Death:

```text
Raw size rewards whales and useless parameter count.
```

### wrong2

```text
Host earns more only by being cheapest/nearest.
```

Death:

```text
Cheapest/nearest routing kills rare high-value experts and specialized capability.
```

### Third

```text
Host earns by verified useful capability adjusted by cost, latency, scarcity, reliability, and policy fit.
```

Reward factors:

```text
expert_quality_score:
  target eval delta
  verified success rate
  regression score
  duplicate score
  backdoor risk
  route outcome history

host_quality_score:
  uptime
  challenge pass rate
  valid receipt rate
  latency
  sandbox/policy compliance
  slashing history

expert_value_modifiers:
  rarity/scarcity
  task demand
  model size only as cost factor, not reward proof
  VRAM requirement
  quantization/runtime efficiency
```

Economic law:

```text
Bigger expert can earn more only if it proves higher utility per task class.
Smarter expert can earn more if verifier and route history show better outcomes.
More powerful host can earn more if it serves more valid work or higher-value experts.
```

## 4. Credit earning paths

## 4.1 Inference earns credits

### wrong1

```text
Host says it answered → host earns.
```

Death:

```text
Self-report mints fake credits.
```

### wrong2

```text
Chain re-executes the model → host earns.
```

Death:

```text
On-chain execution is impossible for real LLM inference economics.
```

### Third

```text
Host earns through InferenceWorkReceipt.
```

Flow:

```text
user task
→ router selects ExpertCard + NodeCard + HostAdvertisement
→ host runs inference off-chain
→ host emits InferenceWorkReceipt
→ challenge window / duplicate-spend guard
→ CreditLedger settlement
→ payer debited
→ host credited
```

Current repo files:

```text
schemas/inference_work_receipt.schema.json
aem_poc/aem_inference_receipts.py
tests/test_aem_inference_receipts.py
docs/AEM_INFERENCE_WORK_RECEIPT_DESIGN.md
```

## 4.2 Training earns credits

### wrong1

```text
Training reward = GPU hours burned.
```

Death:

```text
GPU hours do not prove capability gain.
```

### wrong2

```text
Training reward = final leaderboard score only.
```

Death:

```text
Leaderboard-only rewards overfit and hides data provenance.
```

### Third

```text
Training reward = TrainingReceipt + eval delta + verifier reports.
```

Flow:

```text
trainer trains expert / adapter / verifier / router component
→ TrainingReceipt
→ data/provenance checks
→ before/after eval
→ regression check
→ anti-overfit challenge
→ verifier reports
→ CreditLedger mints accepted training credit
```

Status:

```text
TrainingReceipt is roadmap/next implementation item.
ContributionReceipt and CreditLedger are already present.
```

## 4.3 Contribution earns credits

### wrong1

```text
People upload knowledge/data and automatically earn.
```

Death:

```text
Raw upload rewards spam, poison, unlicensed data, duplicates, and fake expertise.
```

### wrong2

```text
Only compute earns; human knowledge is outside protocol.
```

Death:

```text
Human-owned skills, knowledge, evals, curricula, operators, and data are the strongest bootstrap source.
```

### Third

```text
Contribution earns through KnowledgeContributionReceipt.
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

Current repo files:

```text
schemas/aem_knowledge_contribution.schema.json
aem_poc/aem_bootstrap_growth.py
tests/test_aem_bootstrap_growth.py
docs/AEM_BOOTSTRAP_GROWTH_DESIGN.md
```

## 4.4 Verification earns credits

### wrong1

```text
Verifier earns by agreeing with the majority.
```

Death:

```text
Majority agreement can become cartel behavior.
```

### wrong2

```text
Verifier earns only if centrally trusted.
```

Death:

```text
That recreates a central evaluator.
```

### Third

```text
Verifier earns through challengeable VerifierReport / ChallengeReceipt.
```

Future flow:

```text
verifier receives challenge/eval/sandbox task
→ runs check independently
→ emits VerifierReport
→ if useful and non-fraudulent, earns verification credit
→ if false/collusive, can be slashed
```

Status:

```text
VerifierReport / ChallengeReceipt is a missing primitive.
```

## 5. Spending credits

Credits can be spent on:

```text
inference tasks
training jobs
verification jobs
priority routing
private/local routing premium
expert admission/eval fees
data/eval contribution review
```

Spend flow:

```text
user account
→ CreditSpendAuthorization
→ router budget check
→ selected HostAdvertisement price
→ InferenceWorkReceipt
→ CreditLedger settlement
```

Status:

```text
CreditSpendAuthorization is missing primitive.
```

## 6. Selling / transferring credits

### wrong1

```text
Credits are non-transferable points forever.
```

Death:

```text
Hosts and contributors cannot sell surplus earned capacity; market discovery dies.
```

### wrong2

```text
Credits become speculative token immediately.
```

Death:

```text
Token-first design attracts speculation and regulatory risk before utility is proven.
```

### Third

```text
Credits start as receipt-backed compute credits; transfer/resale is enabled in staged policy.
```

Market stages:

```text
E0: local simulator credits only
E1: testnet credits, no monetary claim
E2: utility credits for real inference/training/verification
E3: resale market after regulatory boundary
E4: mature economy with market orders, reputation, slashing, dispute flow
```

Required future receipts:

```text
CreditTransferReceipt
MarketOrderReceipt
CreditSpendAuthorization
RegulatoryBoundary
Dispute/AppealReceipt
```

## 7. Nearest expert host routing

### wrong1

```text
Route to nearest host.
```

Death:

```text
Nearest host may be weak, stale, expensive, malicious, or policy-incompatible.
```

### wrong2

```text
Route to best global expert.
```

Death:

```text
Best global expert may be slow, overloaded, too expensive, or incompatible with privacy policy.
```

### Third

```text
Route to nearest adequate verified host for the needed expert/capability under budget and policy constraints.
```

Router scoring:

```text
score(host, expert, task) =
  capability_fit
  + locality_score
  + expert_quality_score
  + host_quality_score
  + price_fit
  + freshness
  + policy_fit
  + challenge_pass_rate
  - latency_penalty
  - risk_penalty
```

Routing sequence:

```text
1. classify task capabilities
2. find expert candidates
3. find HostAdvertisements for each expert
4. filter by NodeCard capacity/policy
5. filter by privacy class
6. filter by user max credit budget
7. rank by locality + quality + price + freshness
8. call top candidate or top-k
9. emit RouteTrace and InferenceWorkReceipt
10. settle through CreditLedger after challenge window
```

Current pieces already present:

```text
TaskPacket
ExpertCard
NodeCard
HostAdvertisement
RouteTrace
InferenceWorkReceipt
CreditLedger
```

Missing:

```text
RouterDecision schema
locality_score implementation
availability_challenge_receipt
price_score implementation
reputation ledger
fallback routing
```

## 8. Blockchain + inference boundary

### wrong1

```text
Blockchain runs inference.
```

Death:

```text
Too slow, too expensive, wrong execution layer.
```

### wrong2

```text
No ledger is needed; gateway keeps balances.
```

Death:

```text
Opaque gateway balances recreate centralized accounting and cannot be replayed.
```

### Third

```text
Ledger settles receipt truth; inference stays off-chain.
```

Ledger responsibilities:

```text
store / verify settlement events
reject duplicate spend keys
track balances
track supply delta
record receipt ids
support challenge windows
support slashing/dispute receipts
```

Off-chain responsibilities:

```text
run model inference
train experts
run verifiers
store large artifacts
produce commitments
produce signed receipts
```

## 9. Product flows

## 9.1 User runs own task

```text
user has AEM_CREDIT
→ submits task to gateway
→ router finds expert and nearest adequate host
→ host runs inference
→ user receives answer + receipt id + route trace
→ CreditLedger debits user and credits host
```

## 9.2 Host earns credits

```text
host publishes NodeCard
→ host advertises local expert
→ router sends eligible tasks
→ host emits InferenceWorkReceipt
→ challenge passes
→ CreditLedger credits host account
```

## 9.3 Trainer earns credits

```text
trainer trains expert
→ TrainingReceipt + EvalDelta + VerifierReport
→ expert admitted to canary traffic
→ CreditLedger mints training reward
→ later inference traffic can reward host/trainer policy if enabled
```

## 9.4 Contributor earns credits

```text
contributor submits skill/knowledge/data/eval/curriculum/operator
→ KnowledgeContributionReceipt
→ provenance and delta tests
→ accepted contribution mints AEM_CREDIT
```

## 9.5 Credit resale

```text
host has earned credits
→ creates transfer/market order if resale_allowed
→ buyer acquires credits
→ buyer spends credits on inference/training/verification
```

## 10. Pricing model

## 10.1 Inference price

```text
price = max(
  min_job_credits,
  token_units * host_rate * quality_multiplier * scarcity_multiplier * urgency_multiplier
)
```

Where:

```text
token_units = input_tokens + output_tokens or model-specific metered units
host_rate = HostAdvertisement.offer.inference_credit_rate_micros
quality_multiplier = expert/host performance history
scarcity_multiplier = rare useful expert availability
urgency_multiplier = priority latency
```

## 10.2 Training reward

```text
training_reward = base_reward
                * eval_delta_multiplier
                * generalization_multiplier
                * novelty_multiplier
                * provenance_multiplier
                * anti_overfit_multiplier
                * adoption_multiplier
```

## 10.3 Contribution reward

```text
contribution_reward = base_credit_micros
                    * contribution_quality_multiplier
                    * adoption_multiplier
                    * downstream_eval_impact_multiplier
```

## 10.4 Verification reward

```text
verification_reward = base_verification_fee
                    * check_difficulty
                    * fraud_catch_bonus
                    * timeliness_multiplier
                    * agreement_quality
```

## 11. Anti-gaming gates

```text
fake inference:
  challenge surface + route replay + output commitment open

duplicate spend:
  spend_key = task_hash | expert_id | node_id | nonce

fake contribution:
  source policy + required receipts + measurable delta

unauthorized distillation:
  no_unauthorized_competitor_distillation + verified terms

self-dealing traffic:
  related-account graph + external demand weighting + reward caps

model-size farming:
  no model size alone as reward basis

verifier cartel:
  challengeable verifier reports + slashing + disagreement tracking
```

## 12. Current repo embodiment

Already implemented:

```text
schemas/node_card.schema.json
schemas/host_advertisement.schema.json
schemas/aem_knowledge_contribution.schema.json
schemas/inference_work_receipt.schema.json
schemas/credit_ledger_settlement.schema.json

aem_poc/aem_network_cards.py
aem_poc/aem_bootstrap_growth.py
aem_poc/aem_inference_receipts.py
aem_poc/aem_credit_ledger.py

tests/test_aem_network_cards.py
tests/test_aem_bootstrap_growth.py
tests/test_aem_inference_receipts.py
tests/test_aem_credit_ledger.py
```

Aggregate command:

```bash
make aem-network-economy-check
```

## 13. Missing primitives

```text
RouterDecision
CreditSpendAuthorization
CreditTransferReceipt
MarketOrderReceipt
TrainingReceipt settlement
VerifierRewardReceipt
ChallengeReceipt
SlashingReceipt
ReputationLedger
CollusionDetector
SettlementFinalityRule
RegulatoryBoundary
Dispute/AppealReceipt
ProtocolProposal
MigrationReceipt
```

## 14. Product-grade kill gates

```text
1. Host can self-report work and earn credits.
2. User balance changes without settlement event.
3. Duplicate spend key settles twice.
4. Router hides price or expert/host route.
5. Raw upload mints credits.
6. Unauthorized competitor distillation enters training memory.
7. Private task routes to unknown host.
8. Host advertises expert outside NodeCard policy.
9. Larger model earns more without utility proof.
10. Credit resale happens without transfer receipt and regulatory boundary.
```

## 15. Roadmap specific to this network plan

### Stage N0 — Current foundation

```text
NodeCard
HostAdvertisement
KnowledgeContributionReceipt
InferenceWorkReceipt
CreditLedger settlement simulator
AEM network economy check
```

### Stage N1 — RouterDecision

```text
build router scoring for:
  capability
  locality
  quality
  price
  freshness
  privacy
```

### Stage N2 — Spend authorization

```text
CreditSpendAuthorization
user max budget
route cannot exceed budget
```

### Stage N3 — Credit transfers

```text
CreditTransferReceipt
nonce guard
zero net supply delta
```

### Stage N4 — Training settlement

```text
TrainingReceipt
EvalDelta
VerifierReport
training_mint
```

### Stage N5 — Reputation/slashing

```text
ReputationLedger
SlashingReceipt
ChallengeReceipt
collusion detector
```

### Stage N6 — Public testnet

```text
public tasks only
test credits
node registry
host advertisements
receipt explorer
credit explorer
```

### Stage N7 — Product beta

```text
real gateway
real accounts
utility credits
resale after legal boundary
node/contributor dashboards
```

## 16. Final law

```text
AEM is blockchain + inference only in the correct split:

inference/training/verification happen off-chain on expert nodes;
truth/economics happen through signed receipts, challenge windows, and replayable CreditLedger settlement.
```

## 17. Next pressure

```text
Implement RouterDecision + CreditSpendAuthorization so user tasks can be budgeted and routed to the nearest adequate verified expert host.
```
