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

        logging.info("Adding mouse and keyboard registries")
        self.load_keyboard_mouse_handler()

        # Draw the navigation bar
        logging.info("Adding Navigation Bar")
        self.draw_nav_bar()

        # Launch favorites immediately upon open here
        # logging.info("Loading Favorite Chart: coinbasepro BTC/USD 1m")
        # self.chart_controller.new_chart("coinbasepro", "BTC/USD", "1m")

    def load_keyboard_mouse_handler(self):
        with dpg.handler_registry(show=False, tag="keyboard_handler"):
            k_down = dpg.add_key_down_handler(key=dpg.mvKey_A)
            k_release = dpg.add_key_release_handler(key=dpg.mvKey_A)
            k_press = dpg.add_key_press_handler(key=dpg.mvKey_A)

        with dpg.handler_registry(show=False, tag="mouse_handler"):
            m_wheel = dpg.add_mouse_wheel_handler()
            m_click = dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left)
            m_double_click = dpg.add_mouse_double_click_handler(button=dpg.mvMouseButton_Left)
            m_release = dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left)
            m_drag = dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left)
            m_down = dpg.add_mouse_down_handler(button=dpg.mvMouseButton_Left)
            m_move = dpg.add_mouse_move_handler()

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
                    callback= lambda : self.chart_controller.new_chart("coinbasepro", "BTC/USD", "1m"),
                )
                    
            dpg.add_menu_item(label="Full", callback=dpg.toggle_viewport_fullscreen)
            
            with dpg.menu(label="Charts"):
                dpg.add_menu_item(label="New", callback=self.chart_controller.new_chart_menu)
                dpg.add_menu_item(label="Position Charts", callback=self.chart_controller.position_charts)
                dpg.add_menu_item(label="Settings", callback=self.chart_controller.chart_settings_menu)