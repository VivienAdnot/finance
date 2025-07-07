# import of libraries
import random
import matplotlib.pyplot as plt

# instanciation of needed objects
rnd = random.Random()

counter_gain = 0
counter_loss = 0

def log_gain_loss(value):
	global counter_gain
	global counter_loss
	if (value > 0):
		counter_gain += 1
	else:
		counter_loss += 1

# declaration of  backtest
def backtest(capital, successRate, gain, loss, spread, numberFlips):
	resultat = []
	trade = 0
	
	failureRate = 100 - successRate
	i = numberFlips

	while i > 0 and capital > 0:
		trade = rnd.choices([gain, loss], weights=(successRate, failureRate))
		log_gain_loss(trade[0])
		
		capital = capital + spread + trade[0]
		resultat.append(capital)
		if capital <= 0:
			break
		i-=1
	return resultat

# Example of backtest function calling
startupCapital = 13000
resultat = backtest(
	capital=startupCapital,
	successRate=50,
	gain=26,
	loss=-24,
	spread=-1,
	numberFlips=10000
)
print(counter_gain, counter_loss)

# create an empty chart with a width of 12 and height of 5
plt.figure(figsize=(12,5))
# draw a horizontal line
# plt.axhline(startupCapital, color="gray")
plt.plot(resultat)
plt.show()
plt.close()