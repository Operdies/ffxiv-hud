# coding: utf-8

from ctypes import c_ulong, c_int32, byref, sizeof, windll, c_ulonglong
import win32gui
from win32process import EnumProcessModules, GetModuleFileNameEx


class Reader:
    def __init__(self, window_title='FINAL FANTASY XIV', process_title='FINAL FANTASY XIV'):
        self.process_title = process_title
        self.window_title = window_title
        self.hwnd = None
        self.pid = None
        self.phwnd = None
        self.gp_ptr = None
        self.done = False
        # self.init()

    def get_process_data(self):
        read_access = 0x1F0FFF
        self.done = False
        win32gui.EnumWindows(self.get_hwnd, None)
        if self.hwnd is None:
            return 0
        pid = c_ulong()
        windll.user32.GetWindowThreadProcessId(self.hwnd, byref(pid))
        self.pid = pid.value
        self.phwnd = windll.kernel32.OpenProcess(read_access, False, self.pid)
        self.get_gp_ptr()

    def get_gp_ptr(self):
        base_address = self.get_base_address()
        real_ptr = c_ulonglong()
        bytes_read = c_ulonglong()
        real_ptr.value = base_address + 0x018fe408  # reverse engineered using cheat engine
        for offset in [0x38, 0x10, 0x18, 0x20, 0x20]:
            windll.kernel32.ReadProcessMemory(self.phwnd, real_ptr, byref(real_ptr), sizeof(real_ptr),
                                              byref(bytes_read))
            real_ptr.value += offset

        self.gp_ptr = real_ptr

    def get_gp(self):
        gp = c_int32()
        bytes_read = c_ulonglong()
        windll.kernel32.ReadProcessMemory(self.phwnd, self.gp_ptr, byref(gp), sizeof(gp),
                                          byref(bytes_read))
        if gp.value <= 0 or gp.value >= 800:
            self.get_process_data()
            # print(gp.value)

        return gp.value

    def get_hwnd(self, hwnd, l):
        if self.done:
            return
        self.hwnd = None
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if self.window_title in title:
                self.hwnd = hwnd
                self.done = True

                # print('found', title)


    def get_base_address(self):
        modules = EnumProcessModules(self.phwnd)
        for n_mod in modules:
            modName = GetModuleFileNameEx(self.phwnd, n_mod)
            if self.process_title in modName:
                return n_mod
