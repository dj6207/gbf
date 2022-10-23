import os
from cv2 import imwrite
from winCapture import WindowCapture

class autoScreenShot:
    dataset_folder_num = 0
    screenshot_num = 0
    sc_name = "img"
    ext = ".jpg"
    dataset = "dataset"
    sc = "_sc"

    def __init__(self, path="C:/Users/Devin/Documents/VScode/gbf/yolov5/data/dataset/", mkdir=False, file_cap=10, window_name="Granblue Fantasy - Google Chrome"):
        self.wincap = WindowCapture(None, window_name)
        for _ in os.listdir(path):
            self.dataset_folder_num += 1
        if mkdir:
            self.dataset_folder_num += 1
            os.mkdir(f"{path}{self.dataset}{self.dataset_folder_num}/")
            os.mkdir(f"{path}{self.dataset}{self.dataset_folder_num}/{self.dataset}{self.sc}/")
        self.folder_path = f"{path}{self.dataset}{self.dataset_folder_num}/{self.dataset}{self.sc}/"
        for _ in os.listdir(self.folder_path):
            self.screenshot_num += 1
        self.file_cap = file_cap + self.screenshot_num

    def print_sc(self):
        while True:
                screenshot = self.wincap.get_screenshot()
                imwrite(f"{self.folder_path}{self.sc_name}{self.screenshot_num}{self.ext}", screenshot)
                self.screenshot_num += 1
                if self.screenshot_num >= self.file_cap:
                    print("Done")
                    break

autosc = autoScreenShot(file_cap=1)
autosc.print_sc()