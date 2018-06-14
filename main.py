from src import MainWindow, BotanistHelper
from src import ContextManager, FileDict
from tkinter import Tk
import win32gui
from time import sleep, time

own_hwnd = None
FPS = 250

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
    # with open('eorzea_times.txt', 'r', encoding='ascii') as h:
    #    unix, dt, ratio = [str(line) for line in h.readlines()]
    #
    # unix = float(unix.split(':')[1].strip())
    # dt = parse(dt.split(': ')[1].strip())
    # ratio = float(ratio.split(':')[1].strip())
    with FileDict('settings/time_data') as fd:
        unix = fd['unix']
        dt = fd['dt']
        ratio = fd['ratio']

    bh = BotanistHelper(unix, dt, ratio)

    root = Tk()
    root.protocol('WM_DELETE_WINDOW', exit_gracefully)
    root.wait_visibility(root)
    root.wm_attributes('-transparentcolor', 'black')
    root.geometry('{}x{}+{}+{}'.format(int(fd['width']), fd['height'], fd['x'], fd['y']))
    app = MainWindow(root, bh)

    win32gui.EnumWindows(enumHandler, None)
    # print(own_hwnd)
    # q = deque(maxlen=10)
    prior_hwnd = None
    while True:
        start = time()
        # win32gui.EnumWindows(enumHandler, None)
        # print(own_hwnd)
        hwnd = win32gui.GetForegroundWindow()

        root.update_idletasks()
        root.update()
        app.update_loop()

        if hwnd != own_hwnd and hwnd is not  0:
            prior_hwnd = hwnd

        if prior_hwnd and own_hwnd == win32gui.GetForegroundWindow():
            try:
                win32gui.SetForegroundWindow(prior_hwnd)
                print('restoring', prior_hwnd)
            except :
                pass

        root.call('wm', 'attributes', '.', '-topmost', '1')
        sleep_time = 1 / FPS - (time() - start)
        # sleep(max(1 / FPS - (time() - start), 0))
        if sleep_time > 0:
            sleep(sleep_time) # cap updates at FPS / sec