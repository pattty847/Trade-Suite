import asyncio
import threading
import dearpygui.dearpygui as dpg
import utils.do_stuff as do
import ccxt.pro as ccxtpro
import ccxt
import data
import logging
from utils.loading import loading_overlay
from console import Console

class Charts:
    def __init__(self, parent):
        self.id = str(id(self))
        self.tag = "chart"
        self.parent = parent

        self.menu_tag = self.id + "_menu"
        self.subplot_tag = self.id + "_subplot"
        self.candlestick_plot_tag = self.id + "_candle_series"
        self.volume_plot_tag = self.id + "_volume_plot"

        self.console = Console(1000, self.tag)
        self.last_chart = None

        self.thread = threading.Thread()
        self.loop = asyncio.new_event_loop()
        self.logger = logging.getLogger(__name__)

    def draw_chart(self, exchange, symbol, timeframe):
        
        dpg.delete_item(self.last_chart)
        
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        
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
            label=f"{self.symbol} | {self.timeframe}",
            width=-1,
            height=-1,
            link_all_x=True,
            row_ratios=[0.66, 0.33],
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
                    dpg.add_bar_series(
                        self.candles['dates'],
                        self.candles['volumes'],
                        weight=1.0,
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