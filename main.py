from src import MainWindow, BotanistHelper
from src import ContextManager, FileDict
from src.Database import Crawler
from tkinter import Tk, ttk
import win32gui
from time import sleep, time
from collections import deque
from src.Styles import apply_styles

own_hwnd = None
FPS = 60


def get_xyhw():
    return root.winfo_x(), root.winfo_y(), root.winfo_height(), root.winfo_width()


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


def should_unfocus(prior_hwnd, own_hwnd, app):
    if prior_hwnd == 0:
        return False
    focused = own_hwnd == win32gui.GetForegroundWindow()
    borderless = not app.expander.big
    text_entry_active = app.itemview.entry_focused
    return focused and borderless and not text_entry_active


def update_dims(window_settings):
    x, y, h, w = get_xyhw()
    window_settings['x'] = x
    window_settings['y'] = y
    window_settings['h'] = h
    window_settings['w'] = w


with ContextManager('data'):
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', exit_gracefully)
    apply_styles()
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

    window_settings = FileDict('settings/window_settings', default=500)

    # root.wm_attributes('-transparentcolor', 'black')
    botanist_helper = BotanistHelper(unix, dt, ratio)
    crawler = Crawler()
    root.wait_visibility(root)
    root.geometry(
        '{}x{}+{}+{}'.format(window_settings['w'], window_settings['h'], window_settings['x'], window_settings['y']))
    app = MainWindow(root, botanist_helper, crawler, lambda: win32gui.EnumWindows(enum_handler, None))
    app.update_loop()  # initialise stuff before gui is shown
    win32gui.EnumWindows(enum_handler, None)
    prior_hwnd = None
    q = deque(maxlen=3)


    while True:
        start = time()
        win32gui.EnumWindows(enum_handler, None)
        update_dims(window_settings)
        hwnd = win32gui.GetForegroundWindow()
        root.call('wm', 'attributes', '.', '-topmost', '1')
        root.update_idletasks()
        root.update()
        app.update_loop()

        if hwnd != own_hwnd and hwnd is not 0:
            prior_hwnd = hwnd
            q.append(hwnd)

        if should_unfocus(prior_hwnd, own_hwnd, app):
            for ele in q:
                try:
                    win32gui.SetForegroundWindow(ele)
                    # print('restoring', prior_hwnd)
                    break
                except:

                    # print('failed restoring', prior_hwnd)
                    pass

        sleep_time = 1 / FPS - (time() - start)
        if sleep_time > 0:
            sleep(sleep_time)  # cap updates at FPS / sec
