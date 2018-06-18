import re


class WindowDraggable:
    def __init__(self, label, master, et):
        self.et = et
        self.master = master
        self.label = label
        self.x = None
        self.y = None
        self.move = False
        label.bind('<ButtonPress-1>', self.start_move)
        label.bind('<ButtonRelease-1>', self.stop_move)
        label.bind('<B1-Motion>', self.on_motion)

    def get_dims(self, ele):
        good_re = r'(\d+)x(\d+)\+(\d+)\+(\d+)'
        keys = ['width', 'height', 'x', 'y']
        whxy = re.findall(good_re, self.master.geometry())[0]

        return dict(zip(keys, whxy))

    def start_move(self, e):
        self.x = e.x  # hack value to offset GP bar
        self.y = e.y

    def stop_move(self, e):
        self.x = None
        self.y = None

    def on_motion(self, e):
        x = max((e.x_root - self.x), 0)
        y = max((e.y_root - self.y), 0)
        if self.et.expander.big:
            x -= 8
            y -= 32
        self.master.geometry("+{}+{}".format(x, y))
