import dearpygui.dearpygui as dpg


def push_trade_panel(sender, primary_window_width):
    with dpg.window(label="Trade", width=500, height=500, tag="trade-window", pos=[primary_window_width - 520, 25], on_close= lambda sender: dpg.delete_item(sender)):
        with dpg.menu_bar(tag='trade-menu-bar'):

            with dpg.menu(label="Menu"):

                with dpg.menu(label="Settings"):
                    pass
                
        with dpg.group():

            dpg.add_input_float(label="Limit", default_value=20000, format="%.06f", width=-1)

        with dpg.table(header_row=False, borders_innerH=True, 
                borders_outerH=True, borders_innerV=True, 
                borders_outerV=True, width=-1):
        
            # Add two columns
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row(height=50):

                dpg.add_button(label='Buy', height=48, width=-1)
                dpg.add_button(label='Sell', height=48, width=-1)
            
        with dpg.table(header_row=False, borders_innerH=True, 
                borders_outerH=True, borders_innerV=True, 
                borders_outerV=True, width=-1):

            dpg.add_table_column()

            with dpg.table_row(height=50):

                dpg.add_button(label='Cancel', height=48, width=-1)