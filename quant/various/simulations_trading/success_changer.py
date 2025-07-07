# import of libraries
import random
import matplotlib.pyplot as plt

# instanciation of needed objects
rnd = random.Random()

def successChanger(capital, successRate1, successRate2, realSet, gain, loss, spread, numberFlips):
	result = []
	startedCapital = capital
	successRate = 0
	lossRate = 0

	i = numberFlips
	while i > 0 and capital > 0:
		if i > (numberFlips * realSet):
			successRate = successRate1
			lossRate = 100 - successRate1
		else:
			successRate = successRate2
			lossRate = 100 - successRate2

		a = rnd.choices([gain, loss], weights=(successRate, lossRate))

		capital = capital + a[0] - spread
		result.append(capital)
		if capital <= 0:
			break
		i-=1

	# figsize: width and height in inches
	# plt.figure(figsize=(12,5))
	plt.axhline(startedCapital, color="gray") # horizontal gray line
	plt.axvline(startedCapital * realSet, color="gray") # vertical gray line

	# print(result)
	plt.plot(result)
	plt.show()
	plt.close()

successChanger(
    capital=1000,
    successRate1=94,
    successRate2=50,
	# taille de la deuxième partie de la simulation (première = backtest, deuxième = réel)
    realSet=0.5,
    gain=22.5,
    loss=-47.4,
    spread=1,
    numberFlips=1000
)