# AEM Roadmap — design Execution Plan

This roadmap turns AEM from architecture note into an executable growth protocol.

## Stage 0 — Protocol Spine

### Rejected option A

```text
start with model training
```

Death: without protocol, every artifact is unadmittable.

### Rejected option B

```text
start with a huge specification
```

Death: spec-only work becomes protocol theater.

### Third

```text
start with the minimum artifacts that make admission possible
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
an expert without card + receipt + report is not part of the network
```

---

## Stage 1 — Local Runnable Loop

### Rejected option A

```text
distribution first
```

Death: distributed bugs hide protocol bugs.

### Rejected option B

```text
local demo is enough
```

Death: a local demo without traces cannot grow into mesh behavior.

### Third

```text
local loop with mesh-shaped artifacts
```

Build:

```text
load ExpertCard from JSON
validate schema
route task
run verifier
write route_trace.jsonl
run unit tests
```

Objective gate:

```text
if route/admission cannot be replayed locally, public mesh is premature
```

---

## Stage 2 — Code Patch Expert MVP

### Rejected option A

```text
first expert should be general intelligence
```

Death: no objective Objective.

### Rejected option B

```text
first expert can be toy text completion
```

Death: no hard verifier.

### Third

```text
first expert = code patch capability with unit-test Objective
```

Build:

```text
synthetic bug repo fixture
TaskPacket: issue + failing test
ExpertReply: patch
Verifier: apply patch + run tests
Admission: pass/fail + diff constraints
```

Objective gate:

```text
expert is useful only if it fixes held-out tests
```

---

## Stage 3 — 12GB QLoRA Expert Training

### Rejected option A

```text
consumer GPUs cannot train anything useful
```

Death: adapter experts are enough for first capability growth.

### Rejected option B

```text
12GB node can train frontier monoliths
```

Death: confuses expert growth with full dense pretraining.

### Third

```text
12GB node trains constrained adapter experts with receipts
```

Build:

```text
qlora_code_patch_7b.yaml
train script
eval before/after
TrainingReceipt emitter
ExpertCard emitter
```

Objective gate:

```text
no eval_delta + no receipt = artifact, not expert
```

---

## Stage 4 — Node Daemon

### Rejected option A

```text
node is just a REST server
```

Death: no proof of work, no verifier role, no mesh health.

### Rejected option B

```text
node is a trusted member by default
```

Death: permissionless workers can lie.

### Third

```text
node is a signed worker-organ with staged trust
```

Build:

```text
aem node profile
aem node serve
aem node verify
aem node train
aem node sign report
```

Objective gate:

```text
node must prove work without receiving full trust
```

---

## Stage 5 — Multi-node LAN Mesh

### Rejected option A

```text
public internet first
```

Death: network/security failures obscure protocol failures.

### Rejected option B

```text
single-machine is enough
```

Death: no failure, latency, or membership pressure.

### Third

```text
2–3 node LAN mesh first
```

Build:

```text
registry server
node heartbeat
task dispatch
verifier dispatch
signed replies
node failure recovery
```

Objective gate:

```text
if one node drops, task flow must not collapse
```

---

## Stage 6 — Verifier Mesh

### Rejected option A

```text
expert author verifies their own expert
```

Death: self-certification.

### Rejected option B

```text
one central verifier solves trust
```

Death: central gatekeeper.

### Third

```text
independent verifier quorum with disagreement handling
```

Build:

```text
independent verifier nodes
repeated verification
disagreement protocol
quarantine policy
```

Objective gate:

```text
self-reported eval never gives admission
```

---

## Stage 7 — Router Learning

### Rejected option A

```text
router stays hand-written
```

Death: cannot scale expert choice.

### Rejected option B

```text
router becomes opaque central model
```

Death: hidden router becomes new corporate gate.

### Third

```text
router learns from public route traces and remains forkable
```

Build:

```text
route traces
success labels
exploration/canary traffic
expert ranking model
fallback policy
router explanation output
```

Objective gate:

```text
router must explain why an expert received traffic
```

---

## Stage 8 — Distillation Memory

### Rejected option A

```text
successful expert outputs are just final answers
```

Death: the mesh does not learn from itself.

### Rejected option B

```text
all traces become training data
```

Death: failure/noise poisoning.

### Third

```text
verified successful traces become curated distillation memory
```

Build:

```text
TraceStore
distill dataset builder
router-v2 training
merged/domain expert training
```

Objective gate:

```text
successful route must become reusable training material
```

---

## Stage 9 — Public Mesh Alpha

### Rejected option A

```text
open public mesh immediately
```

Death: spam, sybil, poisoning, privacy failures.

### Rejected option B

```text
keep everything closed until perfect
```

Death: no open network pressure.

### Third

```text
public alpha with staged trust and privacy levels
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
unknown node never receives private tasks
```

---

## Stage 10 — Low-bit Native Research Branch

### Rejected option A

```text
QLoRA is enough forever
```

Death: adapter growth may hit ceilings.

### Rejected option B

```text
native low-bit research should replace the whole stack now
```

Death: research branch becomes foundation risk.

### Third

```text
native low-bit experts compete inside the same admission protocol
```

Build:

```text
BitNet-like small expert experiments
sparse low-bit expert experiments
quality/VRAM/latency comparisons
admission through the same objective gates
```

Objective gate:

```text
low-bit expert is accepted only if quality/cost wins
```
