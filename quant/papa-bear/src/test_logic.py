import unittest
from logic import compute_average_gains, compute_winners_losers

class TestLogic(unittest.TestCase):

  def test_compute_average_gains(self):
    rows = [
      [10], #0 -6
      [],
      [],
      [8],  #3 -3
      [],
      [30], #5 -1
      [14], #6
    ]
    result = compute_average_gains(rows)
    self.assertEqual(result, [
      [],
      [],
      [],
      [],
      [],
      [],
      [20.56],
    ])

  def test_compute_average_gains_real(self):
    rows = [
      [121.14, 83.41, 46.23, 229.19, 109.33, 160.6, 241.03, 124.25, 66.06, 180.56, 13.2],
      [119.46, 84.26, 48.02, 226.12, 117.16, 155.72, 250.03, 129.21, 69.33, 174.9, 13.52],
      [120.15, 84.39, 50.72, 232.47, 129.45, 158.77, 274.65, 135.35, 72.18, 172.49, 14.24],
      [118.01, 81.97, 53.97, 241.26, 139.96, 151.07, 302.66, 140.88, 74.74, 173., 15.13],
      [117.97, 88.9, 56.94, 252.8, 152.07, 148.79, 336.63, 143.52, 75.64, 172.08, 16.18],
      [114.71, 90.11, 54.97, 242.33, 167.19, 139.01, 316.87, 151.01, 76.09, 161.52, 17.5],
      [113.54, 53.23, 53.23, 256.94, 160.64, 137.45, 300.7, 154.95, 77.56, 162.28, 16.79],
      [114.23, 98.73, 53.81, 252.55, 165.15, 137.78, 289.24, 162.3, 80.13, 172.08, 18.61]
    ]

    result = compute_average_gains(rows)
    self.assertEqual(result, [
      [],
      [],
      [],
      [],
      [],
      [],
      [-3.69, -37.39, 3.53, 8.21, 19.26, -8.18, 6.34, 12.44, 7.7, -5.28, 11.37],
      [-2.31, 37.9, 2.55, 3.29, 17.46, -6.23, -0.74, 14.48, 8.28, 1.48, 21.17]
    ])

  def test_compute_winners_losers(self):
    current_winners_indices = [1, 2, 3]
    new_winners_indices = [2, 4, 6]

    losers_to_sell, winners_to_buy, keep_previous_winners = compute_winners_losers(current_winners_indices, new_winners_indices)
    self.assertEqual(losers_to_sell, [1, 3])
    self.assertEqual(winners_to_buy, [4, 6])
    self.assertEqual(keep_previous_winners, [2])