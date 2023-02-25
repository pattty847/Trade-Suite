from asyncio import run
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
        timeframe=None,
    ):
        self.tag = tag
        self.parent = parent
        self.chart_controller = chart_controller
        self.window_width = window_width
        self.window_height = window_height

        self.id = str(id(self))

        self.menu_tag = self.id + "_menu"
        self.subplot_tag = self.id + "_subplot"
        self.candlestick_plot_tag = (self.id + "_candle_series",)
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

        dpg.add_window(label=f"{self.tag}", tag=self.tag, width=500, height=500)

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
        self.exchange_name = exchange_name
        self.describe = do.get_exchange_info(exchange_name)
        self.symbols = self.describe["symbols"]
        self.timeframes = self.describe["timeframes"]
        self.update_window()

    def update_window(self):
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
        if not favorite:
            self.symbol = dpg.get_value(symbol)
            self.timeframe = dpg.get_value(timeframe)
        else:
            self.symbol = symbol
            self.timeframe = timeframe

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
                self.tag + "_candle_series",
            )
        )
        thread = threading.Thread(
            target=self.start_watch_function,
            args=(self.exchange_name, "watchTrades", self.symbol),
        )
        thread.start()

        dpg.delete_item(self.last_chart)

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
                        self.candles["time"],
                        self.candles["open"],
                        self.candles["close"],
                        self.candles["low"],
                        self.candles["high"],
                        tag=self.id + "_candle_series",
                        time_unit=do.convert_timeframe(self.timeframe),
                    )

                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_candles)

            # Volume plot
            with dpg.plot(tag=self.volume_plot_tag):
                dpg.add_plot_legend()
                xaxis_vol = dpg.add_plot_axis(
                    dpg.mvXAxis, label="Time [UTC]", time=True
                )

                with dpg.plot_axis(dpg.mvYAxis, label="USD"):
                    dpg.add_line_series(self.candles["time"], self.candles["volume"])

                    dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis_vol)

    def start_watch_function(self, exchange_name, method, symbol):
        asyncio.run(self.watch_function(exchange_name, method, symbol))

    async def watch_function(self, exchange_name, method, symbol, *args, **kwargs):
        exchange_class = getattr(ccxtpro, exchange_name)
        exchange = exchange_class(
            {
                "enableRateLimit": True,  # add rate limiter
            }
        )
        while True:
            try:
                # watch the data using the specified method
                data = await getattr(exchange, f"{method}")(symbol, *args, **kwargs)
                print(data)
            except ccxt.BaseError as e:
                # handle errors
                print(str(e))
            finally:
                await exchange.close()