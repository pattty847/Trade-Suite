import dearpygui.dearpygui as dpg
import utils.DoStuff as do
import ccxt
import ccxt.pro as ccxtpro

class Charts:

    def __init__(self, tag, parent):
        self.tag = tag
        self.parent = parent

        self.exchange = None
        self.describe = None
        self.symbols = None
        self.timeframes = None

        dpg.add_window(
            label=f"{self.tag}", 
            tag=self.tag, 
            width=500, 
            height=500
        )

        self.draw_nav_bar()


    def draw_nav_bar(self):
        with dpg.menu_bar(parent=self.tag):
            with dpg.menu(label="Chart"):
                dpg.add_listbox(ccxt.exchanges, label="Exchange", num_items=10, callback=self.create_exchange)


    def create_exchange(self, sender, exchange_name, user_data):
        exchange_class = getattr(ccxtpro, exchange_name)
        self.exchange = exchange_class({
            'enableRateLimit': True,  # adjust as needed
            # add other exchange-specific options here
        })
        self.describe = self.exchange.describe()
        self.symbols = self.describe.get("symbols", None)
        self.timeframes = self.describe.get("timeframes", None)
        dpg.configure_item(self.tag, label=f"{exchange_name.upper()}")