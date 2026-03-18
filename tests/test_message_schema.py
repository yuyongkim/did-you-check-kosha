import unittest
import uuid

from src.shared.message_schema import validate_message_envelope


class MessageSchemaTests(unittest.TestCase):
    def test_valid_calculation_request(self) -> None:
        message = {
            "message_id": str(uuid.uuid4()),
            "message_type": "calculation_request",
            "correlation_id": str(uuid.uuid4()),
            "trace_id": str(uuid.uuid4()),
            "from_agent": "orchestrator",
            "to_agent": "piping_specialist",
            "timestamp_utc": "2026-02-26T10:30:00Z",
            "priority": "normal",
            "timeout_sec": 300,
            "payload": {
                "calculation_type": "remaining_life",
                "input_data": {"design_pressure": 150}
            },
            "meta": {
                "discipline": "piping",
                "workflow_id": "standard_calculation",
                "standards_context_version": "v0.1"
            }
        }
        result = validate_message_envelope(message)
        self.assertTrue(result.valid)
        self.assertEqual(result.errors, [])

    def test_invalid_missing_payload_field(self) -> None:
        message = {
            "message_id": str(uuid.uuid4()),
            "message_type": "calculation_request",
            "correlation_id": str(uuid.uuid4()),
            "trace_id": str(uuid.uuid4()),
            "from_agent": "orchestrator",
            "to_agent": "piping_specialist",
            "timestamp_utc": "2026-02-26T10:30:00Z",
            "priority": "normal",
            "timeout_sec": 300,
            "payload": {
                "calculation_type": "remaining_life"
            },
            "meta": {}
        }
        result = validate_message_envelope(message)
        self.assertFalse(result.valid)
        self.assertTrue(any("Missing payload fields" in e for e in result.errors))


if __name__ == "__main__":
    unittest.main()
