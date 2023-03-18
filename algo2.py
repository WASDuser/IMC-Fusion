from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Trade


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """ 
        # Initialize the method output dict as an empty dict
        result = {}
        pos_allowance = 20
        #for debugging
        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []
                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                ask_limit = 9998    
                bid_ceiling = 10002
                try:
                    print('prev order: ', list(state.own_trades.keys())[product])
                except:
                    print('key not found, missing', product)
                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = min(order_depth.sell_orders[best_ask], pos_allowance)
                    
                    if best_ask <= ask_limit:
                        print("BUY", product, str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, best_ask_volume))
                        pos_allowance -= best_ask_volume

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                # sign should be negative since it is a sell order
                
                
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = min(order_depth.buy_orders[best_bid], pos_allowance)
                    if best_bid >= bid_ceiling:
                        print("SELL", product, str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        pos_allowance -= best_bid_volume

                # Add all the above orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        
            if product == 'BANANAS':
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []
                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                ask_limit = 4952
                bid_limit = 4927
                try:
                    print('prev order: ', list(state.own_trades.keys())[product]    )
                except:
                    print('key not found, missing', product)
                #print('most recent order is: ', most_recent_order.__str__())
                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = min(order_depth.sell_orders[best_ask], 19)
                    if best_ask <= bid_limit:
                        print("BUY", product, str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                # sign should be negative since it is a sell order
                
                
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = min(order_depth.buy_orders[best_bid], 19)
                    if best_bid >= ask_limit:
                        print("SELL", product, str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))

                # Add all the above orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
                
            
        return result