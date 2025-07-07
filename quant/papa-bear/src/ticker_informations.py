tickers_informations = {
  0: {
    'exchange': 'NASDAQ',
    'ticker': 'IEF',
    'full_name': '7-10 Year Treasury Bond',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  1: {
    'exchange': 'NASDAQ',
    'ticker': 'VNQ',
    'full_name': 'Real Estate',
    'etf_provider': 'Vanguard',
    'etf_brand': 'Vanguard'
  },
  2: {
    'exchange': 'NYSEARCA',
    'ticker': 'EEM',
    'full_name': 'MSCI Emerging Markets',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  3: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWF',
    'full_name': 'Russell 1000 Growth',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  4: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWN',
    'full_name': 'Russell 2000 Value',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  5: {
    'exchange': 'NASDAQ',
    'ticker': 'TLT',
    'full_name': '20+ Year Treasury Bond',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  6: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWO',
    'full_name': 'Russell 2000 Growth',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  7: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWD',
    'full_name': 'Russell 1000 Value',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  8: {
    'exchange': 'NYSEARCA',
    'ticker': 'EFA',
    'full_name': 'Diversified Europe, Australia, Asia, and the Far East',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  9: {
    'exchange': 'NYSEARCA',
    'ticker': 'GLD',
    'full_name': 'Gold',
    'etf_provider': 'State Street Global Advisors',
    'etf_brand': 'State Street Global Advisors'
  },
  10: {
    'exchange': 'NYSEARCA',
    'ticker': 'DBC',
    'full_name': 'Commodities',
    'etf_provider': 'PowerShares',
    'etf_brand': 'PowerShares'
  }
}

def get_ticker_from_indice(indice):
  return tickers_informations[indice]['ticker']

def get_tickers_from_indices(indices):
  result = []
  for indice in indices:
    result.append(tickers_informations[indice]['ticker'])
  return result