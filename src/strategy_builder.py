import dearpygui.dearpygui as dpg
import ccxt.pro as ccxtpro
import ccxt
from .loading import loading_overlay
from .data import DataCollector

# Base Node will define the following attributes which represent a base class for each node added.
# A node equals a small window consisting of an input, calculation, and output.
class Base_Node:
    def __init__(self, label, pos, node_editor, input_label, output_label, input_type):
        self.label = label
        self.pos = pos
        self.node_editor = node_editor
        self.input_label = input_label
        self.output_label = output_label
        self.input_type = input_type
        self.id = dpg.generate_uuid()

    def create_node(self, input_value=None):
        with dpg.node(label=self.label, parent=self.node_editor, pos=self.pos):
            with dpg.node_attribute():
                if self.input_label == "float":
                    dpg.add_input_float(label=self.input_label, width=150, default_value=input_value)
                elif self.output_label == "text":
                    dpg.add_input_text(label=self.input_label, width=150, default_value=input_value)

            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_input_float(label=self.output_label, width=150)
    

class Data_Source_Node(Base_Node, DataCollector):
    
    def __init__(self,  node_editor, pos, strategy):
        super().__init__("Data Source", pos, node_editor, input_label=None, output_label="Data", input_type=None)
        self.strategy = strategy

    def create_node(self):
        with dpg.node(label=self.label, parent=self.node_editor, pos=self.pos) as self.node_id:
            self.id = self.node_id
            with dpg.node_attribute():
                dpg.add_combo(label="Exchange", items=['coinbasepro', 'kucoin', 'kraken', 'cryptocom'], width=150, callback=self.add_source_modal)
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                self.output_label = dpg.add_text("")
    
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

        with dpg.window(modal=True, popup=True, width=-1, height=-1, no_close=True, tag='data_source'):
            symbol = dpg.add_combo(label="Symbol", default_value='BTC/USDT', items=self.symbols, width=150, callback=self.add_source_modal)
            timeframe = dpg.add_combo(label="Timeframe", default_value=self.timeframes[0], items=self.timeframes, width=150, callback=self.add_source_modal)
            dpg.add_button(label="Set Data", callback=self.add_data_source, user_data=[self.exchange, symbol, timeframe])

        
    def add_data_source(self, sender, app_data, user_data):
        dpg.configure_item('data_source', show=False)
        exchange, symbol_widget, timeframe_widget = user_data
        symbol = dpg.get_value(symbol_widget)
        timeframe = dpg.get_value(timeframe_widget)
        new_label = f"{exchange} - {symbol} - {timeframe}"
        dpg.configure_item(self.output_label, label=new_label)
        print(user_data)

class SMA_Node(Base_Node):

    def __init__(self,  node_editor, pos=None):
        super().__init__("SMA", pos, node_editor, input_label="Period", output_label="SMA Value", input_type="int")


class EMA_Node(Base_Node):
    
    def __init__(self,  node_editor, pos=None):
        super().__init__("EMA", pos, node_editor, input_label="F1", output_label="F2", input_type="float")


class MACD_Node(Base_Node):
    
    def __init__(self,  node_editor, pos=None):
        super().__init__("MACD", pos, node_editor, input_label="F1", output_label="F2", input_type="float")


class CrossOver_Node(Base_Node):
    
    def __init__(self,  node_editor, pos=None):
        super().__init__("CROSSOVER", pos, node_editor, input_label="F1", output_label="F2", input_type="float")


class CrossUnder_Node(Base_Node):
    
    def __init__(self,  node_editor, pos=None):
        super().__init__("CROSSUNDER", pos, node_editor, input_label="F1", output_label="F2", input_type="float")


class Strategy_Builder:
    def __init__(self) -> None:
        self.source = ("open", "high", "low", "close", "volume")
        self.nodes = {}  # Keep track of created nodes
    
    def build_ui(self):
        if dpg.does_alias_exist('strategy_builder'):
            return
        with dpg.window(label="Strategy Builder", width=700, height=700, tag='strategy_builder') as strategy_builder_window:
            with dpg.menu_bar():
                with dpg.menu(label="Add Node"):
                    dpg.add_menu_item(label="Data Source", callback=self.add_node, user_data=("Data_Source", strategy_builder_window))
                    dpg.add_menu_item(label="SMA", callback=self.add_node, user_data=("SMA", strategy_builder_window))
                    dpg.add_menu_item(label="EMA", callback=self.add_node, user_data=("EMA", strategy_builder_window))
                    dpg.add_menu_item(label="MACD", callback=self.add_node, user_data=("MACD", strategy_builder_window))
                    dpg.add_menu_item(label="CROSSOVER", callback=self.add_node, user_data=("CROSSOVER", strategy_builder_window))
                    dpg.add_menu_item(label="CROSSUNDER", callback=self.add_node, user_data=("CROSSUNDER", strategy_builder_window))
                dpg.add_menu_item(label="Build", callback=self.build_strategy)

            with dpg.node_editor(parent=strategy_builder_window, callback=lambda sender, app_data: dpg.add_node_link(app_data[0], app_data[1], parent=sender), 
                                delink_callback=lambda sender, app_data: dpg.delete_item(app_data), minimap=True, minimap_location=dpg.mvNodeMiniMap_Location_BottomRight) as self.node_editor:
                pass
                        
    def add_node(self, sender, app_data, user_data):
        node_type, parent = user_data
        if node_type == "Data_Source":
            node = Data_Source_Node(self.node_editor, pos=(10, 10), strategy=self)
        elif node_type == "SMA":
            node = SMA_Node(self.node_editor, pos=(10, 10))
        elif node_type == "EMA":
            node = EMA_Node(self.node_editor, pos=(10, 10))
        elif node_type == "MACD":
            node = MACD_Node(self.node_editor, pos=(10, 10))
        elif node_type == "CROSSOVER":
            node = CrossOver_Node(self.node_editor, pos=(10, 10))
        elif node_type == "CROSSUNDER":
            node = CrossUnder_Node(self.node_editor, pos=(10, 10))
        # Add more conditions for other node types
        node.create_node()
        self.nodes[node.id] = node
        
    def build_strategy(self, sender, app_data, user_data):
        pass