import yfinance as yf
import pandas as pd
from datetime import datetime

def get_stock_prices(tickers):
    """Récupère les prix actuels et historiques pour une liste de tickers"""
    
    print(f"🔍 Récupération des données pour: {', '.join(tickers)}")
    print("-" * 50)
    
    for ticker in tickers:
        try:
            print(f"\n📊 Analyse de {ticker}:")
            
            # Créer l'objet ticker
            stock = yf.Ticker(ticker)
            
            # Récupérer les informations de base
            info = stock.info
            print(f"   Nom: {info.get('longName', 'N/A')}")
            
            # Prix actuel
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if current_price:
                print(f"   Prix actuel: ${current_price:.2f}")
            
            # Données historiques (1 mois pour tester)
            hist = stock.history(period="1mo")
            if not hist.empty:
                latest_close = hist['Close'].iloc[-1]
                print(f"   Dernier cours de clôture: ${latest_close:.2f}")
                print(f"   Nombre de jours de données: {len(hist)}")
                print(f"   Première date: {hist.index[0].strftime('%Y-%m-%d')}")
                print(f"   Dernière date: {hist.index[-1].strftime('%Y-%m-%d')}")
                
                # Performance du mois
                first_close = hist['Close'].iloc[0]
                performance = ((latest_close - first_close) / first_close) * 100
                print(f"   Performance du mois: {performance:.2f}%")
            else:
                print(f"   ❌ Aucune donnée historique disponible")
                
        except Exception as e:
            print(f"   ❌ Erreur pour {ticker}: {str(e)}")

if __name__ == "__main__":
    # Tickers de votre fichier perfcharts.py
    tickers = ["BIL", "SPY", "VXUS"]
    get_stock_prices(tickers)
