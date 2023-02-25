from chart import Charts
import dearpygui.dearpygui as dpg
import uuid


class ChartController:
    def __init__(
        self, parent_window, primary_monitor, window_width, window_height
    ) -> None:
        self.parent_window = parent_window
        self.primary_monitor = primary_monitor
        self.active_charts = dict()
        self.window_width = window_width
        self.window_height = window_height

    def new_chart(self):
        chart_id = str(uuid.uuid4())
        chart = Charts(
            tag=chart_id,
            parent=self.parent_window,
            chart_controller=self,
            window_width=self.window_width,
            window_height=self.window_height,
        )
        self.active_charts[chart.tag] = chart
        self.position_charts()

    def load_favorite(self, exchange_name, symbol, timeframe):
        chart_id = str(uuid.uuid4())
        chart = Charts(
            tag=chart_id,
            parent=self.parent_window,
            chart_controller=self,
            window_width=self.window_width,
            window_height=self.window_height,
            exchange_name="coinbasepro",
            symbol="BTC/USDT",
            timeframe="1h",
        )
        self.active_charts[chart.tag] = chart
        self.position_charts()

    def position_charts(self):
        offset = 26
        width = dpg.get_item_width(self.parent_window)
        height = dpg.get_item_height(self.parent_window) - offset
        num_charts = min(len(self.active_charts), 4)

        # Set the size and position of each chart window
        for i, (chart_tag, chart_obj) in enumerate(self.active_charts.items()):
            if i >= num_charts:
                break
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
