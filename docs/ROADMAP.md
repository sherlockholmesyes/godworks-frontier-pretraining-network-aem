# AEM Roadmap

## Stage 0 — Protocol spine

wrong1: start with model training.
wrong2: start with huge specs.
Third: start with admission artifacts.

Build:

```text
ExpertCard
TaskPacket
AdmissionReport
VerifierReport
RouteTrace
TrainingReceipt
DataShardManifest
TeacherPolicyCard
DistillationReceipt
```

## Stage 1 — Objective admission

wrong1: manifest claims are enough.
wrong2: one central reviewer decides.
Third: objective verifier reports control admission.

Build:

```text
sandbox verifier
objective admission wrapper
trace store
fixture tests
```

Objective:

```text
fake expert rejected even with strong manifest claims
```

## Stage 2 — Code patch verifier

wrong1: first expert should be general chat.
wrong2: wait for perfect eval.
Third: start with code patch tests.

Objective:

```text
candidate solution must pass sandboxed tests
```

## Stage 3 — Distillation gate

wrong1: teacher output is training data by default.
wrong2: teacher signal can never be used.
Third: teacher signal enters only through TeacherPolicyCard, verifier pass, and DistillationReceipt.

Objective:

```text
blocked teacher output rejected before training
allowed teacher plus verifier-passed sample accepted
receipt emitted
```
