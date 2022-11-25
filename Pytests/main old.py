import json
import ccxt as ccxt
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

import utils.DoStuff as do
from Chart import Chart
import trade as trade
import stats as stats

class Program():

    def __init__(self) -> None:
        self.primary_window_width = 2000
        self.primary_window_height = int(self.primary_window_width * 0.5625)

        self.settings = self.load_settings()

        self.exchange_list = ['binance']


    def load_settings(self):
        """ This will load the settings from the file.

        Returns:
            dict: Settings as a dictionary
        """
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        except FileNotFoundError as e:
            with open("settings.json", "w") as f:
                initial_settings = {"exchanges": {"main": {"exchange": "binance", "favorites": 
                                   {"BTCUSDT": "15m", "ETHUSDT": "15m"}}}, "last_timeframe": "1m", "timezone": "2022-10-01T00:00:00Z", "last_symbol": "BTC/USDT"}
                json.dump(initial_settings, f)
        return settings

    # TODO: No longer using ccxt to fetch exchange data. All exchanges will be implimented in src/Exchanges. Function not needed anymore.
    def init_exchanges(self, exchanges):
        """ This function will initialize all exchanges store in the settings file.

        Args:
            exchanges (list): exchanges list

        Returns:
            dict: dictionary of ccxt exchanges accessable by their name
        """
        ccxt_list = {}
        for exchange in self.exchange_list: # TODO: change back to exchanges for all exchanges
            api = getattr(ccxt, exchange)()
            ccxt_list[api.id] = api
        return ccxt_list

    def delete_chart(self, item):
        """This is called when a chart is deleted or closed. 

        Args:
            item (string): this is the exchange name which will be used to delete the items associated with the window
            like the symbol and timeframe listboxes.
        """
        dpg.delete_item(item)
        dpg.delete_item(f"symbol-{item}")
        dpg.delete_item(f"timeframe-{item}")


    def create_chart(self, app_data, user_data, immediate = False):
        app_data = dpg.get_value("exchange-list")
        """ This will be called when you select an exchange from the Chart Settings window

        Args:
            sender (str): sender tag of dpg item
            app_data (str): exchange name
            user_data (str): user data = None
            immediate (bool): Specifies whether we are adding a favorite ticker immediately upon opening the program.
        """
        with dpg.window(label=f'Exchange: [{app_data}]',
            tag=app_data, 
            on_close=self.delete_chart(app_data), 
            width=self.primary_window_width - 25, 
            height=self.primary_window_height - 75, 
            pos=[5, 25]):

            # This will create a chart object with the settings, app_data = exchange name, viewport width and height. 
            # Move to chart file to see how it works. 
            # Push a chart immediately opon open
            self.chart = Chart(self.settings, app_data, self.primary_window_width, self.primary_window_height)

    def chart_settings_panel(self):
        """This is the window for settings. Mainly used, right now, as an exchange chooser. 
        """
        # TODO: Fix on_close

        with dpg.window(label="Chart Settings", tag='settings', autosize=True, pos=[5, 25], on_close = lambda sender: dpg.delete_item(sender)):
            dpg.add_input_text(tag=f"exchange-searcher", hint="Search",
                                            callback=lambda sender, data: do.searcher(f"exchange-searcher", 
                                            f"exchange-list", self.exchange_list))
            # Here when the user clicks an exchange it will create a window for that exchange.
            dpg.add_listbox(self.exchange_list, callback = self.create_chart, num_items=10, label="Exchange", tag="exchange-list")

    
    def trade_panel(self, sender, app_data, user_data):
        trade.push_trade_panel(sender, self.primary_window_width)


    def market_stats_panel(self, sender, app_data, user_data):
        stats.push_stats_panel(sender, self.primary_window_width)


    def dpg_setup(self):
        """ This function will set up the overall dearpygui framework, create a viewport, set the main window, and includes the
        menu bar for the overall program that appears at the top of the viewport.

        """
        dpg.create_context()

        # TODO: Make sure the save configuration works. 
        # dpg.configure_app(init_file="dpg.ini")

        with dpg.window(label="Main Menu", tag="main", no_resize=True, no_scrollbar=True):
            
            with dpg.viewport_menu_bar(tag='main-menu-bar'):

                # TODO: Add more options here
                with dpg.group(horizontal=True):
                    dpg.add_menu_item(label="Settings", callback=self.chart_settings_panel)
                    dpg.add_menu_item(label="Trade", callback=self.trade_panel)
                    dpg.add_menu_item(label="Market Stats", callback=self.market_stats_panel)
                
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


            # Here we can check if there is a main exchange and last_used_symbol that we can open immediately.
            # In the future when more exchanges are added you need to store favorite exchanges like so: "favorite_exchange":[ "binance":["BTC/USDT" (as main ticker)], "bitfinex":[FAVORITE SYMBOLS FOR EXCHANGE] ]
            # if self.settings['exchanges']['main'] != "":
            #     favorites = self.settings['exchanges']['main']
            #     exchange = list(favorites.values())[0]
            #     fav_tf, fav_ticker = list(favorites['favorites'].values())[0], list(favorites['favorites'].keys())[0]
            #     self.create_chart(exchange, (fav_ticker, fav_tf), True)

        dpg.create_viewport(title='Trade Suite', width=self.primary_window_width, height=self.primary_window_height, resizable=False)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main", True)
        while dpg.is_dearpygui_running():
            
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()


if __name__ == "__main__":
    # Create Program
    program = Program()

    # Set up dearpygui and create GUI
    program.dpg_setup()
    