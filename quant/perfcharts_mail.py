import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import os

# Paramètres
tickers = ["SPY", "VXUS", "BIL"]
output_html = "perfchart.html"
dropbox_local_path = os.path.expanduser("~/Dropbox/perfcharts/")
full_html_path = os.path.join(dropbox_local_path, output_html)

# Télécharger données ajustées (1 an)
data = yf.download(tickers, period="1y", interval="1d", auto_adjust=True)["Close"]

# Rebaser à 0% pour comparatif de performance
rebased = (data / data.iloc[0] - 1) * 100

# Créer le graphique interactif
fig = go.Figure()
for ticker in tickers:
    fig.add_trace(go.Scatter(x=rebased.index, y=rebased[ticker], mode='lines', name=ticker))

fig.update_layout(
    title="Performance relative - Base 0%",
    xaxis_title="Date",
    yaxis_title="Performance (%)",
    template="plotly_white"
)

# Sauvegarder le fichier HTML dans Dropbox
os.makedirs(dropbox_local_path, exist_ok=True)
fig.write_html(full_html_path)

print("✅ Graphique enregistré dans Dropbox :", full_html_path)
print("🔗 N'oublie pas de créer un lien partageable Dropbox :")
print("    https://www.dropbox.com/home/perfcharts  → clic droit → 'Créer un lien'")
