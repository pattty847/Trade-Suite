import dearpygui.dearpygui as dpg


def launch_indicator_panel(sender, app_data, user_data):
        
    with dpg.window(label="Indicator", tag="indicator-window", width=400, height=500, pos=[0, 25], on_close = lambda: dpg.delete_item("indicator-window")):

        indicator_list = ["RSI", "MACD", "MFI", "SMA", "EMA", "REV"]
        with dpg.table(header_row=False):

            for col in range(4):
                dpg.add_table_column()

            
            with dpg.table_row():
                for item in indicator_list:
                    dpg.add_selectable(label=item)