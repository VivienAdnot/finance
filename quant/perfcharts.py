import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Performance Comparée (PerfCharts style)")

tickers_input = st.text_input("Entrez des tickers séparés par des virgules", value="BIL,SPY,VXUS")

if tickers_input:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]

    # Télécharger les données sur 1 an (1d interval)
    data = yf.download(tickers, period="1y", interval="1d", auto_adjust=True)["Close"]

    # Supprimer les colonnes vides (si ticker invalide)
    data = data.dropna(axis=1, how="all")

    if data.empty:
        st.error("Aucune donnée disponible. Vérifie les tickers.")
    else:
        rebased = (data / data.iloc[0] - 1) * 100

        fig = go.Figure()
        for ticker in rebased.columns:
            fig.add_trace(go.Scatter(
                x=rebased.index,
                y=rebased[ticker],
                mode='lines',
                name=f"{ticker} ({rebased[ticker].iloc[-1]:.2f}%)",
                hovertemplate='%{x}<br>%{y:.2f}%<extra></extra>'
            ))

        fig.update_layout(
            title="Comparaison des performances (base 0%)",
            xaxis_title="Date",
            yaxis_title="Performance (%)",
            xaxis=dict(
                showgrid=True,
                tickformat="%b\n%Y",         # Affiche Mois + Année
                dtick="M1",                  # Tick tous les mois
                tickangle=-45
            ),
            yaxis=dict(showgrid=True),
            height=700
        )


        st.plotly_chart(fig, use_container_width=True)
