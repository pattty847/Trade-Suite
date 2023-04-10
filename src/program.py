# This is the main program class where all UI elements contained on the front page are defind
import dearpygui.dearpygui as dpg
from gui.strategy import Strategy
from chart import Charts
from utils.loading import loading_overlay

# Name can be changed to the official name later.
class Program:
    def __init__(self, viewport) -> None:
        self.viewport = viewport
        self.parent = self.viewport.tag
    
    # First call for this class
    def build_ui(self):
        self.add_menu_bar()
        self.add_tab_bar()
        
    def add_menu_bar(self):
        with dpg.menu_bar(parent=self.parent):
            with dpg.menu(label="test"):
                pass
            
    def add_tab_bar(self):
        # Add a tab bar to the main window
        with dpg.tab_bar(parent=self.parent):

            with dpg.tab(label='Charts'):
                with dpg.child_window(menubar=True) as charts:
                    self.chart = Charts(charts, self.viewport)
                    # self.chart.draw_chart('coinbasepro', 'BTC/USD', '1m')
                
            with dpg.tab(label="Strategy"):
                with dpg.child_window() as strategy:
                    self.strategy = Strategy(strategy, self.viewport)
                    self.strategy.build_ui()