import dearpygui.dearpygui as dpg
from nav_bar_callbacks import NavBarController
from chart_controller import ChartController
import utils.DoStuff as do
import dearpygui.demo as demo

class PrimaryWindow:

    def __init__(self, primary_monitor) -> None:
        self.title = "Trade Suite " + "v1.1"
        self.primary_monitor = primary_monitor
        self.primary_window = "primary_window"
        self.window_width = self.primary_monitor.width
        self.window_height = self.primary_monitor.height
        self.chart_controller = ChartController(self.primary_window)
        self.nav_bar_controller = NavBarController(self.primary_window, self.chart_controller)

    def start_program(self):
        """ This function will initialize the DearPyGui event loop and draw the Primary Window / Start the program. """
        dpg.create_context()

        # TRADE-SUITE START
        # Load the font registry
        self.load_font()

        # Draw the main window
        self.draw_window()

        # Draw the navigation bar
        self.draw_nav_bar()

        # DEARPYGUI VIEWPORT SETUP
        x_pos = self.primary_monitor.x + int(self.primary_monitor.width / 2) - int(self.window_width / 2)
        y_pos = self.primary_monitor.y + int(self.primary_monitor.height / 2) - int(self.window_height / 2)
        dpg.create_viewport(title=self.title, x_pos=x_pos, y_pos=y_pos, width=self.window_width, height=self.window_height)        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(self.primary_window, True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def draw_window(self):
        # Primary Window for Program
        dpg.add_window(tag=self.primary_window)

    def load_font(self):
        # add a font registry and loads main font
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf filec
            default_font = dpg.add_font("fonts/LandasansMedium-ALJ6m.otf", 20)
            dpg.bind_font(default_font)

    def draw_nav_bar(self):
        with dpg.viewport_menu_bar(parent=self.primary_window):
            do.draw_dpg_tools()

            with dpg.menu(label="?"):
                dpg.add_menu_item(label="New", callback=self.nav_bar_controller.new_chart)