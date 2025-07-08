import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import warnings

# Configuration pour supprimer les warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")
st.title("Asset Performance Comparison Dashboard")

@st.cache_data(ttl=600)
def download_ticker_cached(ticker):
    """Télécharge les données d'un ticker avec cache"""
    try:
        # Essayer avec yfinance
        data = yf.Ticker(ticker).history(period="1y", auto_adjust=True)
        
        if not data.empty and 'Close' in data.columns:
            return data
        else:
            # Essayer avec une période plus courte
            data = yf.Ticker(ticker).history(period="6mo", auto_adjust=True)
            return data
            
    except Exception:
        return pd.DataFrame()

def download_ticker_with_retry(ticker):
    """Télécharge un ticker avec gestion d'erreurs"""
    data = download_ticker_cached(ticker)
    
    if not data.empty:
        return data
    else:
        st.error(f"❌ {ticker}: Impossible de télécharger les données")
        return pd.DataFrame()

# Interface utilisateur
col1, col2 = st.columns([3, 1])

# Session state pour les tickers
if 'tickers_input' not in st.session_state:
    st.session_state.tickers_input = "BIL,SPY,VXUS"

with col1:
    tickers_input = st.text_input("Entrez des tickers séparés par des virgules", 
                                  value=st.session_state.tickers_input)

with col2:
    if st.button("🔄 Réinitialiser cache"):
        st.cache_data.clear()
        st.success("Cache vidé!")

# Boutons prédéfinis pour tickers populaires
st.write("**Groupes d'actifs:**")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("World Stocks"):
        st.cache_data.clear()
        st.session_state.tickers_input = "BIL,SPY,VXUS"
        st.rerun()
with col2:
    if st.button("Bonds"):
        st.cache_data.clear()
        st.session_state.tickers_input = "BIL,HYG,VCIT"
        st.rerun()
with col3:
    if st.button("Real Estate"):
        st.cache_data.clear()
        st.session_state.tickers_input = "BIL,VNQ,REM"
        st.rerun()
with col4:
    if st.button("Economic Stress"):
        st.cache_data.clear()
        st.session_state.tickers_input = "BIL,GLD,TLT"
        st.rerun()

# Traitement principal
if tickers_input:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
    
    # Télécharger les données
    data = pd.DataFrame()
    
    with st.spinner("Téléchargement des données..."):
        for ticker in tickers:
            ticker_data = download_ticker_with_retry(ticker)
            
            if not ticker_data.empty:
                data[ticker] = ticker_data['Close']

    # Supprimer les colonnes vides
    data = data.dropna(axis=1, how="all")

    if data.empty:
        st.error("Aucune donnée disponible. Vérifiez les tickers ou essayez plus tard.")
    else:
        # Calculer les performances relatives (base 0%)
        rebased = (data / data.iloc[0] - 1) * 100

        # Créer le graphique
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
                tickformat="%b\n%Y",
                dtick="M1",
                tickangle=-45
            ),
            yaxis=dict(showgrid=True),
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)
