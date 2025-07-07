import unittest
from portfolio import Portfolio

class TestPorfolio(unittest.TestCase):
  def build_portfolio(self, cash=None):
    _cash = cash if cash else 500.00
    lines = {
      'SPY': {
        'book': [10.00, 10.00, 10.00, 10.00, 10.00, 15.00, 15.00],
        'market_price': 15.00
      },
      'GLD': {
        'book': [70.00, 70.00, 70.00],
        'market_price': 70.00
      }
    }
    default_portfolio = Portfolio(cash=_cash, lines=lines)
    return default_portfolio

  def test_lines(self):
    portfolio = self.build_portfolio()
    self.assertEqual(list(portfolio.lines.keys()), ['SPY', 'GLD'])

  def test_value(self):
    portfolio = self.build_portfolio()
    self.assertEqual(portfolio.value, 815.00)
    self.assertEqual(portfolio.value_history, [815.00])

  def test_update_market_price(self):
    portfolio = self.build_portfolio()
    self.assertEqual(portfolio.value, 815.00)
    self.assertEqual(portfolio.value_history, [815.00])

    portfolio.update_market_price(ticker='SPY', market_price=20.00)
    self.assertEqual(portfolio.lines['SPY']['market_price'], 20.00)
    self.assertEqual(portfolio.value, 850.00)
    self.assertEqual(portfolio.value_history, [815.00, 850.00])

    portfolio.update_market_price(ticker='GLD', market_price=90.00)
    self.assertEqual(portfolio.lines['GLD']['market_price'], 90.00)
    self.assertEqual(portfolio.value, 910.00)
    self.assertEqual(portfolio.value_history, [815.00, 850, 910.00])

  def test_buy_should_be_ok(self):
    portfolio = self.build_portfolio()
    self.assertEqual(len(portfolio.lines['SPY']['book']), 7)
    
    portfolio.buy_at_market(units=10, ticker='SPY', price=10.00)
    self.assertEqual(len(portfolio.lines['SPY']['book']), 17)
    self.assertEqual(portfolio.cash, 395.38)
    # the value has decreased because SPY value is back at 10, not 15
    self.assertEqual(portfolio.value, 775.38)
    self.assertEqual(portfolio.value_history, [815.0, 780.0, 775.38])

  def test_buy_should_raise_error(self):
    portfolio = Portfolio(cash=10.00)
    try:
      portfolio.buy_at_market(units=10, ticker='SPY', price=10.00)
    except ValueError as err:
      self.assertEqual(err.args[0], '10.0€ cash available is insufficient to buy 10 units of SPY at 10.0€ with a fee of 4.62€')
      self.assertEqual(portfolio.cash, 10.00)

  def test_sell_high_should_increase_value(self):
    portfolio = self.build_portfolio()
    portfolio.update_market_price(ticker='GLD', market_price=90.00)
    self.assertEqual(portfolio.value_history, [815.00, 875.00])

    portfolio.sell_at_market(ticker='GLD', units=2)
    self.assertEqual(portfolio.cash, 675.23)
    self.assertEqual(portfolio.value, 870.23)
    # the value has not changed, we just transformed stocks into cash
    self.assertEqual(portfolio.value_history, [815.0, 875.0, 870.23])

  def test_sell_all(self):
    portfolio = self.build_portfolio()
    portfolio.sell_all_at_market()
    self.assertEqual(portfolio.cash, 815.00)
    self.assertEqual(len(portfolio.lines['SPY']['book']), 0)
    self.assertEqual(len(portfolio.lines['GLD']['book']), 0)

  def test_get_average_book_price(self):
    portfolio = self.build_portfolio()
    self.assertEqual(portfolio.get_average_book_price('SPY'), 11.43)
    self.assertEqual(portfolio.get_average_book_price('GLD'), 70.00)

  def test_get_latent_profit(self):
    portfolio = self.build_portfolio()
    portfolio.update_market_price(ticker='SPY', market_price=20.00)
    portfolio.update_market_price(ticker='GLD', market_price=90.00)
    self.assertEqual(portfolio.get_latent_profit('SPY'), 59.99)
    self.assertEqual(portfolio.get_latent_profit('GLD'), 60.00)

  # def test_sell_fee_degiro(self):
  #   portfolio = self.build_portfolio()
  #   market_price = 20.00
  #   portfolio.update_market_price(ticker='SPY', market_price=market_price)
  #   units_to_remove = len(portfolio.lines['SPY']['book'])
    
  #   for _ in range(units_to_remove):
  #     book_price = self.lines[ticker]['book'].pop()
  #     # print(f'sell_at_market:: {self.cash} + {market_price} => {round(self.cash + market_price, 2)}')
  #     profit_or_loss = market_price - book_price

  #   book_price = portfolio.lines['SPY']['book'].pop()
  #   profit_or_loss = market_price - book_price
