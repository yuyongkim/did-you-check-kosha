import unittest

from src.verification.reverse_check import reverse_remaining_life_check


class ReverseCheckTests(unittest.TestCase):
    def test_reverse_check_pass(self) -> None:
        result = reverse_remaining_life_check(
            current_thickness_mm=8.0,
            corrosion_rate_mm_per_year=0.2,
            service_years=5,
            historical_initial_thickness_mm=9.0,
            tolerance_percent=5.0,
        )
        self.assertTrue(result.passed)

    def test_reverse_check_fail(self) -> None:
        result = reverse_remaining_life_check(
            current_thickness_mm=8.0,
            corrosion_rate_mm_per_year=0.2,
            service_years=5,
            historical_initial_thickness_mm=11.0,
            tolerance_percent=5.0,
        )
        self.assertFalse(result.passed)


if __name__ == "__main__":
    unittest.main()

