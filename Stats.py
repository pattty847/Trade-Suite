import dearpygui.dearpygui as dpg
import utils.DoStuff as do
import pandas as pd


def pull_stats():
    URL = 'https://coinalyze.net/'
    stats = pd.read_html(URL)[0][["Coin", "Price", "Chg 24H", "Vol 24H", "Open Interest", "OI Chg 24H", "OI Share", "OI / VOL24H", "FR AVG", "PFR AVG", "Liqs. 24H"]]
    
    try:
        with open("CSV\\previous_stats.csv", "r"):
            previous_stats = pd.read_csv("CSV\\previous_stats.csv")
    except FileNotFoundError as e:
        stats.to_csv(f"previous_stats.csv", index=False)
        previous_stats = None
    
    return (stats, previous_stats)

def push_stats_panel(sender, primary_window_width):

    market_stats = pull_stats()[0]

    with dpg.window(label="Crypto Stats", tag="stats-window", width=800, height=1000, pos=[15, 60], on_close = lambda sender: dpg.delete_item(sender)):
        
        with dpg.table(tag='stats-table', borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, resizable=True, sortable=True, callback=do.sort_callback):
            
            for i in range(market_stats.shape[1]):                    # Generates the correct amount of columns
                dpg.add_table_column(label=market_stats.columns[i])   # Adds the headers
            
            for i in range(market_stats.shape[0]):                    # Shows the first n rows
                
                with dpg.table_row():
                    
                    for j in range(market_stats.shape[1]):
                        
                        dpg.add_text(f"{market_stats.iloc[i,j]}")