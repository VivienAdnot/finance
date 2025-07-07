import matplotlib.pyplot as plt
import numpy as np

years1 = ['2012','2013']
scores1 = [0.2, 0.3]

years2 = ['2013','2014','2015']
scores2 = [0.5, -0.4, 0.8]

#convert string list to integer list
y1 = list(map(int, years1))
y2 = list(map(int, years2))

plt.plot(y1, scores1, marker="o")
plt.plot(y2, scores2, marker="o")
plt.xticks(y1+y2)

plt.show()