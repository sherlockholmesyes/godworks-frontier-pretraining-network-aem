# AEM Missing Bricks and Tech Stack design

This file lists the protocol/technology bricks needed to make AEM/AEM work.

It is not a library shopping list. It separates:

```text
available external bricks
missing AEM-specific bricks
first PoC for each brick
kill gates
```

Existing useful directions:

```text
DiLoCo / OpenDiLoCo:
  low-communication distributed training

Petals:
  collaborative inference/fine-tuning precedent

QLoRA:
  4-bit frozen base + adapter training

SWARM:
  heterogeneous unreliable devices

INTELLECT-style permissionless training:
  untrusted worker verification

BitNet / native low-bit:
  experimental low-bit training direction

vLLM / SGLang / llama.cpp:
  serving/runtime engines
```

But there is no complete existing stack for:

```text
growing quantized expert mesh
with admission/router/verifier/distillation/economy
on consumer nodes
with receipt-backed credits
```

That is what AEM must build.

---

# 0. Main design

## wrong1

```text
Need to build a distributed trainer.
```

Death:

```text
A distributed trainer copies the corporate form: one run, one checkpoint, one training fabric.
```

## wrong2

```text
Need to build a marketplace of LoRAs/experts.
```

Death:

```text
A marketplace without router/admission/verifier becomes adapter spam.
```

## Third

```text
Need to build a protocol stack for growth of verified capabilities.
```

Protocol stack:

```text
Expert Capsule Protocol
Node Runtime
Router
Objective Verifier Mesh
Data Ledger
Training Recipes
Distillation Memory
Reputation / Credit Layer
Security / Privacy Layer
Open Gateway
```

---

# 1. Expert Capsule Protocol

## wrong1

```text
expert = LoRA file
```

Death:

```text
LoRA without manifest/eval/runtime/admission/receipts is only a mod.
```

## wrong2

```text
expert = separate model/API
```

Death:

```text
Then the mesh becomes thousands of unrelated chatbots.
```

## Third

```text
expert = capability capsule
```

Need to build:

```text
ExpertCard
ExpertArtifact
ExpertRuntimeContract
ExpertEvalReport
ExpertTrainingReceipt
ExpertSignature
```

Minimum fields:

```text
expert_id
base_model_hash
tokenizer_hash
compatible_core_version
expert_type
quantization
vram_min_gb
training_recipe
data_hashes
eval_delta
regression_delta
risk_scores
latency_profile
license
signature
```

Missing:

```text
Common ABI for pluggable LLM experts that can be trained, verified, routed, rewarded, and distilled.
```

First PoC:

```text
expert.card.json
adapter.safetensors / expert.gguf / runtime.json
eval_report.json
training_receipt.json
signature.txt
```

---

# 2. Node Runtime

## wrong1

```text
node = GPU that computes model chunks
```

Death:

```text
That is too low-level and ignores receipts, policy, training, verification, and routing.
```

## wrong2

```text
node = ordinary inference server
```

Death:

```text
Ordinary inference servers do not emit training receipts, verifier reports, or credit-eligible work proofs.
```

## Third

```text
node = worker-organ
```

Need daemon:

```text
aem-node
  profile GPU/VRAM/RAM/bandwidth
  serve expert
  train expert
  run verifier
  sign results
  report health
  accept canary traffic
```

External backends can be used:

```text
llama.cpp / GGUF for edge quantized inference
vLLM / SGLang for high-throughput serving
bitsandbytes / PEFT for QLoRA
container/sandbox backend for verifier jobs
```

AEM-specific missing part:

```text
single worker daemon that combines serving, training, verification, signatures, expert package loading, and mesh reporting.
```

First PoC:

```bash
aem node profile
aem node serve examples/code_patch_expert_card.json
aem node verify task.json
```

Current repo partial embodiment:

```text
schemas/node_card.schema.json
schemas/host_advertisement.schema.json
aem_poc/aem_network_cards.py
```

---

# 3. Quantized Expert Training Stack

## wrong1

```text
quantization = compress after training
```

Death:

```text
That is an inference optimization, not a growth mechanism.
```

## wrong2

```text
train full frontier in 4-bit on home GPUs immediately
```

Death:

```text
QLoRA-style training is adapter training over frozen low-bit base, not magic full frontier pretraining.
```

## Third

```text
low-bit training = modes for expert growth
```

Training modes:

```text
A. QLoRA adapter expert
B. continued-pretrain small expert
C. verifier/reward expert
D. distilled expert
E. native low-bit expert, BitNet-like
F. sparse low-bit expert
```

Missing:

```text
reproducible train_expert recipes for 12GB/16GB/24GB nodes that emit TrainingReceipt, not just weights.
```

First PoC:

```text
recipes/qlora_code_patch_7b.yaml
recipes/distill_verifier_3b.yaml
recipes/lowbit_expert_experimental.yaml
```

Kill gate:

```text
No eval_delta + receipt → not an expert, only an artifact.
```

---

# 4. Router

## wrong1

```text
router = token-level MoE gate
```

Death:

```text
Public internet cannot carry token hidden state for every layer without killing latency.
```

## wrong2

```text
router = manual plugin selector
```

Death:

```text
Manual selection makes a catalog, not a model.
```

## Third

```text
router = task-level immune scheduler
```

Needs:

```text
TaskClassifier
CapabilityIndex
ExpertRanker
TrafficCanary
FallbackPolicy
FusionPolicy
Cost/Latency/Trust score
```

Missing:

```text
forkable open router trained on public eval traces and canary traffic without becoming central power.
```

First PoC:

```text
router_v0:
  classify task
  filter compatible experts
  apply objective reports
  route top-k
  compare outputs
  emit trace
```

Current repo partial embodiment:

```text
schemas/route_trace.schema.json
aem_poc/trace_store.py
aem_poc/patch_gate_demo.py
```

---

# 5. Objective Verifier Mesh

## wrong1

```text
expert is good if it has attractive eval numbers
```

Death:

```text
Eval numbers can be faked, contaminated, overfit, or cherry-picked.
```

## wrong2

```text
one central evaluator decides admission
```

Death:

```text
That recreates OpenAI/Anthropic-style central control as a verifier monopoly.
```

## Third

```text
admission = independent objective gates
```

Verifier mesh types:

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

Missing:

```text
permissionless verifier protocol for expert admission under untrusted workers.
```

First PoC:

```text
verifier/code_patch:
  apply patch
  run tests in sandbox
  check diff size
  check no forbidden files touched
  emit AdmissionReport
```

Current repo partial embodiment:

```text
aem_poc/patch_gate_demo.py
aem_poc/evidence_pipeline.py
schemas/evidence_* schemas
```

---

# 6. Data Ledger

## wrong1

```text
data = download the internet
```

Death:

```text
Poisoning, copyright mess, PII, benchmark contamination, and duplicates.
```

## wrong2

```text
data = central golden corpus
```

Death:

```text
Central data control becomes central network control.
```

## Third

```text
data = content-addressed shards with provenance + eval impact
```

Need:

```text
DataShardManifest
SourceLicense
PII status
Dedup hashes
Contamination checks
UsedByExpert list
EvalImpact report
```

Missing:

```text
data ledger that links an expert to concrete shards and proves those shards improved capability.
```

First PoC:

```text
data_shard.card.json
dataset_hash
license
source_type
decontamination_report
experts_using_this_shard
eval_delta_after_training
```

---

# 7. Distillation Memory

## wrong1

```text
keep adding experts forever
```

Death:

```text
The mesh becomes large, expensive, redundant, and chaotic.
```

## wrong2

```text
periodically merge everything into one monolith
```

Death:

```text
That destroys distributed expert growth and returns to checkpoint centrality.
```

## Third

```text
successful traces become distillation memory
```

Need to store:

```text
task
router decision
expert outputs
verifier results
winning answer
failure reasons
cost/latency
distillation label
```

Then train:

```text
better router
better verifier
merged expert
new core generation
```

Missing:

```text
trace format that turns successful mesh behavior into training data.
```

Current partial embodiment:

```text
route_trace.jsonl
TraceStore
compact/replay/evidence pipeline
```

First PoC:

```text
TraceStore:
  route_trace.jsonl
  verifier_trace.jsonl
  distill_dataset_builder.py
```

---

# 8. Expert Dedup / Conflict Map

## wrong1

```text
more experts = more intelligence
```

Death:

```text
Ten duplicate adapters are not ten capabilities.
```

## wrong2

```text
keep only the single best expert
```

Death:

```text
Different experts can be useful in different niches and constraints.
```

## Third

```text
maintain a capability coverage map
```

Need:

```text
capability embedding
expert similarity
domain coverage
conflict graph
regression graph
specialization map
```

Missing:

```text
capability topology for experts.
```

First PoC:

```text
duplicate_score = output similarity + eval overlap + data overlap
```

---

# 9. Reputation / Credit Layer

## wrong1

```text
people will burn GPU for ideology
```

Death:

```text
Some will, but mass network reliability requires economic incentives.
```

## wrong2

```text
start with a token
```

Death:

```text
That attracts crypto-grift before useful network work exists.
```

## Third

```text
start with compute credits + reputation, backed by receipts
```

Need:

```text
node reputation
expert reputation
verifier reputation
credit balance
anti-sybil score
slashing for fake reports
traffic rewards
```

Current repo embodiment:

```text
AEM_CREDIT
NodeCard economic_policy
HostAdvertisement offer
InferenceWorkReceipt
KnowledgeContributionReceipt
CreditLedger settlement simulator
```

Missing:

```text
non-scam compute-credit economy for open expert mesh:
transfers, spend authorizations, slashing, market orders, reputation.
```

First PoC:

```text
credits ledger:
  node_id
  verified_jobs_done
  accepted_experts
  failed_admissions
  earned_credits
  spent_credits
```

---

# 10. Security / Privacy Layer

## wrong1

```text
permissionless means trust everyone
```

Death:

```text
Fraud, data leakage, prompt theft, fake experts, and Sybil nodes dominate.
```

## wrong2

```text
security means close the network
```

Death:

```text
Closed network loses the open growth advantage.
```

## Third

```text
permissionless edge + staged trust
```

Need:

```text
signed expert artifacts
sandboxed verifier execution
private-task routing policy
local-only mode
redacted task packets
backdoor probes
canary prompts
rate limits
node quarantine
```

Privacy law:

```text
private user data must not go to unknown worker without explicit policy.
```

First PoC:

```text
privacy_level:
  public
  redacted
  trusted_nodes_only
  local_only
```

---

# 11. Low-Communication Expert Growth

## wrong1

```text
DiLoCo solves everything
```

Death:

```text
Low-communication distributed training helps, but it is not the whole expert-growth protocol.
```

## wrong2

```text
AEM does not need distributed training at all
```

Death:

```text
Serious expert growth will need asynchronous and multi-node training modes.
```

## Third

```text
DiLoCo/SWARM-style methods become training modes inside AEM
```

Need:

```text
expert-local pretraining
island training
asynchronous expert update
outer optimizer for expert family
periodic checkpoint merge
```

Missing:

```text
AEM-specific expert family training where nodes grow compatible expert families rather than one monolith.
```

First PoC:

```text
train one small expert on 2 unreliable nodes
compare:
  local-only
  async merge
  DiLoCo-like periodic merge
```

---

# 12. Open Gateway

## wrong1

```text
backend is enough
```

Death:

```text
Users need a familiar API surface.
```

## wrong2

```text
UI is enough
```

Death:

```text
UI without protocol is a toy.
```

## Third

```text
OpenAI-compatible gateway + local mesh protocol
```

Need:

```text
/v1/chat/completions
/v1/embeddings
/v1/experts
/v1/route
/v1/verify
/v1/train
/v1/receipts
/v1/credits
```

Missing:

```text
standard API where AEM looks like an LLM provider but internally routes through expert mesh.
```

First PoC:

```text
aem-router-server:
  OpenAI-compatible endpoint
  internal route trace
  selected expert metadata
  InferenceWorkReceipt
```

---

# Correct implementation order

## Stage 0 — Protocol spine

Goal:

```text
turn repo from PoC into AEM specification
```

Build:

```text
ExpertCard v1
TaskPacket v1
AdmissionReport v1
RouteTrace v1
TrainingReceipt v1
DataShardManifest v1
```

Objective gate:

```text
any expert without card/receipt/report is not part of the network
```

## Stage 1 — Local runnable loop

Goal:

```text
one computer, no distribution, full cycle
```

Build:

```text
load ExpertCard from JSON
validate schema
route task
run verifier
write route_trace.jsonl
run unittest fixture
```

Objective gate:

```text
if route/admission cannot be reproduced locally, mesh is premature
```

## Stage 2 — Code Patch Expert MVP

Goal:

```text
first objectively verified expert
```

Build:

```text
synthetic bug repo fixture
task packet: issue + failing test
expert reply: patch
verifier: apply patch + run tests
admission: pass/fail + diff constraints
```

Objective gate:

```text
expert useful only if it fixes held-out tests
```

## Stage 3 — 12GB QLoRA Expert Training

Goal:

```text
first consumer-GPU training recipe
```

Build:

```text
qlora_code_patch_7b.yaml
train script
eval before/after
TrainingReceipt
ExpertCard
```

Objective gate:

```text
no eval_delta + receipt → artifact, not expert
```

## Stage 4 — Node Daemon

Goal:

```text
machine becomes network node
```

Build:

```text
aem node profile
aem node serve
aem node verify
aem node train
signed node reports
```

Objective gate:

```text
node must prove work without receiving instant trust
```

## Stage 5 — Multi-node LAN Mesh

Goal:

```text
2–3 machines, local network, real routing
```

Build:

```text
registry server
node heartbeat
task dispatch
verifier dispatch
signed replies
```

Objective gate:

```text
if one node falls, the task must not break the whole mesh
```

## Stage 6 — Verifier Mesh

Goal:

```text
expert is checked by someone other than author
```

Build:

```text
independent verifier nodes
repeated verification
disagreement handling
quarantine policy
```

Objective gate:

```text
self-reported eval does not admit expert
```

## Stage 7 — Router Learning

Goal:

```text
router stops being manual if/else
```

Build:

```text
route traces
success labels
exploration/canary traffic
expert ranking model
fallback policy
```

Objective gate:

```text
router must explain why expert received traffic
```

## Stage 8 — Distillation Memory

Goal:

```text
network learns from successful routes
```

Build:

```text
trace store
distill dataset builder
train router v2
train merged/domain expert
```

Objective gate:

```text
successful trace becomes training material
```

## Stage 9 — Public Mesh Alpha

Goal:

```text
people with 12–16GB GPU can connect
```

Build:

```text
node identity
public registry
credits/reputation
rate limits
privacy levels
OpenAI-compatible gateway
```

Objective gate:

```text
unknown node does not receive private tasks
```

## Stage 10 — Low-bit Native Research Branch

Goal:

```text
go beyond QLoRA into new low-bit experts
```

Build:

```text
BitNet-like small expert experiments
sparse low-bit expert experiments
compare against QLoRA experts
measure quality/VRAM/latency
```

Objective gate:

```text
low-bit expert admitted only if it wins quality/cost, not because it sounds interesting
```

---

# Top 10 missing bricks

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
10. Reputation / Credit layer
```

Main missing brick:

```text
admission-controlled growth protocol
```

Not:

```text
just a model
just a trainer
just a marketplace
```

## Next pressure

```text
Implement AEMModelState + ExpertArtifact + TrainingReceipt.
Then prove that AEM can accept an expert only after objective verifier report,
not because the manifest is attractive.
```
