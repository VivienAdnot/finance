import numpy as np
from utils import get_3_max_values, average, compute_percentage_gain, increment_month, convert_to_year, convert_to_month, convert_to_year_15_years_ago
from logger import Logger
from ticker_informations import get_ticker_from_indice, get_tickers_from_indices

# average of current price, 1 month ago, 3 month ago, 6 month ago
def compute_average_gains(rows):
  average_gains = []
  for row_index, row in enumerate(rows):
    average_gains.append([])
    # we need at least 6 month of data
    if row_index >= 6:
      # print('row_index:', row_index)
      for cell_idx, cell in enumerate(row):
        # print( 'cell_idx:', cell_idx, 'cell:', cell)
        current_value = cell
        value_1_month_ago = rows[row_index - 1][cell_idx]
        value_3_month_ago = rows[row_index - 3][cell_idx]
        value_6_month_ago = rows[row_index - 6][cell_idx]

        # print('current_value: ', current_value)
        # print('value_1_month_ago: ', value_1_month_ago)
        # print('value_3_month_ago: ', value_3_month_ago)
        # print('value_6_month_ago: ', value_6_month_ago)

        percentage_gain_1_month = compute_percentage_gain(
          value_current=current_value,
          value_previous=value_1_month_ago
        )
        percentage_gain_3_month = compute_percentage_gain(
          value_current=current_value,
          value_previous=value_3_month_ago
        )
        percentage_gain_6_month = compute_percentage_gain(
          value_current=current_value,
          value_previous=value_6_month_ago  
        )

        # print('percentage_gain_1_month: ', percentage_gain_1_month)
        # print('percentage_gain_3_month: ', percentage_gain_3_month)
        # print('percentage_gain_6_month: ', percentage_gain_6_month)

        average_gain = average(percentage_gain_1_month, percentage_gain_3_month, percentage_gain_6_month)
        # print('average_gain: ', average_gain)
        average_gains[row_index].append(average_gain)
  return average_gains

# determines losers and new winners
def compute_winners_losers(
  current_winners_indices,
  new_winners_indices):

  winners_to_buy = []
  losers_to_sell = []
  keep_previous_winners = []
  
  for index, item in enumerate(current_winners_indices):
    # item_index, shares_amount = item
    if item not in new_winners_indices:
      # losers_to_sell.append((index, item))
      losers_to_sell.append(item)
    else:
      keep_previous_winners.append(item)

  for index, item in enumerate(new_winners_indices):
    if item not in current_winners_indices:
      # winners_to_buy.append((index, item))
      winners_to_buy.append(item)

  return (losers_to_sell, winners_to_buy, keep_previous_winners)

def perform_main_logic(rows, portfolio, portfolio_value):
  logger = Logger()
  average_gains = compute_average_gains(rows)
  # print('average_gains', average_gains)

  current_winners_indices = []
  # month_index will go from 1 to 12
  # we start on 1
  # month_index = 0

  # print('------ loop avg_gain_rows ------')
  for row_index, row in enumerate(average_gains):
    portfolio.month = convert_to_month(row_index)
    portfolio.year = convert_to_year_15_years_ago(row_index)
    if (row_index >= 6):
      print(f'new row: {row_index}')
      cash_before = portfolio.cash
      value_before = portfolio.value

      # print('avg_gains_row_idx', row_index)
      # print('current_winners_indices before arbitrage', current_winners_indices)
      # print(result[0])

      new_winners_indices, new_average_gains = get_3_max_values(row)
      # print('new_winners_indices', new_winners_indices)
      # print('new_average_gains', new_average_gains)
      
      losers_to_sell, winners_to_buy, keep_previous_winners = compute_winners_losers(current_winners_indices, new_winners_indices)
      for keep_ticker_indice in keep_previous_winners:
        ticker = get_ticker_from_indice(keep_ticker_indice)
        new_price = rows[row_index][keep_ticker_indice]
        # print(keep_ticker_indice, ticker, new_price)
        portfolio.update_market_price(ticker=ticker, market_price=new_price)

      # print('losers_to_sell', losers_to_sell)
      losers_tickers_with_price = []
      government_taxes = []
      broker_sell_fees = []
      for loser_ticker_indice in losers_to_sell:
        ticker = get_ticker_from_indice(loser_ticker_indice)
        new_price = rows[row_index][loser_ticker_indice]
        # print(loser_ticker_indice, ticker, new_price)
        portfolio.update_market_price(ticker=ticker, market_price=new_price)
        latent_profit = f'{portfolio.get_latent_profit(ticker)}€'
        units = len(portfolio.lines[ticker]['book'])
        (sell_broker_fee, government_tax) = portfolio.sell_at_market(ticker=ticker)
        broker_sell_fees.append(sell_broker_fee)
        government_taxes.append(government_tax)
        losers_tickers_with_price.append((ticker, latent_profit, f'{units} at {new_price}€'))

      # print('cash after sell', portfolio.cash)

      # print('winners_to_buy', winners_to_buy)
      winners_tickers_with_price = []
      winners_tickers_with_price_and_units = []
      for winner_ticker_indice in winners_to_buy:
        ticker = get_ticker_from_indice(winner_ticker_indice)
        price = rows[row_index][winner_ticker_indice]
        average_gain = row[winner_ticker_indice]
        # print('winner_ticker_indice', winner_ticker_indice, 'row average_gain', average_gain)
        winners_tickers_with_price.append((ticker, price, average_gain))
        # print('winners_tickers_with_price', winners_tickers_with_price)
      if len(winners_tickers_with_price):
        winners_tickers_with_price_and_units = portfolio.buy_winners(winners_tickers_with_price)
        # print('cash after buy', portfolio.cash)

      logger.log(
        portfolio=portfolio,
        round=row_index,
        current_winners_indices=get_tickers_from_indices(current_winners_indices),
        new_winners_indices=get_tickers_from_indices(new_winners_indices),
        cash_before=cash_before,
        keep_previous_winners=keep_previous_winners,
        losers_to_sell=losers_tickers_with_price,
        broker_sell_fees=broker_sell_fees,
        winners_to_buy=winners_tickers_with_price_and_units,
        cash_after=portfolio.cash,
        value=portfolio.value,
        value_variation_absolute=round(portfolio.value-value_before, 2),
        government_taxes=government_taxes
      )

      current_winners_indices[:] = new_winners_indices
      portfolio_value.append(portfolio.value)
      # print('current_winners_indices after arbitrage', current_winners_indices)
  # print('------ end loop avg_gain_rows ------')