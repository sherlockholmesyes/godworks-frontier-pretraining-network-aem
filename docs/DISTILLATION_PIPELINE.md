# Distillation Pipeline

## Goal

Use only allowed teacher signals and convert them into verified AEM artifacts.

## Pipeline

```text
1. load TeacherPolicyCard
2. reject teacher if training is not allowed
3. create candidate sample
4. run objective verifier
5. reject failed sample
6. accept verified sample
7. emit DistillationReceipt
8. attach receipt to ExpertCard admission later
```

## design

Rejected option A:

```text
teacher output is training data by default
```

Death: policy risk enters the model.

Rejected option B:

```text
teacher output is never usable
```

Death: allowed and verified signal is wasted.

Third:

```text
teacher output becomes training data only through policy and verifier gates
```

## First PoC

```text
blocked teacher output rejected before training
allowed teacher plus verifier-passed sample accepted
DistillationReceipt emitted
```
