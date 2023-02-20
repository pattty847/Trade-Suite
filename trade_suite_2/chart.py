import dearpygui.dearpygui as dpg


class Charts:

    def __init__(self, tag, parent):
        self.tag = tag
        self.parent = parent

        dpg.add_window(
            label=f"{self.tag}", 
            tag=self.tag, 
            width=500, 
            height=500
        )

        self.draw_nav_bar()


    def draw_nav_bar(self):
        with dpg.menu_bar(parent=self.tag):
            with dpg.menu(label="Menu"):
                dpg.add_text("This menu is just for show!")