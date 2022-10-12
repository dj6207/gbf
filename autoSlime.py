# GBF Auto Slime
import cv2 as cv
from time import time
import torch
from Ai import WindowCapture

# When screen shotting from chrome make sure to turn off hardware acceleration or else black screen
# initialize the WindowCapture class
# wincap = WindowCapture('Granblue Fantasy - Google Chrome')
wincap = WindowCapture('Task Manager')

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    results = model(screenshot)
    results.show()


    # cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    # loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')