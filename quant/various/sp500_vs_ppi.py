import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Charger les données simulées depuis le CSV
df = pd.read_csv("sp500_ppi_gold_bonds_1950_2024.csv", parse_dates=["Date"])
df.set_index("Date", inplace=True)

# Calcul des ratios logarithmiques
df["Log_SP500_PPI"] = np.log(df["SP500"] / df["PPIACO"])
df["Log_Gold_PPI"] = np.log(df["Gold"] / df["PPIACO"])
df["Log_Bond_PPI"] = np.log(df["US10Y_Bond"] / df["PPIACO"])

# Définir les périodes inflation/déflation historiques (exemples stylisés)
periods = [
    ("Déflation", "1950-01-01", "1965-12-31"),
    ("Inflation", "1966-01-01", "1982-12-31"),
    ("Déflation", "1983-01-01", "1999-12-31"),
    ("Inflation", "2000-01-01", "2012-12-31"),
    ("Déflation", "2013-01-01", "2019-12-31"),
    ("Inflation", "2020-01-01", "2023-12-31"),
]
periods = [(label, pd.to_datetime(start), pd.to_datetime(end)) for label, start, end in periods]

# Affichage
fig, ax = plt.subplots(figsize=(14, 7))

# Tracer les 3 courbes
ax.plot(df.index.to_numpy(), df["Log_SP500_PPI"].to_numpy(), label="log(S&P 500 / PPI)", color="steelblue")
ax.plot(df.index.to_numpy(), df["Log_Gold_PPI"].to_numpy(), label="log(Gold / PPI)", color="goldenrod")
ax.plot(df.index.to_numpy(), df["Log_Bond_PPI"].to_numpy(), label="log(Bonds 10Y / PPI)", color="seagreen")


# Bandes inflation / déflation
for label, start, end in periods:
    ax.axvspan(start, end, color='lightblue' if label == "Déflation" else 'mistyrose', alpha=0.4)
    ax.text((start + (end - start) / 2), ax.get_ylim()[0] + 0.1, label,
            ha='center', va='bottom', fontsize=9, alpha=0.6)

# Mise en forme
ax.set_title("Ratios log(S&P 500 / PPI), log(Or / PPI), log(Obligations 10Y / PPI) (1950–2024)")
ax.set_ylabel("Ratio logarithmique")
ax.set_xlabel("Année")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
plt.tight_layout()
plt.show()
