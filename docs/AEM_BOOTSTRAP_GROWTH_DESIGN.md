# AEM Bootstrap Growth design

wrong1: AEM catches up by distilling frontier competitors.
Death: unauthorized competitor distillation creates legal/policy risk and keeps the network in a follower posture.

wrong2: AEM accepts arbitrary human knowledge uploads for credits.
Death: raw uploads can be low quality, unlicensed, duplicated, poisoned, or impossible to evaluate.

Third: AEM grows by credit-eligible contribution receipts: human-owned/licensed knowledge, skills, data shards, evals, curricula, and operators earn credits only after provenance, anti-distillation, and measurable-delta gates.

Command:

```bash
python -m aem_poc.aem_bootstrap_growth
python -m aem_poc.aem_bootstrap_growth --check
make aem-bootstrap-growth
make aem-bootstrap-growth-check
```

Schema:

```text
schemas/aem_knowledge_contribution.schema.json
```

Code/tests:

```text
aem_poc/aem_bootstrap_growth.py
tests/test_aem_bootstrap_growth.py
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

Economic foundation:

```text
settlement_currency = AEM_CREDIT
credit_account
credit_basis
base_credit_micros
quality_multiplier_floor
quality_multiplier_cap
resale_allowed
```

Allowed credit basis:

```text
accepted_delta
verified_skill_use
eval_improvement
curation_quality
operator_adoption
```

Forbidden reductions:

```text
unauthorized competitor distillation
raw data upload as credit basis
credit minting without provenance receipt
skill claim without execution receipt
```

Anti-distillation boundary:

```text
no_unauthorized_competitor_distillation = true
allowed_teacher_policy_required = true
source_policy.allowed_for_training = true
third-party model outputs require verified terms
```

Growth architecture:

```text
people contribute owned/licensed knowledge, skills, data, evals, curricula, operators
contributions become receipts
receipts pass provenance and delta gates
accepted receipts earn credits
credits fund inference/training/verification in the network
export_policy controls whether others may distill from AEM receipts
```

Death: AEM economy is described as vibes instead of being embedded in contribution receipts and credit gates.

Inheritance: AEM should be a bootstrap growth network that others try to distill, not a follower network built on unauthorized distillation of others.

Next pressure: wire aem-bootstrap-growth-check into a higher-level network/economy check target.
