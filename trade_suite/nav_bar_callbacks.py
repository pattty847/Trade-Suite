import dearpygui.dearpygui as dpg
from chart import Charts
import utils.DoStuff as do

class NavBarController:

    def __init__(self, parent_window, chart_controller) -> None:
        self.parent_window = parent_window
        self.chart_controller = chart_controller

    def new_chart(self, sender, app_data, user_data):

        def draw_chart(sender, app_data, user_data):
            # Extract the exchange, symbol, and timeframe from the user data
            exchange, symbol, timeframe = user_data
            
            chart = Charts(exchange, symbol, timeframe)
            self.chart_controller.create_chart(chart)


        with dpg.window(label="Add New Chart", modal=True):
            exchange = dpg.add_listbox(['Binance', 'Kucoin', 'Coinbasepro', 'Bitmex'], label="Exchange")
            symbol = dpg.add_listbox(['Bitcoin', 'Ethereum'], label="Symbol")
            timeframe = dpg.add_listbox(['1m', '5m'])
            dpg.add_button(label="Close", callback=draw_chart, user_data=[exchange, symbol, timeframe])