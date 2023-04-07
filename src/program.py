# This is the main program class where all UI elements contained on the front page are defind
import json
import os
import ccxt
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from gui.strategy import Strategy
from chart import Charts
from utils.loading import loading_overlay

# Name can be changed to the official name later.
class Program:
    def __init__(self, viewport) -> None:
        self.viewport = viewport
        self.parent = self.viewport.tag
        self.load_favorites()
    
    # First call for this class
    def build_ui(self):
        self.add_menu_bar()
        self.add_tab_bar()
    
    # UI elements defined below
    def add_menu_bar(self):
        with dpg.menu_bar(parent=self.parent):
            
            with dpg.menu(label="Chart"):
                dpg.add_combo(label="Exchanges", items=['coinbasepro', 'kucoin', 'kraken', 'cryptocom'], width=150, callback=self.add_source_modal)
                dpg.add_button(label="Favorites", callback=self.show_favorites_window)
                
            with dpg.menu(label="Indicators"):
                dpg.add_menu_item(label="RSI")
            
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Demo", callback=demo.show_demo)
            
    def add_tab_bar(self):
        # Add a tab bar to the main window
        with dpg.tab_bar(parent=self.parent):

            with dpg.tab(label='Charts'):
                with dpg.child_window() as charts:
                    self.chart = Charts(charts, self.viewport)
                    self.chart.draw_chart('coinbasepro', 'BTC/USD', '1m')
                
            with dpg.tab(label="Tab 2"):
                with dpg.child_window() as strategy:
                    self.strategy = Strategy(strategy, self.viewport)
                    self.strategy.build_ui()
    
    def load_favorites(self):
        if os.path.exists('favorites.json'):
            with open('favorites.json', 'r') as f:
                self.favorites = json.load(f)
        else:
            self.favorites = []

    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def add_favorite(self, exchange, symbol, timeframe):
        favorite = {"exchange": exchange, "symbol": symbol, "timeframe": timeframe}
        if favorite not in self.favorites:
            self.favorites.append(favorite)
            self.save_favorites()
        favorite_str = f"{favorite['exchange']} - {favorite['symbol']} ({favorite['timeframe']}) added to favorites."
        dpg.set_value('added_favorite', favorite_str)

    def remove_favorite(self, sender, app_data, user_data):
        print(user_data)
        del self.favorites[user_data]
        self.save_favorites()
        dpg.delete_item('favorites_list')
        self.draw_favorites_list()
        
    def draw_favorites_list(self):
        with dpg.child_window(id="favorites_list", parent='favorites_window', autosize_x=True, autosize_y=False, horizontal_scrollbar=True):
            for index, favorite in enumerate(self.favorites):
                dpg.add_text(f"{favorite['exchange']} {favorite['symbol']} {favorite['timeframe']}", bullet=True, indent=10)
                with dpg.group(horizontal=True):
                    dpg.add_spacer()
                    dpg.add_button(label="Add", callback=lambda: self.chart.draw_chart(favorite['exchange'], favorite['symbol'], favorite['timeframe']))
                    dpg.add_button(label="Remove", callback=self.remove_favorite, user_data=index)
                dpg.add_separator()
                dpg.add_spacer()

    def show_favorites_window(self):
        def delete_favorites():
            dpg.delete_item('favorites_window')

        with dpg.window(label="Favorites", id="favorites_window", width=400, height=500, on_close=delete_favorites, pos=(25, 25)):
            dpg.add_spacer()
            self.draw_favorites_list()
            
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

        def delete_source_modal():
            dpg.delete_item('data_source')

        with dpg.window(modal=True, width=-1, height=-1, tag='data_source', on_close=delete_source_modal) as source_modal:
            symbol = dpg.add_combo(label="Symbol", default_value='BTC/USDT', items=self.symbols, width=150)
            timeframe = dpg.add_combo(label="Timeframe", default_value=self.timeframes[0], items=self.timeframes, width=150)
            dpg.add_button(label="Add Chart", callback=lambda: self.chart.draw_chart(self.exchange, symbol, timeframe))
            dpg.add_button(label="Add to Favorites", callback=lambda: self.add_favorite(self.exchange, dpg.get_value(symbol), dpg.get_value(timeframe)))
            dpg.add_button(label="Show Favorites", callback=self.show_favorites_window)
            dpg.add_text(tag='added_favorite', wrap=dpg.get_item_width('data_source'))