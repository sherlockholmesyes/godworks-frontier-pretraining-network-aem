# AEM InferenceWorkReceipt design

wrong1: inference work earns credits because the host says it answered.
Death: self-report mints credits for fake work and cannot support resale or settlement.

wrong2: inference work earns credits only if the chain re-executes the model.
Death: on-chain model execution is too expensive, too slow, and leaks execution details.

Third: off-chain inference emits a signed InferenceWorkReceipt with task/expert/node binding, output commitment, cost envelope, duplicate-spend key, and verifier challenge surface.

Commands:

```bash
python -m aem_poc.aem_inference_receipts
python -m aem_poc.aem_inference_receipts --check
make aem-inference-receipts
make aem-inference-receipts-check
```

Schema:

```text
schemas/inference_work_receipt.schema.json
```

Code/tests:

```text
aem_poc/aem_inference_receipts.py
tests/test_aem_inference_receipts.py
```

Receipt binds:

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
work meter
prompt/output commitments
route_trace_id
nonce
challenge surface
duplicate spend guard
policy receipt requirements
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

Validation laws:

```text
receipt node_id must match NodeCard
receipt host_advertisement_id must match HostAdvertisement
receipt expert_id must match HostAdvertisement
credit_account must match NodeCard economic account
settlement_currency must be AEM_CREDIT
credit_charge_micros must match HostAdvertisement rate
spend_key must match task/expert/node/nonce
seen spend_key is rejected
challenge methods must be complete
policy must require inference_work_receipt and route_trace_receipt
metered cost cannot exceed charged credits
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
```

Death: inference credit settlement relies on self-report or impossible on-chain inference.

Inheritance: AEM inference economics must be receipt-backed, challengeable, and duplicate-spend guarded from the first code layer.

Next pressure: add CreditLedger settlement simulator that consumes contribution and inference receipts.
