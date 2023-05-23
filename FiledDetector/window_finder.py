from win32gui import FindWindow
import ctypes
from ctypes.wintypes import HWND, DWORD, RECT


def get_window_rect(window_name: str):
    dwmapi = ctypes.WinDLL("dwmapi")

    hwnd = FindWindow(None, window_name)

    rect = RECT()
    DMWA_EXTENDED_FRAME_BOUNDS = 9
    dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS),
                                ctypes.byref(rect), ctypes.sizeof(rect))

    return (rect.left, rect.top, rect.right, rect.bottom)

print(get_window_rect("Roblox"))