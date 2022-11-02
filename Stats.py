import dearpygui.dearpygui as dpg
from CoinalyzeStats import Stats


def push_stats_panel(sender, primary_window_width):

    market = Stats()
    market_stats = market.get_stats()

    with dpg.window(label="Crypto Stats", tag="stats-window", width=800, height=1000, pos=[15, 60], on_close = lambda sender: dpg.delete_item(sender)):
        
        with dpg.table(tag='stats-table', borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, resizable=True):
            
            for i in range(market_stats.shape[1]):                    # Generates the correct amount of columns
                dpg.add_table_column(label=market_stats.columns[i])   # Adds the headers
            
            for i in range(market_stats.shape[0]):                    # Shows the first n rows
                
                with dpg.table_row():
                    
                    for j in range(market_stats.shape[1]):
                        
                        dpg.add_text(f"{market_stats.iloc[i,j]}")
                        # dpg.highlight_table_cell('stats-table', i, j, [0, 255, 0, 100])