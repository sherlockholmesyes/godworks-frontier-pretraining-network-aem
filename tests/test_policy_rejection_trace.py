import tempfile
import unittest
from pathlib import Path

from aem_poc.loaders import load_task_packet
from aem_poc.patch_gate_demo import root
from aem_poc.trace_store import TraceStore, build_route_trace
from aem_poc.verifier_config import PatchVerifierConfig
from aem_poc.workspace_prep import WorkspacePrep


class PolicyRejectionTraceTest(unittest.TestCase):
    def test_forbidden_patch_rejected_before_workspace_command(self) -> None:
        base = root()
        task = load_task_packet(base / "examples" / "task_code_patch.json")
        config = PatchVerifierConfig.from_task(task)
        diff_text = (base / "examples" / "patches" / "forbidden_file.patch").read_text(encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            prep = WorkspacePrep(policy=config.policy, backend=config.backend).prepare(
                fixture_repo=base / "fixtures" / "code_patch_repo",
                diff_text=diff_text,
                output_dir=Path(tmp) / "workspace_forbidden",
            )
            self.assertFalse(prep.accepted)
            self.assertIsNone(prep.workspace_path)
            self.assertEqual(prep.changed_files, ())
            self.assertTrue(any("file not allowed" in reason for reason in prep.checks))

            trace = build_route_trace(
                task=task,
                candidates=[],
                chosen=None,
                admission_reports=[],
                verifier_reports=[{"kind": "workspace", **prep.to_dict()}],
            )
            store = TraceStore(Path(tmp) / "route_trace.jsonl")
            store.append(trace)
            rows = store.read_all()

        self.assertEqual(len(rows), 1)
        self.assertIsNone(rows[0]["chosen_expert"])
        reports = rows[0]["verifier_reports"]
        self.assertEqual(reports[0]["workspace_path"], None)
        self.assertTrue(any("file not allowed" in reason for reason in reports[0]["checks"]))


if __name__ == "__main__":
    unittest.main()
