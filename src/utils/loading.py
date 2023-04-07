import dearpygui.dearpygui as dpg
import contextlib

@contextlib.contextmanager
def loading_overlay():
    # Create a transparent full-viewport window with no title bar, no border, and no resize option
    with dpg.window(no_title_bar=True, no_resize=True, no_move=True, no_close=True,
                    no_background=True, id="loading_overlay", autosize=True):
        dpg.add_separator()
        dpg.add_text("Loading", id="loading_text")
        dpg.add_separator()
        loading_item = dpg.add_loading_indicator()
    dpg.show_item("loading_overlay")
    try:
        yield loading_item
    finally:
        dpg.delete_item("loading_overlay")