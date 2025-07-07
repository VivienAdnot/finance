import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# Définition des taux d'imposition
FLAT_TAX_RATE = 0.30  # 30% (12.8% IR + 17.2% prélèvements sociaux)

def update_fund_value(fund_value, monetary_fund_rate, monetary_fund_volatility, additional_contribution):
    """ Met à jour la valeur du fonds avec variation aléatoire du taux monétaire """
    fund_rate_variation = random.uniform(-monetary_fund_volatility, monetary_fund_volatility)
    actual_monetary_fund_rate = monetary_fund_rate + fund_rate_variation
    return (fund_value + additional_contribution) * (1 + actual_monetary_fund_rate / 100)

def simulate_investment():
    """ Simule l'investissement et applique la flat tax au moment du retrait """
    # Variables initiales
    initial_cash = 140000  # Montant investi au départ
    monetary_fund_rate = 2  # Taux d'intérêt moyen (%)
    monetary_fund_volatility = 0.5  # Volatilité des taux (%)
    years = 30 # Durée de l'investissement
    additional_contribution = 0  # Ajout de capital (fixe à 0 ici)

    fund_value = initial_cash  # Valeur initiale du fonds
    data = []

    for year in range(1, years + 1):
        fund_value = update_fund_value(fund_value, monetary_fund_rate, monetary_fund_volatility, additional_contribution)
        roi = fund_value - initial_cash  # Plus-value brute

        data.append([year, fund_value, roi])

    # Calcul de la flat tax au moment du retrait
    total_gain = fund_value - initial_cash
    final_tax = total_gain * FLAT_TAX_RATE
    fund_value_after_tax = fund_value - final_tax
    net_gain_after_tax = total_gain - final_tax

    # Résumé des résultats
    print("\n📊 **Récapitulatif de l'investissement** 📊")
    print(f"🔹 Montant investi : {initial_cash:,.2f} €")
    print(f"🔹 Valeur finale avant impôt : {fund_value:,.2f} €")
    print(f"🔹 Plus-value totale : {total_gain:,.2f} €")
    print(f"🔹 Flat tax (30%) : {final_tax:,.2f} €")
    print(f"🔹 Montant récupéré après impôt : {fund_value_after_tax:,.2f} €")
    print(f"🔹 Plus-value nette après impôt : {net_gain_after_tax:,.2f} €\n")

    return data, total_gain, net_gain_after_tax

def run_simulation():
    """ Exécute la simulation et affiche le graphique de l'évolution de l'investissement """
    data, total_gain, net_gain_after_tax = simulate_investment()

    df = pd.DataFrame(data, columns=['Année', 'Valeur du Fonds', 'Plus-Value Brute'])

    # Calcul de la plus-value nette après impôt
    df["Plus-Value Nette"] = df["Plus-Value Brute"] * (1 - FLAT_TAX_RATE)

    # Création du graphique
    plt.figure(figsize=(10, 5))

    # Courbe de la valeur du fonds
    plt.plot(df["Année"], df["Valeur du Fonds"], label="Valeur du Fonds (€)", linestyle='-', marker='o', color='blue')

    # Courbe de la plus-value brute
    plt.plot(df["Année"], df["Plus-Value Brute"], label="Plus-Value Brute (€)", linestyle='--', color='green')

    # Courbe de la plus-value nette après impôt
    plt.plot(df["Année"], df["Plus-Value Nette"], label="Plus-Value Nette après Flat Tax (€)", linestyle='--', color='red')

    # Ligne horizontale pour montrer la plus-value nette finale
    plt.axhline(y=net_gain_after_tax, color='purple', linestyle=':', label=f"Plus-Value Nette Finale: {net_gain_after_tax:,.2f} €")

    plt.xlabel("Années")
    plt.ylabel("Valeur (€)")
    plt.legend()
    plt.title("Évolution de l'Investissement et Impact de la Flat Tax")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    run_simulation()
