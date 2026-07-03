# AEM Missing Bricks — design Map

This document defines the missing technologies required for AEM to become a working accretive pretraining network rather than a manifesto.

```text
AEM = Accretive Expert Mesh
```

## Root cut

### Rejected option A

```text
We need a distributed trainer.
```

Death: a trainer alone copies the corporate shape — one run, one checkpoint, one owner of the training fabric.

### Rejected option B

```text
We need a marketplace of LoRA/expert files.
```

Death: a marketplace without admission, routing, verification, and distillation becomes an adapter landfill.

### Third

```text
We need a protocol stack for verified capability growth.
```

The missing unit is not a model file. The missing unit is a checked growth event:

```text
new expert → training receipt → verifier report → canary routing → trace memory → distillation
```

---

## 1. Expert Capsule ABI

### Rejected option A

```text
expert = LoRA file
```

Death: a LoRA file without a contract is just a mod.

### Rejected option B

```text
expert = separate model/API
```

Death: thousands of separate bots do not form a model.

### Third

```text
expert = capability capsule with an admission contract
```

Needed bricks:

```text
ExpertCard
ExpertArtifact
ExpertRuntimeContract
ExpertEvalReport
ExpertTrainingReceipt
ExpertSignature
```

First implementation target:

```text
expert.card.json
adapter.safetensors / expert.gguf / runtime.json
eval_report.json
training_receipt.json
signature.txt
```

---

## 2. Node Runtime

### Rejected option A

```text
node = GPU shard for one big model
```

Death: this pushes public internet into per-token tensor transport.

### Rejected option B

```text
node = ordinary inference server
```

Death: it cannot train, verify, sign work, or participate in admission.

### Third

```text
node = worker-organ
```

Needed daemon:

```text
aem-node profile
aem-node serve expert
aem-node train expert
aem-node verify task
aem-node sign result
aem-node report health
```

---

## 3. Quantized Expert Training Stack

### Rejected option A

```text
quantization = post-training compression only
```

Death: this helps inference but does not create a growth mechanism.

### Rejected option B

```text
full frontier training can be done immediately in 4-bit on home GPUs
```

Death: this confuses adapter training with full monolithic pretraining.

### Third

```text
low-bit training = multiple expert growth modes
```

Needed modes:

```text
QLoRA adapter expert
continued-pretrain small expert
verifier/reward expert
distilled expert
native low-bit experimental expert
sparse low-bit expert
```

Needed output:

```text
TrainingReceipt + ExpertCard + EvalReport
```

---

## 4. Task-Level Router

### Rejected option A

```text
router = token-level MoE gate
```

Death: remote hidden states over public internet are a latency trap.

### Rejected option B

```text
router = manual plugin picker
```

Death: a catalog is not a model.

### Third

```text
router = task-level immune scheduler
```

Needed bricks:

```text
TaskClassifier
CapabilityIndex
ExpertRanker
TrafficCanary
FallbackPolicy
FusionPolicy
Cost/Latency/Trust scoring
RouteTrace writer
```

---

## 5. Objective Verifier Mesh

### Rejected option A

```text
expert is useful if its manifest says so
```

Death: self-reported evals can be fake or contaminated.

### Rejected option B

```text
one central evaluator should decide admission
```

Death: this recreates a corporate gatekeeper.

### Third

```text
admission = independent objective gates
```

Needed verifiers:

```text
target eval verifier
general regression verifier
duplicate detector
backdoor/trigger detector
latency/cost verifier
sandbox verifier
data contamination verifier
signature/repro verifier
```

---

## 6. Data Ledger

### Rejected option A

```text
data = download the internet
```

Death: poisoning, PII, copyright mess, and benchmark contamination.

### Rejected option B

```text
data = one central blessed corpus
```

Death: central data control restores central model control.

### Third

```text
data = content-addressed shards with provenance and eval impact
```

Needed bricks:

```text
DataShardManifest
SourceLicense
PII status
Dedup hashes
Contamination report
UsedByExpert list
EvalImpact report
```

---

## 7. Distillation Memory

### Rejected option A

```text
just add experts forever
```

Death: the mesh bloats into chaos.

### Rejected option B

```text
periodically merge everything into one monolith
```

Death: the mesh loses its distributed growth form.

### Third

```text
successful routes become distillation memory
```

Needed trace fields:

```text
task
router decision
expert outputs
verifier reports
winning answer
failure reasons
cost/latency
distillation label
```

---

## 8. Expert Dedup / Conflict Map

### Rejected option A

```text
more experts = more intelligence
```

Death: duplicate adapters are not new capability.

### Rejected option B

```text
keep only the single best expert
```

Death: niche specialization gets destroyed.

### Third

```text
build a capability topology
```

Needed bricks:

```text
capability embedding
expert similarity score
domain coverage map
conflict graph
regression graph
specialization map
```

---

## 9. Reputation / Credit Layer

### Rejected option A

```text
people will burn GPUs for the idea forever
```

Death: volunteer compute does not scale reliably.

### Rejected option B

```text
launch a token first
```

Death: token-first turns the project into a grift magnet.

### Third

```text
start with compute credits and reputation
```

Needed bricks:

```text
node reputation
expert reputation
verifier reputation
credit balance
anti-sybil score
slashing/quarantine for fake reports
traffic rewards
```

---

## 10. Security / Privacy Layer

### Rejected option A

```text
permissionless means trust everyone
```

Death: adversarial workers poison the mesh.

### Rejected option B

```text
security means close the network
```

Death: closed trust kills the open mesh.

### Third

```text
permissionless edge + staged trust
```

Needed bricks:

```text
signed expert artifacts
sandboxed verifier execution
privacy-aware routing
local-only mode
redacted task packets
canary prompts
node quarantine
rate limits
```

---

## Compact missing-brick list

```text
1. Expert Capsule ABI
2. TrainingReceipt format
3. Task-level Router
4. Objective Verifier Mesh
5. DataShard Ledger
6. Code Patch sandbox verifier
7. 12GB QLoRA training recipe
8. RouteTrace / Distillation Memory
9. Node daemon with signatures
10. Reputation/Credit layer
```

## Next pressure

```text
fake expert claims + real verifier rejects it
real expert passes small sandbox test
route trace is written to disk
```
