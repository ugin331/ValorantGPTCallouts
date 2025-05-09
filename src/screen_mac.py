import mss


class ScreenshotClient:
    def __init__(self):
        self.sct = mss.mss()

    def mss_capture(self):
        im = self.sct.grab(self.sct.monitors[0])
        return im

    def cleanup(self):
        self.sct.close()
