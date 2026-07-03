import unittest

from aem_poc.protocol import TaskPacket
from aem_poc.verifier_config import PatchVerifierConfig


class VerifierConfigTest(unittest.TestCase):
    def test_default_config(self) -> None:
        task = TaskPacket(task_id="t1", task_type="code_patch", prompt="x")
        config = PatchVerifierConfig.from_task(task)
        self.assertEqual(config.backend, "stdlib_one_file")
        self.assertIn("unittest", config.test_command)
        self.assertEqual(config.policy.allowed_files, ("calc.py",))

    def test_backend_from_task_constraints(self) -> None:
        task = TaskPacket(
            task_id="t2",
            task_type="code_patch",
            prompt="x",
            constraints={"patch_backend": "external"},
        )
        config = PatchVerifierConfig.from_task(task)
        self.assertEqual(config.backend, "external")

    def test_command_from_task_constraints(self) -> None:
        task = TaskPacket(
            task_id="t3",
            task_type="code_patch",
            prompt="x",
            constraints={"test_command": ["python", "-m", "unittest"]},
        )
        config = PatchVerifierConfig.from_task(task)
        self.assertEqual(config.test_command, ("python", "-m", "unittest"))

    def test_policy_from_task_constraints(self) -> None:
        task = TaskPacket(
            task_id="t4",
            task_type="code_patch",
            prompt="x",
            constraints={
                "allowed_files": ["calc.py", "helpers.py"],
                "blocked_prefixes": [".git/"],
                "max_patch_bytes": 128,
                "max_changed_files": 2,
            },
        )
        config = PatchVerifierConfig.from_task(task)
        self.assertEqual(config.policy.allowed_files, ("calc.py", "helpers.py"))
        self.assertEqual(config.policy.blocked_prefixes, (".git/",))
        self.assertEqual(config.policy.max_patch_bytes, 128)
        self.assertEqual(config.policy.max_changed_files, 2)
        payload = config.to_trace_payload()
        self.assertEqual(payload["allowed_files"], ("calc.py", "helpers.py"))


if __name__ == "__main__":
    unittest.main()
