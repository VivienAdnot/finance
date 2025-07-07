import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------- 1. Tickers --------
tickers = {
    "Equities_1": "SPY",    # S&P 500
    "Equities_2": "VXUS",   # World ex-US
    "Bonds_1": "Hyg",       # High Yield Bonds
    "Bonds_2": "VCIT",      # Intermediate Corporate Bonds
    "REITs_1": "VNQ",       # Equity REITs
    "REITs_2": "REM",       # Mortgage REITs
    "Stress_1": "GLD",      # Gold
    "Stress_2": "TLT",      # Long Treasuries
    "Cash": "BIL"           # 1–3 month T-Bills
}

# -------- 2. Télécharger données ajustées mensuelles --------
data = yf.download(list(tickers.values()), start="2017-01-01", interval="1mo", auto_adjust=True)["Close"]
data.columns = data.columns.str.upper()  # Uniformiser les noms en majuscules
data.dropna(inplace=True)

# -------- 3. Uppercase dans le dict tickers aussi --------
tickers = {k: v.upper() for k, v in tickers.items()}


# -------- 3. Initialisation --------
initial_capital = 10000
weights = {"Equities": 0.25, "Bonds": 0.25, "REITs": 0.25, "Stress": 0.25}
modules = ["Equities", "Bonds", "REITs", "Stress"]
portfolio = []
module_values = {m: [] for m in modules}
held_assets = {m: None for m in modules}
buy_prices = {m: None for m in modules}
tax_log = []

# -------- 4. Backtest --------
dates = data.index
capital = initial_capital
history = []

for i in range(12, len(dates)):
    date = dates[i]
    past = dates[i - 12]
    current_prices = data.loc[date]
    past_prices = data.loc[past]

    bil_return = (current_prices[tickers["Cash"]] / past_prices[tickers["Cash"]] - 1) * 100
    selected_assets = {}

    for module in modules:
        t1 = tickers[f"{module}_1"]
        t2 = tickers[f"{module}_2"]
        r1 = (current_prices[t1] / past_prices[t1] - 1) * 100
        r2 = (current_prices[t2] / past_prices[t2] - 1) * 100
        best = t1 if r1 > r2 else t2
        selected = best if max(r1, r2) > bil_return else tickers["Cash"]
        selected_assets[module] = selected

    module_perf = {}
    for mod in modules:
        asset = selected_assets[mod]
        prev_asset = held_assets[mod]
        capital_mod = capital * weights[mod]

        # Calcul plus-value si on vend un ancien actif
        if prev_asset is not None and prev_asset != asset:
            old_price = current_prices[prev_asset]
            buy_price = buy_prices[mod]
            if buy_price is not None:
                gain = old_price - buy_price
                gain_value = gain / buy_price * capital_mod
                tax = 0.3 * gain_value
                capital -= tax
                tax_log.append([date.year, mod, prev_asset, asset, gain_value, tax])

        held_assets[mod] = asset
        buy_prices[mod] = current_prices[asset]
        ret = current_prices[asset] / data.iloc[i - 1][asset]
        module_value = capital_mod * ret
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

# Tax log export
tax_df = pd.DataFrame(tax_log, columns=["Année", "Module", "Ancien_Actif", "Nouvel_Actif", "Plus-value", "Taxe"])

tax_df.to_csv("tax_log_fixed.csv", index=False)
df.to_csv("signals_and_perf_taxed_fixed.csv")

plt.figure(figsize=(12,6))
plt.plot(df.index.to_numpy(), df["Portfolio"].to_numpy(), label="Portefeuille")
plt.title("Composite Dual Momentum avec fiscalité corrigée")
plt.ylabel("Valeur ($)")
plt.xlabel("Date")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
