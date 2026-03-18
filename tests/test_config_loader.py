import pathlib
import unittest

from src.agents.runtime_builder import build_mock_runtime
from src.shared.config_loader import load_and_validate_config


class ConfigLoaderTests(unittest.TestCase):
    def test_sample_config_loads_and_validates(self) -> None:
        path = pathlib.Path("configs/sample_config.json")
        config, errors = load_and_validate_config(path)
        self.assertEqual(errors, [])
        runtime = build_mock_runtime(config)
        self.assertTrue(runtime.has("spec_explorer"))
        self.assertTrue(runtime.has("verification_agent"))


if __name__ == "__main__":
    unittest.main()

