import cv2
import os

def menu():
	lst = [str(n) + " " + file for n,file in enumerate(os.listdir())]
	print(*lst, sep="\n")
	file = os.listdir()[int(input("File n."))]
	return file

file = menu()

vidcap = cv2.VideoCapture(file)
# vidcap = cv2.VideoCapture('test.mp4')
success,image = vidcap.read()
count = 0

while success:
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  # print('Read a new frame: ', success)
  count += 1

