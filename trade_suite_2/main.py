from primary_window import PrimaryWindow
import utils.DoStuff as do
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import logging


class TradeSuite:
    logging.basicConfig(
            level=logging.INFO, 
            filename="info_logs.log", 
            filemode="a", 
            format='%(asctime)s - %(message)s', 
            datefmt='%d-%b-%y %H:%M:%S'
        )
    
    def __init__(self) -> None:
        self.title = "Trade Suite " + "v1.2"
        self.primary_monitor = do.primary_monitor()
        self.window_width = int(self.primary_monitor.width * 0.90)
        self.window_height = int(self.primary_monitor.height * 0.90)
        self.primary_window = PrimaryWindow(
            primary_monitor=self.primary_monitor,
            window_width=self.window_width,
            window_height=self.window_height
        )

    def configure_dpg(self):
        """This function will initialize the DearPyGui event loop and draw the Primary Window / Start the program."""
        dpg.create_context()

        # MAIN ENTRY POINT TO PROGRAMR
        self.primary_window.window_setup()

        # DEARPYGUI VIEWPORT SETUP
        x_pos = (
            self.primary_monitor.x
            + int(self.primary_monitor.width / 2)
            - int(self.window_width / 2)
        )
        y_pos = (
            self.primary_monitor.y
            + int(self.primary_monitor.height / 2)
            - int(self.window_height / 2)
        )
        dpg.create_viewport(
            title=self.title,
            x_pos=x_pos,
            y_pos=y_pos,
            width=self.window_width,
            height=self.window_height,
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(self.primary_window.primary_window, True)
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == "__main__":
    logging.info("-----------------------------------------------")
    logging.info("Starting Trade Suite...")
    trade_suite = TradeSuite()
    trade_suite.configure_dpg()