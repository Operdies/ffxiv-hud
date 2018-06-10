from dateutil.parser import parse
from src import MainWindow, BotanistHelper
from src import ContextManager, FileDict
from tkinter import Tk
import re
import win32gui
from collections import deque

good_re = r'(\d+)x(\d+)\+(\d+)\+(\d+)'

own_hwnd = None


def get_dims(root):
    keys = ['width', 'height', 'x', 'y']
    whxy = re.findall(good_re, root.geometry())[0]

    return dict(zip(keys, whxy))


def enumHandler(hwnd, lParam):
    global own_hwnd
    if win32gui.IsWindowVisible(hwnd):
        text = win32gui.GetWindowText(hwnd)
        if "Eorzea Timer" in text:
            own_hwnd = hwnd


def exit_gracefully():
    print('Now exiting like a flower')
    root.destroy()
    exit(0)


with ContextManager('data'):
    fd = FileDict('settings/time_data')
    # with open('eorzea_times.txt', 'r', encoding='ascii') as h:
    #    unix, dt, ratio = [str(line) for line in h.readlines()]
    #
    # unix = float(unix.split(':')[1].strip())
    # dt = parse(dt.split(': ')[1].strip())
    # ratio = float(ratio.split(':')[1].strip())
    unix = fd['unix']
    dt = fd['dt']
    ratio = fd['ratio']

    bh = BotanistHelper(unix, dt, ratio)

    root = Tk()
    root.protocol('WM_DELETE_WINDOW', exit_gracefully)
    root.wait_visibility(root)
    # root.attributes('-alpha', 0.6)
    root.wm_attributes('-transparentcolor', 'black')
    root.geometry('{}x{}+{}+{}'.format(int(fd['width']), fd['height'], fd['x'], fd['y']))
    # root.geometry('{}x{}+{}+{}'.format(600, fd['height'], fd['x'], fd['y']))
    app = MainWindow(root, bh)

    win32gui.EnumWindows(enumHandler, None)
    # print(own_hwnd)
    q = deque(maxlen=10)
    while True:

        win32gui.EnumWindows(enumHandler, None)
        # print(own_hwnd)
        hwnd = win32gui.GetForegroundWindow()

        root.update_idletasks()
        root.update()
        app.update_loop()


        # x_, y_ = root.winfo_x(), root.winfo_y()
        new = get_dims(root)
        for key in new:
            if fd[key] != new[key]:
                fd[key] = new[key]

        if hwnd != own_hwnd:
            q.append(hwnd)
        if hwnd != own_hwnd and own_hwnd == win32gui.GetForegroundWindow():
            for h in reversed(q):
                try:
                    win32gui.SetForegroundWindow(h)
                    break
                except:
                    print('OBJECTION')
                    continue

        root.call('wm', 'attributes', '.', '-topmost', '1')

        # if x_ != x or y_ != y:
        #    x = x_w
        #    y = y_
        #    fd['x'] = x
        #    fd['y'] = y
