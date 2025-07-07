import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------- 1. Tickers --------
tickers = {
    "Equities_1": "SPY",    # S&P 500
    "Equities_2": "VXUS",   # World ex-US
    "Bonds_1": "HYG",       # High Yield Bonds
    "Bonds_2": "VCIT",      # Intermediate Corporate Bonds
    "REITs_1": "VNQ",       # Equity REITs
    "REITs_2": "REM",       # Mortgage REITs
    "Stress_1": "GLD",      # Gold
    "Stress_2": "TLT",      # Long Treasuries
    "Cash": "BIL"           # 1–3 month T-Bills
}

# -------- 2. Télécharger données ajustées mensuelles --------
data = yf.download(list(tickers.values()), start="2017-01-01", interval="1mo", auto_adjust=True)["Close"]
data.dropna(inplace=True)

# -------- 3. Initialisation --------
initial_capital = 10000
weights = {"Equities": 0.25, "Bonds": 0.25, "REITs": 0.25, "Stress": 0.25}
modules = ["Equities", "Bonds", "REITs", "Stress"]
portfolio = []
module_values = {m: [] for m in modules}

# -------- 4. Backtest --------
dates = data.index
capital = initial_capital
history = []

for i in range(12, len(dates)):  # Commencer après 12 mois pour avoir un lookback
    date = dates[i]
    past = dates[i - 12]
    current_prices = data.loc[date]
    past_prices = data.loc[past]

    bil_return = (current_prices[tickers["Cash"]] / past_prices[tickers["Cash"]] - 1) * 100

    selected_assets = {}

    # --- Module Equities ---
    r1 = (current_prices[tickers["Equities_1"]] / past_prices[tickers["Equities_1"]] - 1) * 100
    r2 = (current_prices[tickers["Equities_2"]] / past_prices[tickers["Equities_2"]] - 1) * 100
    best = tickers["Equities_1"] if r1 > r2 else tickers["Equities_2"]
    selected_assets["Equities"] = best if max(r1, r2) > bil_return else tickers["Cash"]

    # --- Module Bonds ---
    r1 = (current_prices[tickers["Bonds_1"]] / past_prices[tickers["Bonds_1"]] - 1) * 100
    r2 = (current_prices[tickers["Bonds_2"]] / past_prices[tickers["Bonds_2"]] - 1) * 100
    best = tickers["Bonds_1"] if r1 > r2 else tickers["Bonds_2"]
    selected_assets["Bonds"] = best if max(r1, r2) > bil_return else tickers["Cash"]

    # --- Module REITs ---
    r1 = (current_prices[tickers["REITs_1"]] / past_prices[tickers["REITs_1"]] - 1) * 100
    r2 = (current_prices[tickers["REITs_2"]] / past_prices[tickers["REITs_2"]] - 1) * 100
    best = tickers["REITs_1"] if r1 > r2 else tickers["REITs_2"]
    selected_assets["REITs"] = best if max(r1, r2) > bil_return else tickers["Cash"]

    # --- Module Stress ---
    r1 = (current_prices[tickers["Stress_1"]] / past_prices[tickers["Stress_1"]] - 1) * 100
    r2 = (current_prices[tickers["Stress_2"]] / past_prices[tickers["Stress_2"]] - 1) * 100
    best = tickers["Stress_1"] if r1 > r2 else tickers["Stress_2"]
    selected_assets["Stress"] = best if max(r1, r2) > bil_return else tickers["Cash"]

    # --- Allocation & Rebalancing ---
    module_perf = {}
    for mod in modules:
        asset = selected_assets[mod]
        ret = current_prices[asset] / data.iloc[i - 1][asset]
        module_value = capital * weights[mod] * ret
        module_values[mod].append(module_value)
        module_perf[mod] = module_value

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
        "Asset_Stress": selected_assets["Stress"],
    })


# -------- 5. Résultats --------
df = pd.DataFrame(history).set_index("Date")
returns = df["Portfolio"].pct_change().dropna()
cagr = (df["Portfolio"].iloc[-1] / df["Portfolio"].iloc[0]) ** (1 / (len(df) / 12)) - 1
volatility = returns.std() * np.sqrt(12)
max_dd = ((df["Portfolio"] / df["Portfolio"].cummax()) - 1).min()
sharpe = (cagr - 0.02) / volatility

print("\n--- Résultats ---")
print(f"Valeur finale: {df['Portfolio'].iloc[-1]:.2f} $")
print(f"CAGR: {cagr:.2%}")
print(f"Volatilité annualisée: {volatility:.2%}")
print(f"Max Drawdown: {max_dd:.2%}")
print(f"Sharpe Ratio (RF 2%): {sharpe:.2f}")

df.to_csv("signals_and_perf.csv")
print("\n--- Fichier 'signals_and_perf.csv' exporté avec les signaux mensuels ---")


# -------- 6. Courbe --------
plt.figure(figsize=(12,6))
plt.plot(df.index.to_numpy(), df["Portfolio"].to_numpy(), label="Portefeuille")

plt.title("Composite Dual Momentum - Portefeuille")
plt.ylabel("Valeur ($)")
plt.xlabel("Date")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# -------- 7. Corrélation entre modules --------
module_df = df[["Equities", "Bonds", "REITs", "Stress"]]
module_returns = module_df.pct_change().dropna()
corr = module_returns.corr()

print("\n--- Corrélation des modules ---")
print(corr)

plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Corrélation mensuelle entre modules")
plt.tight_layout()
plt.show()
