from asyncore import read
import json
from pydoc import synopsis
from time import time
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import Exchange as data
import utils.DoStuff as do
import ccxt as ccxt
import pandas as pd
import os
import csv

class Chart():

    # TODO: Add comments

    def __init__(self, settings, exchange, viewport_width, viewport_height) -> None:

        self.viewport_height = viewport_height
        self.viewport_width = viewport_width

        self.settings = settings

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


    
    def push_chart(self, sender, app_data, user_data):

        dpg.delete_item(f"chart-{self.previous_symbol}")

        symbol = dpg.get_value(f'symbol-{self.exchange}').strip()
        timeframe = dpg.get_value(f'timeframe-{self.exchange}').strip()
        
        self.previous_symbol = symbol
        
        candles = data.get_candles(self.api, symbol, timeframe, "2022-10-25T00:00:00Z", f'{self.exchange}-child', self.viewport_width, self.viewport_height)

        dpg.delete_item("loading")

        print(candles)
        if not len(candles):
            print("No symbol for that exchange.")
        else:


            # TODO: Figure out how to make the close live

            dates, opens, closes, lows, highs, volume = do.candles_to_list(candles)

            dpg.add_text(f"Symbol: {symbol}", parent=f"{self.exchange}-child")

            with dpg.subplots(2, 1, label="", width=-1, height=-1, link_all_x=True, row_ratios=[1.0, 0.25], parent=f"{self.exchange}-child", tag=f"chart-{symbol}"):

                with dpg.plot(tag=f"candle-{symbol}"):

                    dpg.add_plot_legend()

                    xaxis_candles = dpg.add_plot_axis(dpg.mvXAxis, time=True)

                    with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                        dpg.add_candle_series(dates, opens, closes, lows, highs, time_unit=do.convert_timeframe(self.settings['last_timeframe']))
                        dpg.fit_axis_data(dpg.top_container_stack())
                        dpg.fit_axis_data(xaxis_candles)
                        
                with dpg.plot():

                    dpg.add_plot_legend()
                    xaxis_vol = dpg.add_plot_axis(dpg.mvXAxis, label="Date", time=True)

                    with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                        dpg.add_bar_series(dates, volume, weight=1)
                        dpg.fit_axis_data(dpg.top_container_stack())
                        dpg.fit_axis_data(xaxis_vol)

    def add_chart(self):
        with dpg.child_window(parent=self.exchange, tag=f"{self.exchange}-child"):

            add = dpg.add_text("Add Ticker")

            with dpg.popup(add, mousebutton=dpg.mvMouseButton_Left):

                dpg.add_listbox(self.symbols, label="Symbol", tag=f"symbol-{self.exchange}", num_items=10)

                dpg.add_listbox(self.timeframes, label="Timeframe", tag=f"timeframe-{self.exchange}", num_items=10)

                dpg.add_button(label="Go", callback = self.push_chart)