from ctypes import windll
import win32gui
import mss


def list_windows():
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            print(f"Handle: {hex(hwnd)}, Title: {title}, Class: {class_name}")

    win32gui.EnumWindows(callback, None)


class ScreenshotClient:
    def __init__(self):
        self.tgt = win32gui.FindWindow("VALORANTUnrealWindow", None)
        # self.tgt = win32gui.FindWindow(None, 'Task Manager')
        if self.tgt == 0:
            raise RuntimeError("Can't find target window")
        windll.user32.SetProcessDPIAware()

        self.left, self.top, self.right, self.bot = win32gui.GetWindowRect(self.tgt)
        self.width = self.right - self.left
        self.height = self.bot - self.top

        self.sct = mss.mss()

        # uncomment if not using mss
        # self.tgtDC = win32gui.GetWindowDC(self.tgt)
        # self.mfcDC  = win32ui.CreateDCFromHandle(self.tgtDC)

        # self.saveDC = self.mfcDC.CreateCompatibleDC()
        # print(self.saveDC)

        # self.bitmap = win32ui.CreateBitmap()
        # self.bitmap.CreateCompatibleBitmap(self.mfcDC, self.width, self.height)
        # self.saveDC.SelectObject(self.bitmap)

    def get_window_bitmap(self):
        # make robust to window size changes here!
        windll.user32.PrintWindow(self.tgt, self.saveDC.GetSafeHdc(), 1)
        return self.bitmap

    def get_bitmap_info(self):
        bmpinfo = self.bitmap.GetInfo()
        bmpstr = self.bitmap.GetBitmapBits(True)
        return bmpinfo, bmpstr

    def mss_capture(self):
        bbox = (self.left, self.top, self.right, self.bot)
        im = self.sct.grab(bbox)
        return im

    def cleanup(self):
        self.sct.close()

        # try:
        #     win32gui.DeleteObject(self.bitmap.GetHandle())
        # except:
        #     pass
        # finally:
        #     self.saveDC.DeleteDC()
        #     self.mfcDC.DeleteDC()
        #     win32gui.ReleaseDC(self.tgt, self.tgtDC)
