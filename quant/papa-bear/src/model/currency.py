from math import floor

class Currency:
  value: float

  def __init__(self, amount = 0.0):
    self.value = self.truncate_two_digits(amount)

  def truncate_two_digits(self, number):
    return (floor(number * 100)) / 100.0

  def __add__(self, other):
    if (type(other) == Currency):
      return Currency(self.truncate_two_digits(self.value + other.value))
    return Currency(self.truncate_two_digits(self.value + other))

  def __sub__(self, other):
    if (type(other) == Currency):
      return Currency(self.truncate_two_digits(self.value - other.value))
    return Currency(self.truncate_two_digits(self.value - other))

  def __mul__(self, other):
    if (type(other) == Currency):
      return Currency(self.truncate_two_digits(self.value * other.value))
    return Currency(self.truncate_two_digits(self.value * other))

  def __truediv__(self, other):
    if (type(other) == Currency):
      return Currency(self.truncate_two_digits(self.value / other.value))
    return Currency(self.truncate_two_digits(self.value / other))