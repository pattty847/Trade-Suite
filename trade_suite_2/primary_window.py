import dearpygui.dearpygui as dpg
from chart_controller import ChartController
import utils.DoStuff as do
import logging

class PrimaryWindow:
    def __init__(self, primary_monitor, window_width, window_height) -> None:
        self.primary_monitor = primary_monitor
        self.primary_window = "primary_window"
        self.chart_controller = ChartController(
            self.primary_window, self.primary_monitor, window_width, window_height
        )

    def window_setup(self):
        # Primary Window for Program
        logging.info("Adding Primary Window")
        dpg.add_window(tag=self.primary_window)

        # Load the font registry
        logging.info("Adding Font Registry")
        self.load_font()

        # Draw the navigation bar
        logging.info("Adding Navigation Bar")
        self.draw_nav_bar()

        # Launch favorites immediately upon open here
        # logging.info("Loading Favorite Chart")
        # self.chart_controller.load_favorite("coinbasepro", "BTC/USD", "1m")

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
                    label="BTC/USD 1m",
                    callback= lambda : self.chart_controller.load_favorite("coinbasepro", "BTC/USD", "1m"),
                )
            
            dpg.add_menu_item(label="Symbols", callback=self.chart_controller.side_menu)

            with dpg.menu(label="Charts"):
                dpg.add_menu_item(label="New", callback=self.chart_controller.new_chart)
                dpg.add_menu_item(label="Position Charts", callback=self.chart_controller.position_charts)
                dpg.add_menu_item(label="Settings", callback=self.chart_controller.chart_settings_menu)