# AEM Network Brick Ledger design

wrong1: blockchain + inference means the chain executes or verifies every inference directly.
Death: on-chain inference is too expensive, too slow, leaks topology/output, and cannot be the serving fabric for large experts.

wrong2: inference network means centralized accounting over volunteer hosts.
Death: central balances and opaque routing recreate a platform operator instead of a peer network.

Third: off-chain expert training/inference produces signed receipts; verifier challenges and policy gates convert receipts into transferable credits; the ledger settles credits without pretending that blockchain executes inference.

Command:

```bash
python -m aem_poc.aem_network_bricks
make aem-network-bricks
```

Generated ledger validation:

```bash
make aem-network-bricks-check
```

Optional checked-in JSON sync:

```bash
python -m aem_poc.aem_network_bricks --sync
make aem-network-bricks-sync
```

Machine schema:

```text
schemas/aem_network_brick_ledger.schema.json
```

Ledger status:

```text
brick_count: 11
closed_poc: 1
proto_brick: 4+
research_packet: 5+
```

Current network brick map:

```text
capability_capsule
node_identity_capacity
expert_host_registry
locality_quality_router
inference_work_receipt
training_work_receipt
credit_ledger_settlement
reward_pricing_function
anti_fraud_sybil_slashing
credit_market_exchange
privacy_sandbox_policy
network_governance_upgrade
```

Core economy:

```text
training and inference both produce receipts
receipts pass verifier/policy gates
accepted receipts mint credits
credits can be spent for inference or transferred/sold
larger/smarter/rarer/reliable experts earn more only through verified utility
nearest host wins only if capability, price, policy, and receipt quality pass
```

Non-negotiable boundary:

```text
The chain/ledger settles credit receipts.
The chain does not run model inference.
The network does not mint credits from self-reporting.
```

Each brick includes:

```text
wrong1 / death1
wrong2 / death2
Third
definition
node decomposition
primitive closure
minimal tests
kill criteria
next pressure
```

Open primitive classes:

```text
challengeable inference receipts
runtime cost meter
availability challenge
settlement finality rule
reward scarcity multiplier
anti-monopoly cap
collusion detector
private inference primitive
protocol migration receipt
bounded governance primitive
```

Death: the AEM economy is described as vibes instead of a primitive-closed brick map.

Inheritance: every network/economy claim must decompose into bricks, primitives, receipts, tests, and missing primitive research packets.

Next pressure: implement NodeCard + HostAdvertisement schemas as the first network proto-brick.
