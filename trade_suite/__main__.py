import datetime
import json
import os
import threading
import time
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import ccxt
import utils.DoStuff as do
import stats
import settings.config as config
from settings.config import DefaultSettings as config
from charts import Charts
from screeninfo import get_monitors

class Main(Charts):

    def __init__(self):
        # DPG tags for items
        self.MAIN_WINDOW = "main"
        self.CHART_WINDOW = "chart"
        self.MAIN_MENU_BAR = "main-menu-bar"

        # List of active chart objects
        self.active_exchanges = []

        # Dictionary containing config options
        self.config = self.load_settings()

        # Main viewport size
        self.primary_window_width = self.config['main_window']['primary_window_width']
        self.primary_window_height = int(self.config['main_window']['primary_window_width'] * 0.5625)

        # List of exchange titles
        self.EXCHANGE_LIST = ccxt.exchanges

        # List of user favorite exchanges
        # TODO: Add favorites menu
        self.EXCHANGE_FAVORITES = ["binance", "coinbasepro", "kucoin"]

        # Adds developer menu
        self.dev = True

        # Starts program
        self.run_program()


    def load_settings(self):
        """ This function will be called upon startup to load the settings or store the default settings,
        and set the self.config

        Returns:
            dict: Dictionary object containing a structure like below.
        """

        # TODO (under construction): Using "pydanntic" BaseModel to declare the same default_settings structure here
        settings = config(
            fullscreen=True, 
            main_window={"primary_window_width": 1600},
            last_chart={"binance":["BTCUSDT", "1d"]},
            exchanges={
                "mode": "sandbox",
                "binance": {
                    "apiKey": "",
                    "secret": ""
                },
                "kucoin": {
                    "apiKey": "",
                    "secret": ""
                }
            }
        )

        default_settings = {
            "fullscreen":"True",
            "main_window": {
                "primary_window_width": 1600
            },
            "last_saved_chart":{
                "binance":["BTCUSDT", "1d"]
            },
            "exchanges": {
                "mode": "sandbox",
                "binance": {
                    "apiKey": "",
                    "secret": ""
                },
                "kucoin": {
                    "apiKey": "",
                    "secret": ""
                }
            }
        }

        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError as e:
            with open("config.json", "w") as f:
                json.dump(default_settings, f)
            return default_settings


    def load_markets(self, exchange):
        """ Check if we have an api key and secret for the exchange and return a ccxt exchange object, and 
        if no credentials return one with no trading capabilities plus the markets for that exchange.

        It will save the market data to "exchanges" directory for faster loads.

        Args:
            exchange (str): Name of string.

        Returns:
            ccxt exchange, JSON: Returns the ccxt object and a dict containing all the markets.
        """
        if exchange in self.config['exchanges'].keys() and self.config['exchanges']['mode'] != "sandbox":
            api = getattr(ccxt, exchange) (
                {
                    "id":exchange,
                    "apiKey":self.config['exchanges'][exchange]['apiKey'],
                    "secret":self.config['exchanges'][exchange]['secret']
                }
            )
            print(api.check_required_credentials())
            print(f"Exchange: [{exchange}] | Trading: Yes")
        else:
            print(f"Exchange: [{exchange}] | Trading: No")
            api = getattr(ccxt, exchange) ()

        if not os.path.isdir("exchanges/markets"):
            os.makedirs("exchanges/markets")


        if api.has['fetchOHLCV'] != True:
            print("This exchange does not offer candlestick data.")
            return None
        try:
            with open(f"exchanges/markets/{exchange}-markets.json") as f:
                markets =  json.load(f)
                return api, markets
        except FileNotFoundError as e:
            markets = api.load_markets()
            with open(f"exchanges/markets/{exchange}-markets.json", "w") as f:
                json.dump(markets, f, sort_keys=True)
            return api, markets

    
    def load_fonts(self):
        # add a font registry and loads main font
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf filec
            default_font = dpg.add_font("fonts/LandasansMedium-ALJ6m.otf", 20)
            return default_font



    def new_chart(self, sender, app_data, user_data):
        """ Load a new exchange window (chart).

        Args:
            sender (int): id of listbox user clicked to add chart
            app_data (None): None
            user_data (str): Exchange name user clicked on
        """

        # Check if there is already a window with the tag exchange
        if not dpg.does_item_exist(user_data):
            dpg.add_loading_indicator(circle_count=7, parent=self.MAIN_WINDOW, tag="main-loading", pos=[self.primary_window_width/2, self.primary_window_height/2 - 110], radius=10.0)
        
            # Call load_markets function passing the exchange
            api, markets = self.load_markets(user_data)

            # If the market returned markets and has fetchOHLCV abilities. 
            if markets:
                dpg.delete_item("main-loading")
                user_data = Charts(
                    exchange= user_data,
                    symbol=None,
                    timeframe=None,
                    api=api,
                    viewport_width = self.primary_window_width,
                    viewport_height = self.primary_window_height,
                    markets=markets
                )
                self.active_exchanges.append(user_data)
            else:
                dpg.delete_item("main-loading")

    # TODO: Finish this
    def push_exchange_to_favorites(self, sender, app_data, user_data):
        exchange_value = dpg.get_value("exchange-list")
        if exchange_value not in self.EXCHANGE_FAVORITES:
            self.EXCHANGE_FAVORITES.append(exchange_value)
            dpg.configure_item("favorites-list", items=self.EXCHANGE_FAVORITES)
            dpg.delete_item("error-text")
        else:
            dpg.add_text("Already in Favorites", tag="error-text", parent="add-to-row")

    # TODO: Finish this
    def close_favorites(self):
        dpg.delete_item(dpg.last_container())
        pass


    def add_exchange_to_favorites(self):
        with dpg.window(label="Exchange Favorites", modal=True, width=450, height=355, pos=(self.primary_window_width/2, self.primary_window_height/2), on_close=self.close_favorites):
            with dpg.table():
                dpg.add_table_column(label="Exchanges")
                dpg.add_table_column(label="Favorites")         

                with dpg.table_row():
                    dpg.add_listbox(self.EXCHANGE_LIST, num_items=10, tag="exchange-list")
                    dpg.add_listbox(self.EXCHANGE_FAVORITES, num_items=10, tag="favorites-list")

                with dpg.table_row(tag="add-to-row"):
                    dpg.add_button(label="Add To", callback=self.push_exchange_to_favorites)


    def set_fullscreen_option(self):
        self.config.update({"fullscreen":"False"}) if self.config['fullscreen'] == "True" else self.config.update({"fullscreen":"True"})
        print(self.config['fullscreen'])


    def market_stats_panel(self, sender, app_data, user_data):
        stats.push_stats_panel()


    def clock(self):
        i = 0
        while True:
            dpg.configure_item("clock", label=str(datetime.datetime.now().strftime("%x %X")))
            if i == 0:
                time.sleep(1/datetime.datetime.now().second)
            else:
                time.sleep(1)
            i+=1


    def draw_main_menu_nav_bar(self):

        with dpg.viewport_menu_bar(tag=self.MAIN_MENU_BAR):

            dpg.add_menu_item(label="", tag="clock")
            x = threading.Thread(target=self.clock, daemon=True)
            x.start()
            
            with dpg.menu(label="Full Screen"):
                dpg.add_menu_item(label="Toggle", callback=dpg.toggle_viewport_fullscreen)
                dpg.add_checkbox(
                    label="Open in Fullscreen?", 
                    default_value=True if self.config['fullscreen'] == "True" else False, 
                    callback=self.set_fullscreen_option
                )
        
            if self.dev:
                # Developer Menu
                with dpg.menu(label="DPG Tools"):
                    dpg.add_menu_item(label="Show ImGui Demo", callback=dpg.show_imgui_demo)
                    dpg.add_menu_item(label="Show ImPlot Demo", callback=dpg.show_implot_demo)
                    dpg.add_menu_item(label="Show DPG Demo", callback=demo.show_demo)
                    dpg.add_menu_item(label="Show Debug", callback=dpg.show_debug)
                    dpg.add_menu_item(label="Show About", callback=lambda: dpg.show_tool(dpg.mvTool_About))
                    dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_tool(dpg.mvTool_Metrics))
                    dpg.add_menu_item(label="Show Documentation", callback=lambda: dpg.show_tool(dpg.mvTool_Doc))
                    dpg.add_menu_item(label="Show Debug", callback=lambda: dpg.show_tool(dpg.mvTool_Debug))
                    dpg.add_menu_item(label="Show Style Editor", callback=lambda: dpg.show_tool(dpg.mvTool_Style))
                    dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_tool(dpg.mvTool_Font))
                    dpg.add_menu_item(label="Show Item Registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry))

            
            with dpg.menu(label="New Chart"):
                with dpg.menu(label="Exchange"):
                    for exchange in self.EXCHANGE_LIST:
                        dpg.add_selectable(label=exchange.capitalize(), callback=self.new_chart, user_data=exchange)

                with dpg.menu(label="Favorites"):
                    for exchange in self.EXCHANGE_FAVORITES:
                        dpg.add_selectable(label=exchange.capitalize(), callback=self.new_chart, user_data=exchange.lower())


            dpg.add_menu_item(label="Stats", callback=self.market_stats_panel)


            with dpg.menu(label="Settings"):
                dpg.add_selectable(label="Add Exchange to Favorites", callback=self.add_exchange_to_favorites)


    def draw_main_menu(self, font):
        with dpg.window(label="Main Menu", tag=self.MAIN_WINDOW):

            dpg.bind_font(font)


    def run_program(self):
        """ This function will set up the overall dearpygui framework, create a viewport, set the main window, and includes the
        menu bar function calls for the overall program that appears at the top of the viewport.

        """

        # If the user turns on fullscreen, we set the viewport windows to the resolution of the screen.
        self.isFullscreen()
        
        dpg.create_context()

        with dpg.item_handler_registry(tag="item-handler"):
            pass

        font = self.load_fonts()
        self.draw_main_menu(font)
        self.draw_main_menu_nav_bar()

        # Here we can immediately draw the chart layout using the last saved chart
        last_exchange = list(self.config['last_saved_chart'].keys())[0]
        last_symbol = self.config['last_saved_chart'][last_exchange][0]
        last_timeframe = self.config['last_saved_chart'][last_exchange][1]
        
        api, markets = self.load_markets(last_exchange)
        last_saved_chart = Charts(
            exchange = last_exchange,
            symbol=last_symbol,
            timeframe=last_timeframe,
            api = api,
            viewport_width = self.primary_window_width,
            viewport_height = self.primary_window_height,
            markets=markets
        )
        self.active_exchanges.append(last_saved_chart)
        last_saved_chart.draw_chart(symbol=last_symbol, timeframe=last_timeframe, parent=last_exchange)


        dpg.create_viewport(title='Trade Suite', x_pos=5, y_pos=5, width=self.primary_window_width, height=self.primary_window_height)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        # DPG toggle for fullscreen must go here
        if self.config['fullscreen'] == "True":

            dpg.toggle_viewport_fullscreen()

        dpg.set_primary_window(self.MAIN_WINDOW, True)
        while dpg.is_dearpygui_running():
                        
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            dpg.render_dearpygui_frame()


        # Items placed after the while will be executed upon program close.
        # Use this to save any unsaved config changes.
        with open("config.json", "w") as f:
            json.dump(self.config, f)
        dpg.destroy_context()


    def isFullscreen(self):
        from screeninfo import get_monitors
        def get_monitor_size():
            monitors = get_monitors()
            for m in monitors:
                if m.is_primary:
                    monitors = m
            main_monitor = {"width":monitors.width, "height":monitors.height}
            return main_monitor

        monitor = get_monitor_size()

        if self.config['fullscreen'] == "True":
            self.primary_window_width = monitor["width"]
            self.primary_window_height = monitor["height"]


if __name__ == "__main__":
    trade_suite = Main()