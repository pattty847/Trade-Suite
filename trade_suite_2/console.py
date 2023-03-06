class Dequeue:
    def __init__(self, max_lines, parent):
        self.max_lines = max_lines
        self.tag = parent + "_console"
        self.lines = []

    def append(self, line):
        self.lines.append(f"{line}\n")
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def __len__(self):
        return len(self.lines)

    def __iter__(self):
        return iter(self.lines)


dequeue = Dequeue(1000, "asd")
for i in range(2000):
    dequeue.append(f"Line {i}")

for line in dequeue:
    print(line)