import json
import tempfile
import unittest
from pathlib import Path

from aem_poc.loaders import load_task_packet
from aem_poc.schema_validation import SchemaValidationError, validate_data, validate_or_raise


class SchemaValidationTest(unittest.TestCase):
    def test_valid_task_packet_passes(self) -> None:
        data = {
            "task_id": "t-valid",
            "task_type": "code_patch",
            "prompt": "fix it",
            "constraints": {
                "patch_backend": "stdlib_one_file",
                "allowed_files": ["calc.py"],
                "max_patch_bytes": 128,
                "max_changed_files": 1,
            },
        }
        result = validate_data(data, "task_packet.schema.json")
        self.assertTrue(result.ok)
        self.assertIn(result.mode, {"structural", "jsonschema"})

    def test_invalid_task_packet_fails(self) -> None:
        data = {
            "task_id": "t-invalid",
            "task_type": "code_patch",
            "prompt": "fix it",
            "constraints": {"patch_backend": "bad_backend"},
        }
        result = validate_data(data, "task_packet.schema.json")
        self.assertFalse(result.ok)
        with self.assertRaises(SchemaValidationError):
            validate_or_raise(data, "task_packet.schema.json")

    def test_loader_validates_task_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "task.json"
            path.write_text(
                json.dumps(
                    {
                        "task_id": "t-load",
                        "task_type": "code_patch",
                        "prompt": "fix it",
                        "constraints": {"patch_backend": "stdlib_one_file"},
                    }
                ),
                encoding="utf-8",
            )
            task = load_task_packet(path)
            self.assertEqual(task.constraints["patch_backend"], "stdlib_one_file")


if __name__ == "__main__":
    unittest.main()
