import torch
import cv2 as cv
from time import time
from tools.winCapture import WindowCapture

class AI:
    def __init__(self, model_path="./yolov5/runs/google_cloud/exp15/weights/best.pt", browser_name="Granblue Fantasy - Google Chrome"):
        self.model_path = model_path
        self.browser_name = browser_name
        self.wincap = WindowCapture(self.model_path, self.browser_name)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path)
        self.process = []
    
    def ai_vision(self, screenshot, score_result):
        # screenshot  = self.wincap.get_screenshot()
        # score_result = self.wincap.score_frame(screenshot)
        labeled_frame = self.wincap.plot_boxes(score_result, screenshot)
        cv.imshow('GBF', labeled_frame)

    def ai_neurons(self, loop_time):
        screenshot  = self.wincap.get_screenshot()
        score_result = self.wincap.score_frame(screenshot)
        self.ai_vision(screenshot, score_result)
        self.print_debug(loop_time)
        # Summon Screen
        # Party Select Screen
        # Battle Screen
        # Skill Select Screen
        # Battle Screen
        # Skill Select Screen
        # Result Screen


        



    def print_debug(self, loop_time):
        print('FPS {}'.format(1 / (time() - loop_time)))