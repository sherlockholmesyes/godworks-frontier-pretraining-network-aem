# AEM Technology Stack — design

## Root

Rejected option A:

```text
AEM can be built from one big ML framework
```

Death: one framework cannot cover packaging, verification, routing, receipts, traces, and distributed trust.

Rejected option B:

```text
AEM needs custom everything
```

Death: too much invention before proof.

Third:

```text
AEM needs a thin protocol layer over existing ML runtimes
```

## Required base technologies

### Artifact formats

```text
JSON Schema for cards/reports/traces
safetensors for adapters/weights
GGUF for edge quantized inference artifacts
content hashes for artifacts and data shards
```

### Training runtimes

```text
PyTorch
PEFT / LoRA / QLoRA-style recipes
bitsandbytes or equivalent low-bit backend
small distributed experiments through DiLoCo-like / SWARM-like modes later
```

### Serving runtimes

```text
llama.cpp for consumer edge quantized serving
vLLM for high-throughput serving nodes
SGLang for structured generation/tool-like serving nodes
```

### Verification

```text
unittest/pytest-style harnesses for code experts
sandboxed process runner for patch tests
held-out eval fixtures
regression eval runner
duplicate/backdoor probe runner
```

### Mesh infrastructure

```text
node registry
worker daemon
signed reports
route_trace.jsonl
sqlite for local reputation/credits first
HTTP/gRPC later for node communication
```

### Security and policy

```text
artifact signatures
node identity
quarantine state
privacy/routing modes
rate limits
canary tasks
```

## First implementation target

```text
stdlib PoC
+ JSON files
+ local route trace
+ sandboxed code-patch verifier
+ one QLoRA recipe stub
```

## Next pressure

```text
implement trace_store.py and loaders.py before adding more model code
```
