import yfinance as yf
import pandas as pd
from datetime import datetime

def test_ticker_download(ticker):
    """Teste le téléchargement d'un ticker spécifique"""
    print(f"\n=== Test pour {ticker} ===")
    
    try:
        # Méthode 1: Ticker object
        print(f"Méthode 1 - Ticker object pour {ticker}...")
        ticker_obj = yf.Ticker(ticker)
        data1 = ticker_obj.history(period="1y", auto_adjust=True)
        
        if not data1.empty:
            print(f"✅ Méthode 1 réussie: {len(data1)} points de données")
            print(f"Colonnes: {list(data1.columns)}")
            print(f"Dernier prix: {data1['Close'].iloc[-1]:.2f}")
            return data1
        else:
            print("❌ Méthode 1 échouée: DataFrame vide")
            
    except Exception as e:
        print(f"❌ Méthode 1 échouée: {str(e)}")
    
    try:
        # Méthode 2: yf.download
        print(f"Méthode 2 - yf.download pour {ticker}...")
        data2 = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
        
        if not data2.empty:
            print(f"✅ Méthode 2 réussie: {len(data2)} points de données")
            print(f"Colonnes: {list(data2.columns)}")
            if 'Close' in data2.columns:
                print(f"Dernier prix: {data2['Close'].iloc[-1]:.2f}")
            return data2
        else:
            print("❌ Méthode 2 échouée: DataFrame vide")
            
    except Exception as e:
        print(f"❌ Méthode 2 échouée: {str(e)}")
    
    print(f"❌ Toutes les méthodes ont échoué pour {ticker}")
    return pd.DataFrame()

if __name__ == "__main__":
    # Test des tickers utilisés dans perfcharts.py
    tickers = ["BIL", "SPY", "VXUS"]
    
    print("=== Test des tickers de perfcharts.py ===")
    print(f"Date: {datetime.now()}")
    
    results = {}
    for ticker in tickers:
        data = test_ticker_download(ticker)
        results[ticker] = data
    
    print("\n=== Résumé ===")
    for ticker, data in results.items():
        if not data.empty:
            print(f"✅ {ticker}: {len(data)} points de données")
        else:
            print(f"❌ {ticker}: Échec")
    
    # Test avec d'autres tickers populaires pour comparaison
    print("\n=== Test avec tickers alternatifs ===")
    alt_tickers = ["AAPL", "MSFT", "GOOGL"]
    
    for ticker in alt_tickers:
        data = test_ticker_download(ticker)
        if not data.empty:
            print(f"✅ {ticker} fonctionne bien")
        else:
            print(f"❌ {ticker} ne fonctionne pas non plus")
