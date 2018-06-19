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
        self.max_ptr = None
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
        self.get_max_ptr()

    def get_ptr(self, offsets, address):
        base_address = self.get_base_address()
        real_ptr = c_ulonglong()
        bytes_read = c_ulonglong()
        real_ptr.value = base_address + address  # reverse engineered using cheat engine
        for offset in offsets:
            windll.kernel32.ReadProcessMemory(self.phwnd, real_ptr, byref(real_ptr), sizeof(real_ptr),
                                              byref(bytes_read))
            real_ptr.value += offset

        return real_ptr

    def get_gp_ptr(self):
        gp_offset = 0x018fe408
        pointer_offsets = [0x38, 0x10, 0x18, 0x20, 0x20]
        self.gp_ptr = self.get_ptr(pointer_offsets, gp_offset)

    def get_max_ptr(self):
        max_offset = 0x018F7368
        pointer_offsets = [0xF0, 0x208, 0x0, 0x2F8, 0x1108]

        real_ptr = self.get_ptr(pointer_offsets, max_offset)
        self.max_ptr = real_ptr

    def get_gp(self):
        gp = c_int32()
        max_gp = c_int32()
        bytes_read = c_ulonglong()
        windll.kernel32.ReadProcessMemory(self.phwnd, self.gp_ptr, byref(gp), sizeof(gp),
                                          byref(bytes_read))
        # windll.kernel32.ReadProcessMemory(self.phwnd, self.max_ptr, byref(max_gp), sizeof(max_gp),
        #                                   byref(bytes_read))
        if gp.value <= 0 or gp.value >= 800:
            self.get_process_data()
            # print(gp.value)
        # print(gp.value, max_gp.value)

        # self.gp_ptr.value -= 80
        # for inc in range(8, 200, 8):
        #     v = c_int32()
        #     try:
        #         self.gp_ptr.value += 8
        #         windll.kernel32.ReadProcessMemory(self.phwnd, self.gp_ptr, byref(v), sizeof(v),
        #                                           byref(bytes_read))
        #         print(v.value, bytes_read.value)
        #     except:
        #         continue
        #
        # input()
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
