# AEM Frontier Expert Mesh design

This file captures the AEM/AEM model architecture as a growing expert ecosystem, not a centralized dense checkpoint and not a naive internet-sharded MoE.

Working name:

```text
AEM = Accretive Expert Mesh
```

Core calculation:

```text
frontier_model(t) = core(t)
                  + router(t)
                  + expert_set(t)
                  + verifier_set(t)
                  + data_ledger(t)
                  + distillation_memory(t)
```

## 0. Root cut

### wrong1

```text
MoE = a huge model split into experts inside one datacenter.
```

Death:

```text
This is still the corporate architecture: one checkpoint, one training run, one owner, one router/training fabric.
```

### wrong2

```text
MoE = a pile of home GPUs, each holding a random layer shard.
```

Death:

```text
If each token hidden state crosses the public internet, latency and instability kill the system.
```

### Third

```text
MoE becomes a protocol for capability growth.
```

An expert is not a remote layer. An expert is a capability capsule that can be:

```text
trained locally
verified externally
connected to a router
rewarded with traffic
retired if bad
distilled into future generations
replaced by better experts
```

## 1. Global model state

```text
GLOBAL_MODEL_STATE(t) =
  CORE(t)
  + ROUTER(t)
  + EXPERT_SET(t)
  + VERIFIER_SET(t)
  + DATA_LEDGER(t)
  + DISTILLATION_MEMORY(t)
```

This is not one checkpoint. It is a growing organism where frontier capability emerges from verified expert accretion.

## 2. CORE

### wrong1

```text
Core must be a giant frontier monolith.
```

Death:

```text
Then AEM depends on the same corporate scale and control plane it tries to escape.
```

### wrong2

```text
Core is unnecessary; experts are enough.
```

Death:

```text
Without shared tokenizer, task protocol, latent interface, and router signals, experts cannot form a system.
```

### Third

```text
Core = minimal shared nervous trunk.
```

Core v0:

```text
CORE:
  tokenizer
  shared embedding/latent protocol
  small/medium base LLM
  common task protocol
  router interface
  verifier interface
  distillation target
```

Core does not have to be the smartest part. It has to be compatible and stable.

## 3. Expert Capsule

### wrong1

```text
expert = LoRA file
```

Death:

```text
A LoRA without admission, eval, manifest, runtime contract, and receipts is just a mod file.
```

### wrong2

```text
expert = standalone model/API
```

Death:

```text
Then the network becomes thousands of unrelated chatbots.
```

### Third

```text
expert = verified capability with a connection contract.
```

Expert capsule:

```text
EXPERT_CAPSULE:
  manifest.json
  weights / adapter / quantized expert
  training recipe
  data shard hashes
  eval report
  license
  signature
  runtime endpoint
```

Minimal ExpertCard:

```json
{
  "expert_id": "...",
  "base_model_hash": "...",
  "expert_type": "code_patch | math | verifier | domain | planner | memory | critic",
  "quantization": "4bit_nf4 | int8 | bitnet | fp16",
  "vram_min_gb": 12,
  "training_objective": "...",
  "data_hashes": ["..."],
  "eval_suites": ["..."],
  "eval_delta": {},
  "negative_eval_delta": {},
  "latency_profile": {},
  "license": "...",
  "signature": "..."
}
```

Current repo embodiment:

```text
schemas/expert_card.schema.json
schemas/task_packet.schema.json
schemas/route_trace.schema.json
aem_poc/patch_gate_demo.py
aem_poc/e2e_gate_demo.py
```

## 4. Quantized training layer

### wrong1

```text
quantization = compress the model after training.
```

Death:

```text
That helps inference, but it does not create a distributed frontier growth mechanism.
```

### wrong2

```text
full frontier pretraining can immediately happen in 4-bit on home GPUs.
```

Death:

```text
QLoRA-style training is powerful, but classic QLoRA trains adapters over a frozen 4-bit base; it is not full-parameter frontier pretraining of a giant monolith.
```

### Third

```text
train new quantized/adapted experts instead of retraining the whole monolith.
```

Training modes:

```text
MODE A — QLoRA expert
  frozen 4-bit base
  train LoRA / adapter / expert head

MODE B — continued-pretrain small expert
  small model/expert trained on domain corpus

MODE C — native low-bit expert
  BitNet-like / ternary / 1.58-bit experimental expert

MODE D — verifier expert
  trained to judge, test, reject, route

MODE E — distillation expert
  trained from traces of many successful experts
```

Native low-bit training is a research branch, not a magic proof of frontier quality. It is valuable because it may lower the cost floor for expert creation.

## 5. Router as central organ

### wrong1

```text
router = token-level MoE gate over the internet
```

Death:

```text
Remote per-token hidden-state routing is latency death.
```

### wrong2

```text
router = manual plugin selector
```

Death:

```text
Then there is no model, only a directory.
```

### Third

```text
router = task-level immune scheduler.
```

The router moves:

```text
task packets
candidate answers
patches
proof attempts
plans
critic/verifier jobs
distillation traces
```

Not:

```text
hidden state for every token in every layer
```

Router v0:

```python
def route(task_packet):
    capabilities = classify_task(task_packet)
    candidates = expert_registry.search(capabilities)
    ranked = rank_by_score_latency_trust(candidates)
    outputs = call_top_k(ranked)
    verified = verifier_mesh.check(outputs)
    return fuse_or_select(verified)
```

Router law:

```text
Across the internet, send task packets, candidate answers, verifier scores, and adapter deltas.
Do not send token hidden states as the normal path.
```

## 6. Verifier Mesh

### wrong1

```text
expert is useful if it claims it is useful
```

Death:

```text
Self-report creates fake quality and fake credit.
```

### wrong2

```text
one central evaluator admits experts
```

Death:

```text
That brings back the corporation through a smaller door.
```

### Third

```text
expert utility = independent objective gates.
```

objective gates for admission:

```text
1. target eval improves
2. general eval does not regress past threshold
3. expert is not duplicate of existing expert
4. no obvious backdoor / prompt trigger
5. latency/cost is justified
6. training recipe is reproducible or reputation-trusted
7. multiple verifier nodes confirm the result
8. expert receives small canary traffic first, not power
```

First objective domain:

```text
code_patch_expert → unit tests in sandbox
```

## 7. Growth Loop

This is the AEM version of frontier pretraining.

```text
while true:
  1. new expert is created
  2. local node trains it
  3. expert publishes manifest + weights + eval claims
  4. verifier mesh checks claims
  5. router gives canary traffic
  6. stable useful expert receives more traffic
  7. successful traces enter distillation memory
  8. new router/core/expert generation is trained
```

Old frontier:

```text
one training run → one checkpoint
```

AEM frontier:

```text
many local training events → admission → routing → distillation → new capability layer
```

## 8. Data Ledger

### wrong1

```text
data = download the internet
```

Death:

```text
Poisoning, copyright risk, PII, duplicates, contamination, and benchmark leakage.
```

### wrong2

```text
data = centrally approved golden corpus
```

Death:

```text
That reintroduces centralized authority.
```

### Third

```text
data = versioned shards with provenance and eval impact.
```

DataShard:

```json
{
  "shard_id": "...",
  "domain": "code | math | law | biology | russian | hebrew | ...",
  "source_type": "...",
  "license": "...",
  "dedup_hashes": ["..."],
  "pii_status": "cleaned | unknown | blocked",
  "contamination_checks": ["..."],
  "used_by_experts": ["..."],
  "eval_impact": {}
}
```

Expert without data lineage can run locally but should not receive high trust in the shared router.

## 9. 12–16GB GPU role

A small node is not a bad H100. It is a different organ.

```text
12GB node:
  7B/8B quantized inference
  QLoRA small expert
  verifier tasks
  code test runner
  data cleaning
  embedding/rerank
  rollout generation
  small domain continued-pretrain

16GB node:
  longer context
  larger adapter
  constrained 14B quantized inference/training
  verifier + expert serving

24GB+ node:
  heavy expert training
  multi-expert serving
  distillation jobs
```

## 10. MVP architecture

Do not start with universal general intelligence. Start with a domain where verifier truth is objective.

First domain:

```text
CODE EXPERT MESH
```

MVP:

```text
CORE:
  open 7B/14B coder model

EXPERT TYPE:
  code_patch_expert

NODE:
  12–16GB GPU, QLoRA adapter training

TASK:
  small GitHub issues / bugfix tasks

VERIFIER:
  run tests in sandbox

ROUTER:
  call expert only for coding/patch tasks

ADMISSION:
  expert accepted only if it improves held-out repo pass rate
```

## 11. Component layout v0

```text
aem/
  node/
    worker_daemon.py
    gpu_profile.py
    expert_runtime.py
    train_lora.py
    serve_expert.py

  protocol/
    task_packet.schema.json
    expert_card.schema.json
    expert_reply.schema.json
    admission_report.schema.json

  registry/
    expert_registry.py
    reputation.py
    signatures.py

  router/
    task_classifier.py
    expert_ranker.py
    router_server.py
    fusion.py

  verifier/
    eval_runner.py
    sandbox_tests.py
    adversarial_prompts.py
    duplicate_detector.py

  data/
    shard_manifest.py
    dedup.py
    contamination_check.py

  distill/
    trace_store.py
    distill_dataset_builder.py
    train_next_router.py
```

Current repo already has an early PoC shape under:

```text
aem_poc/
schemas/
docs/
tests/
```

## 12. First protocol objects

```text
TaskPacket:
  task_id
  task_type
  prompt_hash
  context
  constraints
  budget
  privacy_level
  eval_hooks
  required_capabilities

ExpertReply:
  expert_id
  answer_or_patch
  confidence
  reasoning_trace_optional
  cost
  latency
  signature

AdmissionReport:
  expert_id
  target_eval_delta
  regression_eval_delta
  duplicate_score
  adversarial_score
  latency_cost
  trust_score
  decision
```

## 13. Where is frontier?

### wrong1

```text
frontier = strongest checkpoint
```

Death:

```text
This reduces intelligence to artifact size.
```

### wrong2

```text
frontier = sum of all experts
```

Death:

```text
The sum of garbage is not intelligence.
```

### Third

```text
frontier = the network's speed of birthing, verifying, routing, and distilling new capabilities faster than a centralized lab.
```

Metric:

```text
new capability → verified expert → routed usage → distilled traces → better router/core
```

## 14. What to borrow and what to replace

Useful external directions:

```text
DiLoCo/OpenDiLoCo:
  low-communication distributed training

Petals:
  collaborative inference/fine-tuning precedent

QLoRA:
  4-bit base + adapter expert training

SWARM:
  poorly connected heterogeneous unreliable devices

INTELLECT-style permissionless training:
  untrusted worker verification

BitNet / native low-bit:
  low-bit training research branch

vLLM/SGLang/llama.cpp:
  serving/runtime backends
```

But AEM is not any one of these. AEM is the protocol layer that admits, routes, verifies, rewards, and distills expert capabilities.

## 15. Death of this architecture step

```text
"Split MoE layers across home GPUs and call it frontier."
```

Dead.

## 16. Inheritance

```text
expert = capability capsule, not layer
model growth = admission-controlled expert accretion
frontier = verified capability birth rate + router/verifier/distillation loop
```

## 17. Next pressure

```text
Build the minimal Expert Capsule v0 for a 12GB GPU:
code_patch_expert + QLoRA recipe + held-out unit-test verifier + TrainingReceipt + admission gate.
```
