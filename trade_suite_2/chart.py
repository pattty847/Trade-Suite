import asyncio
import threading
import dearpygui.dearpygui as dpg
import utils.DoStuff as do
import ccxt.pro as ccxtpro
import ccxt
import data

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

        self.draw_nav_bar()

        if exchange_name and symbol and timeframe:
            self.create_exchange(None, exchange_name, None)
            self.draw_chart(symbol, timeframe, True)

    def draw_nav_bar(self):
        with dpg.menu_bar(parent=self.tag, tag=self.menu_tag):
            with dpg.menu(label="Exchange"):
                dpg.add_listbox(
                    ccxtpro.exchanges, num_items=10, callback=self.create_exchange
                )

    def create_exchange(self, sender, exchange_name, user_data):
        if self.last_chart is not None:
            dpg.delete_item(self.last_chart)
            
        self.exchange_name = exchange_name
        self.describe = do.get_exchange_info(exchange_name)
        self.symbols = self.describe["symbols"]
        self.timeframes = self.describe["timeframes"]
        self.push_exchange()

    def push_exchange(self):
        dpg.configure_item(self.tag, label=f"{self.exchange_name.upper()}")

        # Remove existing menu items
        dpg.delete_item(self.menu_tag, children_only=True)

        with dpg.menu(label="Exchanges", parent=self.menu_tag):
            dpg.add_listbox(
                ccxtpro.exchanges, num_items=10, callback=self.create_exchange
            )

        # Add new menu items for symbols
        with dpg.menu(label="Symbols", parent=self.menu_tag):
            symbol = dpg.add_listbox(
                list(self.symbols), num_items=10, default_value="BTC/USDT"
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

    def draw_chart(self, symbol, timeframe, favorite=False):
        dpg.delete_item(self.last_chart)
        self.stop_thread()

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
                "2023-02-22 00:00:00",
                1000,
                False,
                self.candlestick_plot_tag,
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

            with dpg.plot():
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

                    self.start_thread()

            # Volume plot
            with dpg.plot(tag=self.volume_plot_tag):
                dpg.add_plot_legend()
                xaxis_vol = dpg.add_plot_axis(
                    dpg.mvXAxis, label="Time [UTC]", time=True
                )

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):
                    dpg.add_bar_series(
                        self.candles['dates'],
                        self.candles['volumes'],
                        weight=10.0
                    )

                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_vol)

    def start_thread(self):
        print("Starting.")
        self.thread = threading.Thread(target=self.start_thread_)
        self.thread.start()

    def start_thread_(self):
        asyncio.set_event_loop(self.loop)

        self.loop.create_task(self.watch_function(self.exchange_name, "watchTrades", self.symbol))

        self.loop.run_forever()

    def stop_thread(self):
        if self.thread.is_alive():
            print("Stopping.")
            del self.chart_controller.active_charts[self.tag]
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join()

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
        timeframe_ms = self.exchange.parse_timeframe(self.timeframe) * 1000
        
        # Get the last candle in the chart
        last_candle = {
            'opens': self.candles['opens'][-1],
            'highs': self.candles['highs'][-1],
            'lows': self.candles['lows'][-1],
            'volumes': self.candles['volumes'][-1],
            'closes': self.candles['closes'][-1]
        }
        
        # Loop through trades
        for trade in trades:

            # If the trade is in a new candle, add a new candle to self.candles
            if trade['timestamp'] >= self.candles['dates'][-1] * 1000 + timeframe_ms:
                self.candles['dates'].append(trade['timestamp'] // 1000)
                self.candles['opens'].append(trade['price'])
                self.candles['highs'].append(trade['price'])
                self.candles['lows'].append(trade['price'])
                self.candles['volumes'].append(trade['amount'])
                self.candles['closes'].append(trade['price'])
                
                # Set last_candle to the new candle
                last_candle = {
                    'opens': trade['price'],
                    'highs': trade['price'],
                    'lows': trade['price'],
                    'volumes': trade['amount'],
                    'closes': trade['price']
                }
            else:
                # If the trade is in the current candle, update the last candle in self.candles
                last_candle['highs'] = max(last_candle['highs'], trade['price'])
                last_candle['lows'] = min(last_candle['lows'], trade['price'])
                last_candle['volumes'] += trade['amount']
                last_candle['closes'] = trade['price']
                
                # Update the last candle in self.candles
                self.candles['highs'][-1] = last_candle['highs']
                self.candles['lows'][-1] = last_candle['lows']
                self.candles['volumes'][-1] = last_candle['volumes']
                self.candles['closes'][-1] = last_candle['closes']
            
        dpg.configure_item(
            self.candlestick_plot_tag, 
            dates=self.candles['dates'], 
            opens=self.candles['opens'],
            highs=self.candles['highs'],
            lows=self.candles['lows'],
            closes=self.candles['closes']
        )
