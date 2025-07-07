# from portfolio import Portfolio
from model.portfolio import Portfolio
import math

class PapaBearPortfolio(Portfolio):
  def sell_losers(self, tickers):
    for loser_ticker in tickers:
      self.sell_at_market(loser_ticker)
    pass

  def compute_ticker_units_to_buy(self, tickers_with_price):
    results = []
    number_assets = len(tickers_with_price)
    max_cash_available_per_asset = round(self.cash / number_assets, 2)
    # print('max_cash_available_per_asset', max_cash_available_per_asset)

    # sorted_tickers_by_gain_desc = sorted(tickers_with_price, key=lambda tup: tup[2], reverse=True)
    # amount = 0

    for (ticker, price, average_gain) in tickers_with_price:
      units = 0
      keep_looping = True
      while keep_looping:
        units += 1
        buy_fee = self.compute_buy_fee_DeGiro_US_non_free_trackers(market_price=price, units=units)
        cost = round((price * units) + buy_fee, 2)
        if cost > max_cash_available_per_asset:
          keep_looping = False
          # do not add 0 units in results
          if units > 1:
            less_units = units - 1
            smaller_buy_fee = self.compute_buy_fee_DeGiro_US_non_free_trackers(market_price=price, units=less_units)
            # print(ticker, less_units, price, smaller_buy_fee, round(price * less_units, 2), round((price * less_units) + smaller_buy_fee, 2))
            results.append((ticker, less_units, price))
            # amount = amount + cost
    
    # second round for filling the rest
    # rest = self.cash - amount
    # if rest > 0:
    #   for (ticker, price, average_gain) in sorted_tickers_by_gain_desc:
    #     buy_fee = self.compute_buy_fee_DeGiro_US_non_free_trackers(market_price=price, units=1)
    #     cost = price + buy_fee
    #     if cost < rest:
    #       amount = amount + cost
    #       rest = self.cash - amount
    #       print(f'buy 1 more unit of {ticker} at {price}€')
    #       results.append((ticker, 1, price))

    return results

  def buy_winners(self, tickers_with_price):
    # print('buy winners')
    result = []
    tickers_with_price_and_units = self.compute_ticker_units_to_buy(tickers_with_price)
    # print()
    for (ticker, units, price) in tickers_with_price_and_units:
      # print()
      buy_fee = self.buy_at_market(units=units, ticker=ticker, price=price)
      # print(ticker, units, price, buy_fee)
      result.append((ticker, units, price, buy_fee))
    return result