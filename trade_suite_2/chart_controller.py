from chart import Charts
import dearpygui.dearpygui as dpg
import uuid

class ChartController:

    def __init__(self, parent_window, primary_monitor) -> None:
        self.parent_window = parent_window
        self.primary_monitor = primary_monitor
        self.active_charts = dict()

    def new_chart(self, sender, app_data, user_data):
        chart_id = str(uuid.uuid4())
        chart = Charts(tag=chart_id, parent=self.parent_window)
        self.active_charts[chart.tag] = chart
        self.position_charts()

    def position_charts(self):
        offset = 26
        width = dpg.get_item_width(self.parent_window)
        height = dpg.get_item_height(self.parent_window) - offset
        num_charts = min(len(self.active_charts), 4)

        # Set the size and position of each chart window
        for i, (chart_id, chart) in enumerate(self.active_charts.items()):
            if i >= num_charts:
                break
            if num_charts == 1:
                dpg.set_item_width(chart_id, width)
                dpg.set_item_height(chart_id, height)
                dpg.set_item_pos(chart_id, [0, offset])
            elif num_charts == 2:
                chart_size = [width / 2, height]
                chart_pos = [i * chart_size[0], offset]
                dpg.set_item_width(chart_id, chart_size[0])
                dpg.set_item_height(chart_id, chart_size[1])
                dpg.set_item_pos(chart_id, chart_pos)
            elif num_charts == 3:
                chart_positions = [[0, offset], [0, height / 2 + offset], [width / 2, height / 2 + offset]]
                chart_size = [[width, height / 2], [width / 2, height / 2], [width / 2, height / 2]]
                chart_pos = chart_positions[i]
                dpg.set_item_width(chart_id, chart_size[i][0])
                dpg.set_item_height(chart_id, chart_size[i][1])
                dpg.set_item_pos(chart_id, chart_pos)
            elif num_charts == 4:
                chart_positions = [[0, offset], [width / 2, offset], [0, height / 2 + offset], [width / 2, height / 2 + offset]]
                chart_size = [width / 2, height / 2]
                chart_pos = chart_positions[i]
                dpg.set_item_width(chart_id, chart_size[0])
                dpg.set_item_height(chart_id, chart_size[1])
                dpg.set_item_pos(chart_id, chart_pos)
