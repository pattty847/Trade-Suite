import uuid


class ChartController:

    def __init__(self, parent_window) -> None:
        self.parent_window = parent_window
        self.charts = dict()

    def create_chart(self, chart):
        self.charts[uuid.uuid4()] = chart