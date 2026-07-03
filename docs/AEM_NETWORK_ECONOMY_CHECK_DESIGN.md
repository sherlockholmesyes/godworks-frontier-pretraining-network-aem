# AEM Network Economy Check design

wrong1: economy checks are separate optional commands.
Death: AEM economy stays fragmented and can regress while individual modules still look valid.

wrong2: economy checks belong inside evidence-local-ci.
Death: evidence-local-ci is an artifact/evidence gate, not the network economy foundation gate.

Third: aem-network-economy-check runs the network/economy foundation gates together while staying separate from evidence-local-ci.

Command:

```bash
make aem-network-economy-check
```

Gate order:

```text
aem-network-bricks-check
aem-network-cards-check
aem-bootstrap-growth-check
aem-skill-receipts-check
aem-inference-receipts-check
aem-credit-ledger-check
```

Covered bricks:

```text
AEM network brick ledger
NodeCard + HostAdvertisement
Bootstrap growth contribution receipts
Product-grade SkillReceipt
InferenceWorkReceipt duplicate-spend/challenge surface
CreditLedger settlement simulator
```

Boundary:

```text
evidence-local-ci proves trace/evidence artifact integrity
aem-network-economy-check proves network/economy protocol shape
```

Economic law:

```text
No credit without receipt.
No receipt without provenance/policy binding.
No skill credit without execution evidence and verifier report.
No inference credit without duplicate-spend guard and challenge surface.
No growth credit from unauthorized competitor distillation.
No balance change without a settlement event.
```

Files:

```text
Makefile
schemas/skill_receipt.schema.json
schemas/inference_work_receipt.schema.json
schemas/credit_ledger_settlement.schema.json
aem_poc/aem_skill_receipts.py
aem_poc/aem_inference_receipts.py
aem_poc/aem_credit_ledger.py
tests/test_aem_skill_receipts.py
tests/test_aem_inference_receipts.py
tests/test_aem_credit_ledger.py
tests/test_aem_network_economy_target.py
README.md
```

Death: AEM economy is described as vibes instead of a primitive-closed code-level gate.

Inheritance: network economics must be executable at protocol level from the start, not patched later as business logic.

Next pressure: wire accepted SkillReceipt into CreditLedger contribution minting as its own event type: skill_mint.
