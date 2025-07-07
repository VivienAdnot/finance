from currency import Currency
import unittest

class TestCurrency(unittest.TestCase):
  def test_ctor(self):
    currency1 = Currency(20 / 3)
    self.assertEqual(currency1.value, 6.66)

  def test_add_currency(self):
    currency1 = Currency(20 / 3)
    self.assertEqual(currency1.value, 6.66)
    currency2 = Currency(10 / 3)
    self.assertEqual(currency2.value, 3.33)

    result = currency1 + currency2
    self.assertEqual(result.value, 9.99)

  def test_add_float(self):
    currency1 = Currency(20 / 3)
    result = currency1 + 3
    self.assertEqual(result.value, 9.66)

  def test_substract_currency(self):
    currency1 = Currency(20 / 3)
    self.assertEqual(currency1.value, 6.66)
    currency2 = Currency(10 / 3)
    self.assertEqual(currency2.value, 3.33)

    result = currency1 - currency2
    self.assertEqual(result.value, 3.33)

  def test_substract_float(self):
    currency1 = Currency(20 / 3)
    result = currency1 - 3
    self.assertEqual(result.value, 3.66)

  def test_multiply_currency(self):
    currency1 = Currency(20 / 3)
    self.assertEqual(currency1.value, 6.66)
    currency2 = Currency(10 / 3)
    self.assertEqual(currency2.value, 3.33)

    result = currency1 * currency2
    self.assertEqual(result.value, 22.17)

  def test_multiply_float(self):
    currency1 = Currency(20 / 3)
    result = currency1 * 3
    self.assertEqual(result.value, 19.98)

  def test_divide_currency(self):
    currency1 = Currency(20 / 3)
    self.assertEqual(currency1.value, 6.66)
    currency2 = Currency(10 / 3)
    self.assertEqual(currency2.value, 3.33)

    result = currency1 / currency2
    self.assertEqual(result.value, 2.0)

