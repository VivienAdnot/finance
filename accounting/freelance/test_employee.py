import unittest
from employee import compute_net_salary, compute_impot_revenu

class TestEmployeeCalculations(unittest.TestCase):

    def test_net_salary(self):
        brut = 80000
        expected_net = brut * (1 - 0.23)
        self.assertAlmostEqual(compute_net_salary(brut), expected_net, places=2)

    def test_impot_revenu(self):
        revenu_net = 60000
        parts = 2
        impots = compute_impot_revenu(revenu_net, parts)
        self.assertTrue(isinstance(impots, float))
        self.assertGreater(impots, 0)

if __name__ == "__main__":
    unittest.main()
