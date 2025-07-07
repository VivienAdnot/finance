def calcul_plus_value(prix_vente, prix_achat, frais_acquisition, annees_detention):
    plus_value_brute = prix_vente - (prix_achat + frais_acquisition)
    
    # Si pas de plus-value, pas de taxe
    if plus_value_brute <= 0:
        return 0, 0, 0
    
    # Calcul des abattements
    if annees_detention < 6:
        abattement_ir = 0
        abattement_ps = 0
    else:
        # Abattement pour l'impôt sur le revenu (19%)
        if annees_detention <= 21:
            abattement_ir = min(100, (annees_detention - 5) * 6)
        else:
            abattement_ir = min(100, 96 + (annees_detention - 21) * 4)
            
        # Abattement pour les prélèvements sociaux (17.2%)
        if annees_detention <= 21:
            abattement_ps = min(100, (annees_detention - 5) * 1.65)
        elif annees_detention == 22:
            abattement_ps = 37.4
        else:
            abattement_ps = min(100, 37.4 + (annees_detention - 22) * 9)
    
    # Calcul des taxes
    base_ir = plus_value_brute * (1 - abattement_ir/100)
    base_ps = plus_value_brute * (1 - abattement_ps/100)
    
    impot_plus_value = base_ir * 0.19
    prelevements_sociaux = base_ps * 0.172
    
    return plus_value_brute, impot_plus_value, prelevements_sociaux

def calcul_placement_monetaire(capital_initial, taux_annuel, duree_annees, taux_imposition):
    resultats_annuels = []
    capital = capital_initial
    
    for annee in range(1, duree_annees + 1):
        interets_annuels = capital * taux_annuel
        impots = interets_annuels * (taux_imposition / 100)
        gain_net = interets_annuels - impots
        capital += gain_net
        
        resultats_annuels.append({
            "Année": annee,
            "Capital": capital,
            "Intérêts bruts": interets_annuels,
            "Impôts": impots,
            "Gain net": gain_net,
            "Gain total net": capital - capital_initial
        })
    
    return resultats_annuels

def calcul_rentabilite(prix_achat, loyer_mensuel, taux_credit, duree_annees, charges_mensuelles, 
                       taxe_fonciere, taux_imposition, apport):
    # Calcul des frais d'acquisition
    frais_acquisition = prix_achat * 0.08  # Approximativement 8% du prix d'achat
    cout_total_acquisition = prix_achat + frais_acquisition
    
    # Vérification que l'apport couvre au moins les frais d'acquisition
    apport_net = apport - frais_acquisition
    montant_emprunte = prix_achat - apport_net
    
    # Calculs initiaux
    loyer_annuel = loyer_mensuel * 12
    rentabilite_brute = (loyer_annuel / cout_total_acquisition) * 100  # Modifié pour inclure les frais
    charges_annuelles = (charges_mensuelles * 12) + taxe_fonciere
    
    # Paramètres du crédit
    taux_mensuel = taux_credit / 12 / 100
    nombre_mensualites = duree_annees * 12
    mensualite = (montant_emprunte * taux_mensuel) / (1 - (1 + taux_mensuel) ** -nombre_mensualites)
    
    # Tableaux pour stocker les résultats année par année
    resultats_annuels = []
    capital_restant = montant_emprunte
    
    cumul_interets_payes = 0
    cumul_loyers_percus = 0
    cumul_charges_payees = 0
    cumul_impots_payes = 0
    
    # Calcul du placement monétaire alternatif
    placement_monetaire = calcul_placement_monetaire(
        capital_initial=apport,
        taux_annuel=0.025,  # 2.5%
        duree_annees=duree_annees,
        taux_imposition=30.0  # Flat tax de 30%
    )
    
    for annee in range(1, duree_annees + 1):
        interets_annuels = 0
        capital_amorti_annuel = 0
        
        # Calcul mois par mois pour l'année en cours
        for _ in range(12):
            interet_mensuel = capital_restant * taux_mensuel
            capital_mensuel = mensualite - interet_mensuel
            interets_annuels += interet_mensuel
            capital_amorti_annuel += capital_mensuel
            capital_restant -= capital_mensuel
        
        # Mise à jour des cumuls
        cumul_interets_payes += interets_annuels
        cumul_loyers_percus += loyer_annuel
        cumul_charges_payees += charges_annuelles
        
        revenu_locatif_imposable = loyer_annuel - charges_annuelles - interets_annuels
        impot_revenu_foncier = (revenu_locatif_imposable * taux_imposition / 100)
        cumul_impots_payes += impot_revenu_foncier
        
        # Calcul de la plus-value si vente cette année-là
        plus_value_brute, impot_plus_value, prelevements_sociaux = calcul_plus_value(
            prix_vente=prix_achat,  # On garde le même prix pour l'instant
            prix_achat=prix_achat,
            frais_acquisition=frais_acquisition,
            annees_detention=annee
        )
        
        # Bilan si vente cette année-là
        bilan_si_vente = {
            "Investissement initial": -cout_total_acquisition,
            "Prix de revente": prix_achat,
            "Plus-value brute": plus_value_brute,
            "Impôt plus-value": -impot_plus_value,
            "Prélèvements sociaux plus-value": -prelevements_sociaux,
            "Loyers perçus cumulés": cumul_loyers_percus,
            "Charges payées cumulées": -cumul_charges_payees,
            "Impôts payés cumulés": -cumul_impots_payes,
            "Intérêts payés cumulés": -cumul_interets_payes,
            "Capital restant dû": -capital_restant,
            "Résultat net": (prix_achat - cout_total_acquisition - impot_plus_value - prelevements_sociaux) + 
                           (cumul_loyers_percus - cumul_charges_payees - 
                            cumul_impots_payes - cumul_interets_payes)
        }
        
        placement_annee = placement_monetaire[annee-1]
        
        # Comparaison des investissements
        comparaison = {
            "Immobilier": {
                "Résultat net": bilan_si_vente["Résultat net"],
                "Détail": {
                    "Capital investi": -cout_total_acquisition,
                    "Prix de revente net": prix_achat - impot_plus_value - prelevements_sociaux,
                    "Revenus locatifs nets cumulés": cumul_loyers_percus - cumul_charges_payees - cumul_impots_payes,
                    "Intérêts payés cumulés": -cumul_interets_payes
                }
            },
            "Placement monétaire": {
                "Résultat net": placement_annee["Gain total net"],
                "Détail": {
                    "Capital": placement_annee["Capital"],
                    "Intérêts bruts cumulés": placement_annee["Capital"] - apport,
                    "Impôts cumulés": -(placement_annee["Capital"] - apport - placement_annee["Gain total net"])
                }
            },
            "Différence": bilan_si_vente["Résultat net"] - placement_annee["Gain total net"]
        }
        
        resultats_annuels.append({
            "Année": annee,
            "Capital restant dû (€)": capital_restant,
            "Intérêts payés (€)": interets_annuels,
            "Capital amorti (€)": capital_amorti_annuel,
            "Revenu imposable (€)": revenu_locatif_imposable,
            "Impôts (€)": impot_revenu_foncier,
            "Bilan si vente": bilan_si_vente,
            "Comparaison placements": comparaison
        })
    
    return {
        "Prix d'achat (€)": prix_achat,
        "Frais d'acquisition (€)": frais_acquisition,
        "Coût total acquisition (€)": cout_total_acquisition,
        "Apport initial (€)": apport,
        "Montant emprunté (€)": montant_emprunte,
        "Mensualité (€)": mensualite,
        "Détail année par année": resultats_annuels
    }

# Exemple d'utilisation
resultats = calcul_rentabilite(
    prix_achat=320000,
    loyer_mensuel=1400,
    taux_credit=3.3,
    duree_annees=20,
    charges_mensuelles=170,
    taxe_fonciere=1100,
    taux_imposition=30.0+17.2,
    apport=140000
)

# Affichage des résultats année par année
print("\nComparaison des investissements année par année:")
for annee in resultats["Détail année par année"]:
    print(f"\nAnnée {annee['Année']}:")
    comp = annee["Comparaison placements"]
    print(f"  Immobilier: {comp['Immobilier']['Résultat net']:,.2f} €")
    print(f"  Placement monétaire: {comp['Placement monétaire']['Résultat net']:,.2f} €")
    print(f"  Différence: {comp['Différence']:,.2f} €")
    print(f"  {'✓ Immobilier gagnant' if comp['Différence'] > 0 else '✓ Placement monétaire gagnant'}")
