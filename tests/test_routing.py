import unittest

from aem_poc.demo import build_registry
from aem_poc.protocol import ObjectiveGateConfig, ObjectiveVerifier, Router, TaskPacket


class RoutingTests(unittest.TestCase):
    def test_router_selects_12gb_code_patch_expert(self) -> None:
        task = TaskPacket(
            task_id="test-task",
            task_type="code_patch",
            prompt="fix a failing unit test",
            required_capabilities=("code", "python"),
        )
        router = Router(
            build_registry(),
            ObjectiveVerifier(
                ObjectiveGateConfig(
                    target_eval_key="code_patch",
                    node_vram_gb=12,
                    max_latency_ms=8000,
                )
            ),
        )

        chosen, reports = router.route(task)

        self.assertIsNotNone(chosen)
        assert chosen is not None
        self.assertEqual(chosen.expert_id, "code_patch_7b_q4_lora_v0")
        rejected = {report.expert_id for report in reports if not report.accepted}
        self.assertIn("echo_lora_bad_v0", rejected)
        self.assertIn("heavy_32b_patch_expert_v0", rejected)

    def test_no_admission_when_threshold_too_high(self) -> None:
        task = TaskPacket(
            task_id="test-task-hard",
            task_type="code_patch",
            prompt="fix a failing unit test",
            required_capabilities=("code",),
        )
        router = Router(
            build_registry(),
            ObjectiveVerifier(
                ObjectiveGateConfig(
                    target_eval_key="code_patch",
                    min_target_delta=0.50,
                    node_vram_gb=12,
                )
            ),
        )

        chosen, reports = router.route(task)

        self.assertIsNone(chosen)
        self.assertTrue(reports)
        self.assertTrue(all(not report.accepted for report in reports))


if __name__ == "__main__":
    unittest.main()
