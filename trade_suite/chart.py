import dearpygui.dearpygui as dpg


class Charts:

    def __init__(self, exchange, symbol, timeframe) -> None:
        self.exchange, self.symbol, self.timeframe = exchange, symbol, timeframe
        self.draw_window()

    def draw_window(self):
        with dpg.window(label=self.exchange):
            pass