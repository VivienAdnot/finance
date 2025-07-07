import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------- 1. Tickers --------
tickers = {
    "Equities_1": "SPY",
    "Equities_2": "VXUS",
    "Bonds_1": "HYG",
    "Bonds_2": "VCIT",
    "REITs_1": "VNQ",
    "REITs_2": "REM",
    "Stress_1": "GLD",
    "Stress_2": "TLT",
    "Cash": "BIL"
}

# -------- 2. Télécharger données mensuelles --------
data = yf.download(list(tickers.values()), start="2017-01-01", interval="1mo", auto_adjust=True)["Close"]
data.dropna(inplace=True)

# -------- 3. Initialisation --------
initial_capital = 10000
weights = {"Equities": 0.25, "Bonds": 0.25, "REITs": 0.25, "Stress": 0.25}
modules = ["Equities", "Bonds", "REITs", "Stress"]
portfolio = []
entry_prices = {m: None for m in modules}
held_assets = {m: None for m in modules}
tax_rate = 0.30

# Historique
history = []

# -------- 4. Backtest --------
dates = data.index
capital = initial_capital

for i in range(12, len(dates)):
    date = dates[i]
    past = dates[i - 12]
    current_prices = data.loc[date]
    past_prices = data.loc[past]

    bil_return = (current_prices[tickers["Cash"]] / past_prices[tickers["Cash"]] - 1) * 100

    selected_assets = {}
    module_perf = {m: 0 for m in modules}

    for mod in modules:
        a1 = tickers[f"{mod}_1"]
        a2 = tickers[f"{mod}_2"]

        r1 = (current_prices[a1] / past_prices[a1] - 1) * 100
        r2 = (current_prices[a2] / past_prices[a2] - 1) * 100

        best = a1 if r1 > r2 else a2
        selected = best if max(r1, r2) > bil_return else tickers["Cash"]
        selected_assets[mod] = selected

        weight = weights[mod]
        old_asset = held_assets[mod]
        new_asset = selected

        try:
            # Cas 1 : Vente et rachat d’un nouvel actif
            if old_asset and old_asset != new_asset:
                old_price = current_prices[old_asset]
                buy_price = entry_prices[mod]
                if buy_price:
                    gain = (old_price - buy_price) / buy_price
                    if gain > 0:
                        taxed_cap = capital * weight * (1 - tax_rate * gain)
                    else:
                        taxed_cap = capital * weight
                else:
                    taxed_cap = capital * weight
            else:
                taxed_cap = capital * weight

            # Réinvestissement
            prev_price = data.iloc[i - 1][new_asset]
            ret = current_prices[new_asset] / prev_price
            module_perf[mod] = taxed_cap * ret
            held_assets[mod] = new_asset
            entry_prices[mod] = current_prices[new_asset]

        except Exception as e:
            print(f"Erreur dans le module {mod} ({new_asset}) : {e}")
            module_perf[mod] = capital * weight  # fallback

    capital = sum(module_perf.values())
    portfolio.append(capital)

    history.append({
        "Date": date,
        "Portfolio": capital,
        "Equities": module_perf["Equities"],
        "Bonds": module_perf["Bonds"],
        "REITs": module_perf["REITs"],
        "Stress": module_perf["Stress"],
        "Asset_Equities": selected_assets["Equities"],
        "Asset_Bonds": selected_assets["Bonds"],
        "Asset_REITs": selected_assets["REITs"],
        "Asset_Stress": selected_assets["Stress"]
    })

# -------- 5. Résultats --------
df = pd.DataFrame(history).set_index("Date")
returns = df["Portfolio"].pct_change().dropna()
cagr = (df["Portfolio"].iloc[-1] / df["Portfolio"].iloc[0]) ** (1 / (len(df) / 12)) - 1
volatility = returns.std() * np.sqrt(12)
max_dd = ((df["Portfolio"] / df["Portfolio"].cummax()) - 1).min()
sharpe = (cagr - 0.02) / volatility

# -------- 6. Affichage & Export --------
print("\n--- Résultats avec fiscalité CTO ---")
print(f"Valeur finale: {df['Portfolio'].iloc[-1]:.2f} $")
print(f"CAGR: {cagr:.2%}")
print(f"Volatilité annualisée: {volatility:.2%}")
print(f"Max Drawdown: {max_dd:.2%}")
print(f"Sharpe Ratio (RF 2%): {sharpe:.2f}")

df.to_csv("signals_and_perf_taxed.csv")
print("\n✅ Exporté vers 'signals_and_perf_taxed.csv'")

# -------- 7. Courbe du portefeuille --------
plt.figure(figsize=(12,6))
plt.plot(df.index.to_numpy(), df["Portfolio"].to_numpy(), label="Portefeuille (net fiscalité)", color="darkblue")
plt.title("Composite Dual Momentum (CTO avec fiscalité)")
plt.xlabel("Date")
plt.ylabel("Valeur du portefeuille ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# -------- 8. Corrélation des modules --------
module_df = df[["Equities", "Bonds", "REITs", "Stress"]]
module_returns = module_df.pct_change().dropna()
corr = module_returns.corr()

plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Corrélation entre modules (mensuelle)")
plt.tight_layout()
plt.show()
