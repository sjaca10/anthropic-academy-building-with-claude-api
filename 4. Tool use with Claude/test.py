import math
import unittest

from main import calculate_pi


class TestCalculatePi(unittest.TestCase):
    def test_five_digits_default(self):
        self.assertEqual(calculate_pi(), 3.14159)

    def test_five_digits_explicit(self):
        self.assertEqual(calculate_pi(5), 3.14159)

    def test_fewer_digits(self):
        self.assertEqual(calculate_pi(0), 3.0)
        self.assertEqual(calculate_pi(1), 3.1)
        self.assertEqual(calculate_pi(2), 3.14)
        self.assertEqual(calculate_pi(3), 3.142)
        self.assertEqual(calculate_pi(4), 3.1416)

    def test_matches_math_pi_when_rounded(self):
        for digits in range(0, 8):
            with self.subTest(digits=digits):
                self.assertEqual(calculate_pi(digits), round(math.pi, digits))

    def test_negative_digits_raises(self):
        with self.assertRaises(ValueError):
            calculate_pi(-1)


if __name__ == "__main__":
    unittest.main()
