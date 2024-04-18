import unittest
from app import hit_count, check_odd_or_even


class GenericTest(unittest.TestCase):

    def test_hitcount_number_type(self):
        self.assertTrue(isinstance(hit_count(), (int)))

    def test_raise_type_error_odd_even(self):
        with self.assertRaises(TypeError):
            check_odd_or_even("HI")

if __name__ == '__main__':
    unittest.main()
