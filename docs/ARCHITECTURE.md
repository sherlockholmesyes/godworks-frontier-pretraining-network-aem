# AEM Architecture Notes

AEM is a PoC for frontier-capability growth by expert accretion.

```text
AEM = Accretive Expert Mesh
```

## design architecture cut

### Rejected option A

```text
More frontier = bigger synchronous checkpoint.
```

Death: this copies the corporate pretraining fabric.

### Rejected option B

```text
More frontier = random consumer GPUs as remote MoE layers.
```

Death: this copies MoE vocabulary but ignores public-internet latency and adversarial workers.

### Third

```text
More frontier = verified capability growth.
```

The unit of growth is not a layer. The unit of growth is an admitted expert capsule.

## Expert capsule contract

An `ExpertCard` is the minimum public claim made by an expert:

```text
identity + base compatibility + quantization + VRAM budget + objective + domains + eval deltas + risks + signature
```

The actual weights can later be:

```text
- QLoRA adapter
- native low-bit expert
- small continued-pretrained model
- verifier model
- tool-policy model
- distillation target
```

## Routing level

AEM routes at task/capability level:

```text
issue → code_patch expert
proof attempt → math/prover expert
candidate answer → verifier expert
debug trace → critic expert
successful trace → distillation memory
```

AEM does **not** route every token hidden state to random public workers.

## objective gates

Current PoC gates are local and deterministic:

```text
target eval delta
general regression delta
duplicate risk
backdoor risk
latency budget
VRAM fit
signature presence
```

Future gates:

```text
reproducible training recipe
multi-node verifier consensus
sandbox execution
held-out contamination checks
traffic canarying
reputation-weighted admission
cost/benefit market score
```

## First living MVP

The first real system should be a code-patch expert mesh:

```text
TaskPacket:
  issue + repo context + failing tests

Expert:
  7B/14B open coder base + 4-bit runtime + QLoRA adapter

Verifier:
  sandboxed unit tests + patch diff constraints

Admission:
  improves pass rate on held-out tasks without broad regression
```

## Next coding pressure

Implement:

```text
1. load ExpertCard from JSON
2. validate against schema
3. run aem-demo against loaded cards
4. add sandbox verifier interface
5. add first synthetic code-patch fixture
```
