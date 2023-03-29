import dearpygui.dearpygui as dpg


class Button:
    def __init__(self, label, stage=True, **kwargs):
        self._children = []
        if stage:
            with dpg.stage() as self.stage:
                self.tag = dpg.add_button(label=label, **kwargs)
        else:
            self.tag = dpg.add_button(label=label, **kwargs)

    def submit(self, parent):
        dpg.push_container_stack(parent)
        dpg.unstage(self.stage)
        dpg.pop_container_stack()


class MainWindow:
    def __init__(self, label, stage=True, **kwargs):
        self._children = []
        if stage:
            with dpg.stage() as self.stage:
                self.tag = dpg.add_window(label=label, **kwargs)
        else:
            self.tag = dpg.add_window(label=label, **kwargs)

    def submit(self, parent):
        dpg.push_container_stack(parent)
        dpg.unstage(self.stage)
        dpg.pop_container_stack()

class ViewPort:
    def __init__(self, title, width, height, x_pos=0, y_pos=0):
        self.title = title
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tag = "root"
        self.objects = []

    def __enter__(self):
        dpg.create_context()
        dpg.add_window(tag=self.tag)
        self.setup_viewport()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(self.tag, True)

        # start custom rendering loop
        while dpg.is_dearpygui_running():
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            for obj in self.objects:
                pass
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def setup_viewport(self):
        b = Button("test", parent=self.tag)
        self.add_object(b)
        for s in self.objects:
            s.submit(self.tag)
        dpg.create_viewport(title=self.title, width=self.width, height=self.height, x_pos=self.x_pos, y_pos=self.y_pos)

    def add_object(self, obj):
        self.objects.append(obj)

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpg.destroy_context()



# with ViewPort(title='Custom Title', width=600, height=200, x_pos=500, y_pos=500) as viewport:
#     # Clean up
#     pass