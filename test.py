import torch

# model_path = './yolov5/runs/train/exp/weights/best.pt'
model_path = './yolov5/runs/google_cloud/best.pt'

model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
img = './test/test2.jpg'
# img = 'C:/Users/Devin/Documents/gbftest.jpg'
results = model(img)
results.show()