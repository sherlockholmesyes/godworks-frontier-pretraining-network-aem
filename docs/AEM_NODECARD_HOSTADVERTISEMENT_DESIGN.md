# AEM NodeCard + HostAdvertisement design

wrong1: node = wallet address.
Death: a wallet cannot expose GPU capacity, locality bucket, uptime window, sandbox policy, earning roles, credit account, or receipt requirements.

wrong2: host advertisement = URL saying an expert is online.
Death: a URL does not bind expert id, node capacity, credit price, payment class, task policy, or challengeable receipt requirements.

Third: NodeCard binds host identity, capacity, locality, policy, and economic floor; HostAdvertisement binds a concrete expert offer to that node with credit price and required work receipts.

Commands:

```bash
python -m aem_poc.aem_network_cards
python -m aem_poc.aem_network_cards --check
make aem-network-cards
make aem-network-cards-check
```

Schemas:

```text
schemas/node_card.schema.json
schemas/host_advertisement.schema.json
```

Code:

```text
aem_poc/aem_network_cards.py
tests/test_aem_network_cards.py
```

NodeCard includes:

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

Economic foundation in NodeCard:

```text
credit_account
settlement_currency = AEM_CREDIT
earning_roles
min_inference_credit_rate_micros
min_training_credit_rate_micros
min_verification_credit_rate_micros
collateral_required_micros
resale_allowed
```

HostAdvertisement includes:

```text
advertisement_id
node_id
expert_id
expert_card_hash
locality_bucket
offer roles
accepted payment
credit rates
availability
policy
receipt_requirements
signature
```

Validation laws:

```text
wallet-only node is invalid
host ad node_id must match NodeCard
host ad locality bucket must match NodeCard
expert_id must be listed in NodeCard.advertised_experts
offer roles must be subset of NodeCard roles
offer rates cannot be below NodeCard minimum rates
AEM_CREDIT must be accepted payment
role receipts are mandatory for earning
advertised task classes must be subset of NodeCard host policy
advertised sandbox profile must be offered by NodeCard
```

Economy boundary:

```text
No earning role without receipt requirement.
No advertised work without credit price.
No credit settlement without AEM_CREDIT account.
No host offer outside node capacity/policy.
```

Death: AEM economy is described as vibes instead of being embedded in code-level network cards.

Inheritance: the network must treat economics as protocol shape, not as a future UI/business layer.

Next pressure: implement InferenceWorkReceipt schema with duplicate-spend guard and challenge surface.
