def estimate_sasu_ir_net_income(
    tjm=770,
    jours_facturés=220,
    salaire_annuel=7000,  # salaire minimum versé
    charges_fixes=2500,   # comptable + assurance
    frais_deductibles=5000,
    taux_csg_crds=0.172,
    cfe=1200
):
    chiffre_affaires = tjm * jours_facturés

    resultat = chiffre_affaires - charges_fixes - frais_deductibles - salaire_annuel
    csg_crds = max(0, resultat) * taux_csg_crds
    revenu_imposable = max(0, resultat) - csg_crds - cfe
    revenu_net_avant_ir = salaire_annuel + frais_deductibles + max(0, revenu_imposable)

    return {
        "chiffre_affaires": chiffre_affaires,
        "revenu_net_avant_ir": revenu_net_avant_ir,
        "salaire_annuel": salaire_annuel,
        "frais_deductibles": frais_deductibles,
        "benefice_apres_csg": max(0, revenu_imposable),
    }
