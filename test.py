# from algo2 import Trader

# from datamodel import Listing, OrderDepth, Trade, TradingState

# timestamp = 1000

# listings = {
# 	"PEARLS": Listing(
# 		symbol="PRODUCT1", 
# 		product="PRODUCT1", 
# 		denomination= "SEASHELLS"
# 	),
# 	"BANANAS": Listing(
# 		symbol="BANANAS", 
# 		product="BANANAS", 
# 		denomination= "SEASHELLS"
# 	),
# }

# order_depths = {
# 	"PEARLS": OrderDepth(),
# 	"BANANAS": OrderDepth(),	
# }

# order_depths["PEARLS"].buy_orders[10002] = 140
# order_depths["PEARLS"].sell_orders[9000] = -10

# own_trades = {
# 	"PEARLS": [
# 		Trade(
# 			symbol="PEARLS",
# 			price=11,
# 			quantity=4,
# 			buyer="SUBMISSION",
# 			seller="",
# 			timestamp=1000
# 		),
# 		Trade(
# 			symbol="PEARLS",
# 			price=12,
# 			quantity=3,
# 			buyer="SUBMISSION",
# 			seller="",
# 			timestamp=1000
# 		)
# 	],
# 	"BANANAS": [
# 		Trade(
# 			symbol="BANANAS",
# 			price=143,
# 			quantity=2,
# 			buyer="",
# 			seller="SUBMISSION",
# 			timestamp=1000
# 		),
# 	]
# }

# market_trades = {
# 	"PEARLS": [
# 		Trade(
# 			symbol="PEARLS",
# 			price=10002,
# 			quantity=4,
# 			buyer="",
# 			seller="",
# 			timestamp=900
# 		)
# 	],
# 	"BANANAS": []
# }

# position = {
# 	"PEARLS": 20,
# 	"BANANAS": -5
# }

# observations = {}

# state = TradingState(
# 	timestamp,
#     listings,
# 	order_depths,
# 	own_trades,
# 	market_trades,
#     position,
#     observations
# )

# Trader().run(state)

class MovingAverage:
	def __init__(self, num):
		self.num = num
		self.array = []
		self.sum = 0

	def isReady(self):
		return len(self.array) == self.num

	def calculateMA(self):
		return self.sum / len(self.array)

	def updateMA(self, numba):
		if self.isReady():
			self.sum -= self.array.pop(0)
		self.array.append(numba)
		self.sum += numba
		

test = MovingAverage(20)

for i in range(1, 101):
	print(i)
	test.updateMA(i)
	if (test.isReady()):
		print(test.calculateMA())
