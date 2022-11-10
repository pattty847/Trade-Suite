import asyncio
import datetime
import pytz
import Exchanges.Binance as Binance
import dearpygui.dearpygui as dpg
import sys
import utils.DoStuff as do
import ccxt as ccxt
import os
import Strategies as strat



class Chart():

    # TODO: Add comments

    def __init__(self, settings, exchange, viewport_width, viewport_height) -> None:

        self.viewport_height = viewport_height
        self.viewport_width = viewport_width

        self.settings = settings

        self.fetch_range = None

        self.api = getattr(ccxt, exchange)()
        self.exchange = exchange # Exchange name

        self.symbols = self.load_symbols()
        self.timeframes = self.load_timeframes()

        self.previous_symbol = None

        self.add_chart()

    
    def load_symbols(self):
        """ This function calls for all tickers from the exchange and returns them as a list.
        """
        try:
            with open(f"src\\Exchanges\\CSV\\{self.exchange}-tickers.csv", "r") as f:
                return f.readlines()
        except FileNotFoundError as e:
            os.makedirs("src\\Exchanges\\CSV")
            with open(f"src\\Exchanges\\CSV\\{self.exchange}-tickers.csv", "w") as f:
                tickers = self.api.fetch_tickers().keys()
                new_tickers = []
                for line in tickers:
                    new_tickers.append(line.replace("/", ""))
                    f.write(line.replace("/", "") + "\n")
                return new_tickers

    
    def load_timeframes(self):
        """ This will return a list of timeframes from the exchange as a list."""
        try:
            with open(f"src\\Exchanges\\CSV\\{self.exchange}-timeframes.csv", "r") as f:
                return f.readlines()
        except FileNotFoundError as e:
            with open(f"src\\Exchanges\\CSV\\{self.exchange}-timeframes.csv", "w") as f:
                timeframes = self.api.timeframes.keys()
                for line in timeframes:
                    f.write(line + "\n")
                return list(timeframes)


    
    def add_market_opens_closes(self):
        """ This function will add NYSE market opens and closes to the chart.
        """
        symbol = dpg.get_value(f'symbol-{self.exchange}').strip()
        
        for time in strat.get_nyse_market_hours("open"):
            dpg.add_plot_annotation(label="NY Open", default_value=(time, 0), color=[116, 209, 88, 255], parent=f"candle-{symbol}")
        for time in strat.get_nyse_market_hours("close"):
            dpg.add_plot_annotation(label="NY Close", default_value=(time, 0), color=[219, 148, 103, 255], parent=f"candle-{symbol}")

    

    # def start_websocket(self, sender, app_data, user_data):
    #     thread = Threading


    
    def push_chart(self, symbol_=None, timeframe_=None):
        """ Function called to push a ticker and timeframe to the window. You can optionally call this function with a ticker and timeframe passed,
        which will be automatically added.

        Args:
            symbol_ (str, optional): A symbol. Defaults to None.
            timeframe_ (str, optional): A timeframe. Defaults to None.
        """
        dpg.delete_item(f"chart-{self.previous_symbol}")
        dpg.delete_item('settings')

        symbol = dpg.get_value(f'symbol-{self.exchange}').strip()
        timeframe = dpg.get_value(f'timeframe-{self.exchange}').strip()

        self.previous_symbol = symbol

        candles = asyncio.run(Binance.fetch_candles(ticker=symbol if not symbol_ else symbol_, timeframe = Binance.timeframes[timeframe] if not timeframe_ else timeframe_, chart_id = f'{self.exchange}-child', viewport_width = self.viewport_width, viewport_height = self.viewport_height))

        # Create websocket by passing the ticker and @kline<timeframe>?
        
        
        if candles == None:
            print("No symbol for this exchange.")
            dpg.delete_item("loading")
            return
        
        dpg.delete_item("loading")

        # TODO: Figure out how to make the close live


        # Candlestick plot and volume plot
        with dpg.subplots(2, 1, label="", width=-1, height=-1, 
                          link_all_x=True, 
                          row_ratios=[1.0, 0.25], 
                          parent=f"{self.exchange}-child", 
                          tag=f"chart-{symbol}"):

            # Candlestick plot
            with dpg.plot(tag=f"candle-{symbol}", label=f"Exchange: {self.exchange.upper()} | Symbol: {symbol if not symbol_ else symbol_} | Timeframe: {timeframe if not timeframe_ else timeframe_}"):

                dpg.add_plot_legend()

                xaxis_candles = dpg.add_plot_axis(dpg.mvXAxis, time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                    dpg.add_candle_series(candles['time'], candles['open'], candles['close'], candles['low'], candles['high'], time_unit=do.convert_timeframe(timeframe if not timeframe_ else timeframe))
                    # dpg.draw_circle(center=(500, 500), radius=5.0, label="test")
                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_candles)
                    
            # Volume plot
            with dpg.plot():

                dpg.add_plot_legend()
                xaxis_vol = dpg.add_plot_axis(dpg.mvXAxis, label="Time [UTC]", time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                    dpg.add_bar_series(candles['time'], candles['volume'])
                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_vol)

            # Indicators menu
            with dpg.menu(label="Chart Settings", parent="main-menu-bar"):
                dpg.add_menu_item(label="[Add] NYSE Opens & Closes", callback=self.add_market_opens_closes)

        # Maybe call a new function passing the websocket, and chart tags so it can be updated?



    def add_chart(self):
        with dpg.child_window(parent=self.exchange, tag=f"{self.exchange}-child"):

            with dpg.group(horizontal=True, tag="favorites"):
                add = dpg.add_button(label="Add Ticker")
                dpg.add_button(label="BTC/USDT", callback= lambda: self.push_chart("BTCUSDT", "15m"))
                dpg.add_button(label="ETH/USDT", callback= lambda: self.push_chart("ETHUSDT", "15m"))

                with dpg.popup(add, mousebutton=dpg.mvMouseButton_Left):
                    dpg.add_input_text(tag=f"symbols-searcher-{self.exchange}", hint="Search",
                                                callback=lambda sender, data: do.searcher(f"symbols-searcher-{self.exchange}", 
                                                f"symbol-{self.exchange}", self.symbols))

                    dpg.add_listbox(self.symbols, label="Symbol", tag=f"symbol-{self.exchange}", num_items=10)

                    dpg.add_listbox(self.timeframes, label="Timeframe", tag=f"timeframe-{self.exchange}", num_items=10)

                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Add to Favorites", callback=lambda: dpg.add_button(label=dpg.get_value(f"symbol-{self.exchange}"), parent="favorites", callback=lambda: self.push_chart(dpg.get_value(f"symbol-{self.exchange}"), dpg.get_value(f"timeframe-{self.exchange}"))))
                        dpg.add_button(label="Go", callback = self.push_chart)