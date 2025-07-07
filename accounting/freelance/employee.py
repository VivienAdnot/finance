from freelancer_is import compute_impot_revenu_simple

def compute_net_salary(brut_annuel):
    taux_charges_salariales = 0.23
    return brut_annuel * (1 - taux_charges_salariales)

def compute_impot_revenu(brut_net_annuel, parts=2):
    return compute_impot_revenu_simple(brut_net_annuel, parts)
