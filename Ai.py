from tkinter import N
import torch
import cv2 as cv
from queue import Queue
from time import time
from tools.winCapture import WindowCapture

class AI:
    def __init__(self, model_path="./yolov5/runs/google_cloud/exp25/weights/best.pt", browser_name="Granblue Fantasy - Google Chrome"):
        self.model = self.load_model(model_path)
        self.classes = self.model.names
        if torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        print(f"Device: {self.device}")
        self.checkpoint_index = 0
        self.label_queue = Queue()
        self.find_queue = Queue()
        self.model_path = model_path
        self.browser_name = browser_name
        self.wincap = WindowCapture(self.browser_name)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path)
        self.cheakpoints = ["Summon Select Screen", "Party Select Screen", "Battle Screen", "Result Screen"]
        self.summons = ["Kaguya", "Nobiyo", "White Rabbit", "Black Rabbit", "Summon"]
    
    def load_model(self, model_path):
        try:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload = True)
            print(f"Model: {model}")
            return model
        except Exception:
            print("Invalid model path")

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def ai_vision(self, score_result, frame, item=None):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = score_result
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.8: #detection values curerntly 0.2
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                rectangle_bgr = (0, 255, 0)
                text_bgr = (0, 0, 255)
                label = self.class_to_label(labels[i])
                cv.rectangle(frame, (x1, y1), (x2, y2), rectangle_bgr, 2)
                # cv.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
                cv.putText(frame, f"{label} {str(row[4])[7:12]}", (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.25, text_bgr, 1)
                # print(labels[i])
                if not item is None and label == item:
                    print("label equal")
                    self.find_queue.put((label, row))
                    return True
                else:
                    self.label_queue.put((label, row))
        cv.imshow('GBF', frame)
        return False

    # def ai_vision(self, screenshot, score_result, item=None):
        # screenshot  = self.wincap.get_screenshot()
        # score_result = self.wincap.score_frame(screenshot)
        # labeled_frame, found_item, found_cord = self.wincap.plot_boxes(score_result, screenshot)
        # labeled_frame = self.plot_boxes(score_result, screenshot, item)
        # cv.imshow('GBF', labeled_frame)

    def ai_neurons(self, loop_time):
        current_checkpoint = self.cheakpoints[self.checkpoint_index]
        frame  = self.wincap.get_screenshot()
        score_result = self.score_frame(frame)
        got_item = self.ai_vision(score_result, frame, current_checkpoint)
        if got_item:
            if self.checkpoint_index == 0:
                self.Summon_Select()
            self.checkpoint_index += 1
        self.label_queue.clear()
        self.find_queue.clear()

        self.print_debug(loop_time)
        # Summon Screen
        # Summon
        # Party Select Screen
        # Ok
        # Battle Screen
        # Sarasa
        # Skill Select Screen
        # Ground Zero
        # Back Button
        # Battle Screen
        # Lunalu
        # Skill Select Screen
        # Facimile
        # Back Button
        # Result Screen
        # Ok Button
        # Replay

    def Summon_Select(self):
        # summon_dict = {"Kaguya": None, "Nobiyo": None, "White Rabbit": None, "Black Rabbit": None, "Summon": None}
        # summon = self.summons.copy()
        # for i in range(len(labels)):
        #     row = cord[i]
        #     label = self.class_to_label(labels[i])
        #     if label in summon:
        #         summon_dict[label] =  row
        #         summon.remove(label)
        # for i in self.summons:
        #     selected_cord = summon_dict.get(i)
        #     if not selected_cord is None:
        #         break
        # self.click_selected(selected_cord)

        #work in progress
        #the find queue will have a queue of all the instance of the label that is asked to be found
        #the label queue will have a list of all the labels in the image excluding the label being ask to find
        #loop through the queue to see if to see if queue has the desired summon
        #when first desired summon is found top loop
        #get the cords of desired summon and call click seletcted
        return

    def click_selected(self, cord):
        print(cord)
             

        



    def print_debug(self, loop_time):
        print('FPS {}'.format(1 / (time() - loop_time)))