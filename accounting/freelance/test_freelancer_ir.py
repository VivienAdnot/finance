import unittest
from freelancer_ir import estimate_sasu_ir_net_income

class TestFreelancerIR(unittest.TestCase):

    def test_estimate_sasu_ir_net_income(self):
        result = estimate_sasu_ir_net_income(
            tjm=770,
            jours_facturés=220,
            salaire_annuel=7000,
            charges_fixes=2500,
            frais_deductibles=5000
        )
        self.assertIn("revenu_net_avant_ir", result)
        self.assertGreater(result["revenu_net_avant_ir"], 0)
        self.assertGreaterEqual(result["benefice_apres_csg"], 0)
        self.assertEqual(round(result["chiffre_affaires"]), 169400)

if __name__ == "__main__":
    unittest.main()
