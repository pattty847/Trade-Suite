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
        with open("settings.json", "r") as f:
            settings = json.load(f)
        return settings


    def init_exchanges(self, exchanges):
        ccxt_list = {}
        for exchange in exchanges:
            api = getattr(ccxt, exchange)()
            ccxt_list[api.id] = api
        return ccxt_list

    def delete_chart(self, item):
        dpg.delete_item(item)
        dpg.delete_item("symbol")
        dpg.delete_item("timeframe")


    def add_chart(self, sender, app_data, user_data):
        with dpg.window(label=f'Exchange: [{app_data}]', 
            tag=app_data, 
            on_close=self.delete_chart(app_data), 
            width=self.primary_window_width - 25, 
            height=self.primary_window_height - 75, 
            pos=[5, 25]):

            chart = Chart(self.settings, app_data)


    def settings_window(self):
        with dpg.window(label="Chart Settings", tag="chart-window", width=500, height=500, pos=[5, 25], on_close=dpg.get_value("chart-window")):
            dpg.add_listbox(self.exchange_list, callback = self.add_chart)


    def dpg_setup(self):
        # Dearpygui setup
        dpg.create_context()
        dpg.configure_app(init_file="dpg.ini")

        with dpg.window(label="Main Menu", tag="main", no_resize=True, no_scrollbar=True):
        
            
            with dpg.menu_bar(tag='main-menu-bar'):

                with dpg.group(horizontal=True):
                    dpg.add_menu_item(label="Settings", callback=self.settings_window)
                
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