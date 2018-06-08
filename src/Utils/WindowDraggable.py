class WindowDraggaable:
    def __init__(self, label, master):
        self.master = master
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, e):
        self.x = e.x
        self.y = e.y

    def StopMove(self, e):
        self.x = None
        self.y = None

    def OnMotion(self, e):
        x = (e.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (e.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        geo = "+{}+{}".format(x, y)
        self.master.geometry(geo)
