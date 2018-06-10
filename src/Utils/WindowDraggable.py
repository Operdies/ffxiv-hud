import re

class WindowDraggaable:
    def __init__(self, label, master, fd):
        self.fd = fd
        self.master = master
        self.label = label
        self.x = None
        self.y = None
        self.move = False
        label.bind('<ButtonPress-1>', self.start_move)
        label.bind('<ButtonRelease-1>', self.stop_move)
        label.bind('<B1-Motion>', self.on_motion)

    def get_dims(self):
        good_re = r'(\d+)x(\d+)\+(\d+)\+(\d+)'
        keys = ['width', 'height', 'x', 'y']
        whxy = re.findall(good_re, self.master.geometry())[0]

        return dict(zip(keys, whxy))

    def start_move(self, e):
        self.x = e.x
        self.y = e.y

    def stop_move(self, e):
        self.x = None
        self.y = None
        new = self.get_dims()
        for key in new:
            self.fd[key] = new[key]

    def on_motion(self, e):
        x = (e.x_root - self.x)
        y = (e.y_root - self.y)
        # self.move = not self.move  # only move on every other tick to avoid stutter
        if x > 0 and y > 0:# and self.move:
            self.master.geometry("+{}+{}".format(x, y))
