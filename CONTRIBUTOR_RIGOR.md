# Contributor Rigor Pack

Credit: inspired by Iwo Szapar's Rigor Pack:
https://www.iwoszapar.com/tools/rigor-pack

This file is an original adaptation for this repository. It does not copy the
source pack's skill bodies.

## Why This Exists

AEM is early infrastructure. Small, verified patches are more useful than broad
rewrites or persuasive architecture essays. This guide gives contributors a
simple public checklist for making a patch reviewable.

## Usefulness Check

Useful here:

- it forces a plan before changing files;
- it makes contributors verify the current repository state instead of relying
  on stale docs;
- it keeps pull requests narrow;
- it requires proof from commands, files, or generated artifacts;
- it keeps public memory and docs free of secrets, raw prompts, and private
  material.

Not enough by itself:

- it does not replace tests, CI, evidence seals, or schema checks;
- it does not prove a network claim without an executable demo or artifact;
- it should not be treated as an external authority over this repo's design.

## Contributor Loop

Before editing:

```text
Task:
Files expected:
Non-scope:
Acceptance command:
Risk if wrong:
```

During editing:

```text
Keep the diff small.
Do not change unrelated files.
Do not add raw prompts, raw outputs, secrets, or private notes.
Map every claim to a file, test, schema, or generated artifact.
```

Before opening a PR:

```text
Run the relevant command.
Paste the exact command and result.
Name one way the patch could still be wrong.
List adjacent issues under "noticed, not changed".
```

## AEM Local Gates

For ordinary changes:

```bash
python -m unittest discover -s tests
python -m aem_poc.demo
```

For evidence or artifact changes:

```bash
make evidence-local-ci
```

For network and credit-settlement changes:

```bash
make aem-network-economy-check
```

If `make` is unavailable on your machine, run the Python command behind the
target and say which command you used.

## PR Format

```text
Task:
Files changed:
Non-scope:
Proof command:
Proof result:
Adversarial check:
Noticed, not changed:
Source credit, if adapting an external idea:
```

## Review Rules

A PR is easier to merge when:

- it strengthens one executable gate;
- it adds or updates a schema when the public contract changes;
- it updates docs only when docs match the running command;
- it keeps generated artifacts reproducible;
- it avoids broad claims about future capability.

A PR should be split when:

- it mixes architecture, implementation, generated artifacts, and docs;
- it changes unrelated task areas;
- it needs more than one acceptance command to explain what it proves.
