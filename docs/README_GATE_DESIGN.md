# README Gate design

wrong1: CI can exist without README entrypoint.
Death: new users miss the executable gates.

wrong2: README should only describe architecture.
Death: prose drifts away from runnable evidence.

Third: README exposes CI status and local verification commands.

Contract:

```text
CI badge
quick start
local verification
current gates
trace artifacts
next pressure
```

Invariant:

```text
a newcomer can run CI-equivalent gates from README alone
```

Next pressure:

```text
add CI artifact upload for compacted traces and manifests
```
