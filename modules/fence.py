class VirtualFence:
    def __init__(self):
        self.box = None
        self.enabled = False

    def set_box(self, box):
        self.box = box

    def toggle(self):
        self.enabled = not self.enabled

    def clear(self):
        self.box = None

    def is_inside(self, px, py):
        if not self.enabled or not self.box:
            return False

        x1, y1, x2, y2 = self.box
        return x1 < px < x2 and y1 < py < y2