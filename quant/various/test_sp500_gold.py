import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 📅 Paramètres
start_date = "1989-01-01"
end_date = "2025-04-01"

TICKER_SP500 = 'SPY'  # S&P 500 Total Return
TICKER_GOLD = 'GLD'       # Gold futures

# 📥 Télécharger les données
data = yf.download([TICKER_SP500, TICKER_GOLD], start=start_date, end=end_date, interval='1mo')
print("Colonnes récupérées :", data.columns)

# 🧹 Nettoyer : garder les prix de clôture uniquement
data = data['Close']
data.columns = ['Gold', 'SP500'] if TICKER_SP500 in data.columns[1] else ['SP500', 'Gold']
data = data.dropna()
data = data.copy()

# 📊 Ratio SP500 / Or + moyenne mobile 84 mois
data['SP500/Gold'] = data['SP500'] / data['Gold']
data['Ratio_MA84'] = data['SP500/Gold'].rolling(window=84).mean()

# 🧼 Supprimer les lignes incomplètes (évite les erreurs et la bande rouge à gauche)
data = data.dropna(subset=['SP500/Gold', 'Ratio_MA84'])

# 📅 Afficher la première date utilisable
print("📆 Première date avec données valides :", data.index.min().strftime('%Y-%m'))

# 📈 Générer le signal d'allocation
data['In_Equities'] = data['SP500/Gold'] > data['Ratio_MA84']

# 🧭 Transitions achat / vente
transitions = data['In_Equities'].astype(int).diff()
sell_dates = data.index[transitions == -1]
buy_dates = data.index[transitions == 1]

# 📋 Afficher les années de transitions
sell_years = sorted(set(pd.DatetimeIndex(sell_dates).year))
buy_years = sorted(set(pd.DatetimeIndex(buy_dates).year))
print("🔻 Années où on VEND les actions :", sell_years)
print("🔺 Années où on RACHÈTE les actions :", buy_years)

# 📈 Tracer ratio + moyenne + fond rouge pour périodes "cash"
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(data.index.to_numpy(), data['SP500/Gold'].to_numpy(), label='Ratio SP500 / Gold', color='blue')
ax.plot(data.index.to_numpy(), data['Ratio_MA84'].to_numpy(), label='Moyenne mobile 84 mois', color='orange', linestyle='--')

# 🟥 Fond rouge = périodes hors actions
in_cash = ~data['In_Equities']
start = None
for i in range(len(in_cash)):
    if in_cash.iloc[i] and start is None:
        start = data.index[i]
    elif not in_cash.iloc[i] and start is not None:
        ax.axvspan(start, data.index[i], color='red', alpha=0.2)
        start = None
if start is not None:
    ax.axvspan(start, data.index[-1], color='red', alpha=0.2)

# 🎨 Mise en forme
ax.set_title("Ratio SP500 / Or et moyenne mobile 84 mois\nZones rouges = périodes en cash")
ax.set_ylabel("Ratio")
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.show()
