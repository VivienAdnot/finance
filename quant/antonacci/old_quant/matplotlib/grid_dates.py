import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import random

def create_date_array(start, length):
  return [start + datetime.timedelta(days=(30.4 * i)) for i in range(length)]

start = datetime.date(2006, 7, 1)
dates = create_date_array(start, 180)
print(dates)

curr = 1000
values = [1000]
for _ in range(179):
  increment = random.randint(-50, 50)
  curr = curr + increment
  values.append(curr)

fig, ax = plt.subplots()
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
ax.grid(True)

ax.plot(dates, values)
plt.show()