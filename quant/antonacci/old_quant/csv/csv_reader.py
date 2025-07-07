import csv
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

dates = []
prices = []

def parseCsv(reader):
  for index, row in enumerate(reader):
    # 2000 dotcom bubble crash
    # if index > 0 and index < 350:

    # 2008 financial crisis
    # if index > 0 and index < 250:

    # 2020 covid-19 pandemic
    if index > 0 and index < 100:

    # 1980 bond market crash
    # if index > 0 and index < 100:

    # 1970s oil crisis
    # if index > 0:
      values = row[0].split(',')
      year = int(values[1])
      month = int(values[2])
      price = int(values[3])
      # print(year, month, price)

      date = datetime.date(year, month, 1)
      dates.append(date)
      prices.append(price)
  dates.reverse()
  prices.reverse()

def graph():
  fig, ax = plt.subplots()
  locator = mdates.AutoDateLocator()
  formatter = mdates.ConciseDateFormatter(locator)
  ax.xaxis.set_major_locator(locator)
  ax.xaxis.set_major_formatter(formatter)
  plt.xlabel('Date')
  plt.ylabel('Price')
  # ax.grid(True)

  # Plotting the line chart
  ax.plot(dates, prices)

  # Calculate the condition based on price comparison with the price 12 months ago
  condition_ok = [prices[i] > prices[i-12] if i >= 12 else False for i in range(len(prices))]
  condition_not_ok = [prices[i] <= prices[i-12] if i >= 12 else True for i in range(len(prices))]

  # Coloring the background based on the condition
  plt.fill_between(dates, 0, prices, where=condition_ok, color='green', alpha=0.3)
  plt.fill_between(dates, 0, prices, where=condition_not_ok, color='red', alpha=0.3)

  # Rotate x-axis tick labels for better readability if needed
  plt.xticks(rotation=45)

  plt.show()

with open('sp500.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  parseCsv(reader)
  graph()