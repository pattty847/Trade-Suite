import datetime
import threading
import time
import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
def get_monitor_size():
    monitors = get_monitors()
    for m in monitors:
        if m.is_primary:
            monitors = m
    main_monitor = {"width":monitors.width, "height":monitors.height}
    return main_monitor

monitor = get_monitor_size()


def thread_():
    i = 0
    while True:
        dpg.set_value("text", f"New text {i}")
        time.sleep(1)
        i+=1



dpg.create_context()

with dpg.window(label="Tutorial", tag="main"):
    # dpg.add_text("asdsad", tag="text")
    # x = threading.Thread(target=thread_, daemon=True)
    # x.start()
    print(datetime.datetime.now().microsecond)
    with dpg.table(header_row=False):

        rows = 2
        columns = 2



        for i in range(0, columns):
            dpg.add_table_column()

        for i in range(0, rows):

            with dpg.table_row():

                for j in range(0, columns):

                    with dpg.child_window():
                        dpg.add_text(f"Row{i} Column{j}")

dpg.create_viewport(title='Custom Title', width=monitor['width'], height=monitor["height"], x_pos=2, y_pos=2)
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.toggle_viewport_fullscreen()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()