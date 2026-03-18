import unittest

from src.shared.errors import ConsensusError
from src.verification.maker import categorical_consensus, numeric_consensus


class MakerTests(unittest.TestCase):
    def test_numeric_consensus_success(self) -> None:
        result = numeric_consensus([10.0, 10.05, 20.0], tolerance=0.01, k_threshold=2)
        self.assertEqual(result.agreement_count, 2)

    def test_numeric_consensus_failure(self) -> None:
        with self.assertRaises(ConsensusError):
            numeric_consensus([10.0, 11.0, 12.0], tolerance=0.001, k_threshold=2)

    def test_categorical_consensus_success(self) -> None:
        self.assertEqual(categorical_consensus(["pass", "pass", "fail"]), "pass")


if __name__ == "__main__":
    unittest.main()

