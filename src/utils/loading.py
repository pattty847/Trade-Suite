import dearpygui.dearpygui as dpg
import contextlib

@contextlib.contextmanager
def loading_overlay():
    width = dpg.get_viewport_width()
    height = dpg.get_viewport_height()

    radius = 10
    thickness = 10
    indicator_width = 2 * (radius + thickness)
    indicator_height = 2 * (radius + thickness)

    # Create a transparent full-viewport window with no title bar, no border, and no resize option
    with dpg.window(no_title_bar=True, no_resize=True, no_move=True, no_close=True,
                    no_background=True, id="loading_overlay", autosize=True,
                    width=width, height=height, pos=(0, 0)):
        
        # Add the loading indicator with the desired style and size
        loading_item = dpg.add_loading_indicator(
            style=0, circle_count=8, speed=1.0, 
            radius=radius, thickness=thickness,
            color=(255, 255, 255),
            pos=(width // 2 - indicator_width, height // 2 - indicator_height))

    dpg.show_item("loading_overlay")
    
    try:
        yield loading_item
    finally:
        dpg.delete_item("loading_overlay")