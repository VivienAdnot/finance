import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Définir la période d'analyse
start_date = "2010-01-01"
end_date = "2024-12-31"

# Télécharger les données depuis Yahoo Finance
tickers = {
    "S&P 500": "^GSPC",
    "Or": "GLD",
    "Obligations 10Y": "IEF"
}

data = yf.download(list(tickers.values()), start=start_date, end=end_date, interval="1mo", auto_adjust=True)["Adj Close"]
data.columns = tickers.keys()
data.dropna(inplace=True)

# Normaliser les données en base 100
data_norm = data / data.iloc[0] * 100

# Simuler des données macroéconomiques (croissance et inflation)
np.random.seed(42)
dates = data.index
growth = pd.Series(np.random.normal(0.5, 0.5, len(dates)), index=dates).rolling(3, min_periods=1).mean().clip(-2, 2)
inflation = pd.Series(np.random.normal(2.0, 1.0, len(dates)), index=dates).rolling(3, min_periods=1).mean().clip(-2, 8)

# Déterminer les régimes macroéconomiques selon Charles Gave
quadrants = []
for g, inf in zip(growth, inflation):
    if g > 0 and inf < 2:
        quadrants.append("Boom déflationniste")
    elif g > 0 and inf >= 2:
        quadrants.append("Boom inflationniste")
    elif g <= 0 and inf >= 2:
        quadrants.append("Récession inflationniste")
    else:
        quadrants.append("Déflation-dépression")

df_macro = pd.DataFrame({
    "Croissance": growth,
    "Inflation": inflation,
    "Quadrant": quadrants
}, index=dates)

# Définir les couleurs pour chaque régime
quadrant_colors = {
    "Boom déflationniste": "#a8dadc",
    "Boom inflationniste": "#f4a261",
    "Récession inflationniste": "#e76f51",
    "Déflation-dépression": "#457b9d"
}

# Identifier les changements de régime pour dessiner les bandes
df_macro["Change"] = df_macro["Quadrant"] != df_macro["Quadrant"].shift(1)
change_points = df_macro[df_macro["Change"]].index.to_list()
change_points.append(df_macro.index[-1])  # Ajouter la fin de la période

# Créer la liste des blocs (début, fin, étiquette, couleur)
blocks = []
for i in range(len(change_points) - 1):
    start = change_points[i]
    end = change_points[i + 1]
    label = df_macro.loc[start, "Quadrant"]
    color = quadrant_colors[label]
    blocks.append((start, end, label, color))

# Tracer le graphique
fig, ax = plt.subplots(figsize=(14, 6))

# Ajouter les bandes colorées
for start, end, label, color in blocks:
    ax.axvspan(start, end, color=color, alpha=0.2)

# Tracer les courbes des actifs
for asset in data_norm.columns:
    ax.plot(data_norm.index.to_numpy(), data_norm[asset].to_numpy(), label=asset)

# Mise en forme du graphique
ax.set_title("Performance des actifs (base 100) avec régimes macroéconomiques de Charles Gave")
ax.set_ylabel("Indice base 100")
ax.set_xlim(data_norm.index.min(), data_norm.index.max())
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend()

plt.tight_layout()
plt.show()
