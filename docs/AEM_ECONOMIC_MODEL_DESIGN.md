# AEM Economic Model design

This file defines how the AEM economy should work as protocol, not as vibes, token hype, or centralized accounting.

It covers:

```text
participants
value creation
credits
earning
spending
pricing
settlement
verification
fraud resistance
resale
governance boundaries
product-grade kill gates
```

This is a protocol-economic model for AEM_CREDIT. It is not a legal classification, securities claim, investment promise, or guarantee of future value. Legal/regulatory treatment is an explicit missing primitive and must be handled before public monetary markets.

---

# 0. Root design

## wrong1

```text
AEM economy = token first.
```

Death:

```text
A token before useful work attracts speculation, Sybil farming, fake demand, and regulatory drag before the network proves utility.
```

## wrong2

```text
AEM economy = centralized credits controlled by one operator.
```

Death:

```text
Central credits recreate the platform form: one account database, one pricing authority, one off-switch, and opaque balance mutation.
```

## Third

```text
AEM economy = receipt-backed compute credit system.
```

AEM_CREDIT is created, moved, or burned only through replayable receipts and settlement events.

Core law:

```text
No credit without receipt.
No receipt without policy/provenance binding.
No balance change without CreditLedger settlement event.
No public market without regulatory boundary.
```

---

# 1. Economic object: AEM_CREDIT

## Definition

```text
AEM_CREDIT = protocol accounting unit for buying, selling, rewarding, and settling verified network work.
```

It is used for:

```text
inference spend
training reward
verification reward
knowledge/skill/data/eval/curriculum/operator contribution reward
host payment
credit transfer/resale where allowed
slashing and dispute accounting
```

It is not initially defined as:

```text
equity
governance right
profit share
security claim
unbounded speculative asset
```

## Unit

```text
1 AEM_CREDIT = 1_000_000 credit_micros
```

All protocol calculations use integer micros:

```text
amount_micros: integer
```

---

# 2. Participants

## User / buyer

Consumes inference, training, verification, or private/local tasks.

Pays:

```text
AEM_CREDIT spend authorization
```

Receives:

```text
answer / patch / artifact
route_trace_id
receipt_id
settlement_event_id
```

## Host node

Runs local expert inference, training, verification, data cleaning, or sandbox jobs.

Must publish:

```text
NodeCard
HostAdvertisement
```

Earns through:

```text
InferenceWorkReceipt
TrainingReceipt
VerifierReport / verification receipt
```

## Expert author / trainer

Creates or improves an expert.

Earns through:

```text
TrainingReceipt
ExpertArtifact admission
future traffic share if policy supports it
```

## Contributor

Contributes owned/licensed:

```text
knowledge
skill
data_shard
eval
curriculum
operator
```

Earns through:

```text
KnowledgeContributionReceipt
accepted measurable delta
```

## Verifier node

Runs challenge/eval/sandbox/provenance checks.

Earns through:

```text
VerifierReport
challenge receipt
slashing proof when valid
```

## Router / gateway operator

Runs public or local gateway and routes tasks.

May earn through:

```text
routing fee
gateway fee
settlement fee
```

But must not become central brain.

## Credit market participant

Buys/sells transferable AEM_CREDIT if policy and legal boundary allow.

Must not bypass work-backed accounting.

---

# 3. Value flows

## Flow A — Inference purchase

```text
user spend authorization
→ router selects ExpertCard + NodeCard + HostAdvertisement
→ host performs off-chain inference
→ InferenceWorkReceipt
→ challenge window / duplicate-spend guard
→ CreditLedger settlement
→ user debited
→ host credited
```

Settlement events:

```text
inference_debit
inference_host_credit
```

Supply effect:

```text
zero net supply change
```

## Flow B — Training reward

```text
trainer runs recipe
→ TrainingReceipt
→ eval delta + regression delta + provenance checks
→ verifier reports
→ CreditLedger settlement
→ trainer credited
```

Settlement event:

```text
training_mint
```

Supply effect:

```text
net supply increases only if training delta is accepted
```

## Flow C — Human knowledge / skill / data contribution reward

```text
contributor submits contribution
→ content commitment + source policy + anti-distillation policy
→ measurable delta tests
→ KnowledgeContributionReceipt
→ CreditLedger settlement
→ contributor credited
```

Settlement event:

```text
contribution_mint
```

Supply effect:

```text
net supply increases only if contribution is accepted
```

## Flow D — Verification reward

```text
verifier receives challenge/eval task
→ runs independent test
→ VerifierReport
→ if valid and useful, CreditLedger settlement
→ verifier credited
```

Settlement event:

```text
verification_mint or verification_fee_transfer
```

Supply effect:

```text
policy-dependent: minted for public-good verification or paid from requester/challenge pool
```

## Flow E — Credit transfer / resale

```text
seller has settled credit balance
→ transfer authorization
→ buyer payment outside or inside supported rails
→ CreditTransferReceipt
→ CreditLedger transfer
```

Settlement events:

```text
credit_transfer_debit
credit_transfer_credit
```

Supply effect:

```text
zero net supply change
```

Regulatory boundary:

```text
must be explicit before public resale markets
```

---

# 4. Receipt classes

## InferenceWorkReceipt

Purpose:

```text
prove a host performed inference work eligible for credit transfer
```

Must bind:

```text
task_hash
expert_id
expert_card_hash
node_id
host_advertisement_id
credit_account
settlement_currency = AEM_CREDIT
credit_charge_micros
prompt_commitment
output_commitment
route_trace_id
nonce
duplicate_spend.spend_key
challenge_surface
policy.receipt_requirements
signature
```

Kill gates:

```text
seen spend_key rejected
missing challenge surface rejected
host ad mismatch rejected
wrong credit charge rejected
open challenge window rejected
```

## TrainingReceipt

Purpose:

```text
prove model/expert training produced accepted measurable capability delta
```

Must bind:

```text
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

Kill gates:

```text
no eval_delta → no credit
no provenance → no credit
regression exceeds threshold → no admission
anti-overfit fails → no mint
```

## KnowledgeContributionReceipt

Purpose:

```text
reward human-owned/licensed knowledge, skill, data, eval, curriculum, or operator contribution
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

Kill gates:

```text
raw upload size earns zero
third-party model outputs require verified terms
unauthorized competitor distillation rejected
missing provenance rejected
no measurable delta rejected
```

## VerifierReport / ChallengeReceipt

Purpose:

```text
prove verifier work and make receipts challengeable
```

Must bind:

```text
verifier_node_id
target_receipt_id
checks_run
findings
pass_fail
challenge_refs
signature
```

Kill gates:

```text
self-verification alone cannot admit high-trust expert
verifier cartel must be challengeable
false verifier reports can be slashed
```

## CreditLedgerSettlementReport

Purpose:

```text
turn accepted receipts into deterministic AEM_CREDIT events and balances
```

Must include:

```text
settlement_version
settlement_currency
challenge_window_closed
accepted events
rejections
accounts
seen_spend_keys
net_supply_delta_micros
```

---

# 5. Mint / transfer / burn rules

## Mint

Mint happens only for accepted productive work:

```text
contribution_mint
training_mint
verification_mint
protocol_bootstrap_grant, if explicitly governed
```

Mint must always have:

```text
source_receipt_id
account
amount_micros
reason
settlement_currency
policy version
```

## Transfer

Transfer moves existing credits:

```text
inference_debit + inference_host_credit
credit_transfer_debit + credit_transfer_credit
market_sale_debit + market_sale_credit
```

Transfer has zero net supply delta.

## Burn

Burn removes credits from supply, if used for:

```text
protocol fees
anti-spam deposits
slashing penalties
optional burn-to-priority mechanisms
```

Burn must be explicit and replayable.

---

# 6. Pricing model

## Inference price

Base calculation:

```text
inference_price = max(
  min_job_credits,
  token_units * host_rate * quality_multiplier * scarcity_multiplier * urgency_multiplier
)
```

Where:

```text
token_units:
  input_tokens + output_tokens, or model-specific metered units

host_rate:
  HostAdvertisement.offer.inference_credit_rate_micros

quality_multiplier:
  based on expert verifier history and task-class performance

scarcity_multiplier:
  higher for rare/valuable capabilities with low supply

urgency_multiplier:
  higher for low-latency priority service
```

Product-grade cap:

```text
user may set max_credit_spend_micros
router must reject routes above budget
```

## Training reward

Base calculation:

```text
training_reward = base_training_reward
                * eval_delta_multiplier
                * generalization_multiplier
                * novelty_multiplier
                * provenance_multiplier
                * anti_overfit_multiplier
                * adoption_multiplier
```

Hard caps:

```text
reward_cap_by_recipe
reward_cap_by_epoch
reward_cap_by_expert_family
```

No reward if:

```text
eval_delta <= threshold
regression_delta > threshold
anti_overfit fails
source policy fails
```

## Contribution reward

Base calculation:

```text
contribution_reward = base_credit_micros
                    * contribution_quality_multiplier
                    * adoption_multiplier
                    * downstream_eval_impact_multiplier
```

Contribution quality cannot be raw size.

Allowed credit basis:

```text
accepted_delta
verified_skill_use
eval_improvement
curation_quality
operator_adoption
```

## Verification reward

Base calculation:

```text
verification_reward = base_verification_fee
                    * check_difficulty
                    * agreement_quality
                    * fraud_catch_bonus
                    * timeliness_multiplier
```

Verifier slashing risk:

```text
false report
collusion
low-quality spam verification
missed obvious fraud under challenge
```

---

# 7. Quality multipliers

## Expert quality score

```text
expert_quality_score = f(
  target_eval_delta,
  regression_delta,
  verified_success_rate,
  route_outcome_history,
  duplicate_score,
  backdoor_risk,
  latency_cost_ratio,
  user_feedback_when_allowed
)
```

## Host quality score

```text
host_quality_score = f(
  uptime,
  valid_receipt_rate,
  challenge_pass_rate,
  latency,
  policy_compliance,
  duplicate_rejection_history,
  slashing_history
)
```

## Contributor quality score

```text
contributor_quality_score = f(
  accepted_delta_history,
  provenance_cleanliness,
  downstream_adoption,
  rejected_submission_rate,
  dispute_history
)
```

## Verifier quality score

```text
verifier_quality_score = f(
  agreement_with_later_consensus,
  fraud_detection_value,
  false_positive_rate,
  false_negative_rate,
  challenge_response_quality
)
```

---

# 8. Anti-gaming / fraud gates

## Fake inference

Attack:

```text
host claims work without running expert
```

Gates:

```text
output_commitment_open
route_trace_replay
metered_cost_audit
expert_hash_check
challenge sampling
```

## Duplicate spend

Attack:

```text
same inference receipt settles twice
```

Gate:

```text
spend_key = task_hash | expert_id | node_id | nonce
seen_spend_keys rejects duplicate
```

## Fake contribution

Attack:

```text
upload unowned or low-quality content for credits
```

Gates:

```text
source_policy
license check
human_authored_or_owned
required receipts
measurable delta
kill criteria
```

## Unauthorized competitor distillation

Attack:

```text
extract competitor outputs and claim bootstrap growth
```

Gates:

```text
no_unauthorized_competitor_distillation = true
allowed_teacher_policy_required = true
third_party_terms_verified = true if outputs are present
```

## Sybil nodes

Attack:

```text
many fake nodes create fake work loops
```

Gates:

```text
collateral requirement
challenge sampling
reputation graph
collusion detector
credit velocity caps
slashing receipts
```

## Self-dealing traffic

Attack:

```text
same actor buys fake inference from own host to farm quality/rewards
```

Gates:

```text
related-account graph
reward caps
external demand weighting
challenge sampling
no quality multiplier from self-dealing traffic alone
```

## Model size farming

Attack:

```text
large but useless expert demands higher reward
```

Gate:

```text
no model size alone as reward basis
quality/cost ratio required
verified capability delta required
```

---

# 9. Credit lifecycle

## Earn

Credits are earned by:

```text
valid inference work
accepted training delta
accepted contribution delta
valid verification work
valid slashing/fraud proof, if policy rewards it
```

## Spend

Credits are spent on:

```text
inference tasks
training jobs
verification jobs
priority routing
private/local routing premiums
expert admission/eval fees
```

## Save

Credits can be held for future work consumption.

## Transfer / sell

Credits can be transferred or sold only when:

```text
resale_allowed = true
regulatory boundary satisfied
CreditTransferReceipt exists
no double-spend
source of credits is settled
```

## Slash

Credits can be slashed for:

```text
fake receipts
collusion
invalid verification
policy breach
private data leak
malicious expert behavior
```

## Expire / decay

Optional policy:

```text
unused promotional credits may expire
earned work credits should not silently expire unless policy says so
reputation may decay; settled credits should not mutate invisibly
```

---

# 10. Supply control

## Mint sources

```text
accepted contribution work
accepted training work
accepted verification work
bootstrap grants, if governance-approved
```

## Sink sources

```text
protocol fees
slashing burn
anti-spam deposits
optional settlement fees
```

## Transfer-only flows

```text
inference payment
credit resale
credit transfer
```

## Supply invariant

```text
net_supply_delta = sum(mints) - sum(burns)
```

Transfers must not change net supply.

Product-grade CreditLedger must be replayable from events.

---

# 11. Market design stages

## Stage E0 — Internal credits only

```text
credits only inside local simulator
no public resale
no monetary claims
```

Purpose:

```text
prove receipts, settlement, duplicate-spend guard, and accounting
```

## Stage E1 — Testnet credits

```text
public test credits
no monetary value claim
faucet + earned test credits
fake-work attacks encouraged
```

Purpose:

```text
stress fraud gates and routing economics
```

## Stage E2 — Utility credits

```text
credits buy real inference/training/verification capacity
limited transfer
KYC/legal/regulatory boundary depends on jurisdiction
```

Purpose:

```text
real work-backed network economy
```

## Stage E3 — Resale market

```text
transferable credits with marketplace rails
explicit legal/regulatory review
market order receipts
dispute flow
```

Purpose:

```text
allow hosts/contributors to sell surplus credits
```

## Stage E4 — Mature economy

```text
reputation-weighted routing
liquidity providers if legally allowed
insurance/staking/slashing pools
cross-gateway settlement
```

Purpose:

```text
robust open compute economy
```

---

# 12. Participant incentives

## User

Wants:

```text
cheap inference
fast response
privacy
quality
receipt proof
predictable spend
```

Receives:

```text
answer
route trace
receipt
settlement event
quality/fallback guarantees
```

## Host

Wants:

```text
traffic
credit earnings
reputation growth
higher reward for better experts/hardware
resale ability
```

Must provide:

```text
NodeCard
HostAdvertisement
valid receipts
challenge compliance
policy compliance
```

## Trainer

Wants:

```text
credit for useful expert improvements
traffic share
reputation
future distillation/adoption reward
```

Must provide:

```text
TrainingReceipt
recipe hash
data/provenance refs
eval delta
verifier reports
```

## Contributor

Wants:

```text
credit for knowledge/skill/data/eval/curriculum/operator contribution
```

Must provide:

```text
source policy
content commitment
anti-distillation policy
measurable delta
receipt requirements
```

## Verifier

Wants:

```text
credit for useful verification and fraud detection
```

Must provide:

```text
VerifierReport
challenge proof
reproducible findings
```

---

# 13. Revenue / fee model

Fees should not be first-class until receipts work.

Possible protocol fees:

```text
settlement_fee_micros
routing_fee_micros
gateway_fee_micros
marketplace_fee_micros
challenge_fee_micros
admission_eval_fee_micros
```

Fee rules:

```text
fee must be visible in settlement event
fee cannot mutate balances silently
fee cannot bypass contributor/host rewards
fee schedule must be versioned
```

Recommended early policy:

```text
E0/E1: no protocol fee
E2: small gateway/routing fee only
E3+: marketplace/settlement fees if legally clear
```

---

# 14. Pricing examples

## Example 1 — Inference

Input:

```text
input_tokens = 12
output_tokens = 8
host_rate = 150 credit_micros/token
min_job = 100 credit_micros
```

Computation:

```text
price = max(100, (12 + 8) * 150)
price = 3000 credit_micros
```

Events:

```text
inference_debit user -3000
inference_host_credit host +3000
net_supply_delta 0
```

## Example 2 — Contribution

Input:

```text
base_credit = 1000
quality_multiplier = 3.0
cap = 5.0
```

Computation:

```text
mint = 1000 * min(3.0, 5.0)
mint = 3000 credit_micros
```

Event:

```text
contribution_mint contributor +3000
net_supply_delta +3000
```

## Example 3 — Duplicate inference attack

Input:

```text
same spend_key appears twice
```

Result:

```text
first receipt may settle
second receipt rejected
no second host credit
```

---

# 15. Governance boundaries

## wrong1

```text
Maintainer can change economics by editing code.
```

Death:

```text
Silent mutation breaks trust and makes credits arbitrary.
```

## wrong2

```text
Token vote controls everything.
```

Death:

```text
Token vote can capture verifier truth and safety policy.
```

## Third

```text
Versioned economic policy + bounded governance domains + migration receipts.
```

Governance domains:

```text
fee schedule
reward caps
challenge windows
slashing thresholds
privacy defaults
market enablement
schema upgrades
```

Non-governable by simple vote:

```text
verifier factual result
receipt replay history
private data policy bypass
retroactive arbitrary balance mutation
```

Missing primitives:

```text
ProtocolProposal
MigrationReceipt
bounded_vote
regulatory_boundary
appeal_window
```

---

# 16. Product-grade economic kill gates

AEM economy is not product grade if any of these fail:

```text
1. Host self-report can mint credits.
2. Raw upload can mint credits.
3. Duplicate spend key can settle twice.
4. Balance can change without settlement event.
5. Unauthorized competitor distillation can enter contribution memory.
6. Inference can settle before challenge window closes.
7. Router can hide price from user.
8. Node can advertise work below its own economic floor without explicit policy.
9. Verifier can self-approve high-trust work alone.
10. Credit supply cannot be replayed from events.
11. Resale can happen without transfer receipt.
12. Slashing can happen without evidence receipt.
```

---

# 17. Current repo embodiment

Already implemented as protocol/code/tests:

```text
NodeCard
HostAdvertisement
KnowledgeContributionReceipt
InferenceWorkReceipt
CreditLedger settlement simulator
AEM network/economy aggregate check
```

Files:

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

Commands:

```bash
make aem-network-economy-check
make aem-credit-ledger-check
make aem-inference-receipts-check
make aem-bootstrap-growth-check
make aem-network-cards-check
```

---

# 18. Missing economic primitives

```text
CreditTransferReceipt
CreditSpendAuthorization
TrainingReceipt settlement
VerifierRewardReceipt
SlashingReceipt
ChallengeReceipt
MarketOrderReceipt
ReputationLedger
CollusionDetector
SettlementFinalityRule
RegulatoryBoundary
Dispute/AppealReceipt
ProtocolProposal
MigrationReceipt
```

---

# 19. Immediate next implementation plan

## Step 1 — CreditTransferReceipt

```text
schemas/credit_transfer_receipt.schema.json
aem_poc/aem_credit_transfers.py
tests/test_aem_credit_transfers.py
```

Kill gate:

```text
same transfer nonce cannot settle twice
transfer preserves total supply
```

## Step 2 — CreditSpendAuthorization

```text
schemas/credit_spend_authorization.schema.json
```

Kill gate:

```text
inference gateway cannot spend above user max budget
```

## Step 3 — TrainingReceipt settlement

```text
schemas/training_receipt.schema.json
```

Kill gate:

```text
TrainingReceipt mints credits only after eval delta + verifier reports
```

## Step 4 — SlashingReceipt

```text
schemas/slashing_receipt.schema.json
```

Kill gate:

```text
fake receipt can reduce collateral/reputation only with evidence proof
```

## Step 5 — MarketOrderReceipt

```text
schemas/market_order_receipt.schema.json
```

Kill gate:

```text
seller cannot sell credits twice
market order cannot imply equity/governance claim
```

---

# 20. Final one-line law

```text
AEM economy is not a token economy first.
AEM economy is a receipt-settled capability economy:
verified work → settlement event → AEM_CREDIT balance → more verified work.
```
