# coding: utf-8

from ctypes import c_ulong, c_int32, byref, sizeof, windll, c_ulonglong
import win32gui
from win32process import EnumProcessModules, GetModuleFileNameEx


class Reader:
    def __init__(self, window_title='FINAL FANTASY XIV', process_title='FINAL FANTASY XIV'):
        self.process_title = process_title
        self.window_title = window_title
        self.read_access = 0x1F0FFF
        self.hwnd = None
        win32gui.EnumWindows(self.enumhandler, None)

        pid = c_ulong()
        windll.user32.GetWindowThreadProcessId(self.hwnd, byref(pid))

        self.pid = pid.value
        # address = c_ulonglong()
        # address.value = 0x1DBA67BC070
        # print(address.value)
        self.phwnd = windll.kernel32.OpenProcess(self.read_access, False, self.pid)
        base_address = self.getAddressBase()

        value = c_int32()
        real_ptr = c_ulonglong()
        bytes_read = c_ulonglong()
        real_ptr.value = base_address + 0x018fe408
        # for offset in [0x38, 0x10, 0x18, 0x20,  0x20]:
        for offset in [0x38, 0x10, 0x18, 0x20,  0x20]:
            windll.kernel32.ReadProcessMemory(self.phwnd, real_ptr, byref(real_ptr), sizeof(real_ptr),
                                              byref(bytes_read))
            real_ptr.value += offset
            print(hex(real_ptr.value))

        print(hex(real_ptr.value))
        # print('0x2395E82C390')

        windll.kernel32.ReadProcessMemory(self.phwnd, real_ptr, byref(value), sizeof(value),
                                          byref(bytes_read))

        print(value.value)
        print(bytes_read.value)

    def enumhandler(self, hwnd, l):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if 'FINAL FANTASY XIV' in title:
                self.hwnd = hwnd
                print('found', title)

    def getAddressBase(self):
        modules = EnumProcessModules(self.phwnd)
        for n_mod in modules:
            modName = GetModuleFileNameEx(self.phwnd, n_mod)
            if self.process_title in modName:
                return n_mod


Reader()
