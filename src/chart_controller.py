import dearpygui.dearpygui as dpg
import uuid
from chart import Charts
import logging
import ccxt
import utils.DoStuff as do

class ChartController:
    def __init__(
        self, parent_window, primary_monitor, window_width, window_height
    ) -> None:
        self.parent_window = parent_window
        self.primary_monitor = primary_monitor
        self.active_charts = {}
        self.window_width = window_width
        self.window_height = window_height
        self.exchanges = ["coinbasepro", "bitfinex", "binanceus", "bybit", "bitmex"]
        self.rows = 1
        self.cols = 1

    # Testing
    def build_stage(self):

        self.stage = dpg.add_child_window(parent=self.parent_window)

        with dpg.subplots(
            rows=self.rows,
            columns=self.cols,
            label="Test",
            width=-1,
            height=-1,
            link_all_x=True,
            parent=self.stage,
        ):
           with dpg.plot():
               pass

    def new_chart(self, exchange_name, symbol, timeframe):
        tag = str(uuid.uuid4())
        logging.info(f"Creating Chart Object: {tag}")
        chart = Charts(
            tag=tag,
            parent=self.parent_window,
            chart_controller=self,
            window_width=self.window_width,
            window_height=self.window_height,
            exchange_name=exchange_name,
            symbol=symbol,
            timeframe=timeframe,
        )
        self.active_charts[tag] = chart
        self.position_charts()

    def chart_settings_on_close_callback(self, sender):
        dpg.delete_item(sender)

    def chart_settings_menu(self, sender, app_data, user_data):
        if not dpg.does_alias_exist("chart_settings_menu"):
            with dpg.window(
                label="Settings", 
                tag="chart_settings_menu", 
                pos=[self.window_width / 2 - 250, self.window_height / 2 - 250], 
                width=500, 
                height=500, 
                on_close=self.chart_settings_on_close_callback
            ):
                pass

    def new_chart_on_close_callback(self, sender):
        dpg.delete_item(sender)

    def new_chart_menu(self, sender, app_data, user_data):
        with dpg.window(
            pos=[5, 31], 
            width=350, 
            height=self.window_height - 36, 
            on_close=self.new_chart_on_close_callback
        ):
            with dpg.group(tag="side_menu", horizontal=True):
                dpg.add_text("Exchange")
            
            for exchange in self.exchanges:
                with dpg.collapsing_header(label=exchange.upper()):
                    pass

    def position_charts(self):
        offset = 26
        width = dpg.get_item_width(self.parent_window)
        height = dpg.get_item_height(self.parent_window) - offset
        num_charts = min(len(self.active_charts), 4)

        # Set the size and position of each chart window
        for i, (chart_tag, chart_obj) in enumerate(self.active_charts.items()):
            logging.info(f"Positioning chart {i+1}: {chart_tag} / {num_charts}")
            if num_charts == 1:
                dpg.set_item_width(chart_tag, width)
                dpg.set_item_height(chart_tag, height)
                dpg.set_item_pos(chart_tag, [0, offset])
            elif num_charts == 2:
                chart_size = [width / 2, height]
                chart_pos = [i * chart_size[0], offset]
                dpg.set_item_width(chart_tag, chart_size[0])
                dpg.set_item_height(chart_tag, chart_size[1])
                dpg.set_item_pos(chart_tag, chart_pos)
            elif num_charts == 3:
                chart_positions = [
                    [0, offset],
                    [0, height / 2 + offset],
                    [width / 2, height / 2 + offset],
                ]
                chart_size = [
                    [width, height / 2],
                    [width / 2, height / 2],
                    [width / 2, height / 2],
                ]
                chart_pos = chart_positions[i]
                dpg.set_item_width(chart_tag, chart_size[i][0])
                dpg.set_item_height(chart_tag, chart_size[i][1])
                dpg.set_item_pos(chart_tag, chart_pos)
            elif num_charts == 4:
                chart_positions = [
                    [0, offset],
                    [width / 2, offset],
                    [0, height / 2 + offset],
                    [width / 2, height / 2 + offset],
                ]
                chart_size = [width / 2, height / 2]
                chart_pos = chart_positions[i]
                dpg.set_item_width(chart_tag, chart_size[0])
                dpg.set_item_height(chart_tag, chart_size[1])
                dpg.set_item_pos(chart_tag, chart_pos)

    def save_active_charts(self):
        pass
