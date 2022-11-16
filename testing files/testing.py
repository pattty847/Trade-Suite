import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from exchange import exchange

class Chart:

    def __init__(self, tag, primary_window_width, primary_window_height) -> None:
        self.tag = tag

        self.exchange = getattr(exchange, self.tag)

        self.primary_window_width = primary_window_width
        self.primary_window_height = primary_window_height
        

        self.draw_window()

    
    def draw_window(self):
        with dpg.window(
            label=self.tag, 
            tag=self.tag,
            pos=(5, 30),
            width= self.primary_window_width - 25,
            height= self.primary_window_height - 75): 

            with dpg.menu_bar():
                with dpg.menu():
                    pass

            with dpg.child_window():
                pass



class MainMenu():

    """ MainMenu will inherit from Chart. A chart contains the necessary functions and attributes to draw a chart window for a certain exchagne. """
    
    def __init__(self, tag):

        # List of exchanges that can be added to a chart window. 
        self.exchanges = ['binance', 'binance_futures']

        self.config = {
            "main_window":{"primary_window_width":2500},
            "default_symbol":"BTCUSDT",
            "default_exchange":"binance",
            "default_timeframe":"1h"
        }
        self.primary_window_width = self.config['main_window']['primary_window_width']
        self.primary_window_height = int(self.config['main_window']['primary_window_width'] * 0.5625)

        self.layout = 2

        self.active_windows = []

        self.run_program()


    def run_program(self):
        """ This function will set up the overall dearpygui framework, create a viewport, set the main window, and includes the
        menu bar for the overall program that appears at the top of the viewport.

        """
        
        dpg.create_context()

        with dpg.item_handler_registry(tag="item-handler"):
            pass

        self.load_fonts()
        self.draw_main_window()
        self.draw_charts_menu_nav_bar(parent="main")



        dpg.create_viewport(title='Trade Suite', width=self.primary_window_width, height=self.primary_window_height, resizable=False, x_pos=25, y_pos=25)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main", True)
        while dpg.is_dearpygui_running():
                        
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()


    def draw_main_window(self):
        # Our main window will be set to the main viewport for the program. Charts will be constructed from new windows from which they are given an exchange name as their tag.

        with dpg.window(label="Main Menu", tag="main", no_resize=True, no_scrollbar=True):
            pass


    def draw_charts_menu_nav_bar(self, parent):
        with dpg.menu_bar(parent=parent):

            with dpg.menu(label="Add Chart"):
                for exchange in self.exchanges:
                    with dpg.menu(label=exchange):
                        dpg.add_selectable(label="New Chart", callback=self.create_new_chart, user_data=exchange)


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


    def create_new_chart(self, sender, app_data, user_data):

        exchange = user_data
        
        if not dpg.does_alias_exist(exchange):
            exchange = Chart(exchange, self.primary_window_width, self.primary_window_height)
                

                
    def load_fonts(self):
        # add a font registry
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf filec
            default_font = dpg.add_font("assets/LandasansMedium-ALJ6m.otf", 20)
            dpg.bind_font(default_font)

    def set_timeframe(self, sender, app_data, user_data):
        self.timeframe = dpg.get_value(sender)
        dpg.configure_item(sender, label=dpg.get_value(sender))

    def set_symbol(self, sender, app_data, user_data):
        self.symbol = dpg.get_value(sender)
        dpg.configure_item(sender, label=dpg.get_value(sender))



main_menu = MainMenu("main-chart")