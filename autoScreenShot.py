# auto screenshot
import pyautogui
import os
from pynput.keyboard import Key, Listener

class autoScreenShot:
    screenshot_num = 0
    folder_path = ""
    sc_name = "img"
    ext = ".png"

    def __init__(self, path):
        self.folder_path = path
        for _ in os.listdir(path):
            self.screenshot_num += 1

    def printSc(self, key):
        if key == Key.print_screen:
            windows_screenshot = pyautogui.screenshot()
            windows_screenshot.save(self.folder_path + self.sc_name + str(self.screenshot_num) + self.ext)
            self.screenshot_num += 1
        elif key == Key.delete:
            return False

    def start_autosc(self):
        with Listener(on_press=self.printSc) as listener:
            listener.join()

autosc = autoScreenShot("C:/Users/Devin/Documents/VScode/gbf/images/")
autosc.start_autosc()