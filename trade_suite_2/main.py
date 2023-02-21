from primary_window import PrimaryWindow
import utils.DoStuff as do
import dearpygui.dearpygui as dpg


class TradeSuite:

    def __init__(self) -> None:
        self.title = "Trade Suite " + "v1.1"
        self.primary_monitor = do.primary_monitor()
        self.window_width = int(self.primary_monitor.width * 0.80)
        self.window_height = int(self.primary_monitor.height * 0.80)
        self.primary_window = PrimaryWindow(
            primary_monitor=self.primary_monitor,
            window_width=self.window_width,
            window_height=self.window_height
        )

    def configure_dpg(self):
        """ This function will initialize the DearPyGui event loop and draw the Primary Window / Start the program. """
        dpg.create_context()

        self.primary_window.window_setup()

        # DEARPYGUI VIEWPORT SETUP
        x_pos = self.primary_monitor.x + int(self.primary_monitor.width / 2) - int(self.window_width / 2)
        y_pos = self.primary_monitor.y + int(self.primary_monitor.height / 2) - int(self.window_height / 2)
        dpg.create_viewport(title=self.title, x_pos=x_pos, y_pos=y_pos, width=self.window_width, height=self.window_height)        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(self.primary_window.primary_window, True)
        dpg.start_dearpygui()
        dpg.destroy_context()


trade_suite = TradeSuite()
trade_suite.configure_dpg()