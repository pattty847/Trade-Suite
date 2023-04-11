import asyncio
import dearpygui.dearpygui as dpg
import pandas as pd
import utils.do_stuff as do
import ccxt.pro as ccxtpro

class Orderbook():
    def __init__(self, label, exchange_name, symbol, limit) -> None:
        self.exchange_name = exchange_name
        self.symbol = symbol
        self.limit = limit
        self.bids = []
        self.asks = []

        with dpg.window(
            label=label,
            width=400,
            height=500,
            pos=(25, 25),
            on_close=self.on_close,
            menubar=True) as self.tag:
            
            with dpg.menu_bar():
                with dpg.menu(label="Spread"):
                    dpg.add_slider_int(label="slider float", max_value=10, callback=self.set_spread)
        
            with dpg.plot(width=-1, height=-1):
                self.xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Price", no_gridlines=True)
                with dpg.plot_axis(dpg.mvYAxis):
                    # dpg.set_axis_limits(dpg.last_item(), 0, 110)
                    self.bid_series = dpg.add_bar_series([], [], label="Bids", weight=1)
                    self.ask_series = dpg.add_bar_series([], [], label="Asks", weight=1)
            
        asyncio.run(self.fetch_data())

    async def fetch_data(self):
        async def fetch(exchange_name, symbol, limit):
            exchange_class = getattr(ccxtpro, exchange_name)
            exchange = exchange_class({"enableRateLimit": True, "newUpdates": True})

            while True:
                try:
                    self.orderbook = await getattr(exchange, "watchOrderBook")(symbol, limit)

                    if self.orderbook['bids'] and self.orderbook['asks']:
                        self.update_chart()

                except KeyboardInterrupt:
                    print("KeyboardInterrupt detected. Closing exchange...")
                    await exchange.close()
                    break

            print("Exchange closed.")

        await fetch(self.exchange_name, self.symbol, self.limit)

    def update_chart(self):
        bid_prices = [float(bid[0]) for bid in self.orderbook['bids']]
        bid_sizes = [float(bid[1]) for bid in self.orderbook['bids']]
        
        ask_prices = [float(ask[0]) for ask in self.orderbook['asks']]
        ask_sizes = [float(ask[1]) for ask in self.orderbook['asks']]

        # dpg.set_axis_limits(dpg.last_item(), 0, 110)
        dpg.configure_item(self.bid_series, x=bid_prices, y=bid_sizes)
        dpg.configure_item(self.ask_series, x=ask_prices, y=ask_sizes)
        mid = (self.orderbook['bids'][0][0] + self.orderbook['asks'][0][0]) / 2
        lower_limit = mid * 0.99
        upper_limit = mid * 1.01
        # print(mid, lower_limit, upper_limit)

        dpg.set_axis_limits(self.xaxis, lower_limit, upper_limit)


    def on_close(self):
        dpg.delete_item(self.tag)
        
    def set_spread(self, sender, app_data, user_data):
        print(sender, app_data, user_data)
        # mid = (self.orderbook['bids'][0][0] + self.orderbook['asks'][0][0]) / 2
        # lower_limit = mid * 0.9
        # upper_limit = mid * 1.1
        # print(mid, lower_limit, upper_limit)

        # dpg.set_axis_limits(self.xaxis, lower_limit, upper_limit)