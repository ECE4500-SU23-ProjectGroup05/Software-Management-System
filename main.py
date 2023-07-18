import sys
import time
import queue
import config
import win32con
import win32gui
import threading
import communication

from PIL import Image
from pystray import MenuItem, Icon


class WinHandle:
    """
    Self-defined class to handle the program windows.
    """
    window_minimized = False
    hwnd = win32gui.GetForegroundWindow()

    def minimize_to_tray(self):
        if not self.window_minimized:
            win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)
            self.window_minimized = True

    def restore_window(self):
        if self.window_minimized:
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            self.window_minimized = False
        win32gui.SetForegroundWindow(self.hwnd)


def on_exit(_icon):
    _icon.visible = False
    _icon.stop()


def on_click(_icon, _item):
    win_handler.restore_window()


def on_minimize(_icon):
    win_handler.minimize_to_tray()
    _icon.notify("The program has been minimized to tray.", "Notification")


def error_handler(_exception):
    print("NOTICE: Error occurs. Please refer to error.log for details.")
    with open("error.log", 'w') as log:
        log.write(str(_exception))
    print("        The program will end in 5 seconds...")
    time.sleep(5)


def setup(_icon):
    icon.visible = True
    thread = threading.Thread(target=run_main, args=(), daemon=True)
    thread.start()

    while icon.visible:
        try:
            exception = exception_q.get(block=False)
            error_handler(exception)
            icon.stop(), sys.exit(0)
        except queue.Empty:
            time.sleep(0.1)

    icon.stop()
    sys.exit(0)


def run_main():
    try:
        settings = config.read_settings()
        websocket_url = "ws://" + str(settings["server-IP"]) \
                        + ":" + str(settings["port"]) + "/ws/socket-server/"
        print("=== The client is now running ===")
        communicator = communication.Communication(websocket_url, settings["time"])
        communicator.connect_server(communicator.bidirectional_communication, settings["reconnect"])
    except Exception as _e:
        exception_q.put(_e)


exception_q = queue.Queue()

win_handler = WinHandle()

menu = (MenuItem('Menu', on_click, default=True, visible=False),
        MenuItem('Minimize to Tray', on_minimize),
        MenuItem('Show Window', on_click),
        MenuItem('Exit', on_exit))

icon = Icon("name", Image.open("icon.jpg"), "Program Control", menu)

icon.run(setup)
