import asyncio
import threading
import dearpygui.dearpygui as dpg
import utils.DoStuff as do
import ccxt.pro as ccxtpro
import ccxt
import data
import logging
from console import Console

class Charts:
    def __init__(
        self,
        tag,
        parent,
        chart_controller,
        window_width,
        window_height,
        exchange_name=None,
        symbol=None,
        timeframe=None
    ):
        self.id = str(id(self))
        self.tag = tag
        self.parent = parent
        self.chart_controller = chart_controller
        self.window_width = window_width
        self.window_height = window_height

        self.menu_tag = self.id + "_menu"
        self.subplot_tag = self.id + "_subplot"
        self.candlestick_plot_tag = self.id + "_candle_series"
        self.volume_plot_tag = self.id + "_volume_plot"

        self.console = Console(1000, self.tag)

        self.last_chart = None
        self.exchange_name = None
        self.ccxt_object = None

        self.describe = None
        self.symbols = None
        self.symbol = None
        self.timeframes = None
        self.timeframe = None

        self.candles = None
        self.last_candle_time = None
        self.current_candle = None

        self.thread = threading.Thread()
        self.loop = asyncio.new_event_loop()

        dpg.add_window(label=f"{self.tag}", tag=self.tag, width=500, height=500, on_close=self.stop_thread)

        if exchange_name and symbol and timeframe:
            self.push_nav_bar(exchange_name)
            self.draw_chart(symbol, timeframe, True)
        else:
            self.push_nav_bar("coinbasepro")
            self.draw_chart("BTC/USD", "1m", True)
            self.chart_controller.position_charts()

    def push_nav_bar(self, exchange_name):
        if self.last_chart is not None:
            dpg.delete_item(self.last_chart)
            
        self.exchange_name = exchange_name
        self.describe = do.get_exchange_info(exchange_name)
        self.symbols = self.describe["symbols"]
        self.timeframes = self.describe["timeframes"]

        dpg.configure_item(self.tag, label=f"{self.exchange_name.upper()}")

        with dpg.menu_bar(parent=self.tag, tag=self.menu_tag):

            # Add new menu items for symbols
            with dpg.menu(label="Symbols", parent=self.menu_tag):
                dpg.add_input_text(tag=f"{self.tag}-searcher", hint="Search",
                    callback=lambda sender, data: do.searcher(f"{self.tag}-searcher", 
                    f"{self.tag}-symbols-listbox", self.symbols)
                )

                symbol = dpg.add_listbox(
                    sorted(self.symbols), 
                    default_value="BTC/USDT",
                    tag=f"{self.tag}-symbols-listbox", 
                    callback=lambda : dpg.configure_item(f"{self.tag}-searcher", 
                    label=dpg.get_value(f"{self.tag}-searcher")),
                    num_items=10
                )

            # Add new menu items for timeframes
            if self.timeframes:
                with dpg.menu(label="Timeframes", parent=self.menu_tag):
                    timeframe = dpg.add_listbox(
                        list(self.timeframes), num_items=10, default_value="1m"
                    )

            dpg.add_menu_item(
                label="Add",
                parent=self.menu_tag,
                callback=lambda: self.draw_chart(symbol, timeframe),
            )

            dpg.add_menu_item(label="Indicators", callback=self.indicators_menu)

    def indicators_menu_on_close(self, sender):
        dpg.delete_item(sender)
    
    def indicators_menu(self):
        with dpg.window(
                label="Settings", 
                tag="chart_settings_menu", 
                pos=[self.window_width / 2 - 250, self.window_height / 2 - 250], 
                width=500, 
                height=500, 
                on_close=self.indicators_menu_on_close
            ):
            dpg.add_button(label="SMA", callback=lambda: dpg.add_line_series(self.candles['dates'], self.candles['closes']))

    def push_console(self):
        with dpg.window(label="Console", tag=self.tag + "_console"):
            dpg.add_input_text(tag="_console")

    def draw_chart(self, symbol, timeframe, favorite=False):
        dpg.delete_item(self.last_chart)

        self.symbol = dpg.get_value(symbol) if not favorite else symbol
        self.timeframe = dpg.get_value(timeframe) if not favorite else timeframe

        dpg.delete_item(self.id + "_loading")
        dpg.add_loading_indicator(
            tag=self.id + "_loading",
            pos=[self.window_width / 2, self.window_height / 2 - 110],
            radius=10.0,
            style=1,
            parent=self.tag,
        )

        self.candles = asyncio.run(
            data.fetch_candles(
                self.exchange_name,
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
            parent=self.tag,
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
                        tag=self.candlestick_plot_tag,
                        time_unit=do.convert_timeframe(self.timeframe),
                    )

                    dpg.fit_axis_data(dpg.top_container_stack())
                dpg.fit_axis_data(xaxis_candles)

                if self.thread.is_alive():
                    self.stop_thread()
                self.start_thread()

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

        self.loop.create_task(self.watch_function(self.exchange_name, "watchTrades", self.symbol))

        self.loop.run_forever()

    def stop_thread(self):

        if self.thread.is_alive():
            logging.info(f"Stopping thread for {self.exchange_name} {self.symbol} {self.timeframe}")
            logging.info(f"Deleting chart: {self.tag}")

            del self.chart_controller.active_charts[self.tag]
            self.loop.stop()
            self.thread.join()
            asyncio.run(self.exchange.close())
            return 
        
        logging.info(f"Deleting chart: {self.tag}")

        del self.chart_controller.active_charts[self.tag]
        self.chart_controller.position_charts()

    async def watch_function(self, exchange_name, method, symbol):
        exchange_class = getattr(ccxtpro, exchange_name)
        self.exchange = exchange_class(
            {
                "enableRateLimit": True,  # add rate limiter
            }
        )
        while self.thread.is_alive():
            try:
                # watch the data using the specified method
                trades = await getattr(self.exchange, f"{method}")(symbol)

                print(trades)

                self.update_chart(trades)
            except ccxt.BaseError as e:
                await self.exchange.close()

        await self.exchange.close()

    def update_chart(self, trades):
        # store the timeframe in milliseconds
        self.timeframe_ms = self.exchange.parse_timeframe(self.timeframe) * 1000
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