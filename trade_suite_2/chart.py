from asyncio import run
import asyncio
import uuid
import dearpygui.dearpygui as dpg
import utils.DoStuff as do
import ccxt.pro as ccxtpro
import data

class Charts:

    def __init__(self, tag, parent):
        self.tag = tag
        self.parent = parent

        self.id = str(id(self))

        self.menu_tag = self.id + '_menu'
        self.subplot_tag = self.id + '_subplot'
        self.candlestick_plot_tag = self.id + '_candlestick_plot'
        self.volume_plot_tag = self.id + '_volume_plot'
        self.last_chart = None

        self.exchange_name = None
        self.ccxt_object = None
        self.describe = None
        self.symbols = None
        self.symbol = None
        self.timeframes = None
        self.timeframe = None
        self.candles = None

        dpg.add_window(
            label=f"{self.tag}", 
            tag=self.tag, 
            width=500, 
            height=500
        )

        self.draw_nav_bar()


    def draw_nav_bar(self):
        with dpg.menu_bar(parent=self.tag, tag=self.menu_tag):
            with dpg.menu(label="Exchange"):
                dpg.add_listbox(ccxtpro.exchanges, num_items=10, callback=self.create_exchange)

    def create_exchange(self, sender, exchange_name, user_data):
        exchange_class = getattr(ccxtpro, exchange_name)
        self.ccxt_object = exchange_class({
            'enableRateLimit': True,  # adjust as needed
            # add other exchange-specific options here
        })
        self.exchange_name = exchange_name
        self.describe = do.get_exchange_info(exchange_name)
        self.symbols = self.describe['symbols']
        self.timeframes = self.describe['timeframes']
        self.update_window()

    def update_window(self):
        dpg.configure_item(self.tag, label=f"{self.exchange_name.upper()}")

        # Remove existing menu items
        dpg.delete_item(self.menu_tag, children_only=True)

        with dpg.menu(label="Exchanges", parent=self.menu_tag):
            dpg.add_listbox(ccxtpro.exchanges, num_items=10, callback=self.create_exchange)

        # Add new menu items for symbols
        with dpg.menu(label="Symbols", parent=self.menu_tag):
            symbol = dpg.add_listbox(list(self.symbols), num_items=10, default_value="BTC/USDT")

        # Add new menu items for timeframes
        if self.timeframes:
            with dpg.menu(label="Timeframes", parent=self.menu_tag):
                timeframe = dpg.add_listbox(list(self.timeframes), num_items=10, default_value="1d")

        dpg.add_menu_item(label="Add", parent=self.menu_tag, callback=lambda:self.draw_chart(symbol, timeframe))
        dpg.add_menu_item(label="Save Layout", parent=self.menu_tag)

    def draw_chart(self, symbol, timeframe):

        self.symbol = dpg.get_value(symbol)
        self.timeframe = dpg.get_value(timeframe)
        print(self.symbol, self.timeframe)
        self.candles = asyncio.run(data.fetch_candles(self.exchange_name, self.symbol, self.timeframe, "2023-01-01 00:00:00", 1000, False))

        dpg.delete_item(self.last_chart)

        with dpg.subplots(
            rows=2, 
            columns=1, 
            label=f"{self.symbol} | {self.timeframe}", 
            width=-1, 
            height=-1, 
            link_all_x=True, 
            row_ratios=[1.0, 0.25], 
            parent=self.tag,
            tag=f"{self.subplot_tag}_{self.symbol}_{self.timeframe}"):

            self.last_chart = f"{self.subplot_tag}_{self.symbol}_{self.timeframe}"

            with dpg.plot(tag=self.candlestick_plot_tag):
                dpg.add_plot_legend()

                xaxis_candles = dpg.add_plot_axis(dpg.mvXAxis, time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                    dpg.add_candle_series(
                        self.candles['time'], 
                        self.candles['open'], 
                        self.candles['close'], 
                        self.candles['low'], 
                        self.candles['high'],
                        tag=self.id + "_candle_series",
                        time_unit=do.convert_timeframe(self.timeframe)
                    )
                    
                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_candles)
                    
            # Volume plot
            with dpg.plot(tag=self.volume_plot_tag):

                dpg.add_plot_legend()
                xaxis_vol = dpg.add_plot_axis(dpg.mvXAxis, label="Time [UTC]", time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):

                    dpg.add_bar_series(self.candles['time'], self.candles['volume'])
                    
                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_vol)