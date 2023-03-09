import dearpygui.dearpygui as dpg


class Console:
    def __init__(self, max_lines, parent):
        self.max_lines = max_lines
        self.tag = parent + "_console"
        self.lines = []

    def append(self, line):
        self.lines.append(f"{line}")
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def __len__(self):
        return len(self.lines)

    def __iter__(self):
        return iter(self.lines)


dequeue = Console(1000, "asd")
for i in range(2000):
    dequeue.append(f"Line {i}\n")

def push():
    for line in dequeue:
        dpg.add_text(line, parent="Primary Window")


# dpg.create_context()

# with dpg.window(tag="Primary Window"):
#     dpg.add_button(label="Click", callback=push)

# dpg.create_viewport(title='Custom Title', width=600, height=200, y_pos=200)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.set_primary_window("Primary Window", True)
# dpg.start_dearpygui()
# dpg.destroy_context()