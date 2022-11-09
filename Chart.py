import asyncio
import datetime
import pytz
import Exchanges.FTX as FTX
import dearpygui.dearpygui as dpg
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
        """This function will check if symbols are stored for the exchange in /data/<exchange>, and if not it will save 
        them to a csv file then return the symbols list. If it has them stored it will read and return.

        Returns:
            list: symbol list
        """
        file = f"data\\{self.exchange}"
        if os.path.exists(file):
            
            with open(f"{file}\\symbols.csv") as f:
                return f.readlines()

        else:
            
            os.makedirs(file)

            symbols = list(self.api.fetch_tickers().keys())
            
            with open(f"{file}\\symbols.csv", "w") as f:
                
                for sym in symbols:
                    f.write(sym+"\n")

            return symbols

    
    def load_timeframes(self):
        """ This will check if the exchange has the data for their timeframes and return it. If not it will used a list of 
        most likely timeframes. 

        Returns:
            list: List of timeframes for exchange
        """

        if(self.api.has['fetchOHLCV']):
            timeframes = list(self.api.timeframes.keys())
            return timeframes
        else:
            with open(f"timeframes.csv") as f:
                return f.readlines()

    
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


    
    def push_chart(self, sender, app_data, user_data):
        dpg.delete_item(f"chart-{self.previous_symbol}")

        symbol = dpg.get_value(f'symbol-{self.exchange}').strip()
        timeframe = dpg.get_value(f'timeframe-{self.exchange}').strip()

        self.previous_symbol = symbol

    

        candles = asyncio.run(FTX.fetch_candles(symbol, 
                              FTX.timeframes[timeframe], 
                              f'{self.exchange}-child', 
                              self.viewport_width, 
                              self.viewport_height,
                              start_time=datetime.datetime.now(tz=pytz.utc).timestamp() * 1000))
        
        
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
            with dpg.plot(tag=f"candle-{symbol}", label=f"Exchange: {self.exchange.upper()} | Symbol: {symbol} | Timeframe: {timeframe}"):

                dpg.add_plot_legend()

                xaxis_candles = dpg.add_plot_axis(dpg.mvXAxis, time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                    dpg.add_candle_series(candles['time'], candles['open'], candles['close'], candles['low'], candles['high'], time_unit=do.convert_timeframe(timeframe))
                    # dpg.draw_circle(center=(500, 500), radius=5.0, label="test")
                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_candles)
                    
            # Volume plot
            with dpg.plot():

                dpg.add_plot_legend()
                xaxis_vol = dpg.add_plot_axis(dpg.mvXAxis, label="Time [UTC]", time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                    dpg.add_bar_series(candles['time'], candles['volume'], weight=1)
                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_vol)

            # Indicators menu
            with dpg.menu(label="Chart Settings", parent="main-menu-bar"):
                dpg.add_menu_item(label="[Add] NYSE Opens & Closes", callback=self.add_market_opens_closes)




    def add_chart(self):
        with dpg.child_window(parent=self.exchange, tag=f"{self.exchange}-child"):

            with dpg.group(horizontal=True):
                add = dpg.add_button(label="Add Ticker")
                dpg.add_button(label="BTC/USDT")
                dpg.add_button(label="ETH/USDT")

                with dpg.popup(add, mousebutton=dpg.mvMouseButton_Left):
                    dpg.add_input_text(tag=f"symbols-searcher-{self.exchange}", hint="Search",
                                                callback=lambda sender, data: do.searcher(f"symbols-searcher-{self.exchange}", 
                                                f"symbol-{self.exchange}", self.symbols))

                    dpg.add_listbox(self.symbols, label="Symbol", tag=f"symbol-{self.exchange}", num_items=10)

                    dpg.add_listbox(self.timeframes, label="Timeframe", tag=f"timeframe-{self.exchange}", num_items=10)

                    dpg.add_button(label="Go", callback = self.push_chart)