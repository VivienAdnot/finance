import csv

with open('papa_bear.csv', mode='w') as papa_bear_file:
    papa_bear_file_writer = csv.writer(papa_bear_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    papa_bear_file_writer.writerow(['round', 'year', 'month', 'current_winners_indices', 'cash before', 'value', 'losers_to_sell' ,'winners_to_buy', 'tickers_with_price', 'cash after', 'absolute value variation'])
    papa_bear_file_writer.writerow([0, 0, 0, [], 1000.00, 1000.00, [], [4], 'SPY:500', 500.00, 0.00])