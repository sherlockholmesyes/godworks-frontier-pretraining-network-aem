# AEM CreditLedger Settlement design

wrong1: credits are just a centralized balance table.
Death: central balances recreate a platform operator and do not prove why credits were minted or transferred.

wrong2: every inference/payment must be an on-chain execution.
Death: per-inference chain execution is too slow and expensive for expert serving.

Third: CreditLedger consumes signed contribution, skill, and inference receipts, applies policy/challenge/duplicate-spend gates, then emits deterministic AEM_CREDIT settlement events.

Commands:

```bash
python -m aem_poc.aem_credit_ledger_skill
python -m aem_poc.aem_credit_ledger_skill --check
make aem-credit-ledger
make aem-credit-ledger-check
make aem-network-economy-check
```

Schema:

```text
schemas/credit_ledger_settlement.schema.json
```

Code/tests:

```text
aem_poc/aem_credit_ledger.py
aem_poc/aem_credit_ledger_skill.py
tests/test_aem_credit_ledger.py
tests/test_aem_credit_ledger_skill.py
```

Settlement event types:

```text
contribution_mint
skill_mint
inference_debit
inference_host_credit
```

Contribution settlement:

```text
KnowledgeContributionReceipt / Data / Eval / Curriculum / Operator
→ validate provenance, anti-distillation, credit policy, required receipts
→ contribution_mint AEM_CREDIT to contribution credit_account
```

Skill settlement:

```text
SkillReceipt
→ validate skill contract, execution evidence, positive delta, verifier refs, anti-distillation policy
→ skill_mint AEM_CREDIT to skill credit_account
```

Inference settlement:

```text
InferenceWorkReceipt
→ validate NodeCard + HostAdvertisement binding
→ require closed challenge window
→ reject seen spend_key
→ debit payer account
→ credit host account
```

Supply rule:

```text
contribution_mint and skill_mint increase net supply
inference_debit + inference_host_credit transfers existing credits and has zero net supply delta
```

Duplicate-spend guard:

```text
seen spend_key is rejected
spend_key = task_hash | expert_id | node_id | nonce
```

Rejection examples:

```text
invalid contribution provenance
invalid skill delta or missing verifier report
open challenge window
duplicate spend key
bad host advertisement binding
wrong credit charge
missing challenge surface
```

Aggregate gate:

```text
aem-network-economy-check includes aem-credit-ledger-check
```

Death: AEM credits are described as vibes instead of deterministic receipt settlement.

Inheritance: no AEM_CREDIT balance change without a receipt, event, account, policy reason, and replayable settlement report.

Next pressure: add CreditTransferReceipt and CreditSpendAuthorization so skill-earned credits can be spent or transferred with nonce guards.
