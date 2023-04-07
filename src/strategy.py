import dearpygui.dearpygui as dpg

from .strategy_builder import Strategy_Builder

class Strategy:
    def __init__(self, parent, viewport):
        self.viewport = viewport
        self.parent = parent
        self.strategy_builder = Strategy_Builder()
        
        # This will be called and initialized when the user chooses a symbol and timeframe
        self.source = None
        
        # Get the viewport (main window) width
        viewport_width = dpg.get_viewport_width()
        # Calculate the desired width for the child window (20% of viewport width)
        child_width = int(0.20 * viewport_width)
        # Calculate the horizontal position for the child window (right-aligned)
        self.child_x_pos = viewport_width - child_width

        self.build_ui()
                    
    def build_ui(self):
        with dpg.child_window(parent=self.parent, width=self.child_x_pos - 12, height=-1, menubar=True):
            with dpg.menu_bar():
                dpg.add_menu_item(label="Strategy Builder", callback=self.strategy_builder.build_ui)
                
            with dpg.plot(width=-1, height=-1) as self.plot:
                pass
        
        # Create the child window with the specified dimensions and position
        with dpg.child_window(parent=self.parent, width=-1, height=-1, pos=[self.child_x_pos, 50], menubar=True):
            with dpg.menu_bar():
                with dpg.menu(label="Strategy"):
                    dpg.add_menu_item(label="Save Strategy", callback=self.save_strategy)
                    dpg.add_menu_item(label="Load Strategy", callback=self.load_strategy)
                
            with dpg.group(tag='strategy'):
                with dpg.group():
                    dpg.add_text("Timeframe:")
                    dpg.add_combo(items=["1m", "5m", "15m", "1h", "4h", "1d"],
                                default_value="1h",
                                callback=self.change_timeframe,
                                width=-1)
                
                with dpg.group():
                    dpg.add_text("Indicators:")
                    dpg.add_listbox(items=["SMA", "EMA", "RSI", "MACD"],
                                num_items=4,
                                callback=self.add_indicator,
                                width=-1)
                    
                with dpg.group():
                    dpg.add_text("Exchange:")
                    dpg.add_combo(items=["Exchange 1", "Exchange 2", "Exchange 3"],
                                default_value="Exchange 1",
                                callback=self.change_exchange,
                                width=-1)
                    dpg.add_text("Symbol:")
                    dpg.add_input_text(callback=self.change_symbol,
                                width=-1)
                
                with dpg.group():
                    dpg.add_text("Stop-Loss (%):")
                    dpg.add_input_float(callback=self.set_stop_loss, width=-1)
                    dpg.add_text("Take-Profit (%):")
                    dpg.add_input_float(callback=self.set_take_profit, width=-1)
                    dpg.add_text("Trade Size:")
                    dpg.add_input_float(callback=self.set_trade_size, width=-1)
                
                # Backtesting Controls
                with dpg.group():
                    dpg.add_text("Backtest Range:")
                    dpg.add_input_text(callback=self.set_backtest_start, label="Start Date", width=-1)
                    dpg.add_input_text(callback=self.set_backtest_end, label="End Date", width=-1)
                    dpg.add_button(label="Run Backtest", callback=self.run_backtest, width=-1)
                
                # Strategy Logs
                with dpg.group():
                    dpg.add_text("Strategy Logs:")
                    dpg.add_input_text(multiline=True, readonly=True, tag="strategy_logs", width=-1, height=100)
                    
                with dpg.group():
                    dpg.add_button(label="Start Strategy", callback=self.start_strategy, width=-1)
                    dpg.add_button(label="Stop Strategy", callback=self.stop_strategy, width=-1)
                    dpg.add_button(label="Monitor Symbol", callback=self.monitor_symbol, width=-1)

    # Callbacks for the interactive controls
    def change_timeframe(self, sender, app_data):
        # Implement logic to change the timeframe
        pass

    def add_indicator(self, sender, app_data):
        # Implement logic to add a technical indicator to the chart
        pass

    def change_exchange(self, sender, app_data):
        # Implement logic to change the selected exchange
        pass

    def change_symbol(self, sender, app_data):
        # Implement logic to change the selected symbol
        pass

    def start_strategy(self, sender, app_data):
        # Implement logic to start a trading strategy
        pass

    def stop_strategy(self, sender, app_data):
        # Implement logic to stop a trading strategy
        pass

    def monitor_symbol(self, sender, app_data):
        # Implement logic to monitor a specific symbol
        pass

    def set_stop_loss(self, value):
        pass

    def set_take_profit(self, value):
        pass

    def set_trade_size(self, value):
        pass

    def set_backtest_start(self, value):
        pass

    def set_backtest_end(self, value):
        pass

    def run_backtest(self):
        pass

    def save_strategy(self):
        pass

    def load_strategy(self):
        pass
