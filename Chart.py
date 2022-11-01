from asyncore import read
import json
from pydoc import synopsis
from time import time
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import Exchange as data

import ccxt as ccxt
import pandas as pd
import os
import csv

class Chart():

    def __init__(self, settings, exchange) -> None:
        self.settings = settings

        self.api = getattr(ccxt, exchange)()
        self.exchange = exchange # Exchange name

        self.symbols = self.load_symbols()
        self.timeframes = self.load_timeframes()

        self.add_chart()

    
    def load_symbols(self):
        """This function will check if symbols are stored for the exchange, and if not it will save them then return the symbols list

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

        if(self.api.has['fetchOHLCV']):
            timeframes = list(self.api.timeframes.keys())
            return timeframes
        else:
            with open(f"timeframes.csv") as f:
                return f.readlines()


    
    def push_chart(self, sender, app_data, user_data):

        dpg.configure_item

        symbol = dpg.get_value('symbol').strip()
        timeframe = dpg.get_value('timeframe').strip()
        print(symbol, timeframe)
        
        candles = data.get_candles(self.api, symbol, timeframe, "2022-10-01T00:00:00Z", f'{self.exchange}-child')
        # ohlcv

        dpg.delete_item("loading")

        print(candles)
        if not len(candles):
            print("No symbol for that exchange.")


        # add plot to parent


    def add_chart(self):
        with dpg.child_window(parent=self.exchange, tag=f"{self.exchange}-child"):

            add = dpg.add_text("Add Ticker")

            with dpg.popup(add, mousebutton=dpg.mvMouseButton_Left):

                dpg.add_listbox(self.symbols, label="Symbol", tag="symbol", num_items=10)

                dpg.add_listbox(self.timeframes, label="Timeframe", tag="timeframe", num_items=10)

                dpg.add_button(label="Go", callback = self.push_chart)


                

            #     with dpg.popup(symbol, mousebutton=dpg.mvMouseButton_Left):

            #         dpg.add_input_text(tag=f"symbols-searcher-{self.chart_id}", hint="Search", callback=lambda sender, data: self.searcher(f"symbols-searcher-{self.chart_id}", f"symbol-{self.chart_id}", self.api.symbols))

            #         dpg.add_listbox(self.api.symbols, tag=f'symbol-{self.chart_id}', show=True, callback=lambda s, a: self.change_symbol(s, a, self.chart_id))

            #     with dpg.popup(timeframe, mousebutton=dpg.mvMouseButton_Left):

            #         dpg.add_listbox(self.api.timeframes, tag=f'timeframe-{self.chart_id}', callback=lambda s, a : self.change_timeframe(s, a, self.chart_id), width=100)

            #     with dpg.popup(date, mousebutton=dpg.mvMouseButton_Left):
            #         # The default date will be the last saved date in the settings file

            #         date = self.settings['last_since'].split("T")[0].split("-")
            #         year = str(int(date[0][2:]))
            #         year_ = f'1{year}'
            #         since = {'month_day': int(date[2]), 'year':int(year_), 'month':int(date[1])}
                    
            #         dpg.add_date_picker(level=dpg.mvDatePickerLevel_Day, label='From', default_value=since)

            # with dpg.subplots(2, 1, label="", width=-1, height=-1, link_all_x=True, row_ratios=[1.0, 0.25]):

            #     with dpg.plot():

            #         dpg.add_plot_legend()
            #         xaxis_candle_tag = f'candle-series-xaxis-{self.chart_id}'
            #         dpg.add_plot_axis(dpg.mvXAxis, tag=xaxis_candle_tag, time=True)

            #         with dpg.plot_axis(dpg.mvYAxis, tag=f'candle-series-yaxis-{self.chart_id}', label="USD"):

            #             dpg.add_candle_series(dates, opens, closes, lows, highs, tag=f'candle-series-{self.chart_id}', time_unit=self.do.convert_timeframe(self.settings['last_timeframe']))
            #             dpg.fit_axis_data(dpg.top_container_stack())
            #             dpg.fit_axis_data(xaxis_candle_tag)
                        
            #     with dpg.plot():

            #         dpg.add_plot_legend()
            #         xaxis_volume_tag = f'volume-series-xaxis-{self.chart_id}'
            #         dpg.add_plot_axis(dpg.mvXAxis, label="Date", tag=xaxis_volume_tag, time=True)

            #         with dpg.plot_axis(dpg.mvYAxis, label="USD", tag=f'volume-series-yaxis-{self.chart_id}'):

            #             dpg.add_bar_series(dates, volume, tag=f'volume-series-{self.chart_id}', weight=1)
            #             dpg.fit_axis_data(dpg.top_container_stack())
            #             dpg.fit_axis_data(xaxis_volume_tag)