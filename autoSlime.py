# GBF Auto Slime
import cv2 as cv
from ai import AI
from time import time

loop_time = time()
slime_ai = AI()
while(True):
    slime_ai.ai_neurons(loop_time=loop_time)
    loop_time = time()
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')