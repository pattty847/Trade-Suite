import json
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import utils.DoStuff as do
from charts import Charts
import ccxt

class MainMenu:

    def __init__(self) -> None:
        self.primary_window_width = 2000
        self.primary_window_height = int(self.primary_window_width * 0.5625)

        self.config = {
            "main_window":{"primary_window_width":1600},
            "last_saved_tabs":{
                "binance":{"BTCUSDT":"1h"},
                "kucoin":{"ETHUSDT":"1d"},
                "coinbasepro":{"ETHUSDT":"1d"},
                "bybit":{"ETHUSDT":"1d"}
            },
            "exchanges":{
                "mode":"sandbox",
                "binance":{ "apiKey":"", "secret":"" },
                "kucoin":{ "apiKey":"", "secret":"" }
            }
        }

        self.MAIN_MENU_BAR = "MAIN_MENU_BAR"
        self.window_count = 1

        self.program_init()


    def load_font(self):
        # add a font registry
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf filec
            default_font = dpg.add_font("fonts/LandasansMedium-ALJ6m.otf", 20)
            return default_font


    def load_markets(self, exchange):
        if exchange in self.config['exchanges'].keys() and self.config['exchanges']['mode'] != "sandbox":
            api = getattr(ccxt, exchange) (
                {
                    "apiKey":self.config['exchanges'][exchange]['apiKey'],
                    "secret":self.config['exchanges'][exchange]['secret']
                }
            )
            print(api.check_required_credentials())
            print(f"Exchange: [{exchange}] | Trading: Yes")
        else:
            print(f"Exchange: [{exchange}] | Trading: No")
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

    
    def create_chart(self, sender, app_data, user_data):
        with dpg.tab(label=sender, parent="main-tab-bar"):
            dpg.add_text("Tetss")

    def load_saved_tabs(self):
        for exchange in list(self.config['last_saved_tabs'].keys()):
            for symbol in list(self.config['last_saved_tabs'][exchange]):

                timeframe = self.config['last_saved_tabs'][exchange][symbol]
                parent_name = f"{exchange}-{timeframe}"

                with dpg.tab(label=f"{exchange.upper()} | {timeframe}", parent="main-tab-bar", tag=parent_name):
                    # Here you create a chart attached to the parent tab
                    dpg.add_text(parent_name)
                    
                    # Check if there is already a window with the tag exchange
                    dpg.add_loading_indicator(circle_count=7, parent="main", tag="main-loading", pos=[self.primary_window_width/2, self.primary_window_height/2 - 110], radius=10.0)
                
                    # Call load_markets function passing the exchange
                    api, markets = self.load_markets(exchange)

                    # If the market returned markets and has fetchOHLCV abilities. 
                    dpg.delete_item("main-loading")
                    user_data = Charts(
                        exchange= exchange,
                        parent=parent_name,
                        api=api,
                        viewport_width = self.primary_window_width,
                        viewport_height = self.primary_window_height,
                        markets=markets,
                        symbol=symbol,
                        timeframe=timeframe
                    )
        


    def program_init(self):
        dpg.create_context()

        with dpg.item_handler_registry(tag="item-handler"):
            pass

        with dpg.window(tag="Primary Window"):
            dpg.bind_font(self.load_font())
            with dpg.viewport_menu_bar(tag=self.MAIN_MENU_BAR):

                dpg.add_menu_item(label="Full Screen", callback=dpg.toggle_viewport_fullscreen)
        
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

            with dpg.child_window(pos=(5, 30), tag="main-window"):
                with dpg.tab_bar(tag="main-tab-bar"):
                    # This will load the last saved tabs and their charts
                    self.load_saved_tabs()

            
        dpg.create_viewport(title='Custom Title', width=self.primary_window_width, height=self.primary_window_height)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


x = MainMenu()