# Evidence Artifact Index design

wrong1: evidence files explain themselves.
Death: reviewers must chase producers, schemas, and verifiers across docs and modules.

wrong2: README artifact list is enough.
Death: a flat file list does not show producer, schema, verifier, or purpose.

Third: the repo has one artifact index table for the full uploaded evidence set.

Index:

```text
docs/EVIDENCE_ARTIFACT_INDEX.md
```

Maps every evidence file to:

```text
producer
schema
verifier / gate
purpose
```

Covered artifact classes:

```text
metadata report
first-stage trace evidence
first-stage seal manifest
first-stage seal verify report
second-stage seal manifest
terminal second-stage verify report
```

Current artifact count:

```text
13
```

Files:

```text
docs/EVIDENCE_ARTIFACT_INDEX.md
docs/evidence_artifact_index.json
docs/EVIDENCE_ARTIFACT_INDEX_DESIGN.md
README.md
```

Death: evidence artifact meaning is scattered across the repo.

Inheritance: AEM evidence files need a human-readable and machine-readable map for the whole upload bundle.

Next pressure: make the artifact index include seal stage/role fields, not only producer/schema/verifier/purpose.
