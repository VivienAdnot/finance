import unittest
from freelancer_is import estimate_sasu_is_net_income_v3_with_ir

class TestFreelancerIS(unittest.TestCase):

    def test_estimate_sasu_is_net_income_v3_with_ir(self):
        result = estimate_sasu_is_net_income_v3_with_ir(
            tjm=770,
            jours_facturés=220,
            salaire_brut_annuel=20000,
            charges_fixes=2500,
            frais_deductibles=5000,
            revenu_conjoint_net=24000,
            parts_fiscales=2
        )
        self.assertIn("net_final_apres_ir", result)
        self.assertIn("tmi", result)
        self.assertGreater(result["net_final_apres_ir"], 0)
        self.assertTrue(0 <= result["tmi"] <= 0.45)
        self.assertAlmostEqual(result["revenu_net_foyer"], result["net_final_apres_ir"] + result["impot_revenu_total"], places=1)

if __name__ == "__main__":
    unittest.main()
