import unittest

from src.shared.config_schema import validate_config


class ConfigSchemaTests(unittest.TestCase):
    def test_missing_sections_reported(self) -> None:
        cfg = {"system": {}}
        errors = validate_config(cfg)
        self.assertTrue(any("Missing top-level sections" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
