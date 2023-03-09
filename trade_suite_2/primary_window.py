import dearpygui.dearpygui as dpg
from chart_controller import ChartController
import utils.DoStuff as do


class PrimaryWindow:
    def __init__(self, primary_monitor, window_width, window_height) -> None:
        self.primary_monitor = primary_monitor
        self.primary_window = "primary_window"
        self.chart_controller = ChartController(
            self.primary_window, self.primary_monitor, window_width, window_height
        )

    def window_setup(self):
        # Primary Window for Program
        dpg.add_window(tag=self.primary_window)

        # Load the font registry
        self.load_font()

        # Draw the navigation bar
        self.draw_nav_bar()

        # Launch favorites immediately upon open here
        # self.chart_controller.load_favorite("coinbasepro", "BTC/USD", "1m")
        # self.chart_controller.position_charts()

    def load_font(self):
        # add a font registry and loads main font
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf filec
            default_font = dpg.add_font("fonts/LandasansMedium-ALJ6m.otf", 20)
            dpg.bind_font(default_font)

    def draw_nav_bar(self):
        with dpg.viewport_menu_bar(parent=self.primary_window):
            do.draw_dpg_tools()

            # TODO: for fav in favorites: add menu item
            with dpg.menu(label="Favorites"):
                with dpg.menu(label="CoinbasePro"):
                    dpg.add_menu_item(
                    label="BTC/USDT 1H",
                    callback= lambda : self.chart_controller.load_favorite("coinbasepro", "BTC/USD", "1m"),
                )

            with dpg.menu(label="Charts"):
                dpg.add_menu_item(label="+", callback=self.chart_controller.new_chart)