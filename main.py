from audioop import add
import json
from operator import setitem
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

import ccxt as ccxt
import Exchange as api

import utils.DoStuff as do
from Chart import Chart

class Program():

    def __init__(self) -> None:
        self.primary_window_width = 2000
        self.primary_window_height = int(self.primary_window_width * 0.5625)

        self.settings = self.load_settings()

        self.exchange_list = list(self.init_exchanges(self.settings['exchanges']).keys())

    def load_settings(self):
        """ This will load the settings from the file.

        Returns:
            dict: Settings as a dictionary
        """
        with open("settings.json", "r") as f:
            settings = json.load(f)
        return settings


    def init_exchanges(self, exchanges):
        """ This function will initialize all exchanges store in the settings file.

        Args:
            exchanges (list): exchanges list

        Returns:
            dict: dictionary of ccxt exchanges accessable by their name
        """
        ccxt_list = {}
        for exchange in exchanges:
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


    def add_chart(self, sender, app_data, user_data):
        """ This will be called when you select an exchange from the Chart Settings window

        Args:
            sender (str): sender of dpg item
            app_data (str): exchange name
            user_data (str): user data = None
        """
        with dpg.window(label=f'Exchange: [{app_data}]', 
            tag=app_data, 
            on_close=self.delete_chart(app_data), 
            width=self.primary_window_width - 25, 
            height=self.primary_window_height - 75, 
            pos=[5, 25]):

            Chart(self.settings, app_data)


    def chart_settings(self):
        """This is the window for the settings
        """
        # TODO: Fix on_close

        with dpg.window(label="Chart Settings", width=500, height=500, pos=[5, 25], on_close = lambda sender: dpg.delete_item(sender)):
            dpg.add_listbox(self.exchange_list, callback = self.add_chart)


    def dpg_setup(self):
        # Dearpygui setup
        dpg.create_context()
        dpg.configure_app(init_file="dpg.ini")

        with dpg.window(label="Main Menu", tag="main", no_resize=True, no_scrollbar=True):
        
            
            with dpg.menu_bar(tag='main-menu-bar'):

                with dpg.group(horizontal=True):
                    dpg.add_menu_item(label="Settings", callback=self.chart_settings)
                
                with dpg.menu(label="DPG"):
                    dpg.add_menu_item(label="Debug", callback=dpg.show_debug)
                    dpg.add_menu_item(label="ImGui", callback=dpg.show_imgui_demo)
                    dpg.add_menu_item(label="ImPlot", callback=dpg.show_implot_demo)
                    dpg.add_menu_item(label="Demo", callback=demo.show_demo)

                with dpg.menu(label="Save"):
                    dpg.add_menu_item(label="Save Window Configurations")

        dpg.create_viewport(title='Idk Yet', width=self.primary_window_width, height=self.primary_window_height, resizable=False)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main", True)
        dpg.start_dearpygui()

        dpg.destroy_context()

program = Program()
program.dpg_setup()