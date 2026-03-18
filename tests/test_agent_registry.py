import unittest

from src.agents.registry import missing_required_agents


class AgentRegistryTests(unittest.TestCase):
    def test_missing_required_agents_detected(self) -> None:
        missing = missing_required_agents(["orchestrator", "spec_explorer"])
        self.assertIn("piping_specialist", missing)

    def test_no_missing_agents(self) -> None:
        names = [
            "orchestrator",
            "spec_explorer",
            "piping_specialist",
            "static_equipment_specialist",
            "rotating_specialist",
            "electrical_specialist",
            "instrumentation_specialist",
            "steel_specialist",
            "civil_specialist",
            "calculator_worker",
            "verification_agent",
        ]
        self.assertEqual(missing_required_agents(names), [])


if __name__ == "__main__":
    unittest.main()

