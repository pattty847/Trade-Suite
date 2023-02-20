from primary_window import PrimaryWindow
import utils.DoStuff as do

class TradeSuite:

    def __init__(self) -> None:
        self.primary_window = PrimaryWindow(do.get_primary_window())

    def run(self):
        self.primary_window.start_program()


trade_suite = TradeSuite()
trade_suite.run()