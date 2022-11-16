import dearpygui.dearpygui as dpg
import utils.DoStuff as do
import pandas as pd
import os


def pull_stats():
    URL = 'https://coinalyze.net/'
    columns = ["Coin", "Price", "Chg 24H", "Vol 24H", "Open Interest", "OI Chg 24H", "OI Share", "OI / VOL24H", "FR AVG", "PFR AVG", "Liqs. 24H"]
    stats = pd.read_html(URL)[0][columns]

    top_ten = stats.head(10)
    
    try:
        with open("exchanges/stats/previous_stats.csv", "r"):
            previous_stats = pd.read_csv("exchanges/stats/previous_stats.csv")
    except FileNotFoundError as e:
        os.makedirs("exchanges/stats")
        stats.to_csv(f"exchanges/stats/previous_stats.csv", index=False)
        previous_stats = None
    
    return (stats, previous_stats, columns, top_ten)

def push_stats_panel(sender, primary_window_width):

    market_stats, previous_stats, columns = pull_stats()

    with dpg.window(label="Crypto Stats", tag="stats-window", width=800, height=1000, pos=[15, 60], on_close = lambda sender: dpg.delete_item(sender)):
        
        with dpg.table(tag='stats-table', borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, resizable=True, sortable=True, callback=do.sort_callback):
            
            for col in columns:                                       # Generates the correct amount of columns
                dpg.add_table_column(label=col)                       # Adds the headers

            
            
            for i in range(market_stats.shape[0]):                    # Shows the first n rows
                
                with dpg.table_row():
                    
                    for j in range(market_stats.shape[1]):
                        
                        dpg.add_text(f"{market_stats.iloc[i,j]}")