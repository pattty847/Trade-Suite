import asyncio
import json
import os
import threading
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import utils.do_stuff as do
import ccxt.pro as ccxtpro
import ccxt
import data
import logging
import ai.model as ai
from ai.model import LSTMModel
from utils.loading import loading_overlay
from console import Console

class Charts:
    def __init__(self, parent, viewport):
        self.id = str(id(self))
        self.tag = "chart"
        self.parent = parent
        self.viewport = viewport

        self.menu_tag = self.id + "_menu"
        self.subplot_tag = self.id + "_subplot"
        self.candlestick_plot_tag = self.id + "_candle_series"
        self.volume_plot_tag = self.id + "_volume_plot"

        self.console = Console(1000, self.tag)
        self.last_chart = None
    

        self.thread = threading.Thread()
        self.loop = asyncio.new_event_loop()
        self.logger = logging.getLogger(__name__)
        self.load_favorites()
        
    # UI elements defined below
    def add_menu_bar(self):
        with dpg.menu_bar(parent=self.parent, tag='chart_menu_bar'):
            
            with dpg.menu(label="Chart"):
                dpg.add_combo(label="Exchange", items=['coinbasepro', 'kucoin', 'kraken', 'cryptocom'], width=150, callback=self.add_source_modal)
                
            dpg.add_menu_item(label='Favorites', callback=self.show_favorites_window)
            with dpg.menu(label='Train ML'):
                dpg.add_combo(['LSTM'], label='Model', callback=self.train_ml_model)
                
            with dpg.menu(label="Indicators"):
                dpg.add_menu_item(label="RSI")
            
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Demo", callback=demo.show_demo)

    def draw_chart(self, exchange, symbol, timeframe):
        if not dpg.does_alias_exist('chart_menu_bar'):
            self.add_menu_bar()
        
        dpg.delete_item(self.last_chart)
        
        self.exchange = exchange
        self.symbol = symbol if type(symbol) is not int else dpg.get_value(symbol)
        self.timeframe = timeframe if type(timeframe) is not int else dpg.get_value(timeframe)
        
        print(self.exchange, self.symbol, self.timeframe)

        with loading_overlay():
            self.candles = asyncio.run(
                data.fetch_candles(
                    self.exchange,
                    self.symbol,
                    self.timeframe,
                    "2023-03-01 00:00:00",
                    1000,
                    False
                )
            )

        with dpg.subplots(
            rows=2,
            columns=1,
            label=f"{self.exchange.upper()} | {self.symbol} | {self.timeframe}",
            width=-1,
            height=-1,
            link_all_x=True,
            row_ratios=[0.80, 0.20],
            parent=self.parent,
            tag=f"{self.subplot_tag}_{self.symbol}_{self.timeframe}",
        ):
            self.last_chart = f"{self.subplot_tag}_{self.symbol}_{self.timeframe}"

            with dpg.plot(tag='plot'):
                dpg.add_plot_legend()

                xaxis_candles = dpg.add_plot_axis(dpg.mvXAxis, time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):
                    dpg.delete_item(self.id + "_loading")

                    dpg.add_candle_series(
                        self.candles["dates"],
                        self.candles["opens"],
                        self.candles["closes"],
                        self.candles["lows"],
                        self.candles["highs"],
                        weight=0.1,
                        tag=self.candlestick_plot_tag,
                        time_unit=do.convert_timeframe(self.timeframe),
                    )

                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_candles)

                if self.thread.is_alive():
                    self.stop_thread()
                #self.start_thread()

            # Volume plot
            with dpg.plot():
                dpg.add_plot_legend()
                xaxis_vol = dpg.add_plot_axis(dpg.mvXAxis, label="Time [UTC]", time=True)

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):
                    dpg.add_stair_series(
                        x=self.candles['dates'],
                        y=self.candles['volumes'],
                        tag=self.volume_plot_tag
                    )

                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_vol)

    def start_thread(self):
        print("Starting.")
        self.thread = threading.Thread(target=self.start_loop)
        self.thread.start()

    def start_loop(self):
        asyncio.set_event_loop(self.loop)

        self.loop.create_task(self.watch_trades(self.exchange, "watchTrades", self.symbol))

        self.loop.run_forever()

    def stop_thread(self):

        if self.thread.is_alive():
            self.logger.info(f"Stopping thread for {self.exchange} {self.symbol} {self.timeframe}")
            self.logger.info(f"Deleting chart: {self.tag}")

            self.loop.stop()
            self.thread.join()
            asyncio.run(self.exchange_object.close())
            return 
        
        self.logger.info(f"Deleting chart: {self.tag}")


    async def watch_trades(self, exchange_name, method, symbol):
        exchange_class = getattr(ccxtpro, exchange_name)
        self.exchange_object = exchange_class(
            {
                "enableRateLimit": True,  # add rate limiter
            }
        )
        while self.thread.is_alive():
            try:
                # watch the data using the specified method
                trades = await getattr(self.exchange_object, f"{method}")(symbol)

                print(trades)

                self.update_chart(trades)
            except ccxt.BaseError as e:
                await self.exchange_object.close()

        await self.exchange_object.close()

    def update_chart(self, trades):
        # store the timeframe in milliseconds
        self.timeframe_ms = self.exchange_object.parse_timeframe(self.timeframe) * 1000
        self.close_time = self.candles['dates'][-1] * 1000 + self.timeframe_ms

        # Get the last candle in the chart
        current_candle = {
            'opens': self.candles['opens'][-1],
            'highs': self.candles['highs'][-1],
            'lows': self.candles['lows'][-1],
            'volumes': self.candles['volumes'][-1],
            'closes': self.candles['closes'][-1]
        }
        
        # Loop through trades
        for trade in trades:

            # If the trade is in a new candle, add a new candle to self.candles
            if trade['timestamp'] >= self.close_time:
                self.candles['dates'].append(self.close_time / 1000)
                self.candles['opens'].append(trade['price'])
                self.candles['highs'].append(trade['price'])
                self.candles['lows'].append(trade['price'])
                self.candles['volumes'].append(trade['amount'])
                self.candles['closes'].append(trade['price'])
                
                # Set current_candle to the new candle
                current_candle = {
                    'opens': trade['price'],
                    'highs': trade['price'],
                    'lows': trade['price'],
                    'volumes': trade['amount'],
                    'closes': trade['price']
                }
            else:
                # If the trade is in the current candle, update the last candle in self.candles
                self.candles['highs'][-1] = max(current_candle['highs'], trade['price'])
                self.candles['lows'][-1] = min(current_candle['lows'], trade['price'])
                self.candles['volumes'][-1] += trade['amount']
                self.candles['closes'][-1] = trade['price']

            if trade['amount'] >= 1:
                x = self.candles['dates'][-1]
                y = trade['price']
                size = trade['amount'] # adjust the size to your preference
                dpg.draw_circle(center=[x, y], radius=size, color=[255, 255, 255, 255], thickness=1, parent='plot')

            
            dpg.configure_item(
                self.candlestick_plot_tag, 
                dates=self.candles['dates'], 
                opens=self.candles['opens'],
                highs=self.candles['highs'],
                lows=self.candles['lows'],
                closes=self.candles['closes']
            )

            dpg.configure_item(
                self.volume_plot_tag,
                x=self.candles['dates'],
                y=self.candles['volumes']
            )
            
    def load_favorites(self):
        if os.path.exists('favorites.json'):
            with open('favorites.json', 'r') as f:
                self.favorites = json.load(f)
        else:
            self.favorites = []

    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def add_favorite(self, exchange, symbol, timeframe):
        favorite = {"exchange": exchange, "symbol": symbol, "timeframe": timeframe}
        if favorite not in self.favorites:
            self.favorites.append(favorite)
            self.save_favorites()
        favorite_str = f"{favorite['exchange']} - {favorite['symbol']} ({favorite['timeframe']}) added to favorites."
        dpg.set_value('added_favorite', favorite_str)

    def remove_favorite(self, sender, app_data, user_data):
        print(user_data)
        del self.favorites[user_data]
        self.save_favorites()
        dpg.delete_item('favorites_list')
        self.draw_favorites_list()
        
    def draw_favorites_list(self):
        with dpg.child_window(id="favorites_list", parent='favorites_window', autosize_x=True, autosize_y=False, horizontal_scrollbar=True):
            for index, favorite in enumerate(self.favorites):
                dpg.add_text(f"{favorite['exchange']} {favorite['symbol']} {favorite['timeframe']}", bullet=True, indent=10)
                with dpg.group(horizontal=True):
                    dpg.add_spacer()
                    dpg.add_button(label="Add", callback=lambda: self.draw_chart(favorite['exchange'], favorite['symbol'], favorite['timeframe']))
                    dpg.add_button(label="Remove", callback=self.remove_favorite, user_data=index)
                dpg.add_separator()
                dpg.add_spacer()

    def show_favorites_window(self):
        def delete_favorites():
            dpg.delete_item('favorites_window')

        with dpg.window(label="Favorites", id="favorites_window", width=400, height=500, on_close=delete_favorites, pos=(25, 25)):
            dpg.add_spacer()
            self.draw_favorites_list()
            
    def add_source_modal(self, sender, app_data, user_data):
        self.exchange = dpg.get_value(sender)

        if self.exchange == 'coinbasepro':
            self.ccxt_obj = ccxt.coinbasepro()
        elif self.exchange == 'kucoin':
            self.ccxt_obj = ccxt.kucoin()
        elif self.exchange == 'kraken':
            self.ccxt_obj = ccxt.kraken()
        elif self.exchange == 'cryptocom':
            self.ccxt_obj = ccxt.cryptocom()
        if not self.ccxt_obj.has['fetchOHLCV']:
            return

        with loading_overlay():
            self.ccxt_obj.load_markets()

        self.symbols = sorted(self.ccxt_obj.symbols)
        self.timeframes = sorted(list(self.ccxt_obj.timeframes))

        def delete_source_modal():
            dpg.delete_item('data_source')

        with dpg.window(modal=True, width=-1, height=-1, tag='data_source', on_close=delete_source_modal) as source_modal:
            symbol = dpg.add_combo(label="Symbol", default_value='BTC/USDT', items=self.symbols, width=150)
            timeframe = dpg.add_combo(label="Timeframe", default_value=self.timeframes[0], items=self.timeframes, width=150)
            dpg.add_button(label="Add Chart", callback=lambda: self.draw_chart(self.exchange, symbol, timeframe))
            dpg.add_button(label="Add to Favorites", callback=lambda: self.add_favorite(self.exchange, dpg.get_value(symbol), dpg.get_value(timeframe)))
            dpg.add_button(label="Show Favorites", callback=self.show_favorites_window)
            dpg.add_text(tag='added_favorite', wrap=dpg.get_item_width('data_source'))
            
    def train_ml_model(self, sender, app_data, user_data):
        model = app_data
        model_ = ai.main(self.candles)