# Distillation — design

This document defines policy-gated distillation. It does not support scraping, impersonation, rate-limit bypass, or cloning a provider persona.

## Root cut

Rejected option A:

```text
distillation = clone a competitor output stream
```

Death: this creates legal, policy, and dataset-contamination risk.

Rejected option B:

```text
teacher signals can never be used
```

Death: allowed open teachers, tools, human-owned data, and verified public tasks become unusable.

Third:

```text
distillation = allowed teacher signal converted into verified training artifacts
```

Pipeline:

```text
TeacherPolicyCard
→ candidate sample
→ verifier report
→ accepted sample ledger
→ student training
→ DistillationReceipt
→ AEM expert admission
```

## TeacherPolicyCard

Rejected option A: teacher is any strong model.
Rejected option B: teacher is only our own model.
Third: teacher is a signal source with explicit usage policy.

Gate:

```text
if allowed_for_training is not true, output cannot enter training set
```

## Sample gate

Rejected option A: sample = prompt plus answer.
Rejected option B: sample = full raw logs.
Third: sample = provenance plus verifier result plus accepted answer.

Drop sample if:

```text
no provenance
no training permission
no verifier pass
style/persona mimicry risk
long third-party copyrighted excerpt
```

## Multi-teacher canonicalization

Rejected option A: imitate one teacher.
Rejected option B: majority vote.
Third: disagreement plus verifier creates canonical sample.

Law:

```text
teacher proposes, verifier decides
```

## Receipt

Rejected option A: good dataset is enough.
Rejected option B: reveal every raw sample.
Third: emit an audit receipt.

Required receipt fields:

```text
distillation_run_id
student_base_model
student_output_model
teacher_policy_ids
sample_ledger_hash
accepted_count
rejected_count
rejection_breakdown
eval_before
eval_after
signature
```

## Objective gates

```text
1. teacher policy allows training
2. sample has provenance
3. no hidden prompt extraction
4. no persona cloning target
5. verifier pass or low/no training weight
6. student improves target eval
7. student does not regress guard eval
8. receipt emitted
```

## Next pressure

```text
blocked teacher output rejected before training
allowed teacher plus verifier-passed sample accepted
DistillationReceipt emitted
```
