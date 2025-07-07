import unittest
from numpy.testing import assert_array_equal
from utils import average, compute_percentage_gain, get_3_max_values, convert_to_year, convert_to_month, increment_month

class TestUtils(unittest.TestCase):

  def test_average(self):
    self.assertEqual(average(1, 3, 5), 3.0)
    self.assertEqual(average(1, 3, 5, 8), 4.25)

  def test_compute_percentage_gain(self):
    value_current = 100
    value_previous = 50
    result = compute_percentage_gain(value_current, value_previous)
    self.assertEqual(result, 100.0)

  def test_get_3_winners(self):
    values = [-3.89, -59.99, 2.83, 7.53, 13.58, -9.29, 4.6, 10.48, 6.79, -5.8, 9.01]
    largest_indices, largest_values = get_3_max_values(values)
    assert_array_equal(largest_values, [9.01, 10.48, 13.58])
    assert_array_equal(largest_indices, [10, 7, 4])

  def test_convert_to_year(self):
    self.assertEqual(convert_to_year(10), 0)
    self.assertEqual(convert_to_year(15), 1)
    self.assertEqual(convert_to_year(30), 2)
    self.assertEqual(convert_to_year(45), 3)
    self.assertEqual(convert_to_year(58), 4)
    self.assertEqual(convert_to_year(100), 8)
    self.assertEqual(convert_to_year(140), 11)
    self.assertEqual(convert_to_year(178), 14)
    self.assertEqual(convert_to_year(181), 15)

  def test_convert_to_month(self):
    self.assertEqual(convert_to_month(10), 10)
    self.assertEqual(convert_to_month(13), 1)
    self.assertEqual(convert_to_month(25), 1)

  def test_increment_month(self):
    self.assertEqual(increment_month(1), 2)
    self.assertEqual(increment_month(11), 12)
    self.assertEqual(increment_month(12), 1)