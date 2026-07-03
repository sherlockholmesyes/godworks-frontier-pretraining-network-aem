# AEM SkillReceipt Index Addendum design

This addendum records the product-grade SkillReceipt layer added after the architecture packet index.

## design

### wrong1

```text
Skill stays only as contribution_type=skill inside generic contribution receipts.
```

Death:

```text
A product-grade skill needs executable contract, execution receipts, delta evidence, verifier report refs, and stricter credit basis.
```

### wrong2

```text
Skill is a private claim that earns credits by contributor reputation.
```

Death:

```text
Reputation alone cannot prove the skill executes, improves outcomes, or can be reused by the network.
```

### Third

```text
SkillReceipt = executable skill contract + execution evidence + measurable delta + verifier refs + AEM_CREDIT policy + skill_mint settlement.
```

## Files

```text
schemas/skill_receipt.schema.json
aem_poc/aem_skill_receipts.py
aem_poc/aem_credit_ledger_skill.py
tests/test_aem_skill_receipts.py
tests/test_aem_credit_ledger_skill.py
docs/AEM_SKILL_RECEIPT_DESIGN.md
```

## Commands

```bash
python -m aem_poc.aem_skill_receipts
python -m aem_poc.aem_skill_receipts --check
python -m aem_poc.aem_credit_ledger_skill --check
make aem-skill-receipts
make aem-skill-receipts-check
make aem-credit-ledger-check
make aem-network-economy-check
```

## Economy gate

```text
aem-network-economy-check includes aem-skill-receipts-check and aem-credit-ledger-check
```

## Required product-grade fields

```text
skill_contract
execution_evidence
evaluation
credit_policy
anti_distillation
receipt_requirements
verifier_report_refs
```

## Kill gates

```text
no verified_skill_use credit basis → reject
no execution receipt → reject
no positive delta → reject
no verifier report → reject
unauthorized competitor distillation → reject
third-party outputs without verified terms → reject
invalid skill receipt → no skill_mint
```

## Settlement

```text
valid SkillReceipt → skill_mint → contributor AEM_CREDIT balance
invalid SkillReceipt → rejection → no skill_mint
```

## Next pressure

```text
Add CreditTransferReceipt and CreditSpendAuthorization so skill-earned credits can be spent or transferred with nonce guards.
```
