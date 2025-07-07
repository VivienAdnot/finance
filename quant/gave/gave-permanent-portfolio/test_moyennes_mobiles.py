import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Télécharger les données mensuelles depuis 1989
start_date = "2020-01-01"
end_date = "2025-04-01"

TICKER_SP500 = 'VOO'
TICKER_GOLD = 'GOLDAMGBD228NLBM'

# SP500 Total Return (dividendes réinvestis) + prix de l'or spot
data = yf.download([TICKER_SP500, TICKER_GOLD], start=start_date, end=end_date, interval='1mo')['Adj Close']

print("data downloadée", data)
data.to_csv("data_sp500_gold.csv")

data.columns = [TICKER_SP500, TICKER_GOLD]
data = data.dropna()

# Calcul du ratio et de la moyenne mobile 84 mois (7 ans)
data['SP500/Gold'] = data[TICKER_SP500] / data[TICKER_GOLD]
data['Ratio_MA84'] = data['SP500/Gold'].rolling(window=84).mean()

# Signal d'allocation : actions si ratio > moyenne mobile, sinon cash
data['In_Equities'] = data['SP500/Gold'] > data['Ratio_MA84']

# Détecter les transitions
transitions = data['In_Equities'].astype(int).diff()
print("Transitions détectées", transitions)
# On ne garde que les transitions significatives
sell_dates = data.index[transitions == -1]
buy_dates = data.index[transitions == 1]

# Afficher les années de transition
sell_years = sorted(set(pd.DatetimeIndex(sell_dates).year))
buy_years = sorted(set(pd.DatetimeIndex(buy_dates).year))

print("Années où on VEND les actions :", sell_years)
print("Années où on RACHÈTE les actions :", buy_years)

# Afficher la timeline avec les périodes en cash en rouge
fig, ax = plt.subplots(figsize=(14, 2))
ax.plot(data.index, [1]*len(data), color='lightgray')  # ligne de base

# Bandes rouges = périodes en cash
in_cash = ~data['In_Equities']
start = None
for i in range(len(in_cash)):
    if in_cash.iloc[i] and start is None:
        start = data.index[i]
    elif not in_cash.iloc[i] and start is not None:
        ax.axvspan(start, data.index[i], color='red', alpha=0.4)
        start = None
if start is not None:
    ax.axvspan(start, data.index[-1], color='red', alpha=0.4)

ax.set_yticks([])
ax.set_title("Périodes en cash (rouge) - stratégie SP500/Or vs MM84")
ax.set_xlim(data.index.min(), data.index.max())
plt.tight_layout()
plt.show()
