# E2E Gate Demo — design

## Rejected option A

```text
AEM can accept an expert if the manifest claims strong evals.
```

Death: a beautiful manifest can lie.

## Rejected option B

```text
AEM can only accept experts after manual human review.
```

Death: central review does not scale into a mesh.

## Third

```text
AEM accepts an expert only when manifest gates and objective verifier gates both pass.
```

## Executable path

```bash
python -m aem_poc.e2e_gate_demo
make e2e
python -m unittest discover -s tests
```

## Expected invariant

```text
fake_claim_expert: manifest claims high eval, verifier fails, admission false
real_patch_expert: manifest passes, verifier passes, admission true
route_trace.jsonl: written to disk
distill_receipt.json: written to disk
```

## Distillation gate

Rejected option A:

```text
teacher output enters training by default
```

Rejected option B:

```text
teacher signal is never usable
```

Third:

```text
teacher signal enters only after TeacherCard and verifier gates pass
```

Expected invariant:

```text
blocked teacher sample rejected
allowed teacher sample accepted
receipt emitted
```

## Next pressure

```text
replace hardcoded verifier fixture with a real repo patch fixture
```
