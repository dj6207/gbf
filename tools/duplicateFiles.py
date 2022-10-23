import os 
import shutil



class duplicateFiles:
    image_path = "C:/Users/Devin/Documents/VScode/gbf/yolov5/data/dataset/dataset5/images/"
    label_path = "C:/Users/Devin/Documents/VScode/gbf/yolov5/data/dataset/dataset5/labels/"
    def __init__(self, filename='copy'):
        self.copy = filename
        for i in os.listdir(self.label_path):
            # print(self.label_path)
            shutil.copy2(self.label_path + i,self.label_path + self.copy + i)
        for i in os.listdir(self.image_path):
            shutil.copy2(self.image_path + i,self.image_path + self.copy + i)
        print("Done")

dup = duplicateFiles('copy5')