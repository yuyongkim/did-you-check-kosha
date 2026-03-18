import unittest

from src.shared.red_flags import get_flag, is_blocking, requires_human_review, RedFlagSeverity


class RedFlagTests(unittest.TestCase):
    def test_critical_flag_is_blocking(self) -> None:
        self.assertTrue(is_blocking("STD.INVALID_REFERENCE"))
        self.assertTrue(requires_human_review("STD.INVALID_REFERENCE"))

    def test_medium_timeout_not_blocking(self) -> None:
        self.assertFalse(is_blocking("OPS.TIMEOUT_EXCEEDED"))

    def test_flag_severity(self) -> None:
        flag = get_flag("PHY.NEGATIVE_THICKNESS")
        self.assertEqual(flag.severity, RedFlagSeverity.CRITICAL)


if __name__ == "__main__":
    unittest.main()
