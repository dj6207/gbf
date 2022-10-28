import torch
import cv2 as cv
import pyautogui
import threading
from queue import Queue
from time import sleep, time
from tools.winCapture import WindowCapture

class AI:

    screen_x = 1920
    screem_y = 1080

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
        self.checkpoints = ["Summon Select Screen", "Party Select Screen", "Battle Screen", "Result Screen"]
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
                    # print(f"label equal{(label, row)}")
                    self.find_queue.put((label, row))
                    # return True
                else:
                    # print(f"label_queue equal{(label, row)}")
                    self.label_queue.put((label, row))
        cv.imshow('GBF', frame)
        # return False

    # def ai_vision(self, screenshot, score_result, item=None):
        # screenshot  = self.wincap.get_screenshot()
        # score_result = self.wincap.score_frame(screenshot)
        # labeled_frame, found_item, found_cord = self.wincap.plot_boxes(score_result, screenshot)
        # labeled_frame = self.plot_boxes(score_result, screenshot, item)
        # cv.imshow('GBF', labeled_frame)

    def ai_neurons(self, loop_time):
        current_checkpoint = self.checkpoints[self.checkpoint_index]
        frame  = self.wincap.get_screenshot()
        score_result = self.score_frame(frame)
        self.ai_vision(score_result, frame, current_checkpoint)
        if not self.find_queue.empty():
            if self.checkpoint_index == 0: #Check point 1: Got to summon screen
                self.Summon_Select()
            if self.checkpoint_index == 1: #Check point 2: On the party select screen
                print()
            self.checkpoint_index += 1
        self.label_queue.queue.clear()
        # print(f"label q{self.label_queue.empty()}")
        self.find_queue.queue.clear()
        # print(f"find q{self.find_queue.empty()}")

        self.print_debug(loop_time=loop_time)
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
        summon = self.summons.copy()
        # print(summon)
        summon_dict = {"Kaguya": None, "Nobiyo": None, "White Rabbit": None, "Black Rabbit": None, "Summon": None}
        for _ in range(self.label_queue.qsize()):
            detected_label = self.label_queue.get()
            # print(detected_label)
            if detected_label[0] in summon:
                # summon_dict[detected_label[0]] = detected_label[1] 
                # print("updated")
                summon_dict.update({detected_label[0]:detected_label[1]})
                summon.remove(detected_label[0])
        # print(summon_dict)
        for summon in self.summons:
            summon_cord = summon_dict[summon]
            # print(summon_cord)
            if not summon_cord is None:
                self.click_selected(summon_cord)
                return
        summon_cord = summon_dict["Summon"]
        self.click_selected(summon_cord)
        return

    def Party_Select(self):
        #during party select it is possible that my dumb ass fucking ai will see the cancel fucking button as an ok button
        #bruh this shit even says it has a 97% confidence rating that this fucking cancel button is an ok
        #dont feel like retrainig this bull shit so i might just hard code the clicking of the ok button

        #what to should ai look out for during party select screen
        #all there is to do in this check point is to click the ok button
        #if i remember correctly if you dont have enough ap the game will tell you to refill
        #I guess if the next check point is not reach the program stops???
        #or i can just hard code the location of where to press ok
        #half the time my model have a hard time identifying what is a valid ok button
        #prob just gonnna hard code it for now? ill think of something later

        return

    def Battle_Screen(self):
        
        #what to look out for during battle screen
        #first sara ground zero has to be used first and then the back button has to be used 
        #Sometimes the back buttton might kick you back to the fucking quest select screen
        #That is def an issue but honestly i dont have a fix for that 
        #prob another hard code issue to fix lol also dont feel like training another ai

        #sometimes the god dam loading screen takes fucking forever
        #curently my ai is not trained for loading screen 
        #fix ???? honestly idk
        #i guess i could have a longer wait time between each check point or something

        #battle screen phase 2 this time lunalu's skill 1 or what ever needs to be clicked
        #back button also needs to be pressed this time it will 99% of time take you to result screen

        return

    def Result_Screen(self):

        #result screen last part of the slime process
        #first thing you need to do is to click ok for the exp gained
        #after that is where the everything goes down hill
        #sometimes if you are sliming character for lvl 1 to 80 they can learn new skill in which you need to press ok again
        #this can prob be solved just by ai detecting and clicking ok i guess but honestly i can trust my model to detect ok
        #the next issue is when a character gain an emp level there does not exist and ok button for that one
        #I guess i can just hard code something that clicks in the top of the screen until play again button can be seen ??? idk
        #if all things go well we click play again
        #if ap needed prob just hard code that shit

        return

    def click_selected(self, cord):
        # tensor([0.07771, 0.54658, 0.39032, 0.62438, 0.98318], device='cuda:0')


        x1 = cord[0].item()
        y1 = cord[1].item()
        x2 = cord[2].item()
        y2 = cord[3].item()
        #x1 and y1 is the pos of the top left cornor of an imaginary box
        #x2 and y2 is the pos of the bottim right corner of an imaginary box
        #calculate click x and y
        #to get the mouse to move to the right position must multiply each x by half of resolution length since the browser will take up half the screen
        x_cord = (x1 * (self.screen_x/2) + x2 * (self.screen_x/2))/2
        #x_cord is a float
        #multiply by the full resolution height since the browser will take the whole height
        y_cord = (y1 * self.screem_y + y2 * self.screem_y)/2
        # print(f"Moved to {x_cord}, {y_cord}")
        pyautogui.moveTo(x=x_cord, y=y_cord)
        self.print_debug(x_cord=x_cord, y_cord=y_cord)
        pyautogui.click()
        sleep(1.25)
             

        



    def print_debug(self, loop_time=None, x_cord=None, y_cord=None):
        if (not loop_time is None):
            print('FPS {}'.format(1 / (time() - loop_time)))
        if (not x_cord is None and not y_cord is None):
            print(f"Moved to ({x_cord}, {y_cord})")
        print(self.checkpoints[self.checkpoint_index])
        # print(self.checkpoint_index)