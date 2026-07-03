.PHONY: demo e2e repo-demo trace-compact-demo trace-report-demo evidence-demo evidence-verify-demo evidence-seal-verify-demo evidence-second-stage-seal evidence-second-stage-seal-verify evidence-artifact-index evidence-artifact-index-sync evidence-artifact-index-md-check evidence-artifact-index-md-sync evidence-metadata-check evidence-upload-policy evidence-upload-drift evidence-upload-sync evidence-status evidence-status-example-check evidence-status-example-sync evidence-docs-check evidence-docs-sync aem-network-bricks aem-network-bricks-sync aem-network-bricks-check aem-network-cards aem-network-cards-check aem-bootstrap-growth aem-bootstrap-growth-check aem-skill-receipts aem-skill-receipts-check aem-inference-receipts aem-inference-receipts-check aem-credit-ledger aem-credit-ledger-check aem-network-economy-check evidence-local-ci test

demo:
	python -m aem_poc.demo

e2e:
	python -m aem_poc.e2e_gate_demo

repo-demo:
	python -m aem_poc.patch_gate_demo

trace-compact-demo:
	python -m aem_poc.patch_gate_demo
	python -m aem_poc.trace_maint compact runs/patch_gate_demo/route_trace.jsonl runs/patch_gate_demo/route_trace.compact.jsonl

trace-report-demo: trace-compact-demo
	python -m aem_poc.trace_maint report runs/patch_gate_demo/route_trace.compact.jsonl runs/patch_gate_demo/trace_report.json

evidence-demo:
	python -m aem_poc.evidence_pipeline

evidence-verify-demo: evidence-demo

evidence-seal-verify-demo: evidence-demo
	python -m aem_poc.evidence_seal_verify runs/patch_gate_demo/evidence_seal_manifest.json > runs/patch_gate_demo/evidence_seal_verify_report.json

evidence-second-stage-seal:
	python -m aem_poc.evidence_second_stage_seal --output runs/upload/evidence_second_stage_seal_manifest.json

evidence-second-stage-seal-verify:
	python -m aem_poc.evidence_second_stage_seal_verify runs/upload/evidence_second_stage_seal_manifest.json --output runs/upload/evidence_second_stage_verify_report.json

evidence-artifact-index:
	python -m aem_poc.evidence_artifact_index validate
	python -m aem_poc.evidence_artifact_index list

evidence-artifact-index-sync:
	python -m aem_poc.evidence_artifact_index sync

evidence-artifact-index-md-check:
	python -m aem_poc.evidence_artifact_index md-check

evidence-artifact-index-md-sync:
	python -m aem_poc.evidence_artifact_index md-sync

evidence-metadata-check:
	python -m aem_poc.evidence_metadata_check --output runs/metadata/evidence_metadata_report.json

evidence-upload-policy:
	python -m aem_poc.evidence_upload_policy --check

evidence-upload-drift:
	python -m aem_poc.evidence_upload_drift

evidence-upload-sync:
	python -m aem_poc.evidence_upload_drift --sync

evidence-status:
	python -m aem_poc.evidence_status

evidence-status-example-check:
	python -m aem_poc.evidence_status --check-example

evidence-status-example-sync:
	python -m aem_poc.evidence_status --sync-example

evidence-docs-check:
	$(MAKE) evidence-artifact-index
	$(MAKE) evidence-artifact-index-md-check
	$(MAKE) evidence-status-example-check

evidence-docs-sync:
	$(MAKE) evidence-artifact-index-sync
	$(MAKE) evidence-artifact-index-md-sync
	$(MAKE) evidence-status-example-sync

aem-network-bricks:
	python -m aem_poc.aem_network_bricks

aem-network-bricks-sync:
	python -m aem_poc.aem_network_bricks --sync

aem-network-bricks-check:
	python -m aem_poc.aem_network_bricks

aem-network-cards:
	python -m aem_poc.aem_network_cards

aem-network-cards-check:
	python -m aem_poc.aem_network_cards --check

aem-bootstrap-growth:
	python -m aem_poc.aem_bootstrap_growth

aem-bootstrap-growth-check:
	python -m aem_poc.aem_bootstrap_growth --check

aem-skill-receipts:
	python -m aem_poc.aem_skill_receipts

aem-skill-receipts-check:
	python -m aem_poc.aem_skill_receipts --check

aem-inference-receipts:
	python -m aem_poc.aem_inference_receipts

aem-inference-receipts-check:
	python -m aem_poc.aem_inference_receipts --check

aem-credit-ledger:
	python -m aem_poc.aem_credit_ledger_skill

aem-credit-ledger-check:
	python -m aem_poc.aem_credit_ledger_skill --check

aem-network-economy-check:
	$(MAKE) aem-network-bricks-check
	$(MAKE) aem-network-cards-check
	$(MAKE) aem-bootstrap-growth-check
	$(MAKE) aem-skill-receipts-check
	$(MAKE) aem-inference-receipts-check
	$(MAKE) aem-credit-ledger-check

evidence-local-ci:
	$(MAKE) test
	$(MAKE) evidence-artifact-index
	$(MAKE) evidence-artifact-index-md-check
	$(MAKE) evidence-status
	$(MAKE) evidence-metadata-check
	$(MAKE) evidence-upload-policy
	$(MAKE) evidence-upload-drift
	$(MAKE) evidence-seal-verify-demo
	$(MAKE) evidence-second-stage-seal
	$(MAKE) evidence-second-stage-seal-verify

test:
	python -m unittest discover -s tests
