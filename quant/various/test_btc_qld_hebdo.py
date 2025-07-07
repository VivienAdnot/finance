import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Télécharger les données
TICKER_BTC = 'BTC-USD'
TICKER_QLD = 'QLD'

btc_data = yf.download(TICKER_BTC, start='2018-01-01', interval='1wk', group_by='ticker', auto_adjust=True)
qld_data = yf.download(TICKER_QLD, start='2018-01-01', interval='1wk', group_by='ticker', auto_adjust=True)

btc_prices = btc_data[(TICKER_BTC, 'Close')]
qld_prices = qld_data[(TICKER_QLD, 'Close')]

# 2. Aligner les dates communes
common_dates = btc_prices.index.intersection(qld_prices.index)
btc_prices = btc_prices.loc[common_dates]
qld_prices = qld_prices.loc[common_dates]

# 3. Paramètres
initial_capital = 1000
cash_yield_annual = 0.02
cash_yield_weekly = (1 + cash_yield_annual) ** (1/52) - 1
ema_span = 12  # 12 semaines par défaut (3 mois)

# 4. Calculer les EMA
btc_ema = btc_prices.ewm(span=ema_span, adjust=False).mean()
qld_ema = qld_prices.ewm(span=ema_span, adjust=False).mean()

# 5. Simulation de la stratégie
capital = initial_capital
portfolio = []
status = []

for i in range(1, len(common_dates)):
    btc_now = btc_ema.iloc[i]
    qld_now = qld_ema.iloc[i]
    btc_prev = btc_ema.iloc[i-1]
    qld_prev = qld_ema.iloc[i-1]

    btc_perf = (btc_now / btc_prev) - 1
    qld_perf = (qld_now / qld_prev) - 1

    if btc_perf > qld_perf:
        best_perf = btc_perf
        selected_price_now = btc_prices.iloc[i]
        selected_price_prev = btc_prices.iloc[i-1]
        selected_asset = 'BTC'
    else:
        best_perf = qld_perf
        selected_price_now = qld_prices.iloc[i]
        selected_price_prev = qld_prices.iloc[i-1]
        selected_asset = 'QLD'

    # Seuil pour ne pas investir si faible dynamique
    if best_perf > 0:
        capital *= (selected_price_now / selected_price_prev)
        status.append(selected_asset)
    else:
        capital *= (1 + cash_yield_weekly)
        status.append('Cash')

    portfolio.append(capital)

# 6. Résultats
portfolio_df = pd.DataFrame({
    'Date': common_dates[1:],  # car on commence à partir de i=1
    'Portfolio_Value': portfolio,
    'Status': status
}).set_index('Date')

final_value = portfolio_df['Portfolio_Value'].iloc[-1]
total_years = (portfolio_df.index[-1] - portfolio_df.index[0]).days / 365.25
cagr = (final_value / initial_capital) ** (1 / total_years) - 1

weekly_returns = portfolio_df['Portfolio_Value'].pct_change().dropna()
volatility_annual = weekly_returns.std() * np.sqrt(52)

rolling_max = portfolio_df['Portfolio_Value'].cummax()
drawdowns = (portfolio_df['Portfolio_Value'] - rolling_max) / rolling_max
max_drawdown = drawdowns.min()

sharpe_ratio = (cagr - cash_yield_annual) / volatility_annual if volatility_annual != 0 else np.nan

# 7. Affichage
print("\n--- Résultats de la stratégie EMA Weekly ---")
print(f"Final Value: {final_value:.2f}")
print(f"CAGR: {cagr:.2%}")
print(f"Max Drawdown: {max_drawdown:.2%}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# 9. Durée des trades - Analyse complète

# Créer une série avec les périodes où on reste dans le même actif
status_series = pd.Series(status, index=common_dates[1:])
switches = status_series != status_series.shift(1)

# Marquer les débuts de nouveaux trades
trade_ids = switches.cumsum()

# Grouper par trades
durations = trade_ids.value_counts().sort_index()

# Stats descriptives
min_duration = durations.min()
max_duration = durations.max()
mean_duration = durations.mean()
median_duration = durations.median()
std_duration = durations.std()

print("\n--- Analyse des durées de trades ---")
print(f"Nombre de trades: {len(durations)}")
print(f"Durée minimale: {min_duration} semaines")
print(f"Durée maximale: {max_duration} semaines")
print(f"Durée moyenne: {mean_duration:.2f} semaines")
print(f"Durée médiane: {median_duration:.2f} semaines")
print(f"Écart-type: {std_duration:.2f} semaines")



# 8. Plot
plt.figure(figsize=(14,6))
plt.plot(portfolio_df.index.to_numpy(), portfolio_df['Portfolio_Value'].to_numpy(), label='Portfolio Value')

plt.title('Performance Portfolio (EMA Weekly Dual Momentum)')
plt.xlabel('Date')
plt.ylabel('Capital ($)')
plt.grid(True)
plt.legend()
plt.show()
