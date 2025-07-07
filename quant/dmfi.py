import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ['BIL', 'SHY', 'IEF', 'TLT', 'LQD', 'HYG']
start_date = '2018-05-01'
end_date = '2024-05-01'

data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
momentum = data.pct_change(63)  # ~3 mois

portfolio = pd.Series(index=data.index, dtype='float64')
current_etf = None

for date in data.resample('M').last().index:
    if date not in momentum.index:
        continue
    best = momentum.loc[date].dropna()
    best = best[best > 0]
    if not best.empty:
        current_etf = best.idxmax()
    if current_etf:
        portfolio.loc[date] = data.loc[date, current_etf]

portfolio.ffill(inplace=True)
returns = portfolio.pct_change().fillna(0)
cumulative = (1 + returns).cumprod()

plt.figure(figsize=(12, 6))
plt.plot(cumulative, label='DMFI - Top 1 momentum')
plt.title('Backtest DMFI 2018–2024')
plt.ylabel('Capital')
plt.xlabel('Date')
plt.grid(True)
plt.legend()
plt.show()
