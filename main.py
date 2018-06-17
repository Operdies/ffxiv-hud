from src import MainWindow, BotanistHelper
from src import ContextManager, FileDict
from src.Database import Crawler
from tkinter import Tk
import win32gui
from time import sleep, time
from collections import deque

own_hwnd = None
FPS = 250

dark_grey = '#313031'
darker_grey = '#272627'

def enum_handler(hwnd, lParam):
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
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', exit_gracefully)
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

    # root.wm_attributes('-transparentcolor', 'black')
    botanist_helper = BotanistHelper(unix, dt, ratio)
    crawler = Crawler()
    root.wait_visibility(root)
    root.geometry('{}x{}+{}+{}'.format(640, 28, 500, 500))
    app = MainWindow(root, botanist_helper, crawler, lambda: win32gui.EnumWindows(enum_handler, None))
    app.update_loop()  # initialise stuff before gui is shown
    win32gui.EnumWindows(enum_handler, None)
    prior_hwnd = None
    q = deque(maxlen=3)
    # root.geometry('{}x{}+{}+{}'.format(int(fd['width']), fd['height'], fd['x'], fd['y']))
    # fd['width'], fd['height'], fd['x'], fd['y'] = 620, 20, 500, 500
    while True:
        start = time()
        win32gui.EnumWindows(enum_handler, None)
        # print(own_hwnd)
        hwnd = win32gui.GetForegroundWindow()
        root.call('wm', 'attributes', '.', '-topmost', '1')
        root.update_idletasks()
        root.update()
        app.update_loop()

        if hwnd != own_hwnd and hwnd is not 0:
            prior_hwnd = hwnd
            q.append(hwnd)

        if not app.expander.small and (prior_hwnd and own_hwnd == win32gui.GetForegroundWindow()):
            for ele in q:
                try:
                    win32gui.SetForegroundWindow(ele)
                    print('restoring', prior_hwnd)
                    break
                except:

                    # print('failed restoring', prior_hwnd)
                    pass

        sleep_time = 1 / FPS - (time() - start)
        # sleep(max(1 / FPS - (time() - start), 0))
        if sleep_time > 0:
            sleep(sleep_time)  # cap updates at FPS / sec
