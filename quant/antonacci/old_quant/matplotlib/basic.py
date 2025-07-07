import random
import matplotlib.pyplot as plt

curr = 1000
values = [1000]
for _ in range(180):
  increment = random.randint(-50, 50)
  curr = curr + increment
  values.append(curr)

plt.plot(values)

# plt.xlim(0.5, 4.5)

plt.show()