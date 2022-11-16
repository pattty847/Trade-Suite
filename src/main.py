import json
import os
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import ccxt
from Charts import Charts
import utils.DoStuff as do


# TODO: Maybe have each Chart() --extend--> Main()

class Main(Charts):

    def __init__(self) -> None:
        self.MAIN_WINDOW = "main"
        self.CHART_WINDOW = "chart"
        self.MAIN_MENU_BAR = "main-menu-bar"

        self.active_exchanges = []

        self.config = {
            "main_window":{"primary_window_width":2000},
            "default_symbol":"BTCUSDT",
            "default_exchange":"binance",
            "default_timeframe":"1h"
        }
        self.primary_window_width = self.config['main_window']['primary_window_width']
        self.primary_window_height = int(self.config['main_window']['primary_window_width'] * 0.5625)

        self.EXCHANGE_LIST = ccxt.exchanges

        self.dev = True


    def load_markets(self, exchange):
        api = getattr(ccxt, exchange) ()
        if api.has['fetchOHLCV'] != True:
            print("This exchange does not offer candlestick data.")
            return None
        try:
            with open(f"exchanges/{exchange}-markets.json") as f:
                markets =  json.load(f)
                return api, markets
        except FileNotFoundError as e:
            markets = api.load_markets()
            with open(f"exchanges/{exchange}-markets.json", "w") as f:
                json.dump(markets, f, sort_keys=True)
            return api, markets


    def new_chart(self, sender, app_data, user_data):
        """ Load a new exchange window.

        Args:
            sender (int): id of listbox user clicked to add chart
            app_data (None): None
            user_data (str): Exchange name user clicked on
        """
        # Check if there is already a window with the tag exchange
        if not dpg.does_alias_exist(user_data):
            dpg.add_loading_indicator(circle_count=7, parent=self.MAIN_WINDOW, tag="loading", pos=[self.primary_window_width/2, self.primary_window_height/2 - 110], radius=10.0)
        
            # Call load_markets function passing the exchange
            api, markets = self.load_markets(user_data)

            # If the market returned markets and has fetchOHLCV abilities. 
            if markets:
                dpg.delete_item("loading")
                user_data = Charts(
                    exchange= user_data,
                    api=api,
                    viewport_width = self.primary_window_width,
                    viewport_height = self.primary_window_height,
                    markets=markets
                )
                self.active_exchanges.append(user_data)
                print(self.active_exchanges)
            else:
                dpg.delete_item("loading")


    def draw_main_menu_nav_bar(self):

        with dpg.viewport_menu_bar(tag=self.MAIN_MENU_BAR):
            if self.dev:
                # TODO: Add more DPG GUI things, like stype editor, etc
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

                    


    def draw_main_menu(self, font):
        with dpg.window(label="Main Menu", tag=self.MAIN_WINDOW, no_resize=True, no_scrollbar=True):

            

            dpg.bind_font(font)
                
            self.draw_main_menu_nav_bar()


    def load_fonts(self):
        # add a font registry
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf filec
            default_font = dpg.add_font("assets/LandasansMedium-ALJ6m.otf", 20)
            return default_font


    def run_program(self):
        """ This function will set up the overall dearpygui framework, create a viewport, set the main window, and includes the
        menu bar for the overall program that appears at the top of the viewport.

        """

        # Create our data storage folders upon initial load
        if not os.path.isdir("exchanges"):
            os.makedirs("exchanges")
        
        dpg.create_context()

        with dpg.item_handler_registry(tag="item-handler"):
            pass

        font = self.load_fonts()
        self.draw_main_menu(font)


        dpg.create_viewport(title='Trade Suite', width=self.primary_window_width, height=self.primary_window_height, resizable=False)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(self.MAIN_WINDOW, True)
        while dpg.is_dearpygui_running():
                        
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()


trade_suite = Main()
trade_suite.run_program()