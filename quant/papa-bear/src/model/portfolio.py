from typing import List

class Portfolio:
  cash: float # euros ?
  lines = {}
  value: float # euros ?
  value_history = []
  month = 0
  year=0
  taxes_profit_loss_year_history = []
  taxes_to_pay = 0
  paid_tax_history = {}

  def __init__(self, cash = 0.00, lines = None):
    self.value = 0.00
    self.value_history = []
    self.cash = cash
    self.lines = lines if lines else {}
    # print('portfolio init  -> update_value()')
    self.update_value()

  def pay_government_taxes(self):
    taxes_to_pay = 0.0
    total_year_profit_loss = round(sum(self.taxes_profit_loss_year_history), 2)

    self.paid_tax_history[self.year] = {
      'paid': False,
      'amount': 0,
      'P&L gross': total_year_profit_loss,
      'P&L gross %': round(total_year_profit_loss * 100 / self.value, 2),
      'P&L net': 0.0
    }
    # print(f'{self.year}: total_year_profit_loss: {total_year_profit_loss}')

    if total_year_profit_loss < 0:
      self.paid_tax_history[self.year]['paid'] = True
      self.paid_tax_history[self.year]['amount'] = 0
      self.paid_tax_history[self.year]['P&L net'] = round(total_year_profit_loss, 2)
      self.paid_tax_history[self.year]['P&L net %'] = round(total_year_profit_loss * 100 / self.value, 2)
      print(f'no need to pay taxes this year ({self.year})')
      return

    # in case we didn't finish to pay last year taxes
    self.taxes_to_pay = round(self.taxes_to_pay + total_year_profit_loss * 0.3, 2)
    taxes_to_pay = self.taxes_to_pay
    self.paid_tax_history[self.year]['P&L net'] = round(total_year_profit_loss - self.taxes_to_pay, 2)
    self.paid_tax_history[self.year]['P&L net %'] = round((total_year_profit_loss - self.taxes_to_pay) * 100 / self.value, 2)

    if total_year_profit_loss < 0:
      self.paid_tax_history[self.year]['paid'] = True
      self.paid_tax_history[self.year]['amount'] = 0
      print(f'no need to pay taxes this year ({self.year})')
      return

    # print(f'{self.year}: taxes_to_pay: {self.taxes_to_pay}')

    print(f'{self.year}: try pay {self.taxes_to_pay}€ taxes with {self.cash}€ cash.')

    self.taxes_profit_loss_year_history.clear()
    # if portfolio has enough cash
    if self.cash > self.taxes_to_pay:
      self.cash = round(self.cash - self.taxes_to_pay, 2)
      # print(f'paid whole taxes. cash is now {self.cash}')
      self.paid_tax_history[self.year]['paid'] = True
      self.paid_tax_history[self.year]['amount'] = self.taxes_to_pay
      self.taxes_to_pay = 0
    # if we do not have enough cash
    else:
      self.taxes_to_pay = self.taxes_to_pay - self.cash
      print(f'{self.year}: partially paid taxes. {self.taxes_to_pay} left to pay')
      self.cash = 0
    # print('pay gvnt tax  -> update_value()')
    self.update_value()
    return taxes_to_pay

  def compute_pending_taxes(self, new_profit_or_loss):
    self.taxes_profit_loss_year_history.append(new_profit_or_loss)

  def update_value(self):
    new_value = self.cash
    # print('new_value start', new_value)
    
    for ticker, book in self.lines.items():
      # print(ticker, book)
      market_price = book['market_price']
      units = len(book['book'])
      if units:
        line_value = round(market_price * units, 2)
        # print('line_value', line_value)

        new_value = round(new_value + line_value, 2)
        # print('new_value increment', new_value)
    # no need to update if value has not changed
    if self.value != new_value:
      self.value = new_value
      self.value_history.append(self.value)
      # print('new value', self.value, self.value_history)

  def update_market_price(self, ticker, market_price):
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    self.lines[ticker]['market_price'] = market_price
    # print('update_market_price  -> update_value()')
    self.update_value()

  def buy_at_market(self, units, ticker, price):
    # print(f'buy_at_market with {self.cash}',  units, ticker, price)
    # this method also updates inner book value
    self.update_market_price(ticker=ticker, market_price=price)
    buy_fee = self.compute_buy_fee_DeGiro_US_non_free_trackers(market_price=price, units=units)
    # print('buy fee', buy_fee)
    # this fee lowers our profit
    self.compute_pending_taxes(-buy_fee)
    
    cost = round(units * price, 2)
    cost_with_fee = round(units * price + buy_fee, 2)
    # print('cost', cost)
    # print('cost_with_fee', cost_with_fee)
    if self.cash < cost_with_fee:
      raise ValueError(f'{self.cash}€ cash available is insufficient to buy {units} units of {ticker} at {price}€ with a fee of {buy_fee}€')
    self.cash = round(self.cash - cost, 2)
    # print(f'buy at market {units} units of {ticker} at {price}$. cash is now {self.cash}')
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    
    for _ in range(units):
      self.lines[ticker]['book'].append(price)

    self.pay_broker_fee(buy_fee, fee_type='buy')
    return buy_fee

  def should_pay_tax(self):
    # print(f'should_pay_tax ? month is {self.month}, year is {self.year}, paid_tax_history is {self.paid_tax_history}, result is {self.month == 1 and self.year not in self.paid_tax_history}')
    return self.month >= 1 and self.year != 2006 and self.year not in self.paid_tax_history
    # or self.paid_tax_history[self.year]['paid'] == False)

  # assume we use degiro platform
  def compute_buy_fee_DeGiro_US_non_free_trackers(self, market_price, units, fx_fee=True, free_ETF=False):
    total_price = market_price * units
    # if we use free DeGiro ETF, this will be free
    trading_fee = 2.00 + (total_price * 0.02 / 100) if free_ETF == False else 0.00
    # if we use US trackers instead of FR
    currency_change_fee = (total_price * 0.1 / 100) if fx_fee == True else 0.00
    # degiro collects a fixed fee to connect with US exchanges
    # London Stock Exchange € 0.00 (for both positions and transaction(s))
    # Euronext Derivatives € 2.50 (for transactions)
    # Eurex € 2.50 (for transactions)
    # NYSE € 2.50 (for holding positions)
    giro_exchange_connection_fee = 2.50

    total_fee = trading_fee + currency_change_fee + giro_exchange_connection_fee
    return round(total_fee, 2)

  # assume we use degiro platform
  def compute_broker_sell_fee_DeGiro_US_non_free_trackers(self, market_price, book_price, units):
    total_price = market_price * units
    # base rate of 2.00 + variable rate of 0.02%
    broker_sell_fee = 2.00 + total_price * 0.02 / 100
    # assume it's 0.03€ per 100€
    broker_sell_fee_spread = total_price * 0.03 / 100
    # if we use US trackers instead of FR
    currency_change_fee = total_price * 0.1 / 100
    # degiro collects a fixed fee to connect with US exchanges
    # London Stock Exchange € 0.00 (for both positions and transaction(s))
    # Euronext Derivatives € 2.50 (for transactions)
    # Eurex € 2.50 (for transactions)
    # NYSE € 2.50 (for holding positions)
    giro_exchange_connection_fee = 2.50

    total_fee = broker_sell_fee + broker_sell_fee_spread + currency_change_fee + giro_exchange_connection_fee
    return round(total_fee, 2)

  def pay_broker_fee(self, fee_amount, fee_type):
    self.cash = round(self.cash - fee_amount, 2)
    # print(f'paid {fee_amount}€ {fee_type} fee')
    # print('pay_broker_fee  -> update_value()')
    self.update_value()

  # units None means sell all
  # update_market_price is called outside of the method
  def sell_at_market(self, ticker, units = None):
    government_tax = 0.0
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines. Cannot sell')
    units_count = len(self.lines[ticker]['book'])
    if units and units_count < units:
      raise ValueError(f'line has {units_count} units but we want to sell {units}. Sell only {units_count}')
    units_to_remove = units if units and units < units_count else units_count
    market_price = self.lines[ticker]['market_price']
    average_book_price = self.get_average_book_price(ticker=ticker)

    broker_sell_fee = self.compute_broker_sell_fee_DeGiro_US_non_free_trackers(
      market_price=market_price, book_price=average_book_price, units=units_to_remove)

    profit_or_loss = -broker_sell_fee
    for _ in range(units_to_remove):
      book_price = self.lines[ticker]['book'].pop()
      profit_or_loss = profit_or_loss + (market_price - book_price)
      # print(f'sell_at_market:: {self.cash} + {market_price} => {round(self.cash + market_price, 2)}')
      self.cash = round(self.cash + market_price, 2)
    
    self.compute_pending_taxes(profit_or_loss)
    
    # january: time to pay our taxes
    if self.should_pay_tax():
      government_tax = self.pay_government_taxes()

    self.pay_broker_fee(broker_sell_fee, 'sell')

    return (broker_sell_fee, government_tax)

  def sell_all_at_market(self):
    for ticker in self.lines:
      market_price = self.lines[ticker]['market_price']
      for _ in range(len(self.lines[ticker]['book'])):
        self.lines[ticker]['book'].pop()
        self.cash = round(self.cash + market_price, 2)

  def get_average_book_price(self, ticker):
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines.')
    book = self.lines[ticker]['book']
    if len(book) == 0:
      return 0
    return round(sum(book) / len(book), 2)

  def get_latent_profit(self, ticker):
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines.')
    average_book_price = self.get_average_book_price(ticker)
    units = len(self.lines[ticker]['book'])
    market_price = self.lines[ticker]['market_price']
    return round((market_price * units) - (average_book_price * units), 2)