# This is the main program class where all UI elements contained on the front page are defind
import ccxt
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from chart import Charts
from utils.loading import loading_overlay

# Name can be changed to the official name later.
class Program:
    def __init__(self, viewport) -> None:
        self.viewport = viewport
        self.parent = self.viewport.tag
    
    # First call for this class
    def build_ui(self):
        self.add_menu_bar()
        self.add_tab_bar()
    
    # UI elements defined below
    def add_menu_bar(self):
        with dpg.menu_bar(parent=self.parent):
            
            with dpg.menu(label="Chart"):
                dpg.add_combo(label="Exchange", items=['coinbasepro', 'kucoin', 'kraken', 'cryptocom'], width=150, callback=self.add_source_modal)
            
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Demo", callback=demo.show_demo)
            

    def add_tab_bar(self):
        # Add a tab bar to the main window
        with dpg.tab_bar(parent=self.parent):

            with dpg.tab(label='Tab 1') as tab_1:
                self.chart = Charts(tab_1).draw_chart('coinbasepro', 'BTC/USD', '1m')
                
            with dpg.tab(label="Tab 2") as tab_2:
                pass
    
    def add_source_modal(self, sender, app_data, user_data):
        self.exchange = dpg.get_value(sender)

        if self.exchange == 'coinbasepro':
            self.ccxt_obj = ccxt.coinbasepro()
        elif self.exchange == 'kucoin':
            self.ccxt_obj = ccxt.kucoin()
        elif self.exchange == 'kraken':
            self.ccxt_obj = ccxt.kraken()
        elif self.exchange == 'cryptocom':
            self.ccxt_obj = ccxt.cryptocom()
        if not self.ccxt_obj.has['fetchOHLCV']:
            return

        with loading_overlay():
            self.ccxt_obj.load_markets() 

        self.symbols = sorted(self.ccxt_obj.symbols)
        self.timeframes = sorted(list(self.ccxt_obj.timeframes))
        

        with dpg.window(modal=True, popup=True, width=-1, height=-1, no_close=True, tag='data_source') as source_modal:
            symbol = dpg.add_combo(label="Symbol", default_value='BTC/USDT', items=self.symbols, width=150)
            timeframe = dpg.add_combo(label="Timeframe", default_value=self.timeframes[0], items=self.timeframes, width=150)
            dpg.add_button(label="Add Chart", callback=self.chart.draw_chart, user_data=[self.exchange, symbol, timeframe, source_modal])