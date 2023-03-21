from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Trade


class Trader:

    def __init__(self) -> None:
        self.sellcount = 0
        self.buycount = 0

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """ 
        # Initialize the method output dict as an empty dict
        result = {}
        # apparently can only buy/sell 20 per timestamp hence implemnted this
        pos_allowance = 20
        upperlimit = pos_allowance
        lowerlimit = -upperlimit
        
        margins = {"PEARLS" : (9998, 10002), "BANANAS": (4927, 4952)}

        #for debugging
        # Iterate over all the keys (the available products) contained in the order depths
        for product in ['PEARLS']:
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            # if product == 'PEARLS':
            current = 0
            if product in state.position.keys():
                current= state.position[product]

            # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            order_depth: OrderDepth = state.order_depths[product]

            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []
            # Define a fair value for the PEARLS.
            # Note that this value of 1 is just a dummy value, you should likely change it!
            ask_limit = margins[product][0]    
            bid_ceiling = margins[product][1]
            
            # trying to get access to prev trades but cant for some reason
            print(product, 'prev order: ')
            lst = list()
            if product in state.own_trades.keys():
                lst = state.own_trades[product]
            for traed in lst:
                print(traed.symbol , traed.price , traed.quantity)

            # If statement checks if there are any SELL orders in the PEARLS market
            while len(order_depth.sell_orders) > 0 and current < upperlimit:
                # Sort all the available sell orders by their price,
                # and select only the sell order with the lowest price
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = abs(order_depth.sell_orders[best_ask])
                
                if best_ask <= ask_limit:
                    buyvolume = min(upperlimit - current, best_ask_volume)
                    print("BUY", product, str(buyvolume) + "x", best_ask)
                    orders.append(Order(product, best_ask, buyvolume))

                    self.buycount += 1

                    current += buyvolume
                    order_depth.sell_orders[best_ask] += buyvolume
                    if (buyvolume == best_ask_volume):
                        order_depth.sell_orders.pop(best_ask)
                else: 
                    print("DID NOT BUY", best_ask)
                    break

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                # sign should be negative since it is a sell order
                
            
            current = 0
            if product in state.position.keys():
                current= state.position[product]
            while len(order_depth.buy_orders) > 0 and current > lowerlimit:
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = abs(order_depth.buy_orders[best_bid])
                if best_bid >= bid_ceiling:
                    sellvolume = min(current - lowerlimit, best_bid_volume)
                    print("SELL", product, str(sellvolume) + "x", best_bid)
                    orders.append(Order(product, best_bid, -sellvolume))
                    current -= sellvolume

                    self.sellcount += 1

                    order_depth.buy_orders[best_bid] -= sellvolume
                    if (sellvolume == best_bid_volume):
                        order_depth.buy_orders.pop(best_bid)
                else:
                    print("DID NOT SELL", best_bid)
                    break

            # Add all the above orders to the result dict
            result[product] = orders

            
            print("current position:", current)
            
        print("total sell orders:", self.sellcount)
        print("total buy orders:", self.buycount)
        print("total orders:", self.sellcount + self.buycount)
        print("\n")
        return result

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