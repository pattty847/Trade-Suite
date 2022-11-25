import datetime
import threading
import time
import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
import dearpygui.demo as demo



def get_monitor_size():
    monitors = get_monitors()
    for m in monitors:
        if m.is_primary:
            monitors = m
    main_monitor = {"width":monitors.width, "height":monitors.height}
    return main_monitor

monitor = get_monitor_size()



dpg.create_context()



with dpg.window(label="Tutorial", tag="main"):
    dpg.add_button(label="Show DPG Demo", callback=demo.show_demo)

    with dpg.handler_registry(show=False, tag="__demo_keyboard_handler"):
        k_down = dpg.add_key_down_handler(key=dpg.mvKey_A)
        k_release = dpg.add_key_release_handler(key=dpg.mvKey_A)
        k_press = dpg.add_key_press_handler(key=dpg.mvKey_A)

    with dpg.handler_registry(show=False, tag="__demo_mouse_handler"):
        m_wheel = dpg.add_mouse_wheel_handler()
        m_click = dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left)
        m_double_click = dpg.add_mouse_double_click_handler(button=dpg.mvMouseButton_Left)
        m_release = dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left)
        m_drag = dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left)
        m_down = dpg.add_mouse_down_handler(button=dpg.mvMouseButton_Left)
        m_move = dpg.add_mouse_move_handler()

    dpg.add_checkbox(label="Activate Keyboard Handlers (A key)", callback=lambda s, a: dpg.configure_item("__demo_keyboard_handler", show=a))
    dpg.add_checkbox(label="Activate Mouse Handlers (left button)", callback=lambda s, a: dpg.configure_item("__demo_mouse_handler", show=a))
    kh_down = dpg.add_text("Key id:  seconds:", label="Key Down Handler:", show_label=True)
    kh_release = dpg.add_text("Key id:", label="Key Release Handler:", show_label=True)
    kh_press = dpg.add_text("Key id:", label="Key Press Handler:", show_label=True)
    mh_click = dpg.add_text("Mouse id:", label="Mouse Click Handler", show_label=True)
    mh_double = dpg.add_text("Mouse id:", label="Mouse Double Click Handler", show_label=True)
    mh_down = dpg.add_text("Mouse id:  seconds:", label="Mouse Down Handler", show_label=True)
    mh_release = dpg.add_text("Mouse id:", label="Mouse Release Handler", show_label=True)
    mh_wheel = dpg.add_text("Mouse id:", label="Mouse Wheel Handler", show_label=True)
    mh_move = dpg.add_text("Mouse pos:", label="Mouse Move Handler", show_label=True)
    mh_drag = dpg.add_text("Mouse id:  delta:", label="Mouse Drag Handler", show_label=True)


    def _event_handler(sender, data):
        type=dpg.get_item_info(sender)["type"]
        if type=="mvAppItemType::mvKeyDownHandler":
            dpg.set_value(kh_down, f"Key id: {data[0]}, Seconds:{data[1]}")
        elif type=="mvAppItemType::mvKeyReleaseHandler":
            dpg.set_value(kh_release, f"Key id: {data}")
        elif type=="mvAppItemType::mvKeyPressHandler":
            dpg.set_value(kh_press, f"Key id: {data} + Shift: {dpg.is_key_down(dpg.mvKey_Shift)}")
        elif type=="mvAppItemType::mvMouseClickHandler":
            dpg.set_value(mh_click, f"Mouse id: {data} + Shift: {dpg.is_key_down(dpg.mvKey_Shift)}")
        elif type=="mvAppItemType::mvMouseDoubleClickHandler":
            dpg.set_value(mh_double, f"Mouse id: {data}")
        elif type=="mvAppItemType::mvMouseDownHandler":
            dpg.set_value(mh_down, f"Mouse id: {data[0]}, Seconds:{data[1]}")
        elif type=="mvAppItemType::mvMouseReleaseHandler":
            dpg.set_value(mh_release, f"Mouse id: {data}")
        elif type=="mvAppItemType::mvMouseWheelHandler":
            dpg.set_value(mh_wheel, f"Mouse id: {data}")
        elif type=="mvAppItemType::mvMouseMoveHandler":
            dpg.set_value(mh_move, f"Mouse pos: {data}")
        elif type=="mvAppItemType::mvMouseDragHandler":
            dpg.set_value(mh_drag, f"Mouse id: {data[0]}, Delta:{[data[1], data[2]]}")

    for handler in dpg.get_item_children("__demo_keyboard_handler", 1):
        dpg.set_item_callback(handler, _event_handler)

    for handler in dpg.get_item_children("__demo_mouse_handler", 1):
        dpg.set_item_callback(handler, _event_handler)


dpg.create_viewport(title='Custom Title', width=1200, height=1200, x_pos=2, y_pos=2)
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.toggle_viewport_fullscreen()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()