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


def push():
    for line in dequeue:
        # Wrap each message in a button that displays more info when clicked
        dpg.add_button(label=line, callback=show_details, parent="Console")


def show_details(sender):
    # Show more information about the clicked message
    dpg.add_text(f"Details for {sender}: Lorem ipsum...", parent="Primary Window")


dequeue = Console(1000, "asd")
for i in range(2000):
    dequeue.append(f"Line {i}\n")

# dpg.create_context()

# with dpg.window(tag="Primary Window"):
#     # Add a new console window
#     with dpg.window(tag="Console", width=600, height=200):
#         pass
#     dpg.add_button(label="Click", callback=push)

# dpg.create_viewport(title='Custom Title', width=600, height=200, y_pos=200)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.set_primary_window("Primary Window", True)
# dpg.start_dearpygui()
# dpg.destroy_context()