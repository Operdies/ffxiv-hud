class WindowDraggaable:
    def __init__(self, label, master):
        self.master = master
        self.label = label
        self.x = None
        self.y = None
        label.bind('<ButtonPress-1>', self.start_move)
        label.bind('<ButtonRelease-1>', self.stop_move)
        label.bind('<B1-Motion>', self.on_motion)

    def start_move(self, e):
        self.x = e.x
        self.y = e.y

    def stop_move(self, e):
        self.x = None
        self.y = None

    def on_motion(self, e):
        x = (e.x_root - self.x)
        y = (e.y_root - self.y)
        self.master.geometry("+{}+{}".format(x, y))
