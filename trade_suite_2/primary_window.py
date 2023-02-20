import dearpygui.dearpygui as dpg
from chart_controller import ChartController
import utils.DoStuff as do
import dearpygui.demo as demo

class PrimaryWindow:

    def __init__(self, primary_monitor, window_width, window_height) -> None:
        self.primary_monitor = primary_monitor
        self.primary_window = "primary_window"
        self.chart_controller = ChartController(self.primary_window, self.primary_monitor)

    def window_setup(self):
        # Primary Window for Program
        dpg.add_window(tag=self.primary_window)

        # Load the font registry
        self.load_font()

        # Draw the navigation bar
        self.draw_nav_bar()


    def load_font(self):
        # add a font registry and loads main font
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf filec
            default_font = dpg.add_font("fonts/LandasansMedium-ALJ6m.otf", 20)
            dpg.bind_font(default_font)

    def draw_nav_bar(self):
        with dpg.viewport_menu_bar(parent=self.primary_window):
            do.draw_dpg_tools()

            with dpg.menu(label="Charts"):
                dpg.add_menu_item(label="+", callback=self.chart_controller.new_chart)