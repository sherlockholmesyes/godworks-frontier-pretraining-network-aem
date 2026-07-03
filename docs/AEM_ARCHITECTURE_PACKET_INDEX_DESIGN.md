# AEM Architecture Packet Index design

This file is the index for the current AEM/AEM architecture packet in the repo.

It exists because the architecture is now split across executable specs, unified maps, economics, roadmap, and missing-brick documents.

## design

### wrong1

```text
Everything should live in one huge README.
```

Death:

```text
A single README becomes unreadable and cannot separate models, training, inference, economics, evidence, and missing primitives.
```

### wrong2

```text
Everything can be scattered across many docs without an index.
```

Death:

```text
The state becomes unrecoverable after reset; next agent or contributor cannot find the current architecture spine.
```

### Third

```text
Architecture packet = multiple focused files + one index.
```

## Core architecture docs

```text
docs/AEM_UNIFIED_ARCHITECTURE_DESIGN.md
  Single map of models, training, inference, routing, economy, receipts, settlement, evidence, missing primitives.

README.md
  Repo entrypoint and command surface.

docs/AEM_PRODUCT_GRADE_ROADMAP_DESIGN.md
  Roadmap from current PoC to product-grade inference/training/economy network.

docs/AEM_ECONOMIC_MODEL_DESIGN.md
  Full receipt-backed AEM_CREDIT economic model.
```

## Newly loaded AEM packet docs

```text
docs/AEM_FRONTIER_EXPERT_MESH_DESIGN.md
  Accretive Expert Mesh architecture: core + router + experts + verifiers + data ledger + distillation memory.

docs/AEM_MISSING_BRICKS_TECH_STACK_DESIGN.md
  Missing protocol bricks and implementation order: Expert Capsule ABI, Node Runtime, Router, Verifier Mesh, Data Ledger, Distillation Memory, Credit/Reputation, privacy, gateway.
```

## Network/economy code-level docs

```text
docs/AEM_CREDIT_ROUTED_INFERENCE_NETWORK_DESIGN.md
  Expanded plan for the credit-routed AEM inference/training network: host experts, earn/spend/sell credits, nearest adequate host routing, blockchain+inference boundary.

docs/AEM_NETWORK_BRICKS_DESIGN.md
  Primitive-closed network brick ledger.

docs/AEM_NODECARD_HOSTADVERTISEMENT_DESIGN.md
  NodeCard + HostAdvertisement proto-brick.

docs/AEM_BOOTSTRAP_GROWTH_DESIGN.md
  Human-owned/licensed knowledge/skill/data/eval/curriculum/operator contribution receipts.

docs/AEM_INFERENCE_WORK_RECEIPT_DESIGN.md
  InferenceWorkReceipt with duplicate-spend guard and challenge surface.

docs/AEM_CREDIT_LEDGER_SETTLEMENT_DESIGN.md
  CreditLedger settlement simulator.

docs/AEM_NETWORK_ECONOMY_CHECK_DESIGN.md
  Aggregate network/economy check target.
```

## Evidence docs

```text
docs/EVIDENCE_ARTIFACT_INDEX.md
docs/evidence_artifact_index.json
docs/EVIDENCE_DOWNLOAD_VERIFY.md
docs/EVIDENCE_LOCAL_CI_DESIGN.md
docs/EVIDENCE_STATUS_DESIGN.md
docs/evidence_status.example.json
```

## Current executable command surface

Evidence:

```bash
make evidence-local-ci
make evidence-docs-check
make evidence-docs-sync
```

Network/economy:

```bash
make aem-network-bricks-check
make aem-network-cards-check
make aem-bootstrap-growth-check
make aem-inference-receipts-check
make aem-credit-ledger-check
make aem-network-economy-check
```

Architecture docs just added:

```text
docs/AEM_FRONTIER_EXPERT_MESH_DESIGN.md
docs/AEM_MISSING_BRICKS_TECH_STACK_DESIGN.md
docs/AEM_CREDIT_ROUTED_INFERENCE_NETWORK_DESIGN.md
docs/AEM_ARCHITECTURE_PACKET_INDEX_DESIGN.md
```

## Inheritance

```text
AEM/AEM is not one checkpoint and not a LoRA marketplace.
It is admission-controlled expert accretion:
Core + Router + ExpertCapsules + VerifierMesh + DataLedger + DistillationMemory + Receipts + CreditLedger.
```

## Next pressure

```text
Implement RouterDecision + CreditSpendAuthorization so user tasks can be budgeted and routed to the nearest adequate verified expert host.
```
