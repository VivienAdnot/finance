def compute_impot_revenu(total_revenu_net, parts=2):
    brackets = [
        (0, 11194, 0.0),
        (11195, 28797, 0.11),
        (28798, 82341, 0.30),
        (82342, 177106, 0.41),
        (177107, float('inf'), 0.45)
    ]

    revenu_par_part = total_revenu_net / parts
    impot_par_part = 0
    tmi = 0.0

    for lower, upper, rate in brackets:
        if revenu_par_part > lower:
            taxable = min(upper, revenu_par_part) - lower
            impot_par_part += taxable * rate
            tmi = rate  # dernière tranche atteinte
        else:
            break

    return impot_par_part * parts, tmi

def compute_impot_revenu_simple(total_revenu_net, parts=2):
    total, _ = compute_impot_revenu(total_revenu_net, parts)
    return total

def estimate_sasu_is_net_income_v3_with_ir(
    tjm=770,
    jours_facturés=220,
    salaire_brut_annuel=20000,
    taux_charges_sociales=0.80,
    charges_fixes=2500,
    frais_deductibles=5000,
    revenu_conjoint_net=24000,
    parts_fiscales=2
):
    chiffre_affaires = tjm * jours_facturés
    charges_sociales = salaire_brut_annuel * taux_charges_sociales
    cout_total_salaire = salaire_brut_annuel + charges_sociales

    resultat_comptable = chiffre_affaires - charges_fixes - frais_deductibles - cout_total_salaire

    seuil_is_reduit = 42500
    taux_is_reduit = 0.15
    taux_is_normal = 0.25
    flat_tax_dividendes = 0.30

    if resultat_comptable <= 0:
        is_total = 0
    else:
        if resultat_comptable <= seuil_is_reduit:
            is_total = resultat_comptable * taux_is_reduit
        else:
            is_total = (
                seuil_is_reduit * taux_is_reduit +
                (resultat_comptable - seuil_is_reduit) * taux_is_normal
            )

    resultat_apres_is = max(0, resultat_comptable - is_total)
    dividendes = resultat_apres_is
    flat_tax = dividendes * flat_tax_dividendes

    salaire_net = salaire_brut_annuel * (1 - taux_charges_sociales)
    revenu_net_perso = salaire_net + (dividendes - flat_tax)
    revenu_net_total_foyer = revenu_net_perso + revenu_conjoint_net
    ir_total, tmi = compute_impot_revenu(revenu_net_total_foyer, parts_fiscales)
    net_apres_tous_impots = revenu_net_total_foyer - ir_total

    return {
        "revenu_net_perso_avant_ir": revenu_net_perso,
        "revenu_net_foyer": revenu_net_total_foyer,
        "impot_revenu_total": ir_total,
        "net_final_apres_ir": net_apres_tous_impots,
        "dividendes_nets": dividendes - flat_tax,
        "salaire_net": salaire_net,
        "charges_sociales": charges_sociales,
        "is_total": is_total,
        "flat_tax": flat_tax,
        "tmi": tmi,
    }

def optimise_salaire_vs_dividendes(
    tjm=770,
    jours_facturés=220,
    charges_fixes=2500,
    frais_deductibles=5000,
    salaire_min=7000,
    salaire_max=70000,
    step=1000,
    revenu_conjoint_net=24000,
    parts_fiscales=2
):
    best_result = None
    best_salaire = 0

    for salaire_brut in range(salaire_min, salaire_max + 1, step):
        result = estimate_sasu_is_net_income_v3_with_ir(
            tjm=tjm,
            jours_facturés=jours_facturés,
            salaire_brut_annuel=salaire_brut,
            charges_fixes=charges_fixes,
            frais_deductibles=frais_deductibles,
            revenu_conjoint_net=revenu_conjoint_net,
            parts_fiscales=parts_fiscales
        )

        if best_result is None or result["net_final_apres_ir"] > best_result["net_final_apres_ir"]:
            best_result = result
            best_salaire = salaire_brut

    best_result["salaire_brut_optimisé"] = best_salaire
    return best_result