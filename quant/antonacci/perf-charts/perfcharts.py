import yfinance as yf
import pandas as pd
import numpy as np

# Télécharger les données des 2 ETF sur une période de 2 ans pour avoir suffisamment de données
tickers = ['VOO', 'BIL']
data = yf.download(tickers, start="2022-10-01", end="2024-10-01", interval='1mo')['Adj Close']

#data = yf.download(tickers, period="1y", interval='1mo')['Adj Close']
print(data)

# Calculer les rendements cumulatifs sur 12 mois
cumulative_returns = (data / data.shift(12) - 1) * 100
print(cumulative_returns)

# Calculer l'excès de rendement de VOO sur BIL
excess_return = cumulative_returns['VOO'] - cumulative_returns['BIL']

# Afficher les résultats
print("Cumulative Excess Return (VOO over BIL) at the end of each month:")
print(excess_return.dropna())