from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

from .schema_validation import SchemaValidationError, validate_data


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_PATH = REPO_ROOT / "docs" / "aem_network_brick_ledger.json"
LEDGER_SCHEMA = "aem_network_brick_ledger.schema.json"
LEDGER_VERSION = "2026-07-01.v1"
NETWORK_THIRD = (
    "Off-chain expert training/inference produces signed receipts; verifier challenges and policy gates convert "
    "receipts into transferable credits; the ledger settles credits without pretending that blockchain executes inference."
)


def _node(node_id: str, node_type: str, purpose: str, primitive_status: str) -> dict[str, str]:
    return {"id": node_id, "type": node_type, "purpose": purpose, "primitive_status": primitive_status}


def _brick(
    brick_id: str,
    name: str,
    status: str,
    purpose: str,
    wrong1: str,
    death1: str,
    wrong2: str,
    death2: str,
    third: str,
    definition: dict[str, str],
    nodes: list[dict[str, str]],
    stable: list[str],
    proto: list[str],
    missing: list[str],
    minimal_tests: list[str],
    kill_criteria: list[str],
    next_pressure: str,
) -> dict[str, Any]:
    closure_status = "closed" if not proto and not missing else "partially_closed" if proto and not missing else "open"
    return {
        "id": brick_id,
        "name": name,
        "status": status,
        "purpose": purpose,
        "wrong1": wrong1,
        "death1": death1,
        "wrong2": wrong2,
        "death2": death2,
        "third": third,
        "definition": definition,
        "nodes": nodes,
        "primitive_closure": {
            "closure_status": closure_status,
            "stable_primitives": stable,
            "proto_primitives": proto,
            "missing_primitives": missing,
        },
        "minimal_tests": minimal_tests,
        "kill_criteria": kill_criteria,
        "next_pressure": next_pressure,
    }


def source_bricks() -> list[dict[str, Any]]:
    return [
        _brick(
            "capability_capsule",
            "Capability Capsule / ExpertCard",
            "closed_poc",
            "Describe an expert as an admissible capability capsule rather than a loose model file.",
            "Expert = a local checkpoint someone claims is useful.",
            "A checkpoint without claims, license, eval deltas, and runtime bounds cannot be routed or rewarded safely.",
            "Expert = a global chain account with stake only.",
            "Stake says little about capability, domains, VRAM fit, or verifier evidence.",
            "ExpertCard-like capability capsule: identity, model hash, domains, eval delta, policy, and signature.",
            {
                "input": "expert metadata, model/adaptor hash, domain claims, runtime limits",
                "operation": "normalize claims into a routable and verifiable capability capsule",
                "output": "ExpertCard accepted or rejected by schema/objective gates",
                "measurable_delta": "router can select experts by capability and tests can reject malformed capsules",
            },
            [
                _node("identity", "interface_node", "stable expert id and signature boundary", "stable_primitive"),
                _node("claims", "capability_node", "domains and eval deltas", "stable_primitive"),
                _node("policy", "constraint_node", "license and allowed use", "stable_primitive"),
                _node("runtime", "constraint_node", "VRAM and quantization fit", "stable_primitive"),
            ],
            ["expert_card_schema", "signature_field", "domain_claims", "eval_delta", "runtime_bounds"],
            [],
            [],
            ["schema rejects missing expert id/license/eval delta", "router can read domain and VRAM constraints"],
            ["expert can be routed without capability claims", "malformed expert card is accepted"],
            "Add network-level NodeCard that binds host capacity to one or more ExpertCards.",
        ),
        _brick(
            "node_identity_capacity",
            "Node Identity and Capacity Card",
            "proto_brick",
            "Represent each human participant's machine as a routable host with capacity, locality, uptime, and policy.",
            "Node = wallet address.",
            "A wallet cannot expose GPU, bandwidth, geography, uptime, or sandbox guarantees.",
            "Node = unverifiable self-reported benchmark page.",
            "Self-reported capacity becomes reward farming without challenge receipts.",
            "NodeCard signed by host plus verifier-sampled capacity receipts and privacy-preserving locality buckets.",
            {
                "input": "host key, hardware envelope, locality bucket, available experts, uptime samples",
                "operation": "bind capacity claims to challengeable node receipts",
                "output": "routable NodeCard with confidence score",
                "measurable_delta": "router can prefer nearby capable hosts and punish stale capacity claims",
            },
            [
                _node("host_key", "interface_node", "stable host identity", "stable_primitive"),
                _node("capacity_probe", "test_node", "verifier-sampled hardware/runtime proof", "proto_primitive"),
                _node("locality_bucket", "constraint_node", "nearby routing without exact doxxing", "proto_primitive"),
                _node("uptime_receipt", "state_node", "recent availability evidence", "missing_primitive"),
            ],
            ["host_key", "signed_node_card"],
            ["capacity_probe", "locality_bucket"],
            ["uptime_receipt_primitive"],
            ["create NodeCard and route only if capacity envelope satisfies task", "stale capacity claim loses routing priority"],
            ["wallet-only host is routable", "capacity cannot be challenged", "exact location is required for routing"],
            "Implement NodeCard schema plus deterministic locality bucket and challenge receipt stub.",
        ),
        _brick(
            "expert_host_registry",
            "Expert Host Registry",
            "proto_brick",
            "Map each admitted expert to current hosts, replicas, locality buckets, and availability.",
            "Registry = global list of model URLs.",
            "A URL list cannot price latency, replica health, or host reliability.",
            "Registry = blockchain storage of every heartbeat.",
            "On-chain heartbeat spam is expensive and leaks topology while not proving service quality.",
            "Off-chain signed host advertisements with periodic registry snapshots and challengeable availability receipts.",
            {
                "input": "NodeCard, ExpertCard, signed host advertisement, health samples",
                "operation": "index expert replicas by host, locality, policy, and freshness",
                "output": "routable host set per expert",
                "measurable_delta": "same expert can be routed to nearest healthy replica rather than random host",
            },
            [
                _node("advertisement", "interface_node", "host says expert is available", "proto_primitive"),
                _node("freshness", "state_node", "expiry and heartbeat window", "proto_primitive"),
                _node("replica_set", "operator_node", "group hosts by expert id", "stable_primitive"),
                _node("availability_challenge", "test_node", "prove endpoint can answer", "missing_primitive"),
            ],
            ["expert_id_index", "replica_set"],
            ["host_advertisement", "freshness_window"],
            ["availability_challenge_receipt"],
            ["registry excludes expired host advertisements", "same ExpertCard maps to multiple host candidates"],
            ["expired host remains routable", "registry has no replica freshness", "routing requires full on-chain heartbeat stream"],
            "Add HostAdvertisement schema and registry selection test.",
        ),
        _brick(
            "locality_quality_router",
            "Locality and Quality Router",
            "proto_brick",
            "Select the nearest adequate host for an expert while respecting quality, price, policy, and reliability.",
            "Router = nearest host wins.",
            "Nearest host can be weak, stale, policy-incompatible, or low-quality.",
            "Router = highest-quality expert wins globally.",
            "Global best routing ignores latency, cost, and replica availability.",
            "Router ranks host candidates by capability fit, locality bucket, receipt quality, credit price, and freshness.",
            {
                "input": "TaskPacket, candidate ExpertCards, host registry, credit price hints",
                "operation": "score host-expert pairs under policy and locality constraints",
                "output": "chosen host/expert route with fallback set",
                "measurable_delta": "task routes to a healthy nearby adequate expert instead of nearest-only or best-only",
            },
            [
                _node("capability_fit", "operator_node", "match task to expert domain", "stable_primitive"),
                _node("locality_score", "operator_node", "prefer nearby buckets", "proto_primitive"),
                _node("quality_score", "operator_node", "use receipts and eval deltas", "proto_primitive"),
                _node("price_score", "operator_node", "include credit cost", "missing_primitive"),
            ],
            ["task_domain_match", "route_trace"],
            ["locality_score", "receipt_quality_score"],
            ["credit_price_score"],
            ["router rejects policy-incompatible host", "router chooses lower latency host when quality is adequate"],
            ["nearest host always wins", "global expert always wins", "price cannot affect routing"],
            "Implement host-expert scoring receipt inside RouteTrace without real network transport.",
        ),
        _brick(
            "inference_work_receipt",
            "Inference Work Receipt",
            "research_packet",
            "Turn completed inference into a credit-earning event without trusting self-reported output.",
            "Inference reward = host says it answered.",
            "Self-reporting mints credits for fake work.",
            "Inference reward = chain re-executes model output.",
            "On-chain inference is not viable for large models and leaks execution details.",
            "Signed off-chain inference receipt with task hash, model hash, cost envelope, output commitment, and verifier challenge hooks.",
            {
                "input": "task hash, expert id, host id, output commitment, runtime envelope",
                "operation": "commit to performed inference and expose it to verifier sampling",
                "output": "InferenceReceipt eligible for credit settlement",
                "measurable_delta": "fake work can be challenged while honest work can earn credits without chain inference",
            },
            [
                _node("task_commitment", "interface_node", "bind receipt to request", "stable_primitive"),
                _node("output_commitment", "interface_node", "commit without publishing sensitive output", "proto_primitive"),
                _node("runtime_cost", "state_node", "tokens/time/VRAM envelope", "missing_primitive"),
                _node("verifier_challenge", "test_node", "sample honest execution", "missing_primitive"),
            ],
            ["task_hash", "expert_hash", "host_signature"],
            ["output_commitment"],
            ["runtime_cost_meter", "inference_challenge_protocol"],
            ["receipt cannot be created without task/expert/host binding", "duplicate receipt cannot mint twice"],
            ["host self-report alone mints credits", "receipt contains no challenge surface", "output commitment cannot be verified"],
            "Define InferenceReceipt schema and duplicate-spend rejection test.",
        ),
        _brick(
            "training_work_receipt",
            "Training Work Receipt",
            "proto_brick",
            "Reward useful training/adaptation work without rewarding useless compute burn.",
            "Training reward = GPU hours burned.",
            "GPU hours can be wasted or adversarial and do not prove useful capability gain.",
            "Training reward = only final leaderboard score.",
            "Leaderboards ignore provenance, overfit, and contribution granularity.",
            "TrainingReceipt binds data/provenance, eval delta, policy, and verifier reports to credit eligibility.",
            {
                "input": "training receipt, data/provenance claims, eval delta, verifier reports",
                "operation": "admit training contribution only if policy and eval gates pass",
                "output": "credit-eligible training receipt",
                "measurable_delta": "contributors earn for verified useful training rather than raw compute time",
            },
            [
                _node("training_receipt", "interface_node", "record adaptation event", "stable_primitive"),
                _node("eval_delta", "test_node", "measure target improvement", "stable_primitive"),
                _node("provenance_policy", "constraint_node", "legal/source admissibility", "stable_primitive"),
                _node("anti_overfit_challenge", "test_node", "detect leaderboard gaming", "missing_primitive"),
            ],
            ["training_receipt_schema", "eval_delta", "teacher_policy_card"],
            [],
            ["anti_overfit_challenge"],
            ["receipt with policy violation is rejected", "receipt with no eval delta earns zero credits"],
            ["GPU hours alone mint credits", "policy violation still earns", "overfit delta cannot be challenged"],
            "Tie existing TrainingReceipt/TeacherPolicyCard to a credit eligibility report.",
        ),
        _brick(
            "credit_ledger_settlement",
            "Credit Ledger and Settlement",
            "research_packet",
            "Convert verified work receipts into transferable inference credits without central operator accounting.",
            "Credits = centralized database balance.",
            "Central balances make the network trust a single operator and block resale/exit.",
            "Credits = every inference runs as a blockchain transaction.",
            "Per-inference chain execution is too expensive and too slow for model serving.",
            "Receipt-backed credit ledger: off-chain work receipts, verifier challenge windows, batched settlement, transferable balances.",
            {
                "input": "eligible work receipts, challenge outcomes, pricing policy",
                "operation": "settle credits after fraud window and update transferable balances",
                "output": "credit balance deltas and spendable inference credits",
                "measurable_delta": "honest compute earns transferable credits while fake receipts can be slashed before settlement",
            },
            [
                _node("receipt_batch", "interface_node", "batch eligible work", "proto_primitive"),
                _node("challenge_window", "constraint_node", "delay finality until fraud sampling", "missing_primitive"),
                _node("credit_balance", "state_node", "transferable account balance", "proto_primitive"),
                _node("double_spend_guard", "constraint_node", "prevent reuse of receipts", "stable_primitive"),
            ],
            ["receipt_id", "double_spend_guard"],
            ["receipt_batch", "credit_balance"],
            ["challenge_window", "settlement_finality_rule"],
            ["same receipt cannot mint twice", "credit transfer preserves total supply"],
            ["central-only balance is source of truth", "unverified receipts settle instantly", "supply changes without receipt"],
            "Create CreditLedgerReceipt schema and in-memory settlement simulator.",
        ),
        _brick(
            "reward_pricing_function",
            "Reward and Pricing Function",
            "research_packet",
            "Reward larger, smarter, more useful experts while avoiding pure size farming and monopoly routing.",
            "Reward = model size and hardware power.",
            "Raw size rewards whales even if the expert is useless or unavailable.",
            "Reward = cheapest inference only.",
            "Cheapest-only routing kills high-quality specialized experts and training incentives.",
            "Reward combines verified usefulness, scarcity, latency, cost, reliability, and policy class.",
            {
                "input": "quality receipts, availability receipts, task demand, cost envelope, policy class",
                "operation": "compute credit reward and route price under bounded anti-gaming rules",
                "output": "credit reward multiplier and buyer price quote",
                "measurable_delta": "better useful experts earn more without size-only or cheapest-only collapse",
            },
            [
                _node("quality_multiplier", "operator_node", "reward useful capability", "proto_primitive"),
                _node("scarcity_multiplier", "operator_node", "reward rare useful experts", "missing_primitive"),
                _node("latency_cost", "operator_node", "price nearby service", "proto_primitive"),
                _node("anti_monopoly_cap", "constraint_node", "bound winner-take-all", "missing_primitive"),
            ],
            ["eval_delta", "availability_score"],
            ["quality_multiplier", "latency_cost"],
            ["scarcity_multiplier", "anti_monopoly_cap"],
            ["reward increases for verified quality at same cost", "size-only expert with no quality delta does not earn multiplier"],
            ["raw parameter count determines rewards", "cheapest-only routing wins all tasks", "reward can be gamed by self-dealing demand"],
            "Add reward simulator with adversarial scenarios: whale expert, cheap weak expert, rare specialist.",
        ),
        _brick(
            "anti_fraud_sybil_slashing",
            "Anti-Fraud, Sybil, and Slashing Layer",
            "research_packet",
            "Prevent fake hosts, fake receipts, collusive demand, and Sybil credit farming.",
            "Fraud control = require stake only.",
            "Stake alone favors capital and still permits profitable fraud if challenges are weak.",
            "Fraud control = trust verifier committee only.",
            "Verifier cartel becomes the new centralized operator.",
            "Use stake as collateral plus randomized challenges, receipt reproducibility, peer audits, and slashing evidence.",
            {
                "input": "receipts, challenges, verifier reports, stake/collateral records",
                "operation": "detect fraud patterns and convert proof into slashing or score decay",
                "output": "fraud verdict, slashing event, reputation update",
                "measurable_delta": "fake receipts and Sybil hosts lose expected value under challenge sampling",
            },
            [
                _node("challenge_sampling", "test_node", "randomly verify work", "missing_primitive"),
                _node("reputation_decay", "state_node", "penalize bad history", "proto_primitive"),
                _node("slashing_receipt", "interface_node", "record punishable fraud", "missing_primitive"),
                _node("collusion_detector", "operator_node", "detect closed loops", "missing_primitive"),
            ],
            ["signed_receipts"],
            ["reputation_decay"],
            ["challenge_sampling", "slashing_receipt", "collusion_detector"],
            ["invalid receipt can produce slashable proof", "repeated failures lower routing priority"],
            ["stake-only passes fake work", "verifier cartel cannot be challenged", "collusive demand can farm credits indefinitely"],
            "Define fraud challenge packet and minimal slashing receipt schema.",
        ),
        _brick(
            "credit_market_exchange",
            "Credit Market and Resale Exchange",
            "research_packet",
            "Allow participants to spend earned credits on their own inference, sell credits, or buy credits without breaking work-backed accounting.",
            "Credits = non-transferable quota.",
            "Non-transferable credits kill market discovery and prevent earners from selling surplus.",
            "Credits = fully financial token from day one.",
            "A financial token before proof-of-use invites speculation before useful network value exists.",
            "Transferable work-backed credits with optional marketplace rails and clear separation from equity/governance claims.",
            {
                "input": "settled credit balances, transfer orders, spend authorizations",
                "operation": "move credits between users or burn them for inference",
                "output": "transfer receipt or spend receipt",
                "measurable_delta": "hosts can sell earned capacity while users can buy inference without central quota grants",
            },
            [
                _node("transfer_receipt", "interface_node", "move credits", "proto_primitive"),
                _node("spend_receipt", "interface_node", "burn credits for task", "proto_primitive"),
                _node("market_order", "interface_node", "offer credits for payment", "missing_primitive"),
                _node("regulatory_boundary", "constraint_node", "avoid equity/governance overclaim", "missing_primitive"),
            ],
            ["credit_balance"],
            ["transfer_receipt", "spend_receipt"],
            ["market_order", "regulatory_boundary"],
            ["credit transfer conserves balance", "spend burns balance and creates task authorization"],
            ["credits mint without work", "credits imply ownership/governance by default", "sell order can double-spend credits"],
            "Implement transfer/spend receipt simulator before external marketplace claims.",
        ),
        _brick(
            "privacy_sandbox_policy",
            "Privacy, Sandbox, and Policy Boundary",
            "proto_brick",
            "Run third-party tasks on local experts without leaking private prompts, model secrets, or host machines.",
            "Hosts see every prompt and output by default.",
            "This blocks sensitive use and creates data extraction incentives.",
            "Everything must run in cryptographic black boxes immediately.",
            "Full cryptographic privacy may be too slow or unavailable for early PoC.",
            "Policy-gated task classes, local sandboxing, redaction commitments, and future privacy primitive slots.",
            {
                "input": "TaskPacket, host policy, privacy class, sandbox profile",
                "operation": "admit or reject task execution based on privacy and sandbox compatibility",
                "output": "sandboxed execution authorization or rejection",
                "measurable_delta": "network can route safe classes now while marking missing privacy primitives honestly",
            },
            [
                _node("task_privacy_class", "constraint_node", "classify prompt sensitivity", "proto_primitive"),
                _node("sandbox_profile", "constraint_node", "limit execution rights", "stable_primitive"),
                _node("redaction_commitment", "interface_node", "commit to redacted logs", "proto_primitive"),
                _node("private_inference_primitive", "operator_node", "hide prompt/output from host", "missing_primitive"),
            ],
            ["workspace_policy", "blocked_prefixes", "selected_command_runner"],
            ["task_privacy_class", "redaction_commitment"],
            ["private_inference_primitive"],
            ["policy rejects task class incompatible with host", "sandbox blocks unauthorized file access"],
            ["sensitive prompts are routed to arbitrary hosts", "logs leak private data by default", "privacy is claimed without primitive"],
            "Add TaskPrivacyClass and HostSandboxPolicy schemas.",
        ),
        _brick(
            "network_governance_upgrade",
            "Protocol Governance and Upgrade Ledger",
            "research_packet",
            "Upgrade schemas, rewards, verifier rules, and network policies without silent capture.",
            "Governance = repo maintainer updates rules.",
            "Silent maintainer changes break trust for credit settlement and host economics.",
            "Governance = token vote controls everything.",
            "Token vote can capture technical safety rules and reward incumbents.",
            "Versioned protocol proposals with migration receipts, verifier acceptance, and bounded governance domains.",
            {
                "input": "protocol proposal, affected schemas, migration plan, verifier reports",
                "operation": "admit or reject upgrades through explicit compatibility and migration gates",
                "output": "versioned protocol upgrade receipt",
                "measurable_delta": "network can change rules without invisible ledger/economy mutation",
            },
            [
                _node("proposal_schema", "interface_node", "describe upgrade", "missing_primitive"),
                _node("migration_receipt", "interface_node", "prove old state migrates", "missing_primitive"),
                _node("compatibility_gate", "test_node", "check old receipts remain interpretable", "proto_primitive"),
                _node("bounded_vote", "constraint_node", "limit governance scope", "missing_primitive"),
            ],
            ["schema_versioning"],
            ["compatibility_gate"],
            ["proposal_schema", "migration_receipt", "bounded_vote"],
            ["old receipt validates under migration", "upgrade proposal lists affected primitives"],
            ["maintainer can mutate credit rules silently", "token vote can alter verifier truth unboundedly"],
            "Define ProtocolProposal and MigrationReceipt schemas after credit ledger primitives exist.",
        ),
    ]


def build_network_brick_ledger() -> dict[str, Any]:
    bricks = source_bricks()
    status_counts = dict(sorted(Counter(brick["status"] for brick in bricks).items()))
    missing: set[str] = set()
    for brick in bricks:
        missing.update(brick["primitive_closure"]["missing_primitives"])
    ledger = {
        "ledger_version": LEDGER_VERSION,
        "network_third": NETWORK_THIRD,
        "brick_count": len(bricks),
        "status_counts": status_counts,
        "missing_primitives": sorted(missing),
        "bricks": bricks,
    }
    validate_network_brick_ledger(ledger)
    return ledger


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _shape_ok(data: dict[str, Any]) -> bool:
    required = ("ledger_version", "network_third", "brick_count", "status_counts", "missing_primitives", "bricks")
    if not all(key in data for key in required):
        return False
    if not isinstance(data["ledger_version"], str) or not isinstance(data["network_third"], str):
        return False
    if not isinstance(data["brick_count"], int) or data["brick_count"] < 0:
        return False
    if not isinstance(data["status_counts"], dict) or not all(isinstance(k, str) and isinstance(v, int) for k, v in data["status_counts"].items()):
        return False
    if not _str_list(data["missing_primitives"]):
        return False
    bricks = data["bricks"]
    if not isinstance(bricks, list) or len(bricks) != data["brick_count"]:
        return False
    for brick in bricks:
        if not isinstance(brick, dict):
            return False
        for key in ("id", "name", "status", "purpose", "wrong1", "death1", "wrong2", "death2", "third", "next_pressure"):
            if not isinstance(brick.get(key), str):
                return False
        if brick["status"] not in {"closed_poc", "proto_brick", "research_packet"}:
            return False
        definition = brick.get("definition")
        if not isinstance(definition, dict):
            return False
        for key in ("input", "operation", "output", "measurable_delta"):
            if not isinstance(definition.get(key), str):
                return False
        if not isinstance(brick.get("nodes"), list):
            return False
        closure = brick.get("primitive_closure")
        if not isinstance(closure, dict):
            return False
        if closure.get("closure_status") not in {"closed", "partially_closed", "open"}:
            return False
        for key in ("stable_primitives", "proto_primitives", "missing_primitives"):
            if not _str_list(closure.get(key)):
                return False
        if not _str_list(brick.get("minimal_tests")) or not _str_list(brick.get("kill_criteria")):
            return False
    return True


def validate_network_brick_ledger(ledger: dict[str, Any]) -> None:
    result = validate_data(ledger, LEDGER_SCHEMA)
    if result.ok:
        return
    if result.mode == "structural" and result.errors == (f"unknown schema: {LEDGER_SCHEMA}",):
        if _shape_ok(ledger):
            return
    raise SchemaValidationError(f"{LEDGER_SCHEMA} validation failed: {result.errors}")


def write_network_brick_ledger(output_path: str | Path = DEFAULT_LEDGER_PATH) -> dict[str, Any]:
    ledger = build_network_brick_ledger()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ledger


def load_network_brick_ledger(path: str | Path = DEFAULT_LEDGER_PATH) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SchemaValidationError(f"{path} must contain a JSON object")
    validate_network_brick_ledger(data)
    return data


def ledger_sync_report(path: str | Path = DEFAULT_LEDGER_PATH) -> dict[str, Any]:
    expected = build_network_brick_ledger()
    actual = load_network_brick_ledger(path) if Path(path).exists() else None
    matches = actual == expected
    return {
        "path": str(Path(path)),
        "exists": actual is not None,
        "matches_generated": matches,
        "ok": matches,
        "brick_count": expected["brick_count"],
        "status_counts": expected["status_counts"],
        "missing_primitive_count": len(expected["missing_primitives"]),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print or sync AEM network brick gap ledger")
    parser.add_argument("--output", help="optional output path")
    parser.add_argument("--check", action="store_true", help="check the checked-in ledger matches generated source")
    parser.add_argument("--sync", action="store_true", help="rewrite checked-in ledger from generated source")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = args.output or DEFAULT_LEDGER_PATH
    if args.check:
        report = ledger_sync_report(path)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.sync:
        ledger = write_network_brick_ledger(path)
        report = ledger_sync_report(path)
        report["written"] = True
        report["brick_count"] = ledger["brick_count"]
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    ledger = build_network_brick_ledger()
    print(json.dumps(ledger, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
