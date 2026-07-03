# AEM SkillReceipt design

SkillReceipt is the product-grade receipt for a reusable skill as a credit-eligible network contribution.

It is separate from the generic `aem_knowledge_contribution.schema.json` because product-grade skills need execution evidence, verifier references, an explicit skill contract, and a stronger credit basis.

## design

### wrong1

```text
skill = text/prompt/workflow uploaded by a contributor.
```

Death:

```text
Raw skill text can be vague, unowned, untested, non-executable, or impossible to credit fairly.
```

### wrong2

```text
skill = hidden private know-how that earns credits because contributor claims it works.
```

Death:

```text
Self-reported skill value creates fake credit, unverifiable claims, and opaque dependence.
```

### Third

```text
skill = executable contribution with contract + execution evidence + measurable delta + verifier report + anti-distillation policy.
```

## Product-grade SkillReceipt

Schema:

```text
schemas/skill_receipt.schema.json
```

Module/tests:

```text
aem_poc/aem_skill_receipts.py
tests/test_aem_skill_receipts.py
```

Commands:

```bash
python -m aem_poc.aem_skill_receipts
python -m aem_poc.aem_skill_receipts --check
make aem-skill-receipts
make aem-skill-receipts-check
make aem-network-economy-check
```

## Skill types

```text
prompt_operator
tool_workflow
verification_skill
training_recipe
routing_policy
domain_procedure
data_curation_procedure
```

## Required sections

```text
skill_contract
content_commitment
source_policy
execution_evidence
evaluation
credit_policy
anti_distillation
receipt_requirements
verifier_report_refs
signature
```

## Skill contract

A product-grade skill must define:

```text
input_contract
operation
output_contract
required_tools
runtime_constraints
determinism_level
```

This kills the vague prompt/workflow collapse: if the skill cannot state what it accepts, what it does, and what it emits, it is not a product-grade network skill.

## Execution evidence

A skill must show that it executed and improved a measurable outcome:

```text
demo_task_ids
execution_receipts
before_score
after_score
delta_score
sample_count
```

Kill gates:

```text
delta_score must be positive
after_score must be >= before_score
execution_receipts must not be empty
verifier_report_refs must not be empty
```

## Credit policy

Skill credit basis is stricter than generic contribution credit:

```text
settlement_currency = AEM_CREDIT
credit_basis = verified_skill_use
base_credit_micros
quality_multiplier_floor
quality_multiplier_cap
resale_allowed
```

Skill credit cannot be based on raw size, claimed cleverness, or uploaded text length.

## CreditLedger settlement

Accepted SkillReceipt now settles as:

```text
skill_mint
```

Skill-aware CreditLedger command:

```bash
python -m aem_poc.aem_credit_ledger_skill
python -m aem_poc.aem_credit_ledger_skill --check
make aem-credit-ledger
make aem-credit-ledger-check
```

Settlement law:

```text
valid SkillReceipt → skill_mint → contributor credit_account +AEM_CREDIT
invalid SkillReceipt → rejection → no skill_mint
```

## Receipt requirements

A product-grade skill requires:

```text
provenance_receipt
skill_execution_receipt
skill_delta_eval_receipt
operator_reality_gate_receipt
```

## Anti-distillation boundary

```text
no_unauthorized_competitor_distillation = true
allowed_teacher_policy_required = true
third-party model outputs require verified terms
```

## Validation laws

```text
No skill credit without verified_skill_use.
No skill credit without execution receipt.
No skill credit without positive delta.
No skill credit without verifier report.
No skill credit from unauthorized competitor distillation.
No third-party model outputs unless terms are verified.
No skill without kill criteria.
No SkillReceipt settlement without skill_mint event.
```

## Aggregate economy gate

`aem-network-economy-check` includes:

```text
aem-skill-receipts-check
aem-credit-ledger-check
```

So SkillReceipt is part of the product-grade economy foundation and the settlement path.

## Death

```text
skill remains only a generic contribution type without product-grade execution, verifier, and settlement boundaries.
```

Dead.

## Inheritance

```text
AEM skills are reusable executable operators that earn credits only through evidence-backed, verifier-checked measurable deltas and CreditLedger skill_mint settlement.
```

## Next pressure

```text
Add CreditTransferReceipt and CreditSpendAuthorization so skill-earned credits can be spent or transferred with nonce guards.
```
